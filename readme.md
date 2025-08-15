# The project is composed of three Parts:

## Preparation:
- python -m venv venv
- venv\scripts\activate
- pip install -r rquirements.txt

## 1 - First Part recover english report as text from

- recover report from "ReportsDATASET.csv" (https://www.kaggle.com/datasets/saadaldoaij/radiologists-reports?resource=download)
- save all reports (1982)
- translate all reports to  dest =  'de', 'it', 'fr' ....
- this part uses just google trans, also you need to be online. 

### How to use it


the input parameters are :
- destination  de, it, fr, ....
- save original true / false

> python main.py de true



## 2 - Second Part generating patterns from Rad-lexicon
- https://www.rsna.org/practice-tools/data-tools-and-standards/radlex-radiology-lexicon

- the file  core-playbook-de.csv has been already downloaded

- now we can extract label from core-playbook-de.csv

    >RADEX_LABEL=  ['MODALITY', 'PLAYBOOK_TYPE', 'POPULATION', 'BODY_REGION', 
                'MODALITY_MODIFIER', 'PROCEDURE_MODIFIER', 'ANATOMIC_FOCUS',
                'LATERALITY', 'REASON_FOR_EXAM', 'TECHNIQUE', 'PHARMACEUTICAL', 'VIEW',
                'SHORT_NAME', 'LONG_NAME']

- then create the NER label for our model and using the previous reports ('en') without 
translation to create the train dataset for the model.

### How to use it
>python radlex_bio.py


## 3 - Third Part translate also offline through a web app:

Translate text offline, googletrans works just online.  

MarianMT model permits offlines translations, but before you must download all the models of a part of them list in *languages.json*.
To do that let's run 
>python marian_tranls.py 

all available Models (combination of all languages present in language.json) will be downloaded in  *.models/*. At moment they are 53 with 14 GB.  
**Also download just the necessary.**

A file with the available models (***available_models.json***) will be created too. Here are listed for each language the possible translations supported.

### Ready to start
A small flask app.py permit to launch a web page where is possible to translate uploaded documents.

>python app.py 





before you need to run 