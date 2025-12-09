"""Base abstract class for all trend data sources."""

from abc import ABC, abstractmethod
from typing import List
from models import TrendItem


class BaseTrendSource(ABC):
    """Abstract base class that all trend sources must implement."""

    @abstractmethod
    def fetch_trends(self, limit: int = 10) -> List[TrendItem]:
        """Fetch trending items from the specific platform."""
        raise NotImplementedError
