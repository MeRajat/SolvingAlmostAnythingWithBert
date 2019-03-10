# Solving BioNLP problems using Bert(BioBert Pytorch)

Working Demo For NER can be found [here](http://13.72.66.146:5000/)

This repository contains fine-tuning of Biobert[https://arxiv.org/abs/1901.08746].

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

## Result 

After fine-tuning it with biobert weights result were pretty good, <b>F1-score</b> for BC5CDR was <b>95</b> and for BioNLP13CG was <b>92</b>. 

Examples 

BC5CDR :- 

```
Sentence = The authors describe the case of a 56 - year - old woman with chronic , severe heart failure secondary to dilated cardiomyopathy and absence of significant ventricular arrhythmias who developed QT prolongation and torsade de pointes ventricular tachycardia during one cycle of intermittent low dose ( 2 . 5 mcg / kg per min ) dobutamine . 

Result =
{"tagging":[["The","O"],["authors","O"],["describe","O"],
["the","O"],["case","O"],["of","O"],["a","O"],["56","O"],["-",
"O"],["year","O"],["-","O"],["old","O"],["woman","O"],["with",
"O"],["chronic","O"],[",","O"],["severe","O"],["heart",
"I-Disease"],["failure","I-Disease"],["secondary","O"],["to",
"O"],["dilated","B-Disease"],["cardiomyopathy","I-Disease"],
["and","O"],["absence","O"],["of","O"],["significant","O"],
["ventricular","B-Disease"],["arrhythmias","I-Disease"],
["who","O"],["developed","O"],["QT","B-Disease"],
["prolongation","I-Disease"],["and","O"],["torsade",
"B-Disease"],["de","I-Disease"],["pointes","I-Disease"],
["ventricular","I-Disease"],["tachycardia","I-Disease"],
["during","O"],["one","O"],["cycle","O"],["of","O"],
["intermittent","O"],["low","O"],["dose","O"],["(","O"],["2",
"O"],[".","O"],["5","O"],["mcg","O"],["/","O"],["kg","O"],
["per","O"],["min","O"],[")","O"],["dobutamine","B-Chemical"],
[".","O"]]}

```

BioNLP13CG :- 

```
Sentence = Cooccurrence of reduced expression of alpha - catenin and overexpression of p53 is a predictor of lymph node metastasis in early gastric cancer . 


Result = 
{"tags":[["Cooccurrence","O"],["of","O"],["reduced","O"],
["expression","O"],["of","O"],["alpha",
"B-Gene_or_gene_product"],["-","I-Gene_or_gene_product"],
["catenin","I-Gene_or_gene_product"],["and","O"],
["overexpression","O"],["of","O"],["p53",
"B-Gene_or_gene_product"],["is","O"],["a","O"],["predictor",
"O"],["of","O"],["lymph","B-Multi-tissue_structure"],["node",
"I-Multi-tissue_structure"],["metastasis","O"],["in","O"],
["early","O"],["gastric","B-Cancer"],["cancer","I-Cancer"],
[".","O"]]}

```



<img src="https://github.com/MeRajat/SolvingAlmostAnythingWithBert/blob/ner_medical/extras/ezgif.com-video-to-gif.gif" width="700" height="400" />

