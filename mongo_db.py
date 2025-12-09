from typing import List
from datetime import datetime, timezone
from pymongo import MongoClient
from models import TrendItem


class MongoTrendDB:
    def __init__(self, uri="mongodb://localhost:27017", db_name="trendwatch"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["trends"]

    def save_trends(self, trends: List[TrendItem]):
        docs = []
        for t in trends:
            docs.append({
                "platform": t.platform,
                "title": t.title,
                "url": t.url,
                "score": t.score,
                "rank": t.rank,
                "fetched_at": t.fetched_at.isoformat()  # timezone-aware string
            })
        if docs:
            self.collection.insert_many(docs)

    def get_latest(self, limit: int = 10):
        cursor = self.collection.find().sort("_id", -1).limit(limit)
        items = []

        for doc in cursor:
            fetched_raw = doc.get("fetched_at")

            # Safe conversion to datetime, guaranteed not to crash
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
                    platform=doc["platform"],
                    title=doc["title"],
                    url=doc["url"],
                    score=doc["score"],
                    rank=doc["rank"],
                    fetched_at=fetched_at
                )
            )

        return items
