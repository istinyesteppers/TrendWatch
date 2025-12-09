"""YouTube demo trend source used for polymorphism and testing."""

from datetime import datetime, timezone
from typing import List


from base_source import BaseTrendSource
from models import TrendItem


class YouTubeTrendSource(BaseTrendSource):
    """Provides dummy YouTube trend data for OOP demonstration."""

    def __init__(self, region: str = "US"):
        # default YouTube region
        self.region = region

    # OVERLOADED METHOD: adds optional region parameter
    def fetch_trends(self, limit: int = 10, region: str | None = None) -> List[TrendItem]:
        """Return dummy YouTube trends. Safe against bad inputs."""
        items: List[TrendItem] = []

        # fallback to default region if not provided
        if region is None:
            region = self.region

        # Defensive: avoid non-int or negative limits
        if not isinstance(limit, int) or limit <= 0:
            limit = 10

        # Defensive: ensure region is a non-empty string
        if not isinstance(region, str) or not region.strip():
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
