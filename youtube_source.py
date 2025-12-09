from datetime import datetime, timezone
from typing import List, Optional

from base_source import BaseTrendSource
from models import TrendItem


class YouTubeTrendSource(BaseTrendSource):
    def __init__(self, region: str = "US"):
        # default YouTube region
        self.region = region

    # OVERLOADED METHOD: adds optional region parameter
    def fetch_trends(self, limit: int = 10, region: Optional[str] = None) -> List[TrendItem]:
        region_to_use = region or self.region
        now = datetime.now(timezone.utc)

        items: List[TrendItem] = []

        # DUMMY TRENDS (replace with Selenium later if you want + advanced bonus)
        for i in range(1, limit + 1):
            items.append(
                TrendItem(
                    platform="youtube",
                    title=f"Sample YouTube trend #{i} ({region_to_use})",
                    url=f"https://youtube.com/watch?v=fake{i}",
                    score=1000 - i * 10,
                    rank=i,
                    fetched_at=now,
                )
            )

        return items
