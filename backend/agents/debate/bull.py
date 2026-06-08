from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.agents.debate.state import DebateState

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)

bull_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Bull Analyst. Your objective is to find the most optimistic, growth-oriented interpretations of the data. Look for revenue acceleration, margin expansion, and TAM growth. Ignore risks. Return a list of bullish arguments."),
    ("user", "Ticker: {ticker}\nSEC Data: {sec_data}\nEarnings: {earnings_data}")
])

def run_bull_analyst(state: DebateState) -> dict:
    chain = bull_prompt | llm
    response = chain.invoke({
        "ticker": state["ticker"],
        "sec_data": state.get("sec_data", {}),
        "earnings_data": state.get("earnings_data", {})
    })
    return {"bull_case": [response.content]}
