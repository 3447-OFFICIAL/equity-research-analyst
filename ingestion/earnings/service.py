from typing import Any
import httpx
from urllib.parse import quote
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from backend.core.config import settings
from backend.core.guardrails import validate_ticker

class TranscriptIngestionService:
    def __init__(self):
        self.api_key = settings.fmp_api_key

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def fetch_transcript(self, ticker: str, year: int, quarter: int) -> dict[str, Any]:
        ticker = validate_ticker(ticker)
        safe_ticker = quote(ticker)
        # Simulated API call to an earnings transcript provider
        # Example using a mock FMP endpoint
        url = f"https://financialmodelingprep.com/api/v3/earning_call_transcript/{safe_ticker}"
        
        # We mock the response for demonstration since we don't have a real API key here
        mock_transcript = f"Welcome to the {ticker} Q{quarter} {year} earnings call. Our revenue grew by 15%..."
        
        return {
            "ticker": ticker,
            "quarter": quarter,
            "year": year,
            "content": mock_transcript
        }

    def chunk_transcript(self, transcript: str) -> list[str]:
        # Simple chunking by paragraphs or sentences
        # A more advanced chunker would split by speaker (e.g. CEO vs Analyst)
        paragraphs = transcript.split("\n\n")
        return [p.strip() for p in paragraphs if p.strip()]
