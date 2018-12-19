import torch.nn as nn 
import numpy as np 
from pytorch_pretrained_bert import BertModel

class NERClassification():
    def __init__(self, num_labels = 10):
        self.bert = BertModel.from_pretrained("bert-base-cased").to(device=torch.device("cuda"))
        bert_dim = 768 
        out = torch.nn.Linear(bert_dim, n_labels)
        self.out = nn.Linear(bert_dim, num_labels)
        self.softmax = nn.LogSoftmax()
        self.num_labels = num_labels
        
    def forward(self, input_ids, segment_ids):
        bert_last_layer = self.bert(input_ids.cuda(), segment_ids.cuda())[0][-1]
        op = out(bert_last_layer)
        s_op = self.softmax(op)
        y = s_op.view(-1, 10)
        return y 
        

