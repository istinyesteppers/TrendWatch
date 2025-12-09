from typing import List
from datetime import datetime
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
                "fetched_at": t.fetched_at.isoformat()
            })
        self.collection.insert_many(docs)

    def get_latest(self, limit: int = 10):
        cursor = self.collection.find().sort("_id", -1).limit(limit)
        items = []
        for doc in cursor:
            items.append(
                TrendItem(
                    platform=doc["platform"],
                    title=doc["title"],
                    url=doc["url"],
                    score=doc["score"],
                    rank=doc["rank"],
                    fetched_at=datetime.fromisoformat(doc["fetched_at"])
                )
            )
        return items

