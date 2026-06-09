from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup
import re
from fastapi import HTTPException
from urllib.parse import quote
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from backend.core.config import settings
from backend.core.guardrails import validate_ticker

@dataclass(frozen=True)
class FilingExtraction:
    ticker: str
    form_type: str
    revenue: float | None
    net_income: float | None
    risk_factors: str | None
    mda: str | None


class SECFilingIngestionService:
    def __init__(self):
        self.headers = {"User-Agent": settings.sec_user_agent}
        self.base_url = "https://data.sec.gov/submissions"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError))
    )
    async def download_10k(self, ticker: str, cik: str) -> str:
        ticker = validate_ticker(ticker)
        if not re.match(r"^\d{1,10}$", cik):
            raise HTTPException(status_code=400, detail="Invalid CIK format")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/CIK{cik.zfill(10)}.json", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            # Simplified: Find latest 10-K accession number
            filings = data.get("filings", {}).get("recent", {})
            for idx, form in enumerate(filings.get("form", [])):
                if form == "10-K":
                    accession_no = filings["accessionNumber"][idx].replace("-", "")
                    primary_doc = filings["primaryDocument"][idx]
                    
                    # Fetch document
                    doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_no}/{primary_doc}"
                    doc_resp = await client.get(doc_url, headers=self.headers)
                    return doc_resp.text
            return ""

    async def extract_sections(self, filing_text: str, ticker: str) -> FilingExtraction:
        # Simplified BeautifulSoup extraction for Item 1A and Item 7
        soup = BeautifulSoup(filing_text, "lxml")
        text = soup.get_text(separator="\n")
        
        # In a real app, we'd use regex to find sections. Here we provide a stub.
        return FilingExtraction(
            ticker=ticker,
            form_type="10-K",
            revenue=None,
            net_income=None,
            risk_factors=text[:5000],  # Mocking extraction
            mda=text[5000:10000]
        )

    async def store(self, extraction: FilingExtraction) -> None:
        # Uses Alembic / SQLAlchemy to persist
        pass
