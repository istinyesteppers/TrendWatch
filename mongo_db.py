"""MongoDB backend for storing and retrieving TrendWatch data."""

from typing import List
from datetime import datetime, timezone
from pymongo import MongoClient
from models import TrendItem


class MongoTrendDB:
    """Handles MongoDB storage and retrieval for TrendWatch trends."""

    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "trendwatch"):
        """Initialize MongoDB connection and collection."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["trends"]

    def save_trends(self, trends: List[TrendItem]) -> None:
        """Save a list of TrendItem objects into MongoDB."""
        if not trends:
            return

        docs = [
            {
                "platform": t.platform,
                "title": t.title,
                "url": t.url,
                "score": t.score,
                "rank": t.rank,
                "fetched_at": t.fetched_at.isoformat(),
            }
            for t in trends
        ]

        try:
            self.collection.insert_many(docs)
        except Exception:  # pylint: disable=broad-except
            print("[ERROR] MongoDB insert_many failed.")

    def get_latest(self, limit: int = 10) -> List[TrendItem]:
        """Fetch latest trends and convert them into TrendItem objects."""
        try:
            cursor = self.collection.find().sort("_id", -1).limit(limit)
        except Exception:  # pylint: disable=broad-except
            print("[ERROR] MongoDB query failed.")
            return []

        items: List[TrendItem] = []

        for doc in cursor:
            fetched_str = doc.get("fetched_at", "")
            try:
                fetched_dt = datetime.fromisoformat(fetched_str)
            except Exception:  # pylint: disable=broad-except
                fetched_dt = datetime.now(timezone.utc)

            items.append(
                TrendItem(
                    platform=doc.get("platform", ""),
                    title=doc.get("title", ""),
                    url=doc.get("url", ""),
                    score=int(doc.get("score", 0)),
                    rank=int(doc.get("rank", 0)),
                    fetched_at=fetched_dt,
                )
            )

        return items
