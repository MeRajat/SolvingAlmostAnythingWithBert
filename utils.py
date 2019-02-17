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