from transformers import MarianMTModel, MarianTokenizer

# Load model and tokenizer only once
model_name = "Helsinki-NLP/opus-mt-mr-en"  # Marathi to English
model_en_mr = "Helsinki-NLP/opus-mt-en-mr"  # English to Marathi

tokenizer_mr_en = MarianTokenizer.from_pretrained(model_name)
model_mr_en = MarianMTModel.from_pretrained(model_name)

tokenizer_en_mr = MarianTokenizer.from_pretrained(model_en_mr)
model_en_mr = MarianMTModel.from_pretrained(model_en_mr)

def translate(text, tokenizer, model):
    tokens = tokenizer.prepare_seq2seq_batch([text], return_tensors="pt", padding=True)
    translation = model.generate(**tokens)
    return tokenizer.batch_decode(translation, skip_special_tokens=True)[0]

def check_grammar(text):
    try:
        # Step 1: Translate from Marathi to English
        english_text = translate(text, tokenizer_mr_en, model_mr_en)

        # Step 2: Translate corrected English back to Marathi
        corrected_text = translate(english_text, tokenizer_en_mr, model_en_mr)

        # Dummy comparison to detect if change occurred
        if corrected_text.strip() != text.strip():
            return {
                "status": "errors_found",
                "corrected_text": corrected_text,
                "original_text": text,
                "note": "Corrected using back-and-forth translation"
            }
        else:
            return {
                "status": "no_errors",
                "corrected_text": text,
                "message": "No grammar errors found"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
