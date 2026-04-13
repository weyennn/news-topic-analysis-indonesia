from sklearn.decomposition import LatentDirichletAllocation
from gensim.models import CoherenceModel
from gensim import corpora

def compute_coherence_values(texts, vectorizer, doc_term_matrix, start=2, limit=10, step=1):
    id2word = corpora.Dictionary(texts)
    corpus = [id2word.doc2bow(text) for text in texts]
    feature_names = vectorizer.get_feature_names_out()

    model_list = []
    coherence_values = []

    for num_topics in range(start, limit, step):
        model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        model.fit(doc_term_matrix)
        model_list.append(model)

        topics = []
        for topic_weights in model.components_:
            top_words_idx = topic_weights.argsort()[:-11:-1]
            topics.append([feature_names[i] for i in top_words_idx])

        coherence_model = CoherenceModel(topics=topics, texts=texts, dictionary=id2word, coherence='c_v')
        coherence_values.append(coherence_model.get_coherence())

    return model_list, coherence_values

