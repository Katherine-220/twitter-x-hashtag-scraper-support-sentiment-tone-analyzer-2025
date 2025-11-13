from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

from .user_schema import User

@dataclass
class Tweet:
    type: str
    id: int
    url: str
    text: str
    isQuote: bool
    isRetweet: bool
    retweetCount: int
    replyCount: int
    likeCount: int
    quoteCount: int
    createdAt: datetime
    lang: str
    bookmarkCount: int
    isReply: bool
    source: str
    author: User
    quote: Optional[Dict[str, Any]]
    retweetedTweet: Optional[Dict[str, Any]]
    media: Dict[str, Any]
    cashtags: List[str]
    hashtags: List[str]
    links: List[Any]
    conversationId: int
    card: Optional[Dict[str, Any]]
    coordinates: Optional[Dict[str, float]]
    mentionedUsers: List[User]
    tone: Optional[str]
    sentiment: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tweet into a JSON-serializable dictionary.
        """
        return {
            "type": self.type,
            "id": self.id,
            "url": self.url,
            "text": self.text,
            "isQuote": self.isQuote,
            "isRetweet": self.isRetweet,
            "retweetCount": self.retweetCount,
            "replyCount": self.replyCount,
            "likeCount": self.likeCount,
            "quoteCount": self.quoteCount,
            "createdAt": self.createdAt.isoformat(),
            "lang": self.lang,
            "bookmarkCount": self.bookmarkCount,
            "isReply": self.isReply,
            "source": self.source,
            "author": self.author.to_dict(),
            "quote": self.quote,
            "retweetedTweet": self.retweetedTweet,
            "media": self.media,
            "cashtags": self.cashtags,
            "hashtags": self.hashtags,
            "links": self.links,
            "conversationId": self.conversationId,
            "card": self.card,
            "coordinates": self.coordinates,
            "mentionedUsers": [u.to_dict() for u in self.mentionedUsers],
            "tone": self.tone,
            "sentiment": self.sentiment,
        }