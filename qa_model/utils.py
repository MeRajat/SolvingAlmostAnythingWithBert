import torch
from sklearn.metrics import f1_score,precision_score,recall_score

def warmup_linear(x, warmup = 0.002):
    if x< warmup:
        return x/warmup

    return 1.0 - x


def metric_fn(per_example_loss, label_ids, logits):
# def metric_fn(label_ids, logits):
    predictions = torch.argmax(logits, axis=-1, output_type=tf.int32)
    precision = tf_metrics.precision(label_ids,predictions,13,[1,2,4,5,6,7,8,9],average="macro")
    recall = tf_metrics.recall(label_ids,predictions,13,[1,2,4,5,6,7,8,9],average="macro")
    f = tf_metrics.f1(label_ids,predictions,13,[1,2,4,5,6,7,8,9],average="macro")
    #
    return {
        "eval_precision":precision,
        "eval_recall":recall,
        "eval_f": f,
        #"eval_loss": loss,
    }

def is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False

def remove_extra_spaces(text):
    char_to_word_offset = []
    prev_is_whitespace = True
    doc_tokens = []
    text.replace('/',' ')  # need review
    for c in text:
        if is_whitespace(c):
            prev_is_whitespace = True
        else:
            if prev_is_whitespace:
                doc_tokens.append(c)
            else:
                doc_tokens[-1] += c
            prev_is_whitespace = False
        char_to_word_offset.append(len(doc_tokens) - 1)
    return char_to_word_offset, doc_tokens

def text_preprocessing(text):
    char_to_word_offset, doc_tokens = remove_extra_spaces(text)
    return char_to_word_offset, doc_tokens


def check_is_max_context(doc_spans, cur_span_index, position):
    best_score = None
    best_span_index = None 
    for (span_index, doc_span) in enumerate(doc_spans):
        end = doc_span.start + doc_span.length - 1 
        if position < doc_span.start:
            continue 
        if position > end:
            continue 
        num_left_context = position - doc_span.start 
        num_right_context = end - position 
        score = min(num_left_context, num_right_context) + 0.01 * doc_span.length 
        if best_score is None or score > best_score:
            best_score = score
            best_span_index = span_index
    return cur_span_index == best_span_index

def improve_answer_span(doc_tokens, input_start, input_end, tokenizer, orig_answer_text):
    tok_answer_text = ' '.join(tokenizer.tokenize(orig_answer_text))
    for new_start in range(input_start, input_end + 1):
        for new_end in range(input_end, new_start -1, -1):
            text_span = " ".join(doc_tokens[new_start:(new_end+1)])
            if text_span == tok_answer_text:
                return (input_start, input_end)
    return (input_start, input_end)
