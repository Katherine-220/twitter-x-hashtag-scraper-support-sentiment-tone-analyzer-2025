import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..filters import apply_filters
from ..hashtag_client import HashtagClient
from ..models.tweet_schema import Tweet
from ..sentiment_engine import SentimentEngine

logger = logging.getLogger(__name__)

def _parse_optional_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        # Expect ISO 8601 or "YYYY-MM-DD HH:MM" in UTC
        return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
    except ValueError:
        logger.warning("Invalid datetime format '%s'; ignoring", value)
        return None

def run_fetch_pipeline(
    settings: Dict[str, Any],
    sentiment_engine: SentimentEngine,
) -> List[Tweet]:
    hashtags_file = settings["hashtags_file"]
    max_items = int(settings.get("max_items", 100))

    with open(hashtags_file, "r", encoding="utf-8") as f:
        hashtags = [line.strip() for line in f if line.strip()]

    since = _parse_optional_datetime(settings.get("since"))
    until = _parse_optional_datetime(settings.get("until"))

    client = HashtagClient()
    tweets = client.fetch_hashtag_tweets(
        hashtags=hashtags,
        max_items=max_items,
        language=settings.get("language", "en"),
        since=since,
        until=until,
        verified_only=bool(settings.get("verified_only", False)),
        blue_only=bool(settings.get("blue_verified_only", False)),
    )

    labeled: List[Tweet] = [sentiment_engine.label_tweet(t) for t in tweets]
    filtered = apply_filters(labeled, settings)
    return filtered