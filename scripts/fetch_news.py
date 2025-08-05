import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

RSS_URL = (
    "https://news.google.com/rss/search?q=quantum&hl=en-US&gl=US&ceid=US:en"
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "articles.json")


def fetch_articles(limit=3):
    """Fetch quantum-related news articles from the last seven days."""
    resp = urllib.request.urlopen(RSS_URL)
    data = resp.read()
    root = ET.fromstring(data)

    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    articles = []

    for item in root.findall('.//item'):
        link_elem = item.find('link')
        pub_date_elem = item.find('pubDate')
        if link_elem is None or pub_date_elem is None:
            continue
        pub_date = parsedate_to_datetime(pub_date_elem.text)
        if pub_date >= cutoff:
            articles.append({
                'url': link_elem.text,
                'title': item.findtext('title', ''),
                'published': pub_date.isoformat(),
            })
        if len(articles) >= limit:
            break

    return articles


def save_articles(articles, path=OUTPUT_FILE):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)


def main():
    articles = fetch_articles()
    save_articles(articles)


if __name__ == "__main__":
    main()
