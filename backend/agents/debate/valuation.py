from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.agents.debate.state import DebateState

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.1)

val_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Quantitative Valuation Agent. Review the quantitative metrics. Estimate a rough Base Case, Bull Case, and Bear Case intrinsic value. Return a JSON structure representing the valuation."),
    ("user", "Ticker: {ticker}\nSEC Data: {sec_data}\nEarnings: {earnings_data}")
])

def run_valuation_analyst(state: DebateState) -> dict:
    chain = val_prompt | llm
    # In reality, this would trigger the Monte Carlo module
    response = chain.invoke({
        "ticker": state["ticker"],
        "sec_data": state.get("sec_data", {}),
        "earnings_data": state.get("earnings_data", {})
    })
    return {"valuation": {"summary": response.content}}
