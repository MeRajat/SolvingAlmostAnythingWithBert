import torch 
import numpy as np 
from tqdm import tqdm
import torch.nn as nn
import os
import torch
import collections
import pytorch_pretrained_bert as _bert
from pytorch_pretrained_bert.modeling import PreTrainedBertModel, BertModel
from torch.utils.data import DataLoader,  TensorDataset, RandomSampler
from pytorch_pretrained_bert import modeling
from pytorch_pretrained_bert import optimization
from pytorch_pretrained_bert import tokenization

class InputExample:
    def __init__(self, guid, text, label=None):
        self.guid = guid
        self.text = text # Untokenized text of first sequence 
        self.label = label
        

class InputFeatures:
    def __init__(self, input_ids, input_mask, segment_ids, label_ids):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids 
        
class DataProcessor:
    def get_train_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "train.txt")), "train"
        )

    def get_dev_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "dev.txt")), "dev"
        )
    
    def get_labels(self):
        return ["B-MISC", "I-MISC", "O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X"]
    
    def _create_example(self, lines, set_type):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text = tokenization.convert_to_unicode(line[1])
            label = tokenization.convert_to_unicode(line[0])
            examples.append(InputExample(guid=guid, text=text, label=label))
        return examples

    @classmethod
    def _read_data(cls, input_file):
        with open(input_file) as f:
            lines = []
            words = []
            labels = []
            for line in f:
                contends = line.strip()
                word = line.strip().split(' ')[0]
                label = line.strip().split(' ')[-1]
                if contends.startswith("-DOCSTART-"):
                    words.append('')
                    continue
                    
                if len(contends) == 0 and words[-1] == '.':
                    l = ' '.join([label for label in labels if len(label) > 0])
                    w = ' '.join([word for word in words if len(word) > 0])
                    lines.append([l, w])
                    words = []
                    labels = []
                    continue
                words.append(word)
                labels.append(label)
            return lines      

def convert_example_features(ex_index, example, label_list, max_seq_length, tokenizer):
    # map label to numbers 
    label_map = {}
    for i, label in enumerate(label_list):
        label_map[label] = i
        
    text_list = example.text.split(' ')
    label_list = example.label.split(' ')
    
    tokens = []
    labels = []
    for i, word in enumerate(text_list):
        token = tokenizer.tokenize(word)
        tokens.extend(token)
        label_1 = label_list[i]
        for m in range(len(token)):
            if m == 0:
                labels.append(label_1)
            else:
                labels.append("X")
                
    if len(tokens) >= max_seq_length -1:
        tokens = tokens[0: (max_seq_length - 2)]  # [SEP] and [CLS]
        labels = labels[0:(max_seq_length - 2)] 
        
    ntokens = []
    segment_ids = []
    label_ids = []
    ntokens.append('[CLS]')
    segment_ids.append(0)
    label_ids.append(0)
    for i, token in enumerate(tokens):
        ntokens.append(token)
        segment_ids.append(0)
        label_ids.append(label_map[labels[i]])
        
    ntokens.append("[SEP]")
    segment_ids.append(0)
    label_ids.append(0)
    input_ids = tokenizer.convert_tokens_to_ids(ntokens)
    input_mask = [1] * len(input_ids)
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)
        label_ids.append(0)
    # print(len(input_ids))
    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length
    assert len(label_ids) == max_seq_length
    
    feature = InputFeatures(
        input_ids=input_ids,
        input_mask=input_mask,
        segment_ids=segment_ids,
        label_ids=label_ids
    )
    return feature

def convert_to_features(examples, label_list, max_seq_length, tokenizer):
    features = []
    for ex_index, example in tqdm(enumerate(examples)):
        feature = convert_example_features(ex_index, example, label_list, max_seq_length, tokenizer=tokenizer) 
        features.append(feature)
    return features

