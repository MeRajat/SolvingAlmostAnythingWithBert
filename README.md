# Solving BioNLP problems using Bert(BioBert Pytorch)

This repository contains fine-tuning of Biobert[https://arxiv.org/abs/1901.08746] using pytorch. 

## Preparation :- 
To use biobert, download [weights](https://github.com/naver/biobert-pretrained/releases),  and make it compatible with pytorch using script [convert_to_pytorch_wt.ipynb](https://github.com/MeRajat/SolvingAlmostAnythingWithBert/blob/ner_medical/convert_to_pytorch_wt.ipynb). 

Place converted weights into ```weights/``` folder. 

## NER :- 

NER Data can be downloaded using https://github.com/cambridgeltl/MTL-Bioinformatics-2016. 

Select NER data you want to train on and move it to data folder. 

### Datasets 

We have used [BC5CDR](https://biocreative.bioinformatics.udel.edu/tasks/biocreative-v/track-3-cdr/) and [BioNLP13CG](http://2013.bionlp-st.org/). 

BC5CDR tags :- 
```
    'B-Chemical', 
    'O', 
    'B-Disease', 
    'I-Disease', 
    'I-Chemical'
```

BioNLP13CG tags :- 
``` 'B-Amino_acid',
'B-Anatomical_system',
'B-Cancer',
'B-Cell', 
'B-Cellular_component',
'B-Developing_anatomical_structure',
'B-Gene_or_gene_product', 
'B-Immaterial_anatomical_entity',
'B-Multi-tissue_structure',
'B-Organ',
'B-Organism', 
'B-Organism_subdivision',
'B-Organism_substance',
'B-Pathological_formation', 
'B-Simple_chemical',
'B-Tissue',
'I-Amino_acid',
'I-Anatomical_system',
'I-Cancer', 
'I-Cell',
'I-Cellular_component',
'I-Developing_anatomical_structure',
'I-Gene_or_gene_product', 
'I-Immaterial_anatomical_entity',
'I-Multi-tissue_structure',
'I-Organ',
'I-Organism', 
'I-Organism_subdivision',
'I-Organism_substance',
'I-Pathological_formation',
'I-Simple_chemical', 
'I-Tissue',
'O'
```



