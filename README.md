# Analisis Tren Topik Pemberitaan Nasional Berbasis Data Teks

## Latar Belakang Masalah
Pemberitaan media daring menghasilkan data teks dalam jumlah besar
yang sulit dianalisis secara manual. Tanpa analisis terstruktur,
pola isu dominan dan perubahan topik dalam periode tertentu
sering kali tidak teridentifikasi secara sistematis.

Proyek ini bertujuan untuk menganalisis tren topik pada judul berita
berbahasa Indonesia menggunakan pendekatan *topic modeling*,
guna memperoleh insight mengenai isu-isu utama yang muncul
dalam periode waktu tertentu.

---

## Data
- **Sumber:** Judul berita dari kanal **detikNews**
- **Rentang waktu:** 16 Desember 2021 – 24 Maret 2022
- **Jumlah data:** 1.980 judul berita
- **Format:** Excel (`.xlsx`)
- **Variabel utama:** `title` (judul berita)

Data ini merepresentasikan kecenderungan isu nasional
yang muncul dalam pemberitaan media daring.

---

## Pendekatan Analisis

### 1. Pra-pemrosesan Teks
- Case folding
- Penghapusan angka dan tanda baca
- Stopword removal (Sastrawi + daftar khusus)
- Tokenisasi dan pembentukan n-gram (bigram & trigram)

Tahap ini bertujuan untuk meningkatkan kualitas representasi teks
sebelum dilakukan pemodelan topik.

### 2. Pembentukan Representasi Dokumen
- Vectorisasi teks menggunakan **CountVectorizer**
- Pembentukan dokumen–term matrix sebagai input model

### 3. Topic Modeling
- Penerapan **Latent Dirichlet Allocation (LDA)**
  untuk mengidentifikasi kelompok topik laten
- Pemilihan jumlah topik optimal berdasarkan
  **coherence score (c_v)**

### 4. Visualisasi dan Interpretasi
- Wordcloud untuk interpretasi kata kunci tiap topik
- Perceptual map (PCA 2D) untuk melihat kedekatan antar topik
- Visualisasi interaktif menggunakan **pyLDAvis**

---

## Hasil Analisis
- Model berhasil mengelompokkan judul berita ke dalam
  beberapa topik utama yang merepresentasikan isu nasional.
- Setiap topik ditandai oleh kumpulan kata kunci dominan
  yang memudahkan interpretasi konteks pemberitaan.
- Visualisasi PCA menunjukkan pemisahan topik yang cukup jelas,
  menandakan konsistensi struktur topik dalam data.

---

## Insight Utama
- Pemberitaan nasional menunjukkan konsentrasi pada
  beberapa isu utama yang muncul secara konsisten
  dalam periode pengamatan.
- Analisis topik membantu mereduksi kompleksitas data teks
  menjadi ringkasan isu yang mudah dipahami.
- Pendekatan ini dapat digunakan sebagai dasar
  pemantauan tren menunjukkan fokus media
  terhadap isu tertentu.

---

## Potensi Pemanfaatan
- **Analisis Media:**  
  Mengidentifikasi isu dominan dan pola framing media daring.
- **Pemantauan Isu Publik:**  
  Mendukung analisis tren kebijakan, politik, atau sosial
  berbasis data teks.
- **Data-driven Reporting:**  
  Sebagai dasar pembuatan laporan ringkasan isu secara otomatis.

---

## Visualisasi
- Wordcloud per topik tersedia pada:
  `figures/wordclouds_per_topic/`
- Distribusi topik:
  `figures/lda_topic_distribution.png`
- Visualisasi interaktif:
  `figures/pyldavis_lda.html`

---

## Tools & Library
- Python, Pandas
- Scikit-learn
- Gensim
- Sastrawi
- WordCloud
- Matplotlib
- pyLDAvis

---

## Struktur Proyek
```
lda-berita/
├── data/
│   ├── data_berita_cleaned.xlsx
│   └── stopwords.txt
├── figures/
│   ├── lda_topic_distribution.png
│   ├── pyldavis_lda.html
│   └── wordclouds_per_topic/
├── src/
│   ├── preprocessing.py
│   ├── ngram.py
│   ├── vectorizer.py
│   ├── lda_model.py
│   └── visualization.py
├── main.py
└── requirements.txt
```

## Penulis

Yayang Matira | Mahasiswa Magister Ilmu Komputer | Universitas Gadjah Mada
