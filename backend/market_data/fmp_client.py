import httpx
from typing import Dict, Any, List
from urllib.parse import quote
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from backend.market_data.base import MarketDataProvider
from backend.core.config import settings
from backend.core.guardrails import validate_ticker

class FMPClient(MarketDataProvider):
    """
    Implementation of the MarketDataProvider using Financial Modeling Prep (FMP) API.
    """
    BASE_URL = "https://financialmodelingprep.com/api/v3"
    
    def __init__(self):
        self.api_key = settings.fmp_api_key
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def _fetch(self, endpoint: str, params: dict = None) -> Any:
        if params is None:
            params = {}
        params["apikey"] = self.api_key
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()

    async def get_realtime_price(self, ticker: str) -> float:
        safe_ticker = quote(validate_ticker(ticker))
        data = await self._fetch(f"quote-short/{safe_ticker}")
        if data and len(data) > 0:
            return data[0].get("price", 0.0)
        return 0.0
        
    async def get_historical_prices(self, ticker: str, days: int = 365) -> List[Dict[str, Any]]:
        safe_ticker = quote(validate_ticker(ticker))
        # This endpoint returns last X days of prices
        data = await self._fetch(f"historical-price-full/{safe_ticker}")
        return data.get("historical", [])[:days]
        
    async def get_company_profile(self, ticker: str) -> Dict[str, Any]:
        safe_ticker = quote(validate_ticker(ticker))
        data = await self._fetch(f"profile/{safe_ticker}")
        return data[0] if data else {}
        
    async def get_analyst_estimates(self, ticker: str) -> Dict[str, Any]:
        safe_ticker = quote(validate_ticker(ticker))
        data = await self._fetch(f"analyst-estimates/{safe_ticker}")
        return data[0] if data else {}
