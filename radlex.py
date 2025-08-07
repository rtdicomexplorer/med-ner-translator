import pandas as pd
import re
import nltk

from nltk.tokenize import word_tokenize

RADLEX_CSV = "./documents/core-playbook-dev.csv"  # Vocabulary for pattern-based NER

def extract_text_from_txt(txt_path):
    text = ""
    try:
        with open(txt_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
            print(f"Error reading txt {txt_path}: {e}")
    return text.strip()


def load_radlex_terms_by_label(path):
    df = pd.read_csv(path)


    label_to_columns = {
        "MODALITY": ['MODALITY', 'MODALITY_MODIFIER', 'MODALITY_MODIFIER_2', 'MODALITY_MODIFIER_3'],
        "PROCEDURE_MODIFIER": ['PROCEDURE_MODIFIER', 'PROCEDURE_MODIFIER_2'],
        "ANATOMIC_FOCUS": ['ANATOMIC_FOCUS', 'ANATOMIC_FOCUS_2'],
        "BODY_REGION": ['BODY_REGION', 'BODY_REGION_2', 'BODY_REGION_3', 'BODY_REGION_4', 'BODY_REGION_5'],
        "LATERALITY": ['LATERALITY'],
        "REASON_FOR_EXAM": ['REASON_FOR_EXAM', 'REASON_FOR_EXAM_2', 'REASON_FOR_EXAM_3'],
        "TECHNIQUE": ['TECHNIQUE'],
        "PHARMACEUTICAL": ['PHARMACEUTICAL', 'PHARMACEUTICAL_2'],
        "VIEW": ['VIEW', 'VIEW_2', 'VIEW_3', 'VIEW_4'],
        "NAME": ['SHORT_NAME', 'LONG_NAME']
    }

    stopwords = {'none', 'n/a', 'na', 'unknown'}
    pattern = re.compile(r'^[a-z\s\-]+$')  # letters, spaces, and hyphens
    terms_by_label = {}

    for label, columns in label_to_columns.items():
        term_set = set()
        for col in columns:
            if col not in df.columns:
                continue
            col_values = df[col].dropna().astype(str)
            for val in col_values:
                val = val.strip().lower()
                if val not in stopwords and len(val.split()) <= 6 and pattern.match(val):
                    term_set.add(val)
        terms_by_label[label] = list(term_set)

    return terms_by_label


def find_labeled_radlex_entities(text, labeled_terms):
    matches = []
    for label, terms in list(labeled_terms.items()):
        for term in terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            for match in re.finditer(pattern, text.lower()):
                matches.append({
                    "term": term,
                    "start": match.start(),
                    "end": match.end(),
                    "label": label
                })
    return matches



def text_to_iob(text, entities):
    """
    It uses nlkt natural language tokenizer to recover token....
    """
    
    tokens = word_tokenize(text)
    iob_tags = ['O'] * len(tokens)

    for i, token in enumerate(tokens):
        token_start = text.find(token, sum(len(t) + 1 for t in tokens[:i]))  # account for spaces
        token_end = token_start + len(token)

        for ent in entities:
            if ent["start"] <= token_start < ent["end"]:
                prefix = "B" if token_start == ent["start"] else "I"
                iob_tags[i] = f"{prefix}-{ent['label']}"
                break

    return list(zip(tokens, iob_tags))



def main():
    nltk.download('punkt')
    nltk.download('punkt_tab')
    file_report = "./output_reports/report_0001.txt"


    report =  extract_text_from_txt(file_report)
    
    
    # """
    # CT scan of the abdomen and pelvis with contrast demonstrates no acute findings.
    # There is mild hepatomegaly and a right renal cyst.
    # """

    radlex_terms = load_radlex_terms_by_label(RADLEX_CSV)

    entities = find_labeled_radlex_entities(report, radlex_terms)
    for ent in entities:
        print(ent)

    iob = text_to_iob(report, entities)
    for tok, tag in iob:
        print(f"{tok}\t{tag}")



if __name__ == "__main__":
    main()
