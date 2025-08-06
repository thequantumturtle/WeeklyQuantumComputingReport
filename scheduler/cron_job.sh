#!/bin/bash
# Run the full pipeline: scrape sources, summarize articles, and write script.
set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"

python "$DIR/scraper/scrape_sources.py"
python "$DIR/summarizer/summarize_articles.py"
python "$DIR/script_writer/write_script.py"
