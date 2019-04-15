from pytorch_pretrained_bert.modeling import BertModel
import torch.nn as nn 


class BertForChoice(nn.Module):
    def __init__(self, dropout = 0.2, hidden_size1 = 768, hidden_size2 = 640, num_choices = 5):
        super().__init__()
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
        self.dropout = nn.Dropout(dropout)
        self.classifier1 = nn.Linear(hidden_size1, num_choices)
        self.classifier2 = nn.Linear(hidden_size2, num_choices)
        
    def forward(self, input_ids, segment_ids, input_mask, labels = None):
        batch_size = input_ids.shape[0]
        flat_input_ids = input_ids.view(-1, input_ids.size(-1)).type(torch.LongTensor)
        flat_segment_ids = segment_ids.view(-1, segment_ids.size(-1)).type(torch.LongTensor)
        flat_input_mask = input_mask.view(-1, input_mask.size(-1)).type(torch.LongTensor)

        _, pooled_output = self.bert_model(flat_input_ids, flat_segment_ids, flat_input_mask, output_all_encoded_layers=False)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier1(pooled_output)
        reshaped_logits = logits.reshape(batch_size, -1)
        reshaped_logits = self.classifier2(reshaped_logits)
        
        if labels is not None:
            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(reshaped_logits, labels)
            return loss
        else:
            return reshaped_logits