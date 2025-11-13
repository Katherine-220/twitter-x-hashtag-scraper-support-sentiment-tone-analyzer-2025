from pathlib import Path

from src.pipelines.fetch_pipeline import run_fetch_pipeline
from src.sentiment_engine import SentimentEngine

def test_fetch_pipeline_smoke():
    project_root = Path(__file__).resolve().parents[1]
    hashtags_file = project_root / "data" / "example_hashtags.txt"

    settings = {
        "hashtags_file": str(hashtags_file),
        "output_path": str(project_root / "data" / "test_output.json"),
        "max_items": 20,
        "language": "en",
        "min_like_count": 0,
        "min_retweet_count": 0,
        "min_reply_count": 0,
        "verified_only": False,
        "blue_verified_only": False,
        "since": None,
        "until": None,
    }

    engine = SentimentEngine()
    tweets = run_fetch_pipeline(settings, engine)

    assert tweets, "Expected at least one tweet from pipeline"
    assert len(tweets) <= settings["max_items"]
    for t in tweets:
        assert t.sentiment in {"Positive", "Negative", "Neutral"}
        assert t.tone is not None