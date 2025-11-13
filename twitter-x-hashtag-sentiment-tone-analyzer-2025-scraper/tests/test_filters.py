from datetime import datetime, timezone

from src.filters import (
    apply_filters,
    filter_by_engagement,
    filter_by_language,
    filter_by_verification,
)
from src.models.tweet_schema import Tweet
from src.models.user_schema import User

def _make_user(verified: bool = False, blue: bool = False) -> User:
    return User(
        type="user",
        id=1,
        username="test",
        name="Test User",
        url="https://x.com/test",
        isVerified=verified,
        isBlueVerified=blue,
        profilePicture="https://example.com/avatar.jpg",
        coverPicture=None,
        description="",
        location="Internet",
        followers=10,
        following=5,
        favouritesCount=0,
        mediaCount=0,
        statusesCount=0,
        listedCount=0,
        protected=False,
        createdAt=datetime.now(timezone.utc),
    )

def _make_tweet(
    likes: int = 0,
    rts: int = 0,
    replies: int = 0,
    lang: str = "en",
    verified: bool = False,
    blue: bool = False,
) -> Tweet:
    return Tweet(
        type="tweet",
        id=1,
        url="https://x.com/test/status/1",
        text="test",
        isQuote=False,
        isRetweet=False,
        retweetCount=rts,
        replyCount=replies,
        likeCount=likes,
        quoteCount=0,
        createdAt=datetime.now(timezone.utc),
        lang=lang,
        bookmarkCount=0,
        isReply=False,
        source="test",
        author=_make_user(verified, blue),
        quote=None,
        retweetedTweet=None,
        media={"photos": [], "videos": [], "animated": []},
        cashtags=[],
        hashtags=["TEST"],
        links=[],
        conversationId=1,
        card=None,
        coordinates=None,
        mentionedUsers=[],
        tone=None,
        sentiment=None,
    )

def test_filter_by_engagement():
    t1 = _make_tweet(likes=5, rts=2, replies=1)
    t2 = _make_tweet(likes=1, rts=0, replies=0)
    filtered = filter_by_engagement([t1, t2], min_likes=2, min_retweets=1, min_replies=1)
    assert t1 in filtered
    assert t2 not in filtered

def test_filter_by_language():
    t1 = _make_tweet(lang="en")
    t2 = _make_tweet(lang="es")
    filtered = filter_by_language([t1, t2], "en")
    assert t1 in filtered
    assert t2 not in filtered

def test_filter_by_verification():
    t1 = _make_tweet(verified=True, blue=False)
    t2 = _make_tweet(verified=False, blue=True)
    t3 = _make_tweet(verified=False, blue=False)

    filtered_verified = filter_by_verification([t1, t2, t3], verified_only=True)
    assert t1 in filtered_verified
    assert t2 not in filtered_verified
    assert t3 not in filtered_verified

    filtered_blue = filter_by_verification([t1, t2, t3], verified_only=False, blue_only=True)
    assert t2 in filtered_blue
    assert t1 not in filtered_blue
    assert t3 not in filtered_blue

def test_apply_filters():
    t1 = _make_tweet(likes=10, lang="en", verified=True)
    t2 = _make_tweet(likes=1, lang="es", verified=False)
    settings = {
        "language": "en",
        "min_like_count": 5,
        "min_retweet_count": 0,
        "min_reply_count": 0,
        "verified_only": True,
        "blue_verified_only": False,
    }
    filtered = apply_filters([t1, t2], settings)
    assert t1 in filtered
    assert t2 not in filtered