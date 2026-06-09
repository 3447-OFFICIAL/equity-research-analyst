import re
from fastapi import HTTPException
from pydantic import BaseModel, constr

# Strict alphanumeric validation for Ticker
class TickerInput(BaseModel):
    ticker: str

def validate_ticker(ticker: str) -> str:
    if not re.match(r"^[A-Z]{1,5}$", ticker.upper()):
        raise HTTPException(status_code=400, detail="Invalid ticker format. Potential Injection detected.")
    return ticker.upper()

def sanitize_context(context: str) -> str:
    """
    Remove or escape XML tags from user context so it cannot break out of our <context> blocks.
    """
    if not context:
        return ""
    # Strip <context> or </context> if present
    context = re.sub(r'</?context>', '', context, flags=re.IGNORECASE)
    return context
