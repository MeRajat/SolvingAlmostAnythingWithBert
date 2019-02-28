from data_load import HParams
from new_model import Net
from pytorch_pretrained_bert.modeling import BertConfig
from pytorch_pretrained_bert import BertModel
import parameters
from flask import Flask
from flask import request, abort, jsonify


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


app = Flask(__name__)
@app.route('api/ner/bc5cdr', methods = ['POST'])
def get_bc5cdr():
    if not request.json or not 'query' in request.json:
        abort(400)

    hp = HParams('bc5cdr')
    out = process_query(query=request.json['query'], hp=hp, model=bc5_model)
    return jsonify({'tagging': out})



@app.route('api/ner/bionlp13cg', methods = ['POST'])
def get_bc5cdr():
    if not request.json or not 'query' in request.json:
        abort(400)

    hp = HParams('bionlp3g')
    out = process_query(query=request.json['query'], hp=hp, model=bionlp13cg_model)
    return jsonify({'tagging': out})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9000')