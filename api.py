from data_load import HParams
from new_model import Net
from pytorch_pretrained_bert.modeling import BertConfig
from pytorch_pretrained_bert import BertModel
import parameters

config = BertConfig(vocab_size_or_config_json_file=parameters.BERT_CONFIG_FILE)

def build_model(config, state_dict, hp):
    model = Net(config, len(hp.VOCAB), bert_state_dict=None)
    _ = model.load_state_dict(torch.load(state_dict))
    _ = model.to(hp.device)
    return model 


# Model loaded 
bc5_model = build_model(config, parameters.BC5CDR_WEIGHT, HParams('bc5cdr'))
bionlp13cg_model = build_model(config, parameters.BIONLP13CG_WEIGHT, HParams('bionlp3g'))


# Process Query 
def process_query(query, hp, model):
    split_s = ["[CLS]"] + s.split()+["[SEP]"]
    x = [] # list of ids
    is_heads = [] # list. 1: the token is the first piece of a word

    for w in split_s:
        tokens = hp.tokenizer.tokenize(w) if w not in ("[CLS]", "[SEP]") else [w]
        xx = hp.tokenizer.convert_tokens_to_ids(tokens)
        is_head = [1] + [0]*(len(tokens) - 1)
        x.extend(xx)
        is_heads.extend(is_head)

    x = torch.LongTensor(x).unsqueeze(dim=0)

    # Process query 
    model.eval()
    _, _, y_pred = model(x, torch.Tensor([1,2,3]))  # just a dummy y value 
    preds = y_pred[0].cpu().numpy()[np.array(is_heads) == 1]  # Get prediction where head is 1 

    # convert to real tags and remove <SEP> and <CLS>  tokens labels 
    preds = [hp.idx2tag[i] for i in preds][1:-1]
    final_output = []
    for word, label in zip(s.split(), preds):
        final_output.append([word, label])
    return final_output


def process_output(x, y_pred, is_heads, hp):
    









# Load pretrained model 
s = "These data support the hypothesis that SE - induced mossy fiber sprouting and synaptic reorganization are relevant characteristics of seizure development in these murine strains , resembling rat models of human temporal lobe epilepsy ."

hp = HParams()

split_s = ["[CLS]"] + s.split()+["[SEP]"]

x = [] # list of ids
is_heads = [] # list. 1: the token is the first piece of a word
for w in split_s:
    tokens = hp.tokenizer.tokenize(w) if w not in ("[CLS]", "[SEP]") else [w]
    xx = hp.tokenizer.convert_tokens_to_ids(tokens)
    is_head = [1] + [0]*(len(tokens) - 1)
    x.extend(xx)
    is_heads.extend(is_head)


x = torch.LongTensor(x).unsqueeze(dim=0)

x

_, _, y_pred = model(x, torch.Tensor([1,2,3]))

y_pred

# get where head is 1 
preds = [pred for pred, head in zip(y_pred, is_heads) if head == 1]

preds

hp.idx2tag

' '.join([hp.idx2tag[i] for i in preds[0].cpu().numpy().tolist()])

O O O O O O B-Disease O O O O O O O O O O O O B-Disease O O O O O O O O O O O B-Disease I-Disease I-Disease O