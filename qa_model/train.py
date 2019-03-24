from data import QADataset, pad
from pytorch_pretrained_bert import BertTokenizer, BertAdam
import numpy as np
from torch.utils import data
import parameters 
from pytorch_pretrained_bert.modeling import BertForQuestionAnswering, BertConfig
from collections import OrderedDict
import torch

from comet_ml import Experiment
experiment = Experiment(api_key="4Aw30RGeYclMkVkbBlojeQWEN",
                        project_name="general", workspace="merajat")



tokenizer = BertTokenizer(vocab_file='../weights/pubmed_pmc_470k/vocab.txt', do_lower_case=False)

# Load dataset 
train_dataset = QADataset(f_name='BioASQ-train-4b.json', tokenizer=tokenizer)
train_iter = data.DataLoader(dataset=dataset,
                             batch_size=parameters.batch_size,
                             shuffle=True,
                             num_workers=4,
                             collate_fn=pad)


# Load pretrained state dict 
tmp_d = torch.load('/data/home/rajat/work/biobert/code_ner/weights/pytorch_weight', map_location='cpu')
state_dict = OrderedDict()
for i in list(tmp_d.keys())[:199]:
    x = i
    if i.find('bert') > -1:
        x = '.'.join(i.split('.')[1:])
    state_dict[x] = tmp_d[i]

del(tmp_d)

# create config 
config = BertConfig(vocab_size_or_config_json_file='../weights/pubmed_pmc_470k/bert_config.json')
model = BertForQuestionAnswering(config)
model.bert.load_state_dict(state_dict)

# Load model to cuda 
_ = model.cuda()

# Define optimizer 
# Prepare optimizer
# param_optimizer = list(model.named_parameters())

# # hack to remove pooler, which is not used
# # thus it produce None grad that break apex
# param_optimizer = [n for n in param_optimizer if 'pooler' not in n[0]]

# no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
# optimizer_grouped_parameters = [
#     {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
#     {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
#     ]


optimizer = optim.Adam(model.parameters(), lr = hp.lr)

optimizer = BertAdam(optimizer_grouped_parameters,
                     lr=0.001,
                     warmup=0.1,
                     t_total=10)

