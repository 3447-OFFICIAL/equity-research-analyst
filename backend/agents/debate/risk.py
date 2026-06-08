from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.agents.debate.state import DebateState

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.2)

risk_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Chief Risk Officer. Your objective is to explicitly identify existential, macro, and micro risk factors to the business. Do not take a side, only state the risks. Return a list of risk factors."),
    ("user", "Ticker: {ticker}\nSEC Data: {sec_data}\nEarnings: {earnings_data}")
])

def run_risk_analyst(state: DebateState) -> dict:
    chain = risk_prompt | llm
    response = chain.invoke({
        "ticker": state["ticker"],
        "sec_data": state.get("sec_data", {}),
        "earnings_data": state.get("earnings_data", {})
    })
    return {"risk_factors": [response.content]}
