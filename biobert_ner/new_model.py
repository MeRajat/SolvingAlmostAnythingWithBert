import torch
import torch.nn as nn
from pytorch_pretrained_bert import BertModel

class Net(nn.Module):
    def __init__(self, config, bert_state_dict, vocab_len, device = 'cpu'):
        super().__init__()
        self.bert = BertModel(config)
        if bert_state_dict is not None:
            self.bert.load_state_dict(bert_state_dict)
        self.bert.eval()
        self.rnn = nn.LSTM(bidirectional=True, num_layers=2, input_size=768, hidden_size=768//2, batch_first=True)
        self.fc = nn.Linear(768, vocab_len)
        self.device = device

    def forward(self, x, y):
        '''
        x: (N, T). int64
        y: (N, T). int64

        Returns
        enc: (N, T, VOCAB)
        '''
        x = x.to(self.device)
        y = y.to(self.device)

        with torch.no_grad():
            encoded_layers, _ = self.bert(x)
            enc = encoded_layers[-1]
        enc, _ = self.rnn(enc)
        logits = self.fc(enc)
        y_hat = logits.argmax(-1)
        return logits, y, y_hat