#!/usr/bin/env python3
"""Render weekly script from summarized articles."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.yaml"


def load_config() -> Dict[str, Any]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_latest_summaries(out_dir: Path) -> List[Dict[str, str]]:
    files = sorted(out_dir.glob("summaries_*.json"))
    if not files:
        raise FileNotFoundError(f"No summaries found in {out_dir}")
    latest = files[-1]
    with open(latest, "r", encoding="utf-8") as f:
        return json.load(f)


def render_template(template_path: Path, summaries: List[Dict[str, str]]) -> str:
    env = Environment(loader=FileSystemLoader(template_path.parent))
    template = env.get_template(template_path.name)
    now = datetime.now()
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    week_end = (now + timedelta(days=6 - now.weekday())).strftime("%Y-%m-%d")
    return template.render(
        week_start=week_start, week_end=week_end, summaries=summaries
    )


def main() -> None:
    config = load_config()
    logging.basicConfig(level=getattr(logging, config.get("logging_level", "INFO")))

    out_dir = ROOT / config.get("output_dir", "data/processed")
    summaries = load_latest_summaries(out_dir)
    script_md = render_template(Path(config["template_file"]), summaries)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = out_dir / f"script_{date_str}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(script_md)
    logging.info("Saved %s", output_file)


if __name__ == "__main__":
    main()
