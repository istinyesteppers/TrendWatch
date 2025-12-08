import requests
from datetime import datetime
from typing import List
from models import TrendItem
from base_source import BaseTrendSource


class RedditTrendSource(BaseTrendSource):
    def __init__(self, subreddit: str = "news"):
        self.subreddit = subreddit
        self.url = f"https://www.reddit.com/r/{subreddit}/hot.json"

    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        headers = {"User-Agent": "TrendWatchStudentProject/1.0"}
        response = requests.get(
            self.url,
            headers=headers,
            params={"limit": limit},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        trends: List[TrendItem] = []
        now = datetime.utcnow()

        for i, child in enumerate(data["data"]["children"], start=1):
            post = child["data"]
            title = post.get("title", "")
            url = "https://www.reddit.com" + post.get("permalink", "")
            score = int(post.get("score", 0))

            trends.append(
                TrendItem(
                    platform="reddit",
                    title=title,
                    url=url,
                    score=score,
                    rank=i,
                    fetched_at=now,
                )
            )

        return trends
