import math

from grammer_rules._text_utils import paragraphs, sentences


def _sentence_counts(text):
    return [len(sentences(paragraph)) for paragraph in paragraphs(text)]


def avg_para_length(text):
    counts = _sentence_counts(text)
    if not counts:
        return 0

    return sum(counts) / len(counts)


def variance_para_length(text):
    counts = _sentence_counts(text)
    if not counts:
        return 0

    avg = sum(counts) / len(counts)
    variance = sum((count - avg) ** 2 for count in counts) / len(counts)
    return math.sqrt(variance)


def std_dev_para_length(text):
    return variance_para_length(text)
