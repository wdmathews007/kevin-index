def sentences_starter_pronouns (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]

    discourse_markers = ["she", "they", "he", "we", "you"]
    
    return len([s for s in sentences if s.lower().startswith(tuple(discourse_markers))]) / len(sentences) * 100

def sentences_starter_discourse (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]

    discourse_markers = ["however", "furthermore", "moreover", "additionally", "in conclusion"]
    
    return len([s for s in sentences if s.lower().startswith(tuple(discourse_markers))]) / len(sentences) * 100

def sentences_starter_the (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]
    
    return len([s for s in sentences if s.lower().startswith("and")]) / len(sentences) * 100

def sentences_starter_but (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]
    
    return len([s for s in sentences if s.lower().startswith("but")]) / len(sentences) * 100

def sentences_starter_i (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]
    
    return len([s for s in sentences if s.lower().startswith("i")]) / len(sentences) * 100

def sentences_starter_the (text):
    sentences = [s.strip() for s in re.findall(r"[^.!?]+[.!?]", text)]
    
    return len([s for s in sentences if s.lower().startswith("the")]) / len(sentences) * 100
