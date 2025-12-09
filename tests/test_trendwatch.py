import unittest
from datetime import datetime, timezone

from models import TrendItem
from reddit_source import RedditTrendSource
from monitor import TrendMonitor
from db import TrendDatabase


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


if __name__ == "__main__":
    unittest.main()
