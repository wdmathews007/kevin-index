import os
import sys
import json
import zipfile
import csv
import io

import datasets
import tabulate
from huggingface_hub import hf_hub_download

HUMAN_CACHE = "text_data/human_samples.json"
AI_CACHE = "text_data/ai_samples.json"
SAMPLE_COUNT = 1000

from grammer_rules import (
    punctuationRules,
    scentenceStarters,
    sentenceStructure,
    structuralDiscourse,
    wordChoice,
)


all_measures = [
    punctuationRules.rules,
    scentenceStarters.rules,
    sentenceStructure.rule,
    structuralDiscourse.rule,
    wordChoice.rules,
]

all_measures = [item for sublist in all_measures for item in sublist]


def load_idmgsp_ai():
    """Load AI-generated papers (label=1) from tum-nlp/IDMGSP."""
    zip_path = hf_hub_download(
        repo_id="tum-nlp/IDMGSP", filename="train+gpt3.zip", repo_type="dataset"
    )
    texts = []
    with zipfile.ZipFile(zip_path) as z:
        with z.open("../../../../../../train.csv") as f:
            reader = csv.DictReader(io.TextIOWrapper(f))
            for row in reader:
                if row.get("label") == "1":
                    text = " ".join(
                        filter(None, [row.get("abstract"), row.get("introduction"), row.get("conclusion")])
                    ).strip()
                    if text:
                        texts.append(text)
                if len(texts) >= SAMPLE_COUNT:
                    break
    return texts


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Please provide a directory path to ai generated pdf files and then human written papers."
        )
        quit()

    print("Processing AI generated files...")

    if os.path.exists(AI_CACHE):
        print(f"  Loading from cache: {AI_CACHE}")
        with open(AI_CACHE, "r") as f:
            ai_texts = json.load(f)
    else:
        print("  Downloading AI papers from tum-nlp/IDMGSP (will cache to disk)...")
        ai_texts = load_idmgsp_ai()
        with open(AI_CACHE, "w") as f:
            json.dump(ai_texts, f)
        print(f"  Saved {len(ai_texts)} samples to {AI_CACHE}")

    ai_stats = []
    for text in ai_texts:
        ai_stats.append([measure(text) for measure in all_measures])

    ai_avg_stats = [
        sum(s) / len(ai_stats) for s in zip(*ai_stats)
    ]

    print("Processing human generated files...")

    if os.path.exists(HUMAN_CACHE):
        print(f"  Loading from cache: {HUMAN_CACHE}")
        with open(HUMAN_CACHE, "r") as f:
            human_texts = json.load(f)
    else:
        print("  Downloading from allenai/peS2o (will cache to disk)...")
        human_dataset = datasets.load_dataset(
            "json",
            data_files="hf://datasets/allenai/peS2o/data/v2/train-00000-of-00020.json.gz",
            split="train",
            streaming=True,
        )
        human_texts = []
        for row in human_dataset:
            created = row.get("created")
            if created:
                try:
                    if int(str(created)[:4]) < 2020:
                        human_texts.append(row["text"])
                except (ValueError, TypeError):
                    pass
            if len(human_texts) >= SAMPLE_COUNT:
                break
        with open(HUMAN_CACHE, "w") as f:
            json.dump(human_texts, f)
        print(f"  Saved {len(human_texts)} samples to {HUMAN_CACHE}")

    human_stats = []
    for text in human_texts:
        human_stats.append([measure(text) for measure in all_measures])

    human_avg_stats = [
        sum(s) / len(human_stats) for s in zip(*human_stats)
    ]

    data = [["measure name", "AI papers", "human papers", "diff", "AI or human"]]

    for i in range(len(all_measures)):
        data.append(
            [
                all_measures[i].__name__,
                ai_avg_stats[i],
                human_avg_stats[i],
                abs(ai_avg_stats[i] - human_avg_stats[i]),
                "AI" if ai_avg_stats[i] > human_avg_stats[i] else "human",
            ]
        )

    print(tabulate.tabulate(data, headers="firstrow", tablefmt="fancy_grid"))

    md_path = "results.md"
    with open(md_path, "w") as f:
        f.write("# Comparator Results\n\n")
        f.write(f"- AI samples: {len(ai_texts)} (tum-nlp/IDMGSP label=1, GPT-3 generated, abstract+intro+conclusion)\n")
        f.write(f"- Human samples: {len(human_texts)} (allenai/peS2o v2, pre-2020)\n\n")
        f.write(tabulate.tabulate(data, headers="firstrow", tablefmt="github"))
        f.write("\n")
    print(f"\nResults saved to {md_path}")
