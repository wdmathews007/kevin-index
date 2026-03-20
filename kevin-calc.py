import os
import sys
from pathlib import Path

import flask
from pypdf import PdfReader

from grammer_rules import (
    punctuationRules,
    scentenceStarters,
    sentenceStructure,
    structuralDiscourse,
    wordChoice,
)

kevin_index = [
    punctuationRules.rules,
    scentenceStarters.rules,
    sentenceStructure.rule,
    structuralDiscourse.rule,
    wordChoice.rules,
]

kevin_index = [item for sublist in kevin_index for item in sublist]

weights = [
    -10.0,
    3,
    5,
    1,
    -2,
    -3,
    2,
    1,
    -3,
    -3,
    -3,
    3,
    -3,
    -2,
    -2,
    -2,
    3,
    3,
    -2,
    -2,
    -4,
    -4,
    3,
    -3,
    -3,
    -3
]

def calc_kevin_index(text):
    index = 0
    stat_vals = []

    i = 0
    for i in range(len(kevin_index)):
        val = kevin_index[i](text)
        stat_vals.append(val)

        index += val * weights[i]

    return index, stat_vals


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    return "".join(page.extract_text() or "" for page in reader.pages)


PUBLIC_DIR = Path(__file__).resolve().parent / "public"
app = flask.Flask(__name__, static_folder=str(PUBLIC_DIR), static_url_path="")


@app.get("/")
def serve_index():
    return app.send_static_file("index.html")

@app.post("/api/calculate")
def calculate_api():
    data = flask.request.get_json()
    if not data or "text" not in data:
        return flask.jsonify({"error": "No text provided"}), 400
        
    text = data.get("text", "")
    index, vals = calc_kevin_index(text)
    
    return flask.jsonify({"index": index, "stats": vals})

@app.get("/<path:asset_path>")
def serve_public_asset(asset_path):
    if (PUBLIC_DIR / asset_path).is_file():
        return app.send_static_file(asset_path)

    flask.abort(404)


def run_server():
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    app.run(host=host, port=port, debug=False)


def print_usage():
    script_name = Path(sys.argv[0]).name
    print(f"Usage: python {script_name} serve | <pdf-path>")


if __name__ == "__main__":
    run_server()
