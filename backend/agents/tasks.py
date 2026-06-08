from backend.core.celery_app import celery_app
from backend.agents.workflow import build_research_workflow

@celery_app.task(name="generate_research_report")
def generate_research_report_task(ticker: str):
    workflow = build_research_workflow()
    initial_state = {"ticker": ticker}
    
    # Run the graph synchronously within the celery worker
    final_state = workflow.invoke(initial_state)
    
    return {
        "ticker": ticker,
        "recommendation": final_state.get("recommendation", "HOLD"),
        "confidence_score": final_state.get("confidence_score", 0.0),
        "status": "COMPLETED"
    }
