import parameters as param
import pickle
import numpy as np 
import torch 
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from tqdm import tqdm


class InputExample:
    def __init__(self, id, text, label):
        self.id = id 
        self.text = text 
        self.label = label 


class InputFeatures(object):
    def __init__(self, input_ids, input_mask, segment_ids, predict_mask, one_hot_labels, label_ids, ntokens):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.predict_mask = predict_mask
        self.one_hot_labels = one_hot_labels    
        self.label_ids = label_ids
        self.ntokens = ntokens

# class DataProcessor:
#     def get_train_examples(self, data_dir):
#         raise NotImplementedError()
        
#     def get_dev_examples(self, data_dir):
#         raise NotImplementedError()
        

        

class NerProcessor():
    def get_examples(self, lines_pkl):
        return self._create_example(lines_pkl)
    
    def _create_example(self, lines_pkl):
        train_lines = pickle.load(open(f'data/{lines_pkl}', 'rb'))
        examples = []
        for i, line in enumerate(train_lines):
            id = f'{i}'
            text = (line[0])
            label = (line[1])    
            examples.append(InputExample(id=id, text=text, label=label))
        return examples
    def get_labels(self):
        return ["B", "I", "O", "X", "[CLS]", "[SEP]"] 

    def get_label_map(self):
        label_map = {}
        for (i, label) in enumerate(["B", "I", "O", "X", "[CLS]", "[SEP]"]):
            label_map[label] = i
        return label_map


def return_feature(example, tokenizer, label_map, max_seq_length):
    text_list = example.text.split(' ')
    label_list = example.label.split(' ')
    tokens = []
    labels = []
    predict_mask = [0]
    for i, word in enumerate(text_list):
        token = tokenizer.tokenize(word)
        tokens.extend(token)
        label_l = label_list[i]
        for m in range(len(token)):
            if m == 0:
                predict_mask.append(1)
                labels.append(label_l)
            else:
                predict_mask.append(0)
                labels.append("X")
            
    if len(tokens) >= max_seq_length - 1:
        tokens = tokens[0:(max_seq_length - 2)]
        labels = labels[0:(max_seq_length - 2)]
        predict_mask = predict_mask[0:(max_seq_length - 2)]
    ntokens = []
    segment_ids = []
    label_ids = []
    ntokens.append('[CLS]')
    segment_ids.append(0)
    label_ids.append(label_map["[CLS]"])
    for i, token in enumerate(tokens):
        ntokens.append(token)
        segment_ids.append(0)
        label_ids.append(label_map[labels[i]])
    ntokens.append("[SEP]")
    segment_ids.append(0)
    label_ids.append(label_map["[SEP]"])
    predict_mask.append(0)
    # Verify predict_mask size with label_ids
    while len(predict_mask) < len(label_ids):
        predict_mask.append(0)
    input_ids = tokenizer.convert_tokens_to_ids(ntokens)
    input_mask = [1] * len(input_ids)
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)        
        segment_ids.append(0)
        label_ids.append(0)
        predict_mask.append(0)
        ntokens.append("**NULL**")
    
    one_hot = np.eye(len(label_map.keys()), dtype=np.float32)[label_ids]
    feature = InputFeatures(input_ids=(input_ids),
                           input_mask = (input_mask),
                            segment_ids = (segment_ids),
                            one_hot_labels = (one_hot),
                           predict_mask = predict_mask,
                           label_ids = label_ids,
                           ntokens = ntokens)
    
    return feature



def return_dataloader(examples, tokenizer, label_map, batch_size=32):
    # Convert to features
    features = []
    for i, example in tqdm(enumerate(examples)):
        features.append(return_feature(example, tokenizer=tokenizer, label_map=label_map, max_seq_length=param.MAX_SEQ_LENGTH))

    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    all_one_hot_labels = torch.tensor([f.one_hot_labels for f in features], dtype=torch.float32)
    all_predict_masks = torch.ByteTensor([f.predict_mask for f in features])
    all_label_ids = torch.tensor([f.label_ids for f in features], dtype=torch.long)
    all_ntokens = [f.ntokens for f in features]
    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_one_hot_labels , all_predict_masks, all_label_ids)
    sampler = RandomSampler(dataset)

    dataloader = DataLoader(dataset, sampler=sampler, batch_size=batch_size)
    return dataloader, all_ntokens