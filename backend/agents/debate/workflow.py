from langgraph.graph import StateGraph, END
from backend.agents.debate.state import DebateState
from backend.agents.debate.bull import run_bull_analyst
from backend.agents.debate.bear import run_bear_analyst
from backend.agents.debate.risk import run_risk_analyst
from backend.agents.debate.valuation import run_valuation_analyst
from backend.agents.debate.committee import run_committee, should_reflect

def build_debate_workflow():
    workflow = StateGraph(DebateState)

    # Add Nodes
    workflow.add_node("bull", run_bull_analyst)
    workflow.add_node("bear", run_bear_analyst)
    workflow.add_node("risk", run_risk_analyst)
    workflow.add_node("val", run_valuation_analyst)
    workflow.add_node("committee", run_committee)

    # Add Edges (Parallel execution from Start)
    workflow.set_entry_point("bull") # In a real scatter-gather, we use conditional edges or a fan-out node
    
    # Simple sequential for testing, but logically we can parallelize via fan-out
    # To truly parallelize in LangGraph, we attach all to a start node that routes to all
    
    # For simplicity in this implementation, we will route them sequentially to gather state,
    # OR we use a fan-out.
    # Let's use a dummy node to fan out.
    workflow.add_node("start_debate", lambda x: x)
    workflow.set_entry_point("start_debate")
    
    workflow.add_edge("start_debate", "bull")
    workflow.add_edge("start_debate", "bear")
    workflow.add_edge("start_debate", "risk")
    workflow.add_edge("start_debate", "val")
    
    # All converge to committee
    workflow.add_edge("bull", "committee")
    workflow.add_edge("bear", "committee")
    workflow.add_edge("risk", "committee")
    workflow.add_edge("val", "committee")

    # Conditional routing based on reflection
    workflow.add_conditional_edges(
        "committee",
        should_reflect,
        {
            "reflect": "start_debate", # Send back for another round with committee feedback
            "end": END
        }
    )

    return workflow.compile()
