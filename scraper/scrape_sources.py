#!/usr/bin/env python3
"""Fetch quantum computing news articles from configured sources."""
from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import feedparser
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"
SOURCES_PATH = ROOT / "news_sources.yaml"
OUTPUT_PATH = ROOT / "data/raw/articles.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_sources() -> List[Dict[str, str]]:
    with open(SOURCES_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", [])


def fetch_rss(url: str) -> feedparser.FeedParserDict:
    return feedparser.parse(url)


def main() -> None:
    config = load_config()
    logging.basicConfig(level=getattr(logging, config.get("logging_level", "INFO")))

    sources = load_sources()
    articles: List[Dict[str, Any]] = []
    seen = set()

    for source in sources:
        src_type = source.get("type")
        url = source.get("url")
        name = source.get("name")
        logging.info("Fetching %s", name)

        if src_type == "rss":
            feed = fetch_rss(url)
            for entry in feed.entries:
                title = entry.get("title", "").strip()
                link = entry.get("link")
                if not title or not link:
                    continue
                key = (title.lower(), link)
                if config.get("deduplicate", True) and key in seen:
                    continue
                seen.add(key)

                published = None
                if entry.get("published_parsed"):
                    published = datetime.fromtimestamp(
                        time.mktime(entry.published_parsed)
                    ).isoformat()

                summary = entry.get("summary", "")
                content = (
                    entry.get("content", [{}])[0].get("value")
                    if entry.get("content")
                    else summary
                )
                articles.append(
                    {
                        "source": name,
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "content": content,
                        "published": published,
                    }
                )
        else:
            logging.info(
                "Site scraping not implemented for %s. TODO: add HTML parsing.", url
            )

    # sort by published date if available
    articles.sort(
        key=lambda a: a.get("published") or "",
        reverse=True,
    )
    max_articles = config.get("max_articles", 10)
    articles = articles[:max_articles]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)
    logging.info("Saved %s", OUTPUT_PATH)


if __name__ == "__main__":
    main()
