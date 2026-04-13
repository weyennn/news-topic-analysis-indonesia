# Analisis Topik Pemberitaan Nasional Indonesia

> Topic modeling berbasis **LDA** pada ~2.000 judul berita dari 7 media online Indonesia.
> Mengidentifikasi isu-isu dominan secara otomatis dari data teks terbaru melalui RSS feed.

---

## Latar Belakang

Media daring Indonesia memproduksi ribuan judul berita setiap harinya. Tanpa pendekatan terstruktur,
sulit untuk menangkap gambaran besar — isu apa yang sedang dominan, dan bagaimana pola topik terbentuk
lintas sumber media.

Proyek ini membangun pipeline end-to-end: mulai dari **scraping otomatis** RSS feed, **preprocessing**
teks berbahasa Indonesia, hingga **topic modeling** dengan LDA — lengkap dengan visualisasi interaktif.

---

## Hasil

Model menemukan **7 topik** optimal (coherence score c_v = **0.5092**) dari 2.079 judul berita:

| Topik | Kata Kunci Dominan | Interpretasi |
|---|---|---|
| 1 | makanan, tiket, diskon, usia, industri | Gaya Hidup & Konsumen |
| 2 | china, bank, jepang, bi, pasar, ai | Ekonomi Global & Teknologi |
| 3 | iran, listrik, mbg, militer, arab | Geopolitik & Energi |
| 4 | harga, arsenal, man_city, belanja, selat_hormuz | Olahraga & Pasar |
| 5 | prabowo, trump, putin, perang, israel, kpk, mk | Politik & Konflik Internasional |
| 6 | bisnis, beras, dana, uang, lebaran | Ekonomi Domestik |
| 7 | emas, investasi, ihsg, makan, murah | Pasar Modal & Investasi |

Jumlah topik dipilih secara objektif berdasarkan **coherence score tertinggi** pada rentang 4–12 topik.

---

## Data

Dikumpulkan otomatis via **36 RSS feed** dari 7 media nasional:

| Sumber | Kategori |
|---|---|
| Detik | News, Finance, Inet, Health, Hot, Sport, Travel, Food, Oto, Wolipop |
| CNBC Indonesia | Umum, Market, News, Lifestyle, Entrepreneur |
| Antara News | Terkini, Politik, Hukum, Ekonomi, Olahraga, Humaniora, Lifestyle, Hiburan |
| Tempo | Nasional, Bisnis, Hukum, Dunia |
| Sindonews | Nasional, Ekbis, Internasional, Otomotif |
| CNN Indonesia | Semua Kategori |
| Republika | Umum, Nasional, Ekonomi, Politik |

**~2.000 judul unik** per fetch · kolom: `title`, `source`, `published`, `link`

---

## Pipeline

```
RSS Feeds → Scraping → Preprocessing → N-gram → Vectorization → LDA → Visualization
```

### 1. Scraping (`src/scraper.py`)
- Fetch via `requests` + `feedparser` dengan proper User-Agent
- Deduplication otomatis berdasarkan judul
- 36 feed dari 7 sumber, ~2.000 artikel per eksekusi

### 2. Preprocessing (`src/preprocessing.py`)
- Case folding, hapus angka, tanda baca, HTML entities, URL
- Stopword removal: **Sastrawi** + custom list (~450 kata) mencakup kata fungsi, nama wilayah, nama media, kata framing artikel

### 3. N-gram (`src/n_gram.py`)
- Bigram & trigram via **Gensim Phrases**
- Menangkap frasa seperti `selat_hormuz`, `man_city`, `blokade_selat_hormuz`

### 4. Vektorisasi (`src/vectorizer.py`)
- **CountVectorizer** — `max_features=1000`, `min_df=2`, `max_df=0.95`

### 5. Topic Modeling (`src/lda_model.py`)
- **LDA (sklearn)** dengan `random_state=42`
- Evaluasi coherence score (c_v) pada rentang 4–12 topik
- Model terbaik dipilih otomatis berdasarkan skor tertinggi

### 6. Visualisasi (`src/visualization.py`)
- Coherence score plot (justifikasi pemilihan jumlah topik)
- Wordcloud per topik
- Distribusi topik (bar chart)
- Peta topik 2D (PCA)
- Visualisasi interaktif pyLDAvis

---

## Visualisasi

| File | Keterangan |
|---|---|
| `figures/coherence_scores.png` | Kurva coherence score vs jumlah topik (4–12) |
| `figures/lda_topic_distribution.png` | Distribusi skor tiap topik |
| `figures/topic_pca.png` | Peta kedekatan antar topik (PCA 2D) |
| `figures/wordclouds_per_topic/` | Wordcloud kata kunci per topik |
| `figures/pyldavis_lda.html` | Visualisasi interaktif — buka di browser |

---

## Cara Menjalankan

**1. Clone & setup**
```bash
git clone https://github.com/<username>/news-topic-analysis-indonesia.git
cd news-topic-analysis-indonesia
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

**2. Scrape data terbaru lalu analisis**
```bash
python main.py --scrape
```

**3. Atau gunakan data yang sudah ada**
```bash
python main.py --data data/data_berita_cleaned.xlsx
```

Output tersimpan di `figures/`.

---

## Struktur Proyek

```
news-topic-analysis-indonesia/
├── data/
│   ├── data_berita_cleaned.xlsx   # Dataset awal (detikNews, Des 2021–Mar 2022)
│   └── stopwords.txt              # Custom stopword Bahasa Indonesia (~450 kata)
├── figures/
│   ├── coherence_scores.png
│   ├── lda_topic_distribution.png
│   ├── topic_pca.png
│   ├── pyldavis_lda.html
│   └── wordclouds_per_topic/
├── src/
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── n_gram.py
│   ├── vectorizer.py
│   ├── lda_model.py
│   └── visualization.py
├── main.py
└── requirements.txt
```

> `data/data_berita_scraped.xlsx` di-generate saat `--scrape` dan tidak di-commit ke repo.

---

## Stack

| Kategori | Library |
|---|---|
| Scraping | `requests`, `feedparser` |
| NLP | `Sastrawi`, `Gensim` |
| Modeling | `scikit-learn` (LDA, PCA, CountVectorizer) |
| Visualisasi | `matplotlib`, `wordcloud`, `pyLDAvis` |
| Data | `pandas`, `openpyxl` |

---

## Penulis

**Yayang Matira** · Mahasiswa Magister Ilmu Komputer · Universitas Gadjah Mada
