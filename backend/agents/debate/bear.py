from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from backend.agents.debate.state import DebateState

llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)

bear_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are the Bear Analyst. Your objective is to find the most pessimistic, highly critical interpretations of the data. Look for declining margins, debt burdens, competitor threats, and executive turnover. Ignore growth. Return a list of bearish arguments."),
    ("user", "Ticker: {ticker}\nSEC Data: {sec_data}\nEarnings: {earnings_data}")
])

def run_bear_analyst(state: DebateState) -> dict:
    chain = bear_prompt | llm
    response = chain.invoke({
        "ticker": state["ticker"],
        "sec_data": state.get("sec_data", {}),
        "earnings_data": state.get("earnings_data", {})
    })
    return {"bear_case": [response.content]}
