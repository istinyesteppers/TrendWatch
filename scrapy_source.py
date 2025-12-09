"""Scrapy-based Hacker News trend source for TrendWatch."""

from datetime import datetime, timezone
from typing import List

import scrapy
from scrapy.crawler import CrawlerProcess

from base_source import BaseTrendSource
from models import TrendItem


class HNSpider(scrapy.Spider):
    """
    Simple Scrapy spider that scrapes Hacker News front page.
    We use this just to demonstrate a real Scrapy workflow.
    """
    name = "hn_trends"
    custom_settings = {
        "LOG_ENABLED": False,
        "USER_AGENT": "TrendWatchScraper/1.0",
    }

    def __init__(self, limit: int = 10, items_out=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = ["https://news.ycombinator.com/"]
        self.limit = limit
        self.items_out = items_out if items_out is not None else []

    def parse(self, response):
        """Parse the Hacker News HTML rows and extract title, URL, and rank."""
        # Each story row has class "athing"
        rows = response.css("tr.athing")

        for rank, row in enumerate(rows[: self.limit], start=1):
            title = row.css("span.titleline a::text").get(default="").strip()
            url = row.css("span.titleline a::attr(href)").get(default="")

            # Fake score just for ranking purposes
            score = 1000 - rank * 10

            self.items_out.append(
                {
                    "title": title,
                    "url": url,
                    "score": score,
                    "rank": rank,
                }
            )


class ScrapyHNSource(BaseTrendSource):
    """Scrapes Hacker News front page using Scrapy."""
    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        """Fetch top trends from Hacker News using Scrapy."""
        items_out: List[dict] = []

        process = CrawlerProcess(
            settings={
                "LOG_ENABLED": False,
                "USER_AGENT": "TrendWatchScraper/1.0",
            }
        )

        # Run the Scrapy spider synchronously and fill items_out
        process.crawl(HNSpider, limit=limit, items_out=items_out)
        process.start()

        now = datetime.now(timezone.utc)
        results: List[TrendItem] = []

        if not items_out:
            print("[WARN] Scrapy returned no items.")
            return []

        for item in items_out:
            title = item.get("title", "")
            url = item.get("url", "")
            score = int(item.get("score", 0))
            rank = int(item.get("rank", 0))

            results.append(
                TrendItem(
                    platform="web",
                    title=title,
                    url=url,
                    score=score,
                    rank=rank,
                    fetched_at=now,
                )
            )

        return results
