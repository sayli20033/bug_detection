from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils.file_reader import read_text_from_file
from utils.grammar_checker import check_grammar

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = "../uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    # If file is uploaded
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)
            text = read_text_from_file(filepath)
        else:
            return jsonify({"error": "No file selected"}), 400
    else:
        # If text is directly entered
        text = request.form.get("text")
        if not text:
            return jsonify({"error": "No text provided"}), 400

    # Run grammar check
    result = check_grammar(text)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
