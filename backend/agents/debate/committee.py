import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.agents.debate.state import DebateState

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2, model_kwargs={"response_format": {"type": "json_object"}})

committee_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are the Investment Committee. Your job is to review the arguments from the Bull Analyst, Bear Analyst, Risk Officer, and Valuation Agent. 
    You must decide the final action: BUY, HOLD, or SELL.
    You must output valid JSON with EXACTLY these keys:
    {
      "recommendation": "BUY|HOLD|SELL",
      "confidence": 0.0 to 1.0,
      "feedback": "Any feedback or hallucination corrections (empty if none)"
    }"""),
    ("user", "Ticker: {ticker}\nBull Case: {bull}\nBear Case: {bear}\nRisks: {risks}\nValuation: {val}")
])

def run_committee(state: DebateState) -> dict:
    chain = committee_prompt | llm
    response = chain.invoke({
        "ticker": state["ticker"],
        "bull": state.get("bull_case", []),
        "bear": state.get("bear_case", []),
        "risks": state.get("risk_factors", []),
        "val": state.get("valuation", {})
    })
    
    parsed = json.loads(response.content)
    
    return {
        "final_recommendation": parsed.get("recommendation", "HOLD"),
        "confidence": float(parsed.get("confidence", 0.0)),
        "committee_feedback": [parsed.get("feedback", "")],
        "reflection_count": state.get("reflection_count", 0) + 1
    }

def should_reflect(state: DebateState) -> str:
    # If confidence is too low and we haven't reflected too many times, go back to analysts
    if state.get("confidence", 0.0) < 0.6 and state.get("reflection_count", 0) < 2:
        return "reflect"
    return "end"
