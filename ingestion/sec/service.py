from dataclasses import dataclass
import httpx
from bs4 import BeautifulSoup
from backend.core.config import settings
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

    async def download_10k(self, ticker: str, cik: str) -> str:
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
