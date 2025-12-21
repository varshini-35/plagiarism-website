import requests
from bs4 import BeautifulSoup
import re

SERPAPI_KEY = "f0e2cd3b9c4104652ebae1565b5a78c01ba68426fb806d1026f96566dbcffbac"

STOPWORDS = set("""
the is and of to in for on with at by from as that this it are was were be been
""".split())


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return [w for w in text.split() if w not in STOPWORDS]


def get_ngrams(words, n=3):
    return set(" ".join(words[i:i+n]) for i in range(len(words)-n+1))


def scrape_text(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator=" ")
    except:
        return ""


def check_plagiarism_online(text):

    if len(text.strip()) < 30:
        return 0, "Text too short to check"

    words = clean_text(text)
    input_ngrams = get_ngrams(words)

    if not input_ngrams:
        return 0, "No valid content"

    params = {
        "engine": "google",
        "q": " ".join(words[:8]),
        "api_key": SERPAPI_KEY,
        "num": 5
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    best_percent = 0
    best_source = "No source found"

    for result in results.get("organic_results", []):
        url = result.get("link")
        if not url:
            continue

        page_text = scrape_text(url)
        page_words = clean_text(page_text)
        page_ngrams = get_ngrams(page_words)

        if not page_ngrams:
            continue

        similarity = (len(input_ngrams & page_ngrams) / len(input_ngrams)) * 100

        if similarity > best_percent:
            best_percent = similarity
            best_source = url

    return round(best_percent, 2), best_source
