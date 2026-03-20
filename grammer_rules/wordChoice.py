from grammer_rules._text_utils import (
    count_phrase_occurrences,
    normalized_words,
    percentage,
)


def contraction_rate(text):
    contractions = {
        "aren't",
        "can't",
        "couldn't",
        "didn't",
        "doesn't",
        "don't",
        "hadn't",
        "hasn't",
        "haven't",
        "he'd",
        "he'll",
        "he's",
        "i'd",
        "i'll",
        "i'm",
        "i've",
        "isn't",
        "it's",
        "let's",
        "mightn't",
        "mustn't",
        "shan't",
        "she'd",
        "she'll",
        "she's",
        "shouldn't",
        "that's",
        "there's",
        "they'd",
        "they'll",
        "they're",
        "they've",
        "we'd",
        "we'll",
        "we're",
        "we've",
        "weren't",
        "what'll",
        "what're",
        "what's",
        "what've",
        "where's",
        "who'd",
        "who'll",
        "who're",
        "who's",
        "who've",
        "won't",
        "wouldn't",
        "you'd",
        "you'll",
        "you're",
        "you've",
    }
    words = normalized_words(text)
    return percentage(len([word for word in words if word in contractions]), len(words))


def filler_word_rate(text):
    filler_words = {
        "very",
        "really",
        "quite",
        "just",
        "like",
        "actually",
        "basically",
        "literally",
        "totally",
        "well",
        "so",
        "right",
        "anyway",
        "obviously",
        "seriously",
    }
    words = normalized_words(text)
    return percentage(len([word for word in words if word in filler_words]), len(words))


def discourse_marker_rate(text):
    discourse_markers = [
        "however",
        "furthermore",
        "moreover",
        "additionally",
        "in conclusion",
    ]
    words = normalized_words(text)
    return percentage(
        sum(count_phrase_occurrences(words, marker) for marker in discourse_markers),
        len(words),
    )


def type_token_ratio(text):
    words = normalized_words(text)
    if not words:
        return 0

    return len(set(words)) / len(words)


def avg_word_length(text):
    words = normalized_words(text)
    if not words:
        return 0

    return sum(len(word) for word in words) / len(words)

rules = [
    contraction_rate,
    filler_word_rate,
    discourse_marker_rate,
    type_token_ratio,
    avg_word_length
]
