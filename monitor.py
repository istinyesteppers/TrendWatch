from typing import List
from models import TrendItem
from base_source import BaseTrendSource
from db import TrendDatabase


class TrendMonitor:
    def __init__(self, source: BaseTrendSource, db: TrendDatabase):
        self.source = source
        self.db = db

    def fetch_and_store(self, limit: int = 10) -> None:
        trends: List[TrendItem] = self.source.fetch_trends(limit=limit)
        self.db.save_trends(trends)

    def show_latest(self, limit: int = 10) -> None:
        trends = self.db.get_latest(limit=limit)
        if not trends:
            print("No data in database yet.")
            return

        print(f"\nLast {len(trends)} saved trends:\n")
        for t in trends:
            print(f"[{t.platform.upper()} #{t.rank}] {t.title} (score={t.score})")
            print(f"  {t.url}")
            print(f"  fetched_at={t.fetched_at}")
            print("-" * 80)
