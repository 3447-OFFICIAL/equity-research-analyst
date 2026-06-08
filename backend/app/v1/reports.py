from fastapi import APIRouter

router = APIRouter()


@router.get("/{ticker}")
async def get_report(ticker: str) -> dict[str, str]:
    return {"ticker": ticker.upper(), "report_status": "not_generated"}
