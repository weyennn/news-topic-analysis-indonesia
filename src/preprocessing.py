import pandas as pd
import re
import string
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def load_data(filepath):
    return pd.read_excel(filepath)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'&[a-z]+;', ' ', text)       # hapus HTML entities (&amp;, &nbsp;, dll)
    text = re.sub(r'https?://\S+', '', text)     # hapus URL
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_texts(texts, custom_stopword_path=None):
    factory = StopWordRemoverFactory()
    stopwords = set(factory.get_stop_words())

    if custom_stopword_path:
        with open(custom_stopword_path, 'r', encoding='utf-8') as f:
            custom_words = set([line.strip() for line in f if line.strip()])
            stopwords.update(custom_words)

    cleaned_texts = []
    for text in texts:
        text = clean_text(str(text))
        tokens = text.split()
        tokens = [t for t in tokens if t not in stopwords]
        cleaned_texts.append(tokens)

    return cleaned_texts
