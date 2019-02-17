import torch 
import torch.nn as nn 
from pytorch_pretrained_bert.modeling import BertPreTrainedModel,  BertModel


class BertForNER(BertPreTrainedModel):
    def __init__(self, config, num_labels):
        super(BertForNER, self).__init__(config)
        self.num_labels = num_labels
        self.bert = BertModel(config).cuda()
        self.dropout = torch.nn.Dropout(0.1)
        self.hidden2label = torch.nn.Linear(config.hidden_size, num_labels)
        self.apply(self.init_bert_weights)

    def forward(self, input_ids, segment_ids, input_mask, predict_mask=None, one_hot_labels=None):

        bert_layer, _ = self.bert(input_ids, segment_ids, input_mask, output_all_encoded_layers=False)
        if one_hot_labels is not None:
            bert_layer = self.dropout(bert_layer)
        logits = self.hidden2label(bert_layer)

        if one_hot_labels is not None:
            # p = torch.nn.functional.softmax(logits, -1)
            # losses = -torch.log(torch.sum(one_hot_labels * p, -1))
            # losses = torch.masked_select(losses, predict_mask)
            # return torch.sum(losses)
            log_probs = torch.nn.functional.log_softmax(logits, dim = -1)
            per_example_loss = torch.sum(one_hot_labels * log_probs, dim=-1) 
            per_example_loss = per_example_loss * (input_mask.type(torch.cuda.FloatTensor))
            # Number of tokens 
            num_tokens = int(torch.sum(input_mask))
            ## get masked values ignoring padding
            loss = torch.sum(per_example_loss)/num_tokens
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predict = torch.argmax(probabilities,dim=-1)
            return (loss, per_example_loss, logits,predict)
        else:
            return logits 


# class BertForNER(PreTrainedBertModel):
#     def __init__(self, config, num_labels):
#         super(BertForNER, self).__init__(config)
#         self.num_labels = num_labels
#         self.bert = BertModel(config)
#         self.dropout = nn.Dropout(config.hidden_dropout_prob)
#         self.classifier = nn.Linear(config.hidden_size, num_labels)
#         self.apply(self.init_bert_weights)

#     def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None):
#         sequence_output, _ = self.bert(input_ids, token_type_ids, attention_mask, output_all_encoded_layers=False)
#         sequence_output = self.dropout(sequence_output)
#         logits = self.classifier(sequence_output)

#         if labels is not None:
#             loss_fct = CrossEntropyLoss()
#             # Only keep active parts of the loss
#             if attention_mask is not None:
#                 active_loss = attention_mask.view(-1) == 1
#                 active_logits = logits.view(-1, self.num_labels)[active_loss]
#                 active_labels = labels.view(-1)[active_loss]
#                 loss = loss_fct(active_logits, active_labels)
#             else:
#                 loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
#             return loss
#         else:
#             return logits

