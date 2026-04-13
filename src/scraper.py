import feedparser
import requests
import pandas as pd
import time

# RSS feeds per sumber dan kategori — semua telah diverifikasi aktif
FEEDS = {
    # Antara News (LKBN — kantor berita resmi)
    'Antara - Terkini':          'https://www.antaranews.com/rss/terkini.xml',
    'Antara - Politik':          'https://www.antaranews.com/rss/politik.xml',
    'Antara - Hukum':            'https://www.antaranews.com/rss/hukum.xml',
    'Antara - Ekonomi':          'https://www.antaranews.com/rss/ekonomi.xml',
    'Antara - Olahraga':         'https://www.antaranews.com/rss/olahraga.xml',
    'Antara - Humaniora':        'https://www.antaranews.com/rss/humaniora.xml',
    'Antara - Lifestyle':        'https://www.antaranews.com/rss/lifestyle.xml',
    'Antara - Hiburan':          'https://www.antaranews.com/rss/hiburan.xml',

    # CNN Indonesia
    'CNN Indonesia':             'https://www.cnnindonesia.com/rss',

    # Detik
    'Detik - News':              'https://news.detik.com/rss',
    'Detik - Finance':           'https://finance.detik.com/rss',
    'Detik - Inet':              'https://inet.detik.com/rss',
    'Detik - Health':            'https://health.detik.com/rss',
    'Detik - Hot':               'https://hot.detik.com/rss',
    'Detik - Sport':             'https://sport.detik.com/rss',
    'Detik - Travel':            'https://travel.detik.com/rss',
    'Detik - Food':              'https://food.detik.com/rss',
    'Detik - Oto':               'https://oto.detik.com/rss',
    'Detik - Wolipop':           'https://wolipop.detik.com/rss',

    # Tempo
    'Tempo - Nasional':          'https://rss.tempo.co/nasional',
    'Tempo - Bisnis':            'https://rss.tempo.co/bisnis',
    'Tempo - Hukum':             'https://rss.tempo.co/hukum',
    'Tempo - Dunia':             'https://rss.tempo.co/dunia',

    # Sindonews
    'Sindonews - Nasional':      'https://nasional.sindonews.com/rss',
    'Sindonews - Ekbis':         'https://ekbis.sindonews.com/rss',
    'Sindonews - Internasional': 'https://international.sindonews.com/rss',
    'Sindonews - Otomotif':      'https://otomotif.sindonews.com/rss',

    # CNBC Indonesia
    'CNBC - Umum':               'https://www.cnbcindonesia.com/rss',
    'CNBC - Market':             'https://www.cnbcindonesia.com/market/rss',
    'CNBC - News':               'https://www.cnbcindonesia.com/news/rss',
    'CNBC - Lifestyle':          'https://www.cnbcindonesia.com/lifestyle/rss',
    'CNBC - Entrepreneur':       'https://www.cnbcindonesia.com/entrepreneur/rss',

    # Republika
    'Republika - Umum':          'https://www.republika.co.id/rss',
    'Republika - Nasional':      'https://www.republika.co.id/rss/nasional',
    'Republika - Ekonomi':       'https://www.republika.co.id/rss/ekonomi',
    'Republika - Politik':       'https://www.republika.co.id/rss/nasional/politik',
}

_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


def _fetch_feed(source_name, feed_url, timeout=10):
    try:
        response = requests.get(feed_url, headers=_HEADERS, timeout=timeout)
        response.raise_for_status()
        feed = feedparser.parse(response.text)
        entries = []
        for entry in feed.entries:
            title = entry.get('title', '').strip()
            if not title:
                continue
            entries.append({
                'title':     title,
                'source':    source_name,
                'published': entry.get('published', entry.get('updated', '')),
                'link':      entry.get('link', ''),
            })
        print(f"  {source_name}: {len(entries)} artikel")
        return entries
    except Exception as e:
        print(f"  {source_name}: gagal ({e})")
        return []


def scrape_news(feeds=None, delay=1.0, save_path='data/data_berita_scraped.xlsx'):
    """
    Scrape judul berita dari RSS feeds media online Indonesia.

    Args:
        feeds     : dict {nama_feed: rss_url}. Default: FEEDS (20 feed, 6 sumber).
        delay     : jeda antar request dalam detik.
        save_path : path file output Excel.

    Returns:
        pd.DataFrame dengan kolom [title, source, published, link]
    """
    if feeds is None:
        feeds = FEEDS

    all_entries = []
    print(f"Mengambil berita dari {len(feeds)} feed ({len(set(feeds.keys()))} sumber)...")

    for source_name, feed_url in feeds.items():
        entries = _fetch_feed(source_name, feed_url)
        all_entries.extend(entries)
        time.sleep(delay)

    df = pd.DataFrame(all_entries)
    if df.empty:
        print("Tidak ada data yang berhasil diambil.")
        return df

    before = len(df)
    df = df.drop_duplicates(subset='title').reset_index(drop=True)
    removed = before - len(df)
    if removed:
        print(f"Duplikat dihapus: {removed} entri")

    # Normalisasi nama sumber (hapus suffix kategori untuk kolom 'source')
    df['source'] = df['source'].str.split(' - ').str[0]

    n_sources = df['source'].nunique()
    print(f"Total: {len(df)} judul berita unik dari {n_sources} sumber")
    print(df['source'].value_counts().to_string())

    df.to_excel(save_path, index=False)
    print(f"\nData disimpan: {save_path}")

    return df
