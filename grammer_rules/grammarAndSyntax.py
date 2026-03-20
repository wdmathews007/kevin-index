import re

from grammer_rules._text_utils import percentage, sentences

try:
    import spacy
except ModuleNotFoundError:
    spacy = None


_NLP = None


def _get_nlp():
    global _NLP

    if spacy is None:
        raise RuntimeError("spaCy is required for grammarAndSyntax metrics")

    if _NLP is None:
        _NLP = spacy.load("en_core_web_sm")

    return _NLP


def passive_voice_rate(text):
    doc = _get_nlp()(text)
    text_sentences = list(doc.sents)
    if not text_sentences:
        return 0.0

    passive_count = sum(1 for token in doc if token.dep_ == "auxpass")
    return percentage(passive_count, len(text_sentences))


def question_rate(text):
    text_sentences = sentences(text)
    question_sentences = [
        s.strip() for s in re.findall(r"[^.!?]+[?]", text) if s.strip()
    ]
    return percentage(len(question_sentences), len(text_sentences))


def adverb_rate(text):
    doc = _get_nlp()(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0

    adverb_count = sum(1 for token in words if token.pos_ == "ADV")
    return percentage(adverb_count, len(words))


def noun_phrase_density(text):
    doc = _get_nlp()(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0

    noun_phrases = list(doc.noun_chunks)
    return percentage(len(noun_phrases), len(words))


def subordinate_clause_rate(text):
    doc = _get_nlp()(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0

    sconj_count = sum(1 for token in words if token.pos_ == "SCONJ")
    return percentage(sconj_count, len(words))
