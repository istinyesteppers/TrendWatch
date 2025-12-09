from typing import List
from models import TrendItem
from base_source import BaseTrendSource
from db import TrendDatabase


class TrendMonitor:
    """Coordinates fetching trends from a source and saving them to a database."""
    def __init__(self, source: BaseTrendSource, db: TrendDatabase):
        self.source = source
        self.db = db

    def fetch_and_store(self, limit: int = 10) -> None:
        """Fetch trends from the source and store them in the DB safely."""
        try:
            trends: List[TrendItem] = self.source.fetch_trends(limit=limit)
        except Exception as exc:  # last-resort safety
            print(f"[ERROR] Source fetch failed: {exc}")
            return

        if not trends:
            print("[INFO] No trends fetched. Nothing to save.")
            return

        try:
            self.db.save_trends(trends)
        except Exception as exc:
            print(f"[ERROR] Failed to save trends to database: {exc}")


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
