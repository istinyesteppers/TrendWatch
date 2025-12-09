import requests
from datetime import datetime, timezone
from typing import List

from base_source import BaseTrendSource
from models import TrendItem


class RedditTrendSource(BaseTrendSource):
    def __init__(self, subreddit: str = "news"):
        self.subreddit = subreddit
        self.base_url = f"https://www.reddit.com/r/{subreddit}/top.json"

    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        headers = {"User-Agent": "TrendWatch/1.0"}
        params = {
            "limit": limit,
            "t": "day",
        }

        response = requests.get(
            self.base_url,
            headers=headers,
            params=params,
            timeout=10,
        )
        data = response.json()

        items: List[TrendItem] = []
        now = datetime.now(timezone.utc)

        for rank, child in enumerate(data["data"]["children"], start=1):
            post = child["data"]

            items.append(
                TrendItem(
                    platform="reddit",
                    title=post.get("title", ""),
                    url="https://www.reddit.com" + post.get("permalink", ""),
                    score=int(post.get("score", 0)),
                    rank=rank,
                    fetched_at=now,
                )
            )

        return items
