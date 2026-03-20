import math

from grammer_rules._text_utils import normalized_words, percentage, sentences


def _sentence_lengths(text):
    return [len(normalized_words(sentence)) for sentence in sentences(text)]


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


def sentences_structure_std_dev(text):
    return sentences_structure_variance(text)


def sentences_structure_long(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    return percentage(len([length for length in lengths if length > 40]), len(lengths))


def sentences_structure_short(text):
    lengths = _sentence_lengths(text)
    if not lengths:
        return 0

    return percentage(len([length for length in lengths if length < 5]), len(lengths))

rule = [
    sentences_structure_avg,
    sentences_structure_variance,
    sentences_structure_std_dev,
    sentences_structure_long,
    sentences_structure_short
]
