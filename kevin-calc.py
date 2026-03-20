import json
import math
import os
import sys
from functools import lru_cache
from pathlib import Path

import flask
from pypdf import PdfReader

from grammer_rules import (
    punctuationRules,
    scentenceStarters,
    sentenceStructure,
    wordChoice,
)

kevin_index = [
    punctuationRules.rules,
    scentenceStarters.rules,
    sentenceStructure.rule,
    wordChoice.rules[1:],
]

kevin_index = [item for sublist in kevin_index for item in sublist]
TEXT_DATA_DIR = Path(__file__).resolve().parent / "text_data"
AI_CACHE = TEXT_DATA_DIR / "ai_samples.json"
HUMAN_CACHE = TEXT_DATA_DIR / "human_samples.json"
MAX_ABS_Z_SCORE = 4.0
DISPLAY_WEIGHT_MIN = 0.8
DISPLAY_WEIGHT_MAX = 1.25
RULE_DIRECTION_OVERRIDES = {}
DISPLAY_WEIGHT_OVERRIDES = {}


def _mean(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def _stddev(values):
    if not values:
        return 1.0

    avg = _mean(values)
    variance = sum((value - avg) ** 2 for value in values) / len(values)
    stddev = math.sqrt(variance)
    return stddev if stddev > 1e-9 else 1.0


def _load_samples(path):
    with path.open() as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def get_rule_baselines():
    ai_texts = _load_samples(AI_CACHE)
    human_texts = _load_samples(HUMAN_CACHE)
    baselines = []

    for rule_fn in kevin_index:
        ai_values = [rule_fn(text) for text in ai_texts]
        human_values = [rule_fn(text) for text in human_texts]
        combined_values = ai_values + human_values
        ai_mean = _mean(ai_values)
        human_mean = _mean(human_values)
        spread = _stddev(combined_values)
        direction = RULE_DIRECTION_OVERRIDES.get(
            rule_fn.__name__, 1.0 if ai_mean >= human_mean else -1.0
        )

        baselines.append(
            {
                "midpoint": (ai_mean + human_mean) / 2,
                "spread": spread,
                "direction": direction,
                "strength": abs(ai_mean - human_mean) / spread,
            }
        )

    strengths = [baseline["strength"] for baseline in baselines]
    min_strength = min(strengths, default=0.0)
    max_strength = max(strengths, default=1.0)
    strength_range = max(max_strength - min_strength, 1e-9)

    for baseline in baselines:
        normalized_strength = (baseline["strength"] - min_strength) / strength_range
        baseline["display_weight"] = DISPLAY_WEIGHT_MIN + (
            DISPLAY_WEIGHT_MAX - DISPLAY_WEIGHT_MIN
        ) * math.sqrt(normalized_strength)

    for rule_fn, baseline in zip(kevin_index, baselines):
        if rule_fn.__name__ in DISPLAY_WEIGHT_OVERRIDES:
            baseline["display_weight"] = DISPLAY_WEIGHT_OVERRIDES[rule_fn.__name__]

    return baselines


def calc_kevin_index(text):
    rule_scores = []
    baselines = get_rule_baselines()
    weighted_index = 0.0

    for rule_fn, baseline in zip(kevin_index, baselines):
        value = rule_fn(text)
        signed_z = ((value - baseline["midpoint"]) / baseline["spread"]) * baseline[
            "direction"
        ]
        clipped_z = max(-MAX_ABS_Z_SCORE, min(MAX_ABS_Z_SCORE, signed_z))
        model_weight = baseline["strength"]
        weighted_index += clipped_z * model_weight
        rule_scores.append(
            {
                "key": rule_fn.__name__,
                "signedZ": clipped_z,
                "displayWeight": baseline["display_weight"],
                "modelWeight": model_weight,
                "direction": "AI" if baseline["direction"] > 0 else "human",
            }
        )

    return weighted_index, rule_scores


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
    index, rule_scores = calc_kevin_index(text)

    return flask.jsonify(
        {
            "index": index,
            "rules": rule_scores,
            "stats": [rule["signedZ"] for rule in rule_scores],
        }
    )


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
