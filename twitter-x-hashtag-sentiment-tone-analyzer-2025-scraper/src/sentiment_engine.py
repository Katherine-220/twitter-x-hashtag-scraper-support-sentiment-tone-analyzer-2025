import logging
from dataclasses import asdict
from typing import Literal, Tuple

from .models.tweet_schema import Tweet

SentimentLabel = Literal["Positive", "Negative", "Neutral"]
ToneLabel = Literal[
    "Enthusiastic",
    "Angry",
    "Humorous",
    "Informative",
    "Neutral",
]

logger = logging.getLogger(__name__)

class SentimentEngine:
    """
    Lightweight rule-based sentiment & tone classifier for short tweets.

    This is intentionally simple and dependency-free so that the project runs
    everywhere. For production use you could replace this with a model-backed
    implementation.
    """

    positive_words = {
        "love",
        "great",
        "amazing",
        "bull",
        "moon",
        "up",
        "pump",
        "win",
        "good",
        "awesome",
        "profit",
        "gains",
    }
    negative_words = {
        "hate",
        "bad",
        "down",
        "dump",
        "lose",
        "loss",
        "crash",
        "fear",
        "bear",
        "scam",
    }
    enthusiastic_markers = {"!", "🚀", "🔥", "moon", "pump", "insane"}
    angry_markers = {"angry", "mad", "furious", "ridiculous", "wtf"}
    humorous_markers = {"lol", "lmao", "funny", "😂", "🤣"}
    informative_markers = {"update", "news", "report", "data", "analysis", "thread"}

    def analyze_text(self, text: str) -> Tuple[SentimentLabel, ToneLabel]:
        text_lower = text.lower()
        tokens = text_lower.split()

        pos_score = sum(1 for t in tokens if t in self.positive_words)
        neg_score = sum(1 for t in tokens if t in self.negative_words)

        if pos_score > neg_score:
            sentiment: SentimentLabel = "Positive"
        elif neg_score > pos_score:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        tone: ToneLabel = "Neutral"
        if any(m in text_lower for m in self.enthusiastic_markers):
            tone = "Enthusiastic"
        if any(m in text_lower for m in self.angry_markers):
            tone = "Angry"
        if any(m in text_lower for m in self.humorous_markers):
            tone = "Humorous"
        if any(m in text_lower for m in self.informative_markers):
            tone = "Informative"

        logger.debug("Analyzed text '%s' -> sentiment=%s tone=%s", text, sentiment, tone)
        return sentiment, tone

    def label_tweet(self, tweet: Tweet) -> Tweet:
        sentiment, tone = self.analyze_text(tweet.text)
        tweet.sentiment = sentiment
        tweet.tone = tone
        logger.debug("Labeled tweet: %s", asdict(tweet))
        return tweet