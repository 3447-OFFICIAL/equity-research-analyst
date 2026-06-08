from typing import Any
import httpx
from backend.valuation.dcf import calculate_dcf, DCFResult

class FinancialModelerAgent:
    def __init__(self):
        self.api_key = "MOCK_API_KEY"
    
    async def fetch_financials(self, ticker: str) -> dict[str, Any]:
        # Mocking an API call to get historical financials
        # url = f"https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/{ticker}?apikey={self.api_key}"
        
        # Simulated data for demonstration
        return {
            "ticker": ticker,
            "latest_fcf": 100_000_000,
            "estimated_growth_rate": 0.05,
            "wacc": 0.10,
            "terminal_growth_rate": 0.02,
            "current_market_price": 150.0,
            "shares_outstanding": 10_000_000
        }

    async def run_valuation(self, ticker: str) -> DCFResult:
        financials = await self.fetch_financials(ticker)
        
        starting_fcf = financials["latest_fcf"] / financials["shares_outstanding"]
        
        dcf_result = calculate_dcf(
            starting_fcf=starting_fcf,
            growth_rate=financials["estimated_growth_rate"],
            discount_rate=financials["wacc"],
            terminal_growth_rate=financials["terminal_growth_rate"],
            periods=5,
            market_price=financials["current_market_price"]
        )
        return dcf_result
