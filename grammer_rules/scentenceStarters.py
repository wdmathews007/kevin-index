from grammer_rules._text_utils import percentage, sentence_starts_with, sentences


def _sentence_starter_rate(text, starters):
    text_sentences = sentences(text)
    if not text_sentences:
        return 0

    count = sum(
        1
        for sentence in text_sentences
        if any(sentence_starts_with(sentence, starter) for starter in starters)
    )
    return percentage(count, len(text_sentences))


def sentences_starter_pronouns(text):
    return _sentence_starter_rate(text, ["she", "they", "he", "we", "you"])


def sentences_starter_discourse(text):
    return _sentence_starter_rate(
        text,
        ["however", "furthermore", "moreover", "additionally", "in conclusion"],
    )


def sentences_starter_and(text):
    return _sentence_starter_rate(text, ["and"])


def sentences_starter_but(text):
    return _sentence_starter_rate(text, ["but"])


def sentences_starter_i(text):
    return _sentence_starter_rate(text, ["i"])


def sentences_starter_the(text):
    return _sentence_starter_rate(text, ["the"])

rules = [
    sentences_starter_pronouns,
    sentences_starter_discourse,
    sentences_starter_and,
    sentences_starter_but,
    sentences_starter_i,
    sentences_starter_the
]
