import operator
from typing import Annotated, TypedDict, Any

class DebateState(TypedDict):
    ticker: str
    sec_data: dict[str, Any]
    earnings_data: dict[str, Any]
    bull_case: Annotated[list[str], operator.add]
    bear_case: Annotated[list[str], operator.add]
    risk_factors: Annotated[list[str], operator.add]
    valuation: dict[str, Any]
    committee_feedback: list[str]
    reflection_count: int
    final_recommendation: str
    confidence: float
