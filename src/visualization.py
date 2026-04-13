import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.decomposition import PCA
import pyLDAvis
import pyLDAvis.lda_model
import os


def plot_coherence_scores(coherence_values, start=2, save_path='figures/coherence_scores.png'):
    x = range(start, start + len(coherence_values))

    plt.figure(figsize=(8, 4))
    plt.plot(x, coherence_values, marker='o')
    plt.xlabel("Jumlah Topik")
    plt.ylabel("Coherence Score (c_v)")
    plt.title("Pemilihan Jumlah Topik Optimal")
    plt.xticks(x)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Coherence plot disimpan: {save_path}")
    plt.close()


def plot_topic_distribution(model, doc_term_matrix, save_path='figures/lda_topic_distribution.png'):
    topic_dist = model.transform(doc_term_matrix)
    topic_sums = topic_dist.sum(axis=0)
    topics = [f"Topik {i+1}" for i in range(len(topic_sums))]

    plt.figure(figsize=(8, 5))
    plt.bar(topics, topic_sums)
    plt.xlabel("Topik")
    plt.ylabel("Total Skor Distribusi")
    plt.title("Distribusi Topik LDA")
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Distribusi topik disimpan: {save_path}")
    plt.close()


def plot_topic_pca(model, doc_term_matrix, save_path='figures/topic_pca.png'):
    topic_word = model.components_
    pca = PCA(n_components=2)
    coords = pca.fit_transform(topic_word)

    plt.figure(figsize=(7, 6))
    for i, (x, y) in enumerate(coords):
        plt.scatter(x, y, s=100)
        plt.annotate(f"Topik {i+1}", (x, y), textcoords="offset points", xytext=(8, 4), fontsize=10)
    plt.title("Peta Topik (PCA 2D)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"PCA topik disimpan: {save_path}")
    plt.close()


def generate_wordclouds_per_topic(model, feature_names, save_dir='figures/wordclouds_per_topic'):
    os.makedirs(save_dir, exist_ok=True)

    for topic_idx, topic_weights in enumerate(model.components_):
        top_words_idx = topic_weights.argsort()[:-50 - 1:-1]
        top_words = {feature_names[i]: topic_weights[i] for i in top_words_idx}

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_words)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"Topik {topic_idx + 1}")
        plt.tight_layout()
        path = os.path.join(save_dir, f"wordcloud_topic_{topic_idx + 1}.png")
        plt.savefig(path)
        print(f"Wordcloud disimpan: {path}")
        plt.close()


def visualize_interactive_lda(model, doc_term_matrix, vectorizer, save_html='figures/pyldavis_lda.html'):
    panel = pyLDAvis.lda_model.prepare(model, doc_term_matrix, vectorizer)
    os.makedirs(os.path.dirname(save_html), exist_ok=True)
    pyLDAvis.save_html(panel, save_html)
    print(f"pyLDAvis disimpan: {save_html}")
