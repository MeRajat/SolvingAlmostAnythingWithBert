from pytorch_pretrained_bert import BertTokenizer, tokenization, modeling, BertConfig
from pytorch_pretrained_bert.tokenization import BasicTokenizer, BertTokenizer
from torch.utils.data import DataLoader, Dataset
import ftfy 
import numpy as np 
from tqdm import tqdm 
import torch 
import json 

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

class CommonSenseQA(Dataset):
    def __init__(self, path):
        tokenizer = BasicTokenizer()
        data = open(path, 'r').readlines()
        self.LABELS = ['A', 'B', 'C', 'D', 'E']
        self.questions = []
        self.answers = []
        self.labels = []
        for line in tqdm(data):
            q_data = json.loads(line.strip('\n'))
            qid = q_data['id']
            question = ftfy.fix_encoding(q_data['question']['stem'])
            answers_choices = np.array([
                ftfy.fix_encoding(choice['text'])
                for choice in sorted(
                    q_data['question']['choices'],
                    key=lambda c: c['label'])
            ])
            self.labels.append(self.LABELS.index(q_data.get('answerKey', 'A'))) # Dummy for test data 
            self.questions.append(question)
            self.answers.append(answers_choices)
            

    def __len__(self):
        return len(self.questions)
    
    def __getitem__(self, idx):
        question = self.questions[idx]
        answers_choices = self.answers[idx]
        label = self.labels[idx]
        input_ids = []
        segment_ids = []
        input_mask = []
        question_tokens = tokenizer.tokenize(question)
        answers_tokens = map(tokenizer.tokenize, answers_choices)
        for i, answer_token in enumerate(answers_tokens):
            truncated_question_tokens = question_tokens[
                :max((max_seq_len - 3)//2, max_seq_len - (len(answer_token) + 3))
            ]
            truncated_answer_tokens = answer_token[
                :max((max_seq_len - 3)//2, max_seq_len - (len(question_tokens) + 3))
            ]
            token_ids = ["[CLS]"] + truncated_question_tokens + ["[SEP]"] + truncated_answer_tokens + ["[SEP]"]
            token_segment_ids = [0] + [0] * len(truncated_question_tokens) + [0] + [1] * len(truncated_answer_tokens) + [1]
            input_single_ids = np.zeros(max_seq_len)
            segment_single_ids = np.zeros(max_seq_len)
            
            ip_tokens = tokenizer.convert_tokens_to_ids(token_ids)
            input_single_ids[:len(ip_tokens)] = ip_tokens
            input_ids.append(input_single_ids)
            segment_single_ids[:len(token_segment_ids)] = token_segment_ids
            segment_ids.append(segment_single_ids)
            mask = np.zeros(max_seq_len)
            mask[:len(token_ids)] = 1
            input_mask.append(mask)
        
        
        return_val = []
        for ip, ma, se in  zip(input_ids, segment_ids, input_mask):
            return_val.append(ip)
            return_val.append(ma)    
            return_val.append(se)  
        input_ids0,  input_mask0,  segment_ids0,  input_ids1,  input_mask1,  segment_ids1,  input_ids2,  input_mask2,  segment_ids2,  input_ids3,  input_mask3,  segment_ids3,  input_ids4,  input_mask4,  segment_ids4 = return_val
        
        input_ids = np.stack([input_ids0,
            input_ids1,
            input_ids2,
            input_ids3,
            input_ids4], axis = 1)
        segment_ids = np.stack([segment_ids0,
            segment_ids1,
            segment_ids2,
            segment_ids3,
            segment_ids4], axis = 1)
        input_mask = np.stack([
            input_mask0,
            input_mask1,
            input_mask2,
            input_mask3,
            input_mask4], axis = 1)
        
        return input_ids, segment_ids, input_mask, label

