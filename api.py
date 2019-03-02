from data_load import HParams
from new_model import Net
from pytorch_pretrained_bert.modeling import BertConfig
from pytorch_pretrained_bert import BertModel
import parameters
import numpy as np 
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
import torch
import sys
import uvicorn
import aiohttp


config = BertConfig(vocab_size_or_config_json_file=parameters.BERT_CONFIG_FILE)
app = Starlette()


def build_model(config, state_dict, hp):
    model = Net(config, vocab_len = len(hp.VOCAB), bert_state_dict=None)
    _ = model.load_state_dict(torch.load(state_dict, map_location='cpu'))
    _ = model.to('cpu')  # inference 
    return model 


# Model loaded 
bc5_model = build_model(config, parameters.BC5CDR_WEIGHT, HParams('bc5cdr'))
bionlp13cg_model = build_model(config, parameters.BIONLP13CG_WEIGHT, HParams('bionlp3g'))


# Process Query 
def process_query(query, hp, model):
    s = query
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
    _, _, y_pred = model(x, torch.Tensor([1, 2, 3]))  # just a dummy y value
    preds = y_pred[0].cpu().numpy()[np.array(is_heads) == 1]  # Get prediction where head is 1 

    # convert to real tags and remove <SEP> and <CLS>  tokens labels 
    preds = [hp.idx2tag[i] for i in preds][1:-1]
    final_output = []
    for word, label in zip(s.split(), preds):
        final_output.append([word, label])
    return final_output


def get_bc5cdr(query):
    hp = HParams('bc5cdr')
    out = process_query(query=query, hp=hp, model=bc5_model)
    return JSONResponse({'tagging': out})


def get_bionlp13cg(query):
    hp = HParams('bionlp3g')
    out = process_query(query=query, hp=hp, model=bionlp13cg_model)
    return JSONResponse({'tags': out})


@app.route("/extract-ner", methods=["GET"])
async def extract_ner(request):
    text = request.query_params["text"]
    if "bionlp3g" in request.query_params:
        return get_bionlp13cg(text)
    else:
        return get_bc5cdr(text)


@app.route("/")
def form(_):
    return HTMLResponse(
        """
        <h3>This app will find the NER!<h3>
        <form action="/extract-ner" method="get">
            <textarea rows="10" cols="60" name="text">
            </textarea><br>
            <input type="submit" name="bionlp3g" value="BIO NLP 3G">
            <input type="submit" name="bc5cdr" value="BC 5 CDR">
        </form>
    """)


@app.route("/form")
def redirect_to_homepage(_):
    return RedirectResponse("/")


if __name__ == "__main__":
    # To run this app start application on server with python
    # python FILENAME serve
    # ex: python server.py server
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=9000)
