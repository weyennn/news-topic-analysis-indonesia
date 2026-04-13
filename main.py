import argparse

from src.preprocessing import load_data, preprocess_texts
from src.n_gram import build_ngrams
from src.vectorizer import vectorize_count
from src.lda_model import compute_coherence_values
from src.visualization import (
    plot_coherence_scores,
    plot_topic_distribution,
    plot_topic_pca,
    visualize_interactive_lda,
    generate_wordclouds_per_topic
)


def main():
    parser = argparse.ArgumentParser(description='Analisis topik pemberitaan nasional Indonesia')
    parser.add_argument(
        '--scrape',
        action='store_true',
        help='Ambil data terbaru dari RSS feeds sebelum analisis'
    )
    parser.add_argument(
        '--data',
        default='data/data_berita_cleaned.xlsx',
        help='Path ke file data (default: data/data_berita_cleaned.xlsx)'
    )
    args = parser.parse_args()

    if args.scrape:
        from src.scraper import scrape_news
        data_path = 'data/data_berita_scraped.xlsx'
        df = scrape_news(save_path=data_path)
        if df.empty:
            print("Scraping gagal. Pastikan koneksi internet tersedia.")
            return
    else:
        data_path = args.data
        print("Memuat data...")
        df = load_data(data_path)

    texts = df['title'].astype(str).tolist()
    print(f"Total data: {len(texts)} judul berita")

    print("Pra-pemrosesan teks...")
    cleaned_texts = preprocess_texts(texts, custom_stopword_path='data/stopwords.txt')

    print("Membangun n-gram...")
    ngrammed_texts = build_ngrams(cleaned_texts)

    print("Vektorisasi dokumen...")
    doc_term_matrix, vectorizer = vectorize_count(ngrammed_texts)

    start = 4
    print(f"Menghitung coherence score untuk {start}–12 topik...")
    model_list, coherence_values = compute_coherence_values(
        texts=ngrammed_texts,
        vectorizer=vectorizer,
        doc_term_matrix=doc_term_matrix,
        start=start, limit=13, step=1
    )
    if not model_list:
        print("Tidak ada model berhasil dibuat.")
        return

    plot_coherence_scores(coherence_values, start=start)

    best_idx = coherence_values.index(max(coherence_values))
    best_model = model_list[best_idx]
    best_topic_count = start + best_idx
    print(f"Topik terbaik: {best_topic_count}, coherence = {coherence_values[best_idx]:.4f}")

    print("Membuat visualisasi...")
    generate_wordclouds_per_topic(
        model=best_model,
        feature_names=vectorizer.get_feature_names_out()
    )
    plot_topic_distribution(best_model, doc_term_matrix)
    plot_topic_pca(best_model, doc_term_matrix)
    visualize_interactive_lda(best_model, doc_term_matrix, vectorizer)
    print("Selesai.")


if __name__ == '__main__':
    main()
