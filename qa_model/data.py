from comet_ml import Experiment

from torch.utils import data
import parameters
import torch 
from pytorch_pretrained_bert import BertTokenizer
import utils
import logging
import collections
import json
from tqdm import tqdm 
from pytorch_pretrained_bert import tokenization


_DocSpan = collections.namedtuple("DocSpan", ["start", "length"])

class InputFeatures(object):
  """A single set of features of data."""

  def __init__(self,
               unique_id,
               example_index,
               doc_span_index,
               tokens,
               token_to_orig_map,
               token_is_max_context,
               input_ids,
               input_mask,
               segment_ids,
               start_position=None,
               end_position=None):
    self.unique_id = unique_id
    self.example_index = example_index
    self.doc_span_index = doc_span_index
    self.tokens = tokens
    self.token_to_orig_map = token_to_orig_map
    self.token_is_max_context = token_is_max_context
    self.input_ids = input_ids
    self.input_mask = input_mask
    self.segment_ids = segment_ids
    self.start_position = start_position
    self.end_position = end_position



class QADataset(data.Dataset):
    def __init__(self, f_name, tokenizer):
        super().__init__()
        with open('BioASQ-train-4b.json', 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        self.features = []


        data = input_data['data']   
        for entry in data:
            for para in tqdm(entry["paragraphs"]):
                        text = para["context"]
        char_to_word_offset, doc_tokens = utils.text_preprocessing(text)
        for qa in para['qas']:
            question_text = qa["question"]
            answer = qa['answers'][0]
            orig_answer_text = answer["text"]
            answer_offset = answer["answer_start"]
            answer_length = len(orig_answer_text)
            start_position = char_to_word_offset[answer_offset]
            end_position = char_to_word_offset[answer_offset + answer_length - 1]


            # Check if answer can be retrieved successfully or now 
            actual_text = " ".join(
                doc_tokens[start_position:(end_position + 1)])
            cleaned_answer_text = " ".join(
                tokenization.whitespace_tokenize(orig_answer_text))

            if actual_text.find(cleaned_answer_text) == -1:
                logging.warning(f'could not find answer {cleaned_answer_text} in {actual_text}')
            
            # Process question text 
            query_tokens = tokenizer.tokenize(question_text)
            # Limit query tokens length 
            query_tokens = query_tokens[:parameters.MAX_QUERY_LENGTH] 

            # Now query is tokenized, we need to preserve mapping to original (20) -> ( 20 )
            # It uses sentence piece tokenizer 
            tok_to_orig_index = []
            orig_to_tok_index = []
            all_doc_tokens = []
            for (i, token) in enumerate(doc_tokens):
                orig_to_tok_index.append(len(all_doc_tokens))
                sub_tokens = tokenizer.tokenize(token)
                for sub_token in sub_tokens:
                    tok_to_orig_index.append(i)
                    all_doc_tokens.append(sub_token)


            tok_start_position = None 
            tok_end_position = None 
            tok_start_position = orig_to_tok_index[start_position]
            tok_end_position = orig_to_tok_index[end_position +1] - 1

            input_start, input_end = utils.improve_answer_span(
                    all_doc_tokens, tok_start_position, tok_end_position, tokenizer,
                    orig_answer_text)


            # The -3 accounts for [CLS], [SEP] and [SEP]
            max_tokens_for_doc = parameters.MAX_SEQ_LENGTH - len(query_tokens) - 3

            doc_spans = []
            start_offset = 0
            while start_offset < len(all_doc_tokens):
                length = len(all_doc_tokens) - start_offset
                if length > max_tokens_for_doc:
                    length = max_tokens_for_doc
                doc_spans.append(_DocSpan(start=start_offset, length=length))
                if start_offset + length == len(all_doc_tokens):
                    break
                start_offset += min(length, parameters.DOC_STRIDE)

            for index, doc_span in enumerate(doc_spans):
                tokens = []
                token_to_orig_map = {}
                token_is_max_context = {}
                tokens = ["[CLS]"] + query_tokens + ["[SEP]"]
                segment_ids = [0] * len(tokens)
                
                for i in range(doc_span.length):
                    split_token_index = doc_span.start + i 
                    token_to_orig_map[len(tokens)] = tok_to_orig_index[split_token_index]
                    is_max_context = utils.check_is_max_context(doc_spans, index, split_token_index)
                    token_is_max_context[len(tokens)] = is_max_context
                    tokens.append(all_doc_tokens[split_token_index])
                    segment_ids.append(1)
                tokens.append("[SEP]")
                segment_ids.append(1)
                
                
                input_ids = tokenizer.convert_tokens_to_ids(tokens)
                
                # Mask if real token then 1 and padding 0 
                input_mask = [1] * len(input_ids)
                
                
                
                # Zero par up to the sequence length 
                start_position = None 
                end_position = None 
                
                # remove the spans for which we have nothing to predict 
                doc_start = doc_span.start
                doc_end = doc_span.start + doc_span.length - 1 
                out_of_span = False 
                if not (tok_start_position >= doc_start) and (tok_end_position <= doc_end):
                    out_of_span = True 
                    
                if out_of_span:
                    start_position = 0
                    end_position = 0
                else:
                    doc_offset = len(query_tokens) + 2 
                    start_position = tok_start_position - doc_start + doc_offset
                    end_position = tok_end_position - doc_start + doc_offset   
            

                features.append(InputFeatures(
                    unique_id=unique_id,
                    example_index=example_index,
                    doc_span_index=doc_span_index,
                    tokens=tokens,
                    token_to_orig_map=token_to_orig_map,
                    token_is_max_context=token_is_max_context,
                    input_ids=input_ids,
                    input_mask=input_mask,
                    segment_ids=segment_ids,
                    start_position=start_position,
                    end_position=end_position))


    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        feature = self.features[idx]

        input_ids = feature.input_ids
        input_mask = feature.input_mask 
        segment_ids = feature.segment_ids
        start_position = feature.start_position
        end_position = feature.end_position

        assert len(input_ids) == len(input_mask), f'input_ids is not equal to input_mask'
        assert len(input_ids) == len(segment_ids), f'input_ids is not equal to segment_ids'

        return input_ids, input_mask, segment_ids, start_position, end_position

    
