from transformers import MarianMTModel, MarianTokenizer
import json
import os
from itertools import product

languages = None
available_models = None

languages_file="languages.json"
available_models_file = "available_models.json"
MODEL_DIR ="models"
_model_cache = {}  # Cache loaded models to avoid reloading

with open(languages_file, "r", encoding="utf-8") as f:
    languages = json.load(f)

if os.path.exists(available_models_file):
    with open(available_models_file, "r",encoding="utf-8") as f:
        available_models = json.dumps(json.load(f))



def __get_model_name(src_lang, tgt_lang):
    return f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"

def __get_local_model_path(src_lang, tgt_lang):
    return os.path.join("models", f"opus-mt-{src_lang}-{tgt_lang}")

def __load_model(src_lang, tgt_lang):
    model_key = f"{src_lang}-{tgt_lang}"
    
    if model_key not in _model_cache:
        local_path = __get_local_model_path(src_lang= src_lang,tgt_lang= tgt_lang)

        if not os.path.exists(local_path):
            raise FileNotFoundError(
                f"❌ Translation model not found for {src_lang} → {tgt_lang}.\n"
                f"Expected at: {local_path}\n"
                f"Please run download_models() to fetch it."
            )

        # Load from local path
        tokenizer = MarianTokenizer.from_pretrained(local_path)
        model = MarianMTModel.from_pretrained(local_path)

        _model_cache[model_key] = (tokenizer, model)

    return _model_cache[model_key]



def __get_local_model_path(src_lang, tgt_lang):
    return os.path.join("models", f"opus-mt-{src_lang}-{tgt_lang}")




def __download_models():
    lang_codes = list(languages.keys())  # ['en', 'fr', 'de', ...]
    os.makedirs(MODEL_DIR, exist_ok=True)
    for src_lang, tgt_lang in product(lang_codes, repeat=2):
        if src_lang == tgt_lang:
            continue  # Skip same-language pairs

        model_name = __get_model_name(src_lang, tgt_lang)
        local_path = __get_local_model_path(src_lang, tgt_lang)

        if os.path.exists(local_path):
            print(f"✔️ Already downloaded: {model_name}")
            continue

        try:
            print(f"⬇️ Downloading: {model_name}")
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name)

            tokenizer.save_pretrained(local_path)
            model.save_pretrained(local_path)

            print(f"✅ Saved to: {local_path}\n")
        except Exception as e:
            print(f"❌ Error downloading {model_name}: {e}\n")


def __generate_available_pairs(model_dir="models"):
    pairs = {}
    for folder in os.listdir(model_dir):
        if folder.startswith("opus-mt-"):
            parts = folder.replace("opus-mt-", "").split("-")
            if len(parts) != 2:
                continue
            src, tgt = parts
            pairs.setdefault(src, []).append(tgt)
    with open("available_models.json", "w") as f:
        json.dump(pairs, f, indent=2)
    return pairs


async def translate_text_marian(text, src, dest):
    tokenizer, model = __load_model(src_lang= src, tgt_lang=dest)

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



if __name__ == "__main__":
    __download_models()
    __generate_available_pairs()