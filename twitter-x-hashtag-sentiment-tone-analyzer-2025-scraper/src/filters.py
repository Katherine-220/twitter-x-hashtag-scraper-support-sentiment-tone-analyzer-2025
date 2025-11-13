from typing import Dict, Iterable, List

from .models.tweet_schema import Tweet

def filter_by_engagement(
    tweets: Iterable[Tweet],
    min_likes: int = 0,
    min_retweets: int = 0,
    min_replies: int = 0,
) -> List[Tweet]:
    return [
        t
        for t in tweets
        if t.likeCount >= min_likes
        and t.retweetCount >= min_retweets
        and t.replyCount >= min_replies
    ]

def filter_by_language(tweets: Iterable[Tweet], lang: str) -> List[Tweet]:
    lang = (lang or "").lower()
    if not lang:
        return list(tweets)
    return [t for t in tweets if (t.lang or "").lower() == lang]

def filter_by_verification(
    tweets: Iterable[Tweet],
    verified_only: bool = False,
    blue_only: bool = False,
) -> List[Tweet]:
    if not verified_only and not blue_only:
        return list(tweets)

    result: List[Tweet] = []
    for t in tweets:
        user = t.author
        if verified_only and not user.isVerified:
            continue
        if blue_only and not user.isBlueVerified:
            continue
        result.append(t)
    return result

def apply_filters(tweets: List[Tweet], settings: Dict) -> List[Tweet]:
    tweets = filter_by_language(tweets, settings.get("language", "en"))
    tweets = filter_by_engagement(
        tweets,
        min_likes=int(settings.get("min_like_count", 0)),
        min_retweets=int(settings.get("min_retweet_count", 0)),
        min_replies=int(settings.get("min_reply_count", 0)),
    )
    tweets = filter_by_verification(
        tweets,
        verified_only=bool(settings.get("verified_only", False)),
        blue_only=bool(settings.get("blue_verified_only", False)),
    )
    return tweets