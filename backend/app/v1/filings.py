from fastapi import APIRouter, Depends
from backend.core.security import get_current_active_user
from backend.models.user import User

from fastapi_limiter.depends import RateLimiter

router = APIRouter()


@router.get("/{ticker}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_filings(ticker: str, current_user: User = Depends(get_current_active_user)) -> dict[str, object]:
    return {"ticker": ticker.upper(), "filings": []}
