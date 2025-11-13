import json
from pathlib import Path
from typing import Iterable, List

from ..models.tweet_schema import Tweet

def write_json(tweets: Iterable[Tweet], output_path: str) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    data: List[dict] = [t.to_dict() for t in tweets]
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)