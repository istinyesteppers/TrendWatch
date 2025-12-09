from datetime import datetime, timezone
from typing import List, Optional

from base_source import BaseTrendSource
from models import TrendItem


class YouTubeTrendSource(BaseTrendSource):
    def __init__(self, region: str = "US"):
        # default YouTube region
        self.region = region

    # OVERLOADED METHOD: adds optional region parameter
    def fetch_trends(self, limit: int = 10, region: str = "US") -> List[TrendItem]:
        """Return dummy YouTube trends. Safe against bad inputs."""
        items: List[TrendItem] = []

        # Defensive coding: avoid negative limits or None
        if not isinstance(limit, int) or limit <= 0:
            limit = 10

        if not isinstance(region, str) or len(region) == 0:
            region = "US"

        now = datetime.now(timezone.utc)

        for i in range(1, limit + 1):
            items.append(
                TrendItem(
                    platform="youtube",
                    title=f"Trending YouTube Video #{i} ({region})",
                    url=f"https://youtube.com/watch?v=video{i}",
                    score=500 - i * 5,
                    rank=i,
                    fetched_at=now,
                )
            )

        return items

