from typing import List
from datetime import datetime, timezone

from pymongo import MongoClient
from models import TrendItem


class MongoTrendDB:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "trendwatch"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["trends"]

    def save_trends(self, trends: List[TrendItem]) -> None:
        """Save a list of TrendItem objects into MongoDB safely."""
        if not trends:
            return

        docs = []
        for t in trends:
            docs.append(
                {
                    "platform": t.platform,
                    "title": t.title,
                    "url": t.url,
                    "score": int(t.score),
                    "rank": int(t.rank),
                    "fetched_at": t.fetched_at.isoformat(),  # store as ISO string
                }
            )

        try:
            self.collection.insert_many(docs)
        except Exception as exc:
            print(f"[ERROR] MongoDB insert failed: {exc}")

    def get_latest(self, limit: int = 10) -> List[TrendItem]:
        """Return latest trends as a list of TrendItem, robust to bad data."""
        cursor = self.collection.find().sort("_id", -1).limit(limit)
        items: List[TrendItem] = []

        for doc in cursor:
            fetched_raw = doc.get("fetched_at")

            # Try to parse ISO timestamp, fall back to "now" if broken/missing
            try:
                fetched_at = (
                    datetime.fromisoformat(fetched_raw)
                    if fetched_raw
                    else datetime.now(timezone.utc)
                )
            except Exception:
                fetched_at = datetime.now(timezone.utc)

            items.append(
                TrendItem(
                    platform=doc.get("platform", ""),
                    title=doc.get("title", ""),
                    url=doc.get("url", ""),
                    score=int(doc.get("score", 0)),
                    rank=int(doc.get("rank", 0)),
                    fetched_at=fetched_at,
                )
            )

        return items
