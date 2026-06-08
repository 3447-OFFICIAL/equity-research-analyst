from fastapi import APIRouter

router = APIRouter()


@router.get("/{ticker}")
async def get_company(ticker: str) -> dict[str, str]:
    return {"ticker": ticker.upper(), "status": "placeholder"}
