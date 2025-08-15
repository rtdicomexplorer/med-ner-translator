from flask import Flask, request, render_template, flash
from utils import translate_text_with_detection,run_async, extract_text_from_docx, extract_text_from_pdf
from marian_transl import  translate_text_marian, languages, available_models
from datetime import datetime
import json
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = ""
    translated_marian = ""
    translated_google = ""
    src_lang  = "en"
    dest_lang = "en"  # default
    detected_lang = None
    file_name = None
    

    if request.method == 'POST':
        action = request.form.get('action')
        uploaded_file = request.files.get('file')
        original_text = request.form.get('original_text', '').strip()
        dest_lang = request.form.get('dest_lang', 'en')
        src_lang = request.form.get("src_lang", 'en')
        file_name = request.form.get('file_name')

        # If a file is uploaded, read its content into original_text (overwrites textarea)
        if uploaded_file and uploaded_file.filename:
            file_name = uploaded_file.filename 
            filename = file_name.lower()
            if filename.endswith('.txt'):
                original_text = uploaded_file.read().decode('utf-8')
            elif filename.endswith('.docx'):
                original_text = extract_text_from_docx(uploaded_file)
            elif filename.endswith('.pdf'):
                original_text = extract_text_from_pdf(uploaded_file)
            else:
                flash("Unsupported file type. Please upload .txt or .docx files.")

        # If user clicked translate and there's text in textarea
        if action == 'translate' and original_text:

            try:
                translated_google, lang_recognized = run_async( translate_text_with_detection(original_text, src=src_lang, dest=dest_lang))
            except Exception as e:
                translated_google = f"[ERROR] {e}"

            try:
                translated_marian = run_async(translate_text_marian(text= original_text, src = src_lang, dest = dest_lang))
            except Exception as e:
                    translated_marian  = f"[ERROR] {e}"   


    return render_template(
        'index.html',
        original=original_text,
        translated_google=translated_google,
        translated_marian=translated_marian,
        dest_lang=dest_lang,
        src_lang = src_lang,
        detected_lang=detected_lang,
        file_name=file_name,
        languages=languages,
        language_names=json.dumps(languages),
        available_models=available_models,
        current_year=datetime.now().year  
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
