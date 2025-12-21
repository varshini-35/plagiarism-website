import math
import string

def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text.split()

def freq(words):
    f = {}
    for w in words:
        f[w] = f.get(w, 0) + 1
    return f

def calculate_similarity(t1, t2):
    w1 = preprocess(t1)
    w2 = preprocess(t2)

    f1 = freq(w1)
    f2 = freq(w2)

    words = set(f1.keys()).union(f2.keys())

    dot = sum(f1.get(w, 0) * f2.get(w, 0) for w in words)
    mag1 = math.sqrt(sum(v*v for v in f1.values()))
    mag2 = math.sqrt(sum(v*v for v in f2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0.0

    return round((dot / (mag1 * mag2)) * 100, 2)
