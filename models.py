"""Dataclasses for representing trend items in TrendWatch."""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal

Platform = Literal["reddit", "youtube", "web"]

@dataclass
class TrendItem:
    """Represents a single trending item from any platform."""
    platform: Platform
    title: str
    url: str
    score: int
    rank: int
    fetched_at: datetime
