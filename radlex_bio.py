from transformers import AutoTokenizer
import json

from  radlex import find_labeled_radlex_entities, extract_text_from_txt, load_radlex_terms_by_label,RADLEX_CSV
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


def align_tokens_with_entities_bio(text, entities,tokenizer,):
    """
    Convert entity spans into BIO labels aligned with BERT tokens.
    """
    encoded = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"])
    offsets = encoded["offset_mapping"]

    labels = ["O"] * len(tokens)

    for ent in entities:
        ent_start = ent['start']
        ent_end = ent['end']
        ent_label = ent['label']

        for i, (start, end) in enumerate(offsets):
            if start >= ent_start and end <= ent_end:
                prefix = "B" if start == ent_start else "I"
                labels[i] = f"{prefix}-{ent_label}"

    return list(zip(tokens, labels))


def align_tokens_with_entities_ner(text, entities, tokenizer, label2id):
    encoded = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"])
    offsets = encoded["offset_mapping"]
    labels = ["O"] * len(tokens)

    for ent in entities:
        ent_start = ent['start']
        ent_end = ent['end']
        ent_label = ent['label']
        for i, (start, end) in enumerate(offsets):
            if start == end == 0:
                continue
            if start >= ent_start and end <= ent_end:
                prefix = "B" if start == ent_start else "I"
                labels[i] = f"{prefix}-{ent_label}"

    # Convert BIO tags to label IDs
    ner_tags = [label2id.get(label, 0) for label in labels]
    return {"tokens": tokens, "ner_tags": ner_tags}

def __create_ner_label_list():

    RADEX_LABEL=  ['MODALITY', 'PLAYBOOK_TYPE', 'POPULATION', 'BODY_REGION', 
                'MODALITY_MODIFIER', 'PROCEDURE_MODIFIER', 'ANATOMIC_FOCUS',
                'LATERALITY', 'REASON_FOR_EXAM', 'TECHNIQUE', 'PHARMACEUTICAL', 'VIEW',
                'SHORT_NAME', 'LONG_NAME']
    label_list = ["O"]  # Outside any entity
    for label in RADEX_LABEL:label_list.extend([f"B-{label}", f"I-{label}"])

    return label_list


def save_ner_results_as_html(tokens, ner_tags, id2label, html_path="ner_output.html"):
    rows = []
    for token, tag_id in zip(tokens, ner_tags):
        tag = id2label.get(tag_id, "O")
        label = tag.split("-")[-1] if "-" in tag else "—"
        rows.append(f"<tr><td>{token}</td><td>{tag}</td><td>{label}</td></tr>")

    html = f"""
    <html>
    <head>
        <title>NER Output</title>
        <style>
            table {{
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 80%;
                margin: 2rem auto;
            }}
            td, th {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            th {{
                padding-top: 12px;
                padding-bottom: 12px;
                background-color: #4CAF50;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h2 style="text-align:center;">NER Token Output</h2>
        <table>
            <thead>
                <tr><th>Token</th><th>NER Tag</th><th>Label</th></tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ NER results saved to {html_path}")



def create_ner_dataset(report, radlex_terms, tokenizer, label2id, output_path="train.jsonl"):
    with open(output_path, "w", encoding="utf-8") as f:
        entities = find_labeled_radlex_entities(report, radlex_terms)
        example = align_tokens_with_entities_ner(report, entities, tokenizer, label2id)
        f.write(json.dumps(example, ensure_ascii=False) + "\n")
        print(f"✅ NER data set for training saved to: {output_path}")
        return example

def create_bio_dataset(report, radlex_dict, output_path="bio_dataset.txt"):
    with open(output_path, "w", encoding="utf-8") as out:
        
        entities = find_labeled_radlex_entities(report, radlex_dict)
        token_label_pairs = align_tokens_with_entities_bio(report, entities, tokenizer)
        for token, label in token_label_pairs:
            out.write(f"{token}\t{label}\n")
        out.write("\n")  # blank line between reports
    print(f"✅ BIO data set saved to: {output_path}")



OUTPUTDIR = 'output'
def main():
    import os

    os.makedirs(OUTPUTDIR, exist_ok=True)
    file_report = "./output_reports/report_0001.txt"
    _, report_file_name = os.path.split(file_report)



    report_file_name, _ = os.path.splitext(report_file_name) 

    report =  extract_text_from_txt(file_report)
    
    output_json = os.path.join(OUTPUTDIR,f"{report_file_name}jsonl")
    output_html = os.path.join(OUTPUTDIR,f"{report_file_name}.html")
    output_bio = os.path.join(OUTPUTDIR,f"{report_file_name}.txt")
    
    # """
    # CT scan of the abdomen and pelvis with contrast demonstrates no acute findings.
    # There is mild hepatomegaly and a right renal cyst.
    # """

    radlex_terms = load_radlex_terms_by_label(RADLEX_CSV)

    ner_label_list  = __create_ner_label_list()
    label2id = {label: i for i, label in enumerate(ner_label_list)}
    id2label = {i: label for label, i in label2id.items()}
    ner_result = create_ner_dataset(report,radlex_terms,tokenizer,label2id,output_path=output_json)
    #save the html mapping
    tokens = ner_result.get('tokens')
    ner_tags = ner_result.get('ner_tags')
    save_ner_results_as_html(tokens=tokens, ner_tags=ner_tags, id2label=id2label,html_path=output_html)
       


    create_bio_dataset(report, radlex_terms,output_path=output_bio)


if __name__ == "__main__":
    main()