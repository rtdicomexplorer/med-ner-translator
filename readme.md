## the script is able to:
- recover report from "ReportsDATASET.csv" (https://www.kaggle.com/datasets/saadaldoaij/radiologists-reports?resource=download)
- save all reports (1982)
- translate all reports to  dest =  'de', 'it', 'fr' ....

### How to use it

- python -m venv venv
- venv\scripts\activate
- pip install -r rquirements.txt

the input parameters are :
- destination  de, it, fr
- save original true / false

#### python main.py de true



### Second case generating patterns from Rad-lexicon
- https://www.rsna.org/practice-tools/data-tools-and-standards/radlex-radiology-lexicon

- the file  core-playbook-de.csv has been already downloaded

- now we can extract label from core-playbook-de.csv

    RADEX_LABEL=  ['MODALITY', 'PLAYBOOK_TYPE', 'POPULATION', 'BODY_REGION', 
                'MODALITY_MODIFIER', 'PROCEDURE_MODIFIER', 'ANATOMIC_FOCUS',
                'LATERALITY', 'REASON_FOR_EXAM', 'TECHNIQUE', 'PHARMACEUTICAL', 'VIEW',
                'SHORT_NAME', 'LONG_NAME']

- then create the NER label for our model and using the previous reports ('en') without 
translation to create the train dataset for the model.

#### take a look at radlex_bio.py