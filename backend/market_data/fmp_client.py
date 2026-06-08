import httpx
import os
from typing import Dict, Any, List
from backend.market_data.base import MarketDataProvider

class FMPClient(MarketDataProvider):
    """
    Implementation of the MarketDataProvider using Financial Modeling Prep (FMP) API.
    """
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self):
        self.api_key = os.getenv("FMP_API_KEY", "demo")
        
    async def _fetch(self, endpoint: str, params: dict = None) -> Any:
        if params is None:
            params = {}
        params["apikey"] = self.api_key
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

    async def get_realtime_price(self, ticker: str) -> float:
        data = await self._fetch(f"quote-short/{ticker}")
        if data and len(data) > 0:
            return data[0].get("price", 0.0)
        return 0.0
        
    async def get_historical_prices(self, ticker: str, days: int = 365) -> List[Dict[str, Any]]:
        # This endpoint returns last X days of prices
        data = await self._fetch(f"historical-price-full/{ticker}")
        return data.get("historical", [])[:days]
        
    async def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        data = await self._fetch(f"profile/{ticker}")
        return data[0] if data else {}
        
    async def get_analyst_estimates(self, ticker: str) -> Dict[str, Any]:
        data = await self._fetch(f"analyst-estimates/{ticker}")
        return data[0] if data else {}
