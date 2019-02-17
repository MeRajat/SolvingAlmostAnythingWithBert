from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm, trange
from model import BertForNER
from utils import warmup_linear, 
from data import NerProcessor, return_dataloader
import parameters as param
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.optimization import BertAdam
import torch
import pickle 
from pytorch_pretrained_bert.modeling import BertConfig
import numpy as np 
from sklearn_crfsuite.metrics import flat_classification_report

from sklearn.metrics import f1_score,precision_score,recall_score

# device 
device = torch.device("cuda", torch.cuda.current_device())


# load and create dataloader 
ner = NerProcessor()
train_examples = ner.get_examples('train_lines.pkl')
valid_examples = ner.get_examples('devel_lines.pkl')
test_examples = ner.get_examples('test_lines.pkl')

# Initialize tokenizer 
tokenizer = BertTokenizer(vocab_file=param.VOCAB_FILE, do_lower_case=False)
label_map = ner.get_label_map()


# Data loader 
train_dataloader = return_dataloader(train_examples, tokenizer, label_map)
valid_dataloader = return_dataloader(train_examples, tokenizer, label_map)
test_dataloader = return_dataloader(train_examples, tokenizer, label_map)


# Define model 
state_dict = torch.load(param.state_dict, map_location='cpu')
config = BertConfig(vocab_size_or_config_json_file=param.BERT_CONFIG_FILE)
model = BertForNER(config = config, num_labels=len(label_map.keys()))
model.cuda()
model.train()
# update with already pretrained weight
model.bert.state_dict = state_dict

# Steps
num_train_steps = int(
            len(train_examples) / param.BATCH_SIZE / param.gradient_accumulation_steps * param.EPOPCH)

global_steps = int(len(train_examples)/ param.BATCH_SIZE / param.gradient_accumulation_steps * param.EPOPCH)

param_optimizer = list(model.named_parameters())
no_decay = ['bias', 'LayerNorm.bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
{'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
{'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]
optimizer = BertAdam(optimizer_grouped_parameters, lr=0.01, warmup=0.01, t_total=num_train_steps)


# Training 
for epoch in trange(param.EPOPCH, desc = "EPOCH"):
    _ = model.train(True)
    for step, batch in enumerate(tqdm(train_dataloader, desc=f'{loss.data} at Iteration')):
        batch = tuple(t.to(device) for t in batch)
        input_ids, input_mask, segment_ids, one_hot_labels , predict_mask, label_ids = batch
        loss = model(input_ids, input_mask, segment_ids, predict_mask=predict_mask, one_hot_labels=one_hot_labels)
        if param.gradient_accumulation_steps > 1:
            loss = loss / param.gradient_accumulation_steps
        loss.backward()

        if (step + 1)% param.gradient_accumulation_steps == 0:
            lr_this_step = param.lr * warmup_linear(global_steps / num_train_steps, param.warmup_proportions)
            for param_group in optimizer.param_groups:
                param_group['lr'] =  lr_this_step
            optimizer.step()
            optimizer.zero_grad()
            global_steps += 1

    ## Validation after every epoch 
    _ = model.train(False)
    predictions = []
    orig_labels = []
    for step, batch in enumerate(tqdm(valid_dataloader)):
        batch = tuple(t.to(device) for t in batch)
        input_ids, input_mask, segment_ids, one_hot_labels , predict_mask, label_ids = batch
        logits = model(input_ids, input_mask, segment_ids, predict_mask=predict_mask, one_hot_labels=None)
        logits = logits.detach().cpu().numpy()
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        predict = torch.argmax(probabilities,dim=-1)
        predictions.extend(predict.cpu().numpy())
        orig_labels.extend(label_ids.cpu().numpy())
    print(flat_classification_report(orig_labels , predictions))
    
# validation 

# predictions = []
# for step, batch in enumerate(tqdm(valid_dataloader)):
#     batch = tuple(t.to(device) for t in batch)
#     input_ids, input_mask, segment_ids, one_hot_labels , predict_mask = batch
#     logits = model(input_ids, input_mask, segment_ids, predict_mask=predict_mask, one_hot_labels=None)
#     logits = logits.detach().cpu().numpy()
#     predictions.extend(np.argmax(logits, -1).tolist())



# Set true for model training 




