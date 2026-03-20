

def contraction_rate(text):
    contractions = [
        "aren't", "can't", "couldn't", "didn't", "doesn't", "don't", "hadn't",
        "hasn't", "haven't", "he'd", "he'll", "he's", "i'd", "i'll", "i'm",
        "i've", "isn't", "it's", "let's", "mightn't", "mustn't", "shan't",
        "she'd", "she'll", "she's", "shouldn't", "that's", "there's", "they'd",
        "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", 
        "weren't", "what'll", "what're", "what's", "what've", "where's", "who'd", 
        "who'll", "who're", "who's", "who've", "won't", "wouldn't", "you'd", 
        "you'll", "you're", "you've"
    ]

    return len([word for word in text.split() if word.lower() in contractions]) * 100 / len(text.split())


def filler_word_rate(text):
    filler_words = [
        "very", "really", "quite", "just", "like", "actually", 
        "basically", "literally", "totally", "well", "so", 
        "right", "anyway", "obviously", "seriously"
    ]

    return len([word for word in text.split() if word.lower() in filler_words]) * 100 / len(text.split())

def discourse_marker_rate(text):
    discourse_markers = ["however", "furthermore", "moreover", "additionally", "in conclusion"]

    return len([word for word in text.split() if word.lower() in discourse_markers]) * 100 / len(text.split())


def type_token_ratio(text):
    words = text.split()
    unique_words = set(words)
    return len(unique_words) / len(words)

def avg_word_length(text):
    words = text.split()
    return sum(len(word) for word in words) / len(words)