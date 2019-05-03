from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM
import torch 
import json 
import re 
import ftfy
from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
import torch
import uvicorn
import aiohttp

app = Starlette()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

bert_model = 'bert-large-uncased'
tokenizer = BertTokenizer.from_pretrained(bert_model)
model = BertForMaskedLM.from_pretrained(bert_model)
_ = model.eval().to(device)
print("model loaded")
def get_score(model, tokenizer, q_tensors, s_tensors, m_index, candidate):
    candidate_tokens = tokenizer.tokenize(candidate)
    candidate_ids = tokenizer.convert_tokens_to_ids(candidate_tokens)
    
    preds = model(q_tensors.to(device), s_tensors.to(device))
    predictions_candidates = preds[0, m_index, candidate_ids].mean()
    return predictions_candidates.item()


def get_word(row):
    """
    
    """
    question = re.sub('\_+', ' [MASK] ', ftfy.fix_encoding(row['question']))
    question_tokens = tokenizer.tokenize(question)
    masked_index = question_tokens.index('[MASK]')
    ## Make segments 
    segment_ids = [0] * len(question_tokens)
    segment_tensors = torch.tensor([segment_ids])
    # Convert tokens to ids and tensors 
    question_ids = tokenizer.convert_tokens_to_ids(question_tokens)
    question_tensors = torch.tensor([question_ids]).to(device)
    
    candidates = [ftfy.fix_encoding(row['1']), ftfy.fix_encoding(row['2']), ftfy.fix_encoding(row['3']), ftfy.fix_encoding(row['4'])]
    
    predict_tensor = torch.tensor([get_score(model, tokenizer, question_tensors, segment_tensors, masked_index, candidate) for candidate in candidates])
    predict_idx = torch.argmax(predict_tensor).item()
    return candidates[predict_idx], predict_tensor


@app.route("/fill_blank", methods = ["GET"])
async def fill_blank(request):
    row = {}
    row["question"] = request.query_params["question"]
    row["1"] = request.query_params["op1"]
    row["2"] = request.query_params["op2"]
    row["3"] = request.query_params["op3"]
    row["4"] = request.query_params["op4"]
    correct_word, prob_tensor = get_word(row)
    return JSONResponse({'word': correct_word})




@app.route("/")
def form(_):
    return HTMLResponse("""
    <h3> Try the intelligent fill in the blanks  </h3>
    <form action = "/fill_blank", method = "get">
        <label for="question">Sentence:</label>
        <textarea rows = "10" cols = "60", name = "question"></textarea><br>
        <label for="op1">Option1:</label>
        <textarea rows = "2" cols = "60", name = "op1"></textarea><br>
        <label for="op2">Option2:</label>
        <textarea rows = "2" cols = "60", name = "op2"></textarea><br>
        <label for="op3">Option3:</label>
        <textarea rows = "2" cols = "60", name = "op3"></textarea><br>
        <label for="op4">Option4:</label>
        <textarea rows = "2" cols = "60", name = "op4"></textarea><br>
        <input type="submit" name ="fill blank" value = "fill" >
    </form>
    """)

@app.route("/form")
def redirect_to_homepage(_):
    return RedirectResponse("/")



if __name__ == "__main__":
    # To run this app start application on server with python
    # python FILENAME serve
    # ex: python server.py serve
    # if "serve" in sys.argv:
    uvicorn.run(app, host="0.0.0.0", port=9000)

