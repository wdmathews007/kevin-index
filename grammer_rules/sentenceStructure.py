import math
import re


def _sentences(text):
    return [s.strip() for s in re.findall(r"[^.!?]+(?:[.!?]|$)", text) if s.strip()]


def _sentence_lengths(text):
    return [len(sentence.split()) for sentence in _sentences(text)]


def sentences_structure_avg(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    return sum(lengths) / len(lengths)


def sentences_structure_variance(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    avg = sum(lengths) / len(lengths)
    variance = sum((length - avg) ** 2 for length in lengths) / len(lengths)
    return math.sqrt(variance)


def sentences_structure_long(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    return len([length for length in lengths if length > 40]) / len(lengths) * 100


def sentences_structure_short(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    return len([length for length in lengths if length < 5]) / len(lengths) * 100
