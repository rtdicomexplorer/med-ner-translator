from flask import Flask, request, render_template, flash
from utils import translate_text_with_detection,run_async
from docx import Document
import asyncio

app = Flask(__name__)
app.secret_key = 'your_secret_key'


def extract_text_from_docx(file):
    doc = Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

@app.route('/', methods=['GET', 'POST'])
def index():
    original_text = ""
    translated_text = ""
    dest_lang = "en"  # default
    detected_lang = None

    if request.method == 'POST':
        action = request.form.get('action')
        uploaded_file = request.files.get('file')
        original_text = request.form.get('original_text', '').strip()
        dest_lang = request.form.get('dest_lang', 'en')

        # If a file is uploaded, read its content into original_text (overwrites textarea)
        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()
            if filename.endswith('.txt'):
                original_text = uploaded_file.read().decode('utf-8')
            elif filename.endswith('.docx'):
                original_text = extract_text_from_docx(uploaded_file)
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
        detected_lang=detected_lang
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)