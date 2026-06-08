from typing import Literal, TypedDict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

Recommendation = Literal["BUY", "HOLD", "SELL"]

class ResearchState(TypedDict, total=False):
    ticker: str
    sec_data: str
    earnings_data: str
    financial_analysis: dict[str, float]
    risk_analysis: dict[str, object]
    competitor_comparison: list[dict[str, object]]
    valuation: dict[str, float]
    recommendation: Recommendation
    confidence_score: float

def sec_agent(state: ResearchState) -> dict[str, Any]:
    # Mock SEC analysis
    return {"sec_data": "Extracted Risk Factors and MD&A from SEC."}

def earnings_agent(state: ResearchState) -> dict[str, Any]:
    # Mock Earnings analysis
    return {"earnings_data": "Sentiment is positive, CEO mentioned AI growth."}

def supervisor_agent(state: ResearchState) -> dict[str, Any]:
    # Mock Supervisor
    # In reality, this would use an LLM to synthesize data and pick a recommendation
    return {
        "recommendation": "BUY",
        "confidence_score": 0.85
    }

def build_research_workflow():
    workflow = StateGraph(ResearchState)

    workflow.add_node("sec_agent", sec_agent)
    workflow.add_node("earnings_agent", earnings_agent)
    workflow.add_node("supervisor", supervisor_agent)

    workflow.set_entry_point("sec_agent")
    workflow.add_edge("sec_agent", "earnings_agent")
    workflow.add_edge("earnings_agent", "supervisor")
    workflow.add_edge("supervisor", END)

    return workflow.compile()
