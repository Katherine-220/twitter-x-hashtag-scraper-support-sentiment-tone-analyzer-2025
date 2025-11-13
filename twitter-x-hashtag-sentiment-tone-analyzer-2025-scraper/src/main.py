import argparse
import json
import logging
import logging.config
from pathlib import Path
from typing import Any, Dict, List

from .pipelines.fetch_pipeline import run_fetch_pipeline
from .pipelines.export_pipeline import export_pipeline
from .sentiment_engine import SentimentEngine
from .models.tweet_schema import Tweet

logger = logging.getLogger(__name__)

def load_logging_config(project_root: Path) -> None:
    config_path = project_root / "src" / "config" / "logging.conf"
    if config_path.is_file():
        logging.config.fileConfig(config_path, disable_existing_loggers=False)
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        )

def load_settings(config_path: Path, project_root: Path) -> Dict[str, Any]:
    if not config_path.is_file():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        settings = json.load(f)

    # Normalize paths relative to project root
    hashtags_file = settings.get("hashtags_file", "data/example_hashtags.txt")
    output_path = settings.get("output_path", "data/sample_output.json")

    settings["hashtags_file"] = str(
        (project_root / hashtags_file).resolve()
    )
    settings["output_path"] = str(
        (project_root / output_path).resolve()
    )

    return settings

def parse_args(project_root: Path) -> argparse.Namespace:
    default_config = project_root / "src" / "config" / "settings.example.json"
    parser = argparse.ArgumentParser(
        description="Twitter/X Hashtag Sentiment & Tone Analyzer 2025"
    )
    parser.add_argument(
        "--config",
        type=str,
        default=str(default_config),
        help="Path to settings JSON file (default: settings.example.json)",
    )
    return parser.parse_args()

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    load_logging_config(project_root)
    logger.info("Starting Twitter/X Hashtag Sentiment & Tone Analyzer 2025")

    args = parse_args(project_root)
    config_path = Path(args.config)

    settings = load_settings(config_path, project_root)
    sentiment_engine = SentimentEngine()

    logger.info(
        "Fetching tweets for hashtags from %s",
        settings.get("hashtags_file"),
    )
    tweets: List[Tweet] = run_fetch_pipeline(settings, sentiment_engine)
    logger.info("Fetched %d tweets after filtering", len(tweets))

    output_path = settings["output_path"]
    export_pipeline(tweets, output_path)

    logger.info("Exported %d tweets to %s", len(tweets), output_path)
    logger.info("Done.")

if __name__ == "__main__":
    main()