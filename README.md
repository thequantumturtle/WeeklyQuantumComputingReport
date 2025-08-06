# Weekly Quantum Computing Report

This project generates a weekly Markdown script summarizing the top quantum computing news.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file with your OpenAI API key:
   ```env
   OPENAI_API_KEY=your-key-here
   ```

## Configuration

- `config.yaml` controls runtime options (summary length, output paths, etc.).
- `news_sources.yaml` lists RSS feeds or sites to scrape.

## Usage

Run the full pipeline:
```bash
scheduler/cron_job.sh
```

This will:
1. Fetch articles from the configured sources.
2. Summarize them using the OpenAI model defined in `config.yaml` (falls back to article summaries if no API key).
3. Render the final Markdown script using a Jinja2 template.

Outputs are written to `data/processed/` with date-stamped filenames.

## Notes

- Placeholder comments exist for non-RSS site scraping.
- The template includes an "Expert Take" section for custom commentary.
