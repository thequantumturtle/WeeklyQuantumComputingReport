"""
You are a dev agent helping me build a software tool called Weekly Quantum Computing Report.

Its job is to generate a weekly YouTube script summarizing the **top 10 most relevant and distinct quantum computing news stories**. I will read this script like a state-of-the-field address every Sunday night.

The workflow is:
1. Scrape quantum news from RSS feeds (and possibly websites)
2. Summarize the 10 most relevant stories using OpenAI's GPT-4o
3. Generate a paragraph-style Markdown script with a placeholder "Expert Take" section, using a Jinja2 template
4. Save all outputs with date-stamped filenames

The folder structure already exists:

weeklyquantumcomputingreport/
├── config.yaml
├── news_sources.yaml
├── scraper/scrape_sources.py       # TODO: implement
├── summarizer/summarize_articles.py # TODO: implement
├── script_writer/write_script.py    # TODO: implement
├── templates/weekly_script_template.md
├── scheduler/cron_job.sh            # TODO: implement

---

## Build all missing scripts:

### 1. `scraper/scrape_sources.py`
- Load `news_sources.yaml`
- Use `feedparser` to fetch RSS feed data
- Extract: `title`, `url`, `summary`, `content`
- Deduplicate by title/URL
- Keep only 10 most relevant (e.g., latest 10 by publication date)
- Save results to `data/raw/articles.json`

### 2. `summarizer/summarize_articles.py`
- Load `data/raw/articles.json`
- Summarize each article into a **paragraph** (not bullet points) using GPT-4o
- Use `.env` to load `OPENAI_API_KEY`
- Save results to `data/processed/summaries_<date>.json`

### 3. `script_writer/write_script.py`
- Load `summaries_<date>.json`
- Render the Markdown template `templates/weekly_script_template.md` with Jinja2
- Add an "Expert Take" placeholder section
- Save the final script to `data/processed/script_<date>.md`

### 4. `scheduler/cron_job.sh`
- Bash script that runs all 3 steps in order
- Outputs the final file in `data/processed/`

---

Constraints:
- Use top 10 **distinct** stories each week
- Paragraph-style summaries
- Final Markdown script must be ready to read aloud like a newscaster
- Log progress for each step
- Date-stamp filenames (e.g., `script_2025-08-11.md`)

Implement all 4 files now.
"""
