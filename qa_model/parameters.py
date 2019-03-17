MAX_SEQ_LENGTH = 384
VOCAB_FILE = 'weights/pubmed_pmc_470k/vocab.txt'
state_dict = 'weights/pytorch_weight'
BERT_CONFIG_FILE = 'weights/pubmed_pmc_470k/bert_config.json'
BATCH_SIZE = 32
lr = 1e-3
gradient_accumulation_steps = 1
EPOPCH = 10
warmup_proportions = 0.1

MAX_QUERY_LENGTH = 64 
DOC_STRIDE = 128  # splitting up a long document into chunks 


