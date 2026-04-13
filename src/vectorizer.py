from sklearn.feature_extraction.text import CountVectorizer

def vectorize_count(texts, max_features=1000):
    texts_joined = [' '.join(doc) for doc in texts]
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=max_features)
    doc_term_matrix = vectorizer.fit_transform(texts_joined)
    return doc_term_matrix, vectorizer
