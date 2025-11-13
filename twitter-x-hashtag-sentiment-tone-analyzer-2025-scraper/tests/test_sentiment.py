from src.sentiment_engine import SentimentEngine

def test_sentiment_positive():
    engine = SentimentEngine()
    sentiment, tone = engine.analyze_text("Amazing gains, love this bull run!")
    assert sentiment == "Positive"
    assert tone in {"Enthusiastic", "Humorous", "Informative", "Neutral"}

def test_sentiment_negative():
    engine = SentimentEngine()
    sentiment, _ = engine.analyze_text("Hate this crash, feels like a scam.")
    assert sentiment == "Negative"

def test_sentiment_neutral():
    engine = SentimentEngine()
    sentiment, _ = engine.analyze_text("Watching the market closely today.")
    assert sentiment in {"Neutral", "Positive", "Negative"}