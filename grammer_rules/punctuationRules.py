from grammer_rules._text_utils import word_chunks


def _average_punctuation_per_chunk(text, markers):
    chunks = word_chunks(text, 100)
    if not chunks:
        return 0

    return sum(
        sum(chunk.count(marker) for marker in markers) for chunk in chunks
    ) / len(chunks)


def semicolonFreq(text):
    return _average_punctuation_per_chunk(text, [";"])


def commaFreq(text):
    return _average_punctuation_per_chunk(text, [","])


def emmdashFreq(text):
    return _average_punctuation_per_chunk(text, ["—"])


def ellipsisFreq(text):
    return _average_punctuation_per_chunk(text, ["..."])


def exclamationFreq(text):
    return _average_punctuation_per_chunk(text, ["!"])


def colonFreq(text):
    return _average_punctuation_per_chunk(text, [":"])


def parenthesesFreq(text):
    return _average_punctuation_per_chunk(text, ["(", ")"])
