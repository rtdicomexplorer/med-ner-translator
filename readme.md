## the script is able to:
- recover report from "ReportsDATASET.csv" (https://www.kaggle.com/datasets/saadaldoaij/radiologists-reports?resource=download)
- save all reports (1982)
- translate all reports in  dest =  'de', 'it', 'fr' ....

### How to use it

- python -m venv venv
- venv\scripts\activate
- pip install -r rquirements.txt

the input parameters are :
- destination  de, it, fr
- save original true / false
python main.py de true

