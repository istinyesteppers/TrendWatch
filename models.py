from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Platform = Literal["reddit", "youtube", "web"]

@dataclass
class TrendItem:
    platform: Platform
    title: str
    url: str
    score: int
    rank: int
    fetched_at: datetime
