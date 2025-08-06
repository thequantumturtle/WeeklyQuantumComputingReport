#!/usr/bin/env python3
"""Summarize scraped articles using OpenAI's GPT models."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml
from dotenv import load_dotenv

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - openai might not be installed yet
    OpenAI = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"
RAW_PATH = ROOT / "data/raw/articles.json"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_articles() -> List[Dict[str, Any]]:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw articles file not found: {RAW_PATH}")
    with open(RAW_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize_text(client: OpenAI, model: str, text: str, length: int, timeout: int) -> str:
    prompt = (
        f"Summarize the following article in {length} sentences as a coherent paragraph:\n\n{text}"
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        timeout=timeout,
    )
    return resp.choices[0].message.content.strip()


def main() -> None:
    load_dotenv()
    config = load_config()
    logging.basicConfig(level=getattr(logging, config.get("logging_level", "INFO")))

    articles = load_articles()
    summaries: List[Dict[str, str]] = []

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key and OpenAI else None
    if client is None:
        logging.warning("OPENAI_API_KEY not set or openai package missing; using article summaries without LLM.")

    for article in articles:
        text = article.get("content") or article.get("summary") or ""
        try:
            if client:
                summary = summarize_text(
                    client,
                    config.get("llm_model", "gpt-4o"),
                    text,
                    config.get("summary_length", 3),
                    config.get("openai_timeout", 30),
                )
            else:
                summary = text
        except Exception as exc:  # pragma: no cover
            logging.error("Failed to summarize article '%s': %s", article.get("title"), exc)
            summary = text

        summaries.append(
            {
                "title": article.get("title"),
                "url": article.get("url"),
                "summary": summary.strip(),
            }
        )

    out_dir = ROOT / config.get("output_dir", "data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    out_file = out_dir / f"summaries_{date_str}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2)
    logging.info("Saved %s", out_file)


if __name__ == "__main__":
    main()
