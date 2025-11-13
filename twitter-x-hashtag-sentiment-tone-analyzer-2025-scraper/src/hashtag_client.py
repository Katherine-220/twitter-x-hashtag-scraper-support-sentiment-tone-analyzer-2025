import itertools
import logging
import random
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Iterable, List, Optional

from .models.tweet_schema import Tweet
from .models.user_schema import User

logger = logging.getLogger(__name__)

class HashtagClient:
    """
    Simulated hashtag client.

    In a production scraper this would talk to Twitter/X network APIs or a
    headless browser. For this project we generate realistic synthetic tweets
    so the rest of the pipeline runs without external dependencies.
    """

    def __init__(self) -> None:
        self._id_counter = itertools.count(start=1_000_000_000_000_000_000)

    def _generate_user(self, idx: int, verified_only: bool, blue_only: bool) -> User:
        is_verified = verified_only or random.random() < 0.3
        is_blue = blue_only or random.random() < 0.2

        username = f"user{idx}"
        return User(
            type="user",
            id=idx,
            username=username,
            name=f"User {idx}",
            url=f"https://x.com/{username}",
            isVerified=is_verified,
            isBlueVerified=is_blue,
            profilePicture=f"https://example.com/avatars/{idx}.jpg",
            coverPicture=None,
            description=f"Synthetic account #{idx}",
            location="Internet",
            followers=random.randint(10, 50_000),
            following=random.randint(5, 5_000),
            favouritesCount=random.randint(0, 10_000),
            mediaCount=random.randint(0, 1_000),
            statusesCount=random.randint(0, 50_000),
            listedCount=random.randint(0, 500),
            protected=False,
            createdAt=datetime.now(timezone.utc)
            - timedelta(days=random.randint(30, 365 * 5)),
        )

    def _generate_text(self, hashtag: str) -> str:
        templates = [
            "Loving the vibes around {tag} today!",
            "Not sure how I feel about {tag} right now...",
            "{tag} is going absolutely crazy. What a ride.",
            "Anyone else watching {tag} closely?",
            "This might be the start of something big for {tag}.",
            "{tag} is overhyped, change my mind.",
        ]
        template = random.choice(templates)
        return template.format(tag=hashtag)

    def _generate_media(self, idx: int) -> dict:
        if random.random() < 0.6:
            return {
                "photos": [
                    {"url": f"https://example.com/media/{idx}_photo.jpg"},
                ],
                "videos": [],
                "animated": [],
            }
        return {"photos": [], "videos": [], "animated": []}

    def fetch_hashtag_tweets(
        self,
        hashtags: Iterable[str],
        max_items: int,
        language: Optional[str] = None,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        verified_only: bool = False,
        blue_only: bool = False,
    ) -> List[Tweet]:
        language = language or "en"
        since = since or (datetime.now(timezone.utc) - timedelta(days=1))
        until = until or datetime.now(timezone.utc)

        result: List[Tweet] = []
        hashtags = [h.strip() for h in hashtags if h.strip()]
        if not hashtags:
            logger.warning("No hashtags provided to fetch_hashtag_tweets")
            return result

        logger.debug(
            "Generating synthetic tweets for hashtags=%s, max_items=%d",
            hashtags,
            max_items,
        )

        for i in range(max_items):
            h = random.choice(hashtags)
            tweet_id = next(self._id_counter)
            created_at = since + (until - since) * random.random()
            user = self._generate_user(i + 1, verified_only, blue_only)
            text = self._generate_text(h)

            tweet = Tweet(
                type="tweet",
                id=tweet_id,
                url=f"https://x.com/{user.username}/status/{tweet_id}",
                text=text,
                isQuote=False,
                isRetweet=False,
                retweetCount=random.randint(0, 500),
                replyCount=random.randint(0, 300),
                likeCount=random.randint(0, 2_000),
                quoteCount=random.randint(0, 100),
                createdAt=created_at,
                lang=language,
                bookmarkCount=random.randint(0, 200),
                isReply=random.random() < 0.2,
                source="Synthetic Twitter Client",
                author=user,
                quote=None,
                retweetedTweet=None,
                media=self._generate_media(i + 1),
                cashtags=[],
                hashtags=[h.lstrip("#")],
                links=[],
                conversationId=tweet_id,
                card=None,
                coordinates=None,
                mentionedUsers=[],
                tone=None,
                sentiment=None,
            )
            logger.debug("Generated tweet: %s", asdict(tweet))
            result.append(tweet)

        return result