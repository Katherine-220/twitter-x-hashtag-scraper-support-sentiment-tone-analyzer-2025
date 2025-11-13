import logging
from typing import List

from ..models.tweet_schema import Tweet
from ..outputs.exporter_json import write_json

logger = logging.getLogger(__name__)

def export_pipeline(tweets: List[Tweet], output_path: str) -> None:
    logger.info("Writing %d tweets to %s", len(tweets), output_path)
    write_json(tweets, output_path)