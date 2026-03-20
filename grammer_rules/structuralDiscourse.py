import math
import re


def _paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _sentence_count(paragraph):
    return len([s for s in re.findall(r"[^.!?]+(?:[.!?]|$)", paragraph) if s.strip()])


def avg_para_length(text):
    paragraphs = _paragraphs(text)
    if not paragraphs:
        return 0

    return sum(_sentence_count(paragraph) for paragraph in paragraphs) / len(paragraphs)


def variance_para_length(text):
    paragraphs = _paragraphs(text)
    if not paragraphs:
        return 0

    avg = sum(_sentence_count(paragraph) for paragraph in paragraphs) / len(paragraphs)
    variance = sum(
        (_sentence_count(paragraph) - avg) ** 2 for paragraph in paragraphs
    ) / len(paragraphs)
    return math.sqrt(variance)
