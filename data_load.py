import numpy as np 
import torch.utils import data 

import torch 
from pytorch_pretrained_bert import BertTokenizer


class HParams:
    VOCAB = ('<PAD>', 'B-Chemical' 'O', 'B-Disease' , 'I-Disease', 'I-Chemical')
    tag2idx = {v:k for k,v in enumerate(VOCAB)}
    idx2tag = {k:v for k,v in enumerate(VOCAB)}

    batch_size = 128 
    lr = 0.0001
    n_epochs = 30 

    tokenizer = BertTokenizer(vocab_file='/home/ubuntu/biobert/weights/pubmed_pmc_470k/vocab.txt', do_lower_case=False)


hp = HParams()
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class NERDataser(data.Dataset):
    def __init__(self, path):
        instances = open(path).read().strip().split('\n\n')
        sents = []
        tags_li = []
        for instance in instances:
            words = [line.split()[0] for line in entry.splitlines()]
            tags = ([line.split()[-1] for line in entry.splitlines()])
            sents.append(["[CLS]"] + words + ["[SEP]"])
            tags_li.append(["<PAD>"] + tags + ["<PAD>"])
        self.sents, self.tags_li = sents, tags_li

    def __len__(self):
        return len(self.sents)


    def __getitem(self, idx):
        words, tags = self.sents[idx], self.tags_li[idx] # words, tags: string list

        # We give credits only to the first piece.
        x, y = [], [] # list of ids
        is_heads = [] # list. 1: the token is the first piece of a word
        for w, t in zip(words, tags):
            tokens = hp.tokenizer.tokenize(w) if w not in ("[CLS]", "[SEP]") else [w]
            xx = hp.tokenizer.convert_tokens_to_ids(tokens)

            is_head = [1] + [0]*(len(tokens) - 1)

            t = [t] + ["<PAD>"] * (len(tokens) - 1)  # <PAD>: no decision
            yy = [hp.tag2idx[each] for each in t]  # (T,)

            x.extend(xx)
            is_heads.extend(is_head)
            y.extend(yy)

        assert len(x)==len(y)==len(is_heads), f"len(x)={len(x)}, len(y)={len(y)}, len(is_heads)={len(is_heads)}"

        # seqlen
        seqlen = len(y)

        # to string
        words = " ".join(words)
        tags = " ".join(tags)
        return words, x, is_heads, tags, y, seqlen


def pad(batch):
    '''Pads to the longest sample'''
    f = lambda x: [sample[x] for sample in batch]
    words = f(0)
    is_heads = f(2)
    tags = f(3)
    seqlens = f(-1)
    maxlen = np.array(seqlens).max()

    f = lambda x, seqlen: [sample[x] + [0] * (seqlen - len(sample[x])) for sample in batch] # 0: <pad>
    x = f(1, maxlen)
    y = f(-2, maxlen)


    f = torch.LongTensor

    return words, f(x), is_heads, tags, f(y), seqlens