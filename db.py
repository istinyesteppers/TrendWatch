from typing import List
from pymongo import MongoClient
from .models import TrendItem

class TrendRepository:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "trendwatch"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["trends"]

    def save_trends(self, trends: List[TrendItem]) -> None:
        if not trends:
            return
        docs = [t.__dict__ for t in trends]
        self.collection.insert_many(docs)

    def get_latest(self, platform: str, limit: int = 20):
        return list(
            self.collection
            .find({"platform": platform})
            .sort("fetched_at", -1)
            .limit(limit)
        )
