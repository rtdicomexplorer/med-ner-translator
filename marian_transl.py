from transformers import MarianMTModel, MarianTokenizer

# Cache loaded models to avoid reloading
_model_cache = {}

def get_model_name(src_lang, tgt_lang):
    return f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"

def load_model(src_lang, tgt_lang):
    model_key = f"{src_lang}-{tgt_lang}"
    if model_key not in _model_cache:
        model_name = get_model_name(src_lang, tgt_lang)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        _model_cache[model_key] = (tokenizer, model)
    return _model_cache[model_key]


async def translate_text_marian(text, src_lang, tgt_lang):
    tokenizer, model = load_model(src_lang, tgt_lang)

    lines = text.splitlines()
    translations = []

    for line in lines:
        line = line.strip()
        if not line:
            translations.append('')  # preserve empty lines
            continue

        inputs = tokenizer(line, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        translations.append(output)

    return '\n'.join(translations)
