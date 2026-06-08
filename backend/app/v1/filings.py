from fastapi import APIRouter

router = APIRouter()


@router.get("/{ticker}")
async def get_filings(ticker: str) -> dict[str, object]:
    return {"ticker": ticker.upper(), "filings": []}
