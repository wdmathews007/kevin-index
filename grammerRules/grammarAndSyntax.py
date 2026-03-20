import re
import spacy

nlp = spacy.load("en_core_web_sm")

def passive_voice_rate(text):
    doc = nlp(text)
    sentences = list(doc.sents)
    if not sentences:
        return 0.0
        
    passive_count = sum(1 for token in doc if token.dep_ == "auxpass")
    return (passive_count / len(sentences)) * 100

def question_rate(text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]
    question_sentences = [s.strip() for s in re.findall(r"[^.!?]+[?]", text)]

    return len(question_sentences) / len(sentences) * 100

def adverb_rate(text):
    doc = nlp(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0
        
    adverb_count = sum(1 for token in words if token.pos_ == "ADV")
    return (adverb_count / len(words)) * 100
    

def noun_phrase_density(text):
    doc = nlp(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0
        
    noun_phrases = list(doc.noun_chunks)
    return (len(noun_phrases) / len(words)) * 100

def subordinate_clause_rate(text):
    doc = nlp(text)
    words = [token for token in doc if not token.is_punct and not token.is_space]
    if not words:
        return 0.0
        
    sconj_count = sum(1 for token in words if token.pos_ == "SCONJ")
    return (sconj_count / len(words)) * 100
