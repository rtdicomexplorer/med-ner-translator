from flask import Flask, request, render_template, flash
from utils import translate_text_with_detection,run_async, extract_text_from_docx, extract_text_from_pdf
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'your_secret_key'


import json
import os

# Load languages from JSON once at startup
with open(os.path.join(os.path.dirname(__file__), 'languages.json'), 'r', encoding='utf-8') as f:
    languages = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = ""
    translated_text = ""
    dest_lang = "en"  # default
    detected_lang = None
    file_name = None

    if request.method == 'POST':
        action = request.form.get('action')
        uploaded_file = request.files.get('file')
        original_text = request.form.get('original_text', '').strip()
        dest_lang = request.form.get('dest_lang', 'en')
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

                translated_text, detected_lang = run_async( translate_text_with_detection(original_text, dest=dest_lang)
                                            )
            except Exception as e:
                translated_text = f"[ERROR] {e}"

    return render_template(
        'index.html',
        original=original_text,
        translated=translated_text,
        dest_lang=dest_lang,
        detected_lang=detected_lang,
        file_name=file_name,
        languages=languages,
        current_year=datetime.now().year  
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
