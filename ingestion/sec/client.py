import asyncio
import httpx
from typing import Dict, Any

class SecEdgarClient:
    """
    Async client for SEC EDGAR API with strict rate limiting (10 req/sec) and User-Agent enforcement.
    """
    BASE_URL = "https://data.sec.gov/api/xbrl/companyfacts"
    
    def __init__(self, user_agent: str = "EquityResearchPlatform admin@equityresearch.com"):
        self.headers = {"User-Agent": user_agent}
        self.semaphore = asyncio.Semaphore(10) # Max 10 concurrent requests
        
    async def get_company_facts(self, cik: str) -> Dict[str, Any]:
        """
        Fetches all historical XBRL facts for a given CIK.
        CIK must be zero-padded to 10 digits.
        """
        padded_cik = str(cik).zfill(10)
        url = f"{self.BASE_URL}/CIK{padded_cik}.json"
        
        async with self.semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=self.headers)
                
                if response.status_code == 429:
                    # SEC rate limit hit, backoff
                    await asyncio.sleep(1.0)
                    return await self.get_company_facts(cik)
                    
                response.raise_for_status()
                
                # Small delay to ensure we don't burst over the 10/sec limit
                await asyncio.sleep(0.1) 
                return response.json()
