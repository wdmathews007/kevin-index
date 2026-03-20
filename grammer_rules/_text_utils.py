import re

_SENTENCE_RE = re.compile(r"[^.!?]+(?:[.!?]+|$)")
_WORD_RE = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")


def sentences(text):
    return [s.strip() for s in _SENTENCE_RE.findall(text) if s.strip()]


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def normalized_words(text):
    return _WORD_RE.findall(text.lower())


def word_chunks(text, chunk_size):
    words = text.split()
    return [
        " ".join(words[index : index + chunk_size])
        for index in range(0, len(words), chunk_size)
    ]


def percentage(count, total):
    if not total:
        return 0

    return count * 100 / total


def sentence_starts_with(sentence, phrase):
    words = normalized_words(sentence)
    phrase_words = normalized_words(phrase)
    if len(words) < len(phrase_words):
        return False

    return words[: len(phrase_words)] == phrase_words


def count_phrase_occurrences(words, phrase):
    phrase_words = normalized_words(phrase)
    if not words or not phrase_words or len(words) < len(phrase_words):
        return 0

    return sum(
        1
        for index in range(len(words) - len(phrase_words) + 1)
        if words[index : index + len(phrase_words)] == phrase_words
    )
