import unittest
from datetime import datetime, timezone
from typing import List

from models import TrendItem
from reddit_source import RedditTrendSource
from monitor import TrendMonitor
from db import TrendDatabase
from youtube_source import YouTubeTrendSource
from base_source import BaseTrendSource


class TestTrendItem(unittest.TestCase):
    def test_trend_item_fields(self):
        now = datetime.now(timezone.utc)
        item = TrendItem(
            platform="reddit",
            title="Test",
            url="https://example.com",
            score=100,
            rank=1,
            fetched_at=now,
        )
        self.assertEqual(item.platform, "reddit")
        self.assertEqual(item.title, "Test")
        self.assertEqual(item.rank, 1)
        self.assertEqual(item.score, 100)
        self.assertEqual(item.fetched_at, now)


class TestSQLiteIntegration(unittest.TestCase):
    def test_fetch_and_store_with_sqlite(self):
        # Use a temporary SQLite DB file for testing
        db = TrendDatabase("test_trends.db")
        source = RedditTrendSource("news")
        monitor = TrendMonitor(source, db)

        # Just check that it doesn't crash and returns a list
        items = source.fetch_trends(limit=3)
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)
        self.assertIsInstance(items[0], TrendItem)

        # Save and then read back
        db.save_trends(items)
        latest = db.get_latest(limit=3)
        self.assertGreater(len(latest), 0)
        self.assertIsInstance(latest[0], TrendItem)


class TestYouTubeSource(unittest.TestCase):
    def test_youtube_handles_bad_input(self):
        src = YouTubeTrendSource(region="US")

        # Intentionally pass bad values
        items = src.fetch_trends(limit="not-an-int", region=None)

        # Should not crash, should return a non-empty list of TrendItem
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)
        first = items[0]
        self.assertIsInstance(first, TrendItem)
        self.assertEqual(first.platform, "youtube")


class EmptySource(BaseTrendSource):
    """Fake source that returns no trends, for robustness testing."""

    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        return []


class TestMonitorWithEmptySource(unittest.TestCase):
    def test_monitor_handles_empty_source(self):
        # Use fake source that always returns []
        source = EmptySource()
        db = TrendDatabase("test_trends_empty.db")
        monitor = TrendMonitor(source, db)

        # Should not crash even though source returns no data
        monitor.fetch_and_store(limit=5)

        latest = db.get_latest(limit=5)
        # If nothing was saved, this can be empty, but must not crash
        self.assertIsInstance(latest, list)
        self.assertEqual(len(latest), 0)


if __name__ == "__main__":
    unittest.main()
