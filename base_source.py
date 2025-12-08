from abc import ABC, abstractmethod
from typing import List
from .models import TrendItem

class BaseTrendSource(ABC):
    @abstractmethod
    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        """Fetch top 'limit' trending items."""
        pass
