from abc import ABC, abstractmethod
from typing import Dict, Any, List

class MarketDataProvider(ABC):
    """
    Abstract Base Class for all external market data providers.
    Ensures a unified interface regardless of the underlying API (FMP, AlphaVantage, etc).
    """
    
    @abstractmethod
    async def get_realtime_price(self, ticker: str) -> float:
        pass
        
    @abstractmethod
    async def get_historical_prices(self, ticker: str, days: int = 365) -> List[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    async def get_analyst_estimates(self, ticker: str) -> Dict[str, Any]:
        pass
