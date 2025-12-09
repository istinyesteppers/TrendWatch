import requests
from datetime import datetime, timezone
from typing import List

from base_source import BaseTrendSource
from models import TrendItem


class RedditTrendSource(BaseTrendSource):
    """Fetches top posts from a subreddit using the Reddit JSON API."""

    def __init__(self, subreddit: str = "news"):
        self.subreddit = subreddit
        self.base_url = f"https://www.reddit.com/r/{subreddit}/top.json"

    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        """Fetch top posts from the subreddit. Returns an empty list on failure."""
        headers = {"User-Agent": "TrendWatch/1.0"}
        params = {
            "limit": limit,
            "t": "day",
        }

        items: List[TrendItem] = []

        try:
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10,
            )
            response.raise_for_status()  # raises for 4xx / 5xx
        except requests.RequestException as exc:
            print(f"[ERROR] Failed to fetch from Reddit: {exc}")
            return items  # empty list => caller knows nothing was fetched

        try:
            data = response.json()
        except ValueError as exc:
            print(f"[ERROR] Invalid JSON from Reddit: {exc}")
            return items

        children = data.get("data", {}).get("children", [])
        if not children:
            print("[WARN] Reddit returned no posts.")
            return items

        now = datetime.now(timezone.utc)

        for rank, child in enumerate(children[:limit], start=1):
            post = child.get("data", {})

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

