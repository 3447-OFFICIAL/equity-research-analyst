from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from backend.app.routes import api_router
from backend.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Equity Research Analyst API",
        version="0.1.0",
        description="Research automation API for filings, transcripts, RAG, valuation, and recommendations.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router)

    @app.websocket("/ws/reports/stream/{task_id}")
    async def websocket_endpoint(websocket: WebSocket, task_id: str):
        await websocket.accept()
        try:
            # Simulate streaming updates from Celery worker / LangGraph
            # In production, subscribe to Redis Pub/Sub for task updates
            stages = ["SEC Filing Agent", "Earnings Call Agent", "Valuation Agent", "Supervisor Agent"]
            for i, stage in enumerate(stages):
                await asyncio.sleep(1) # mock processing delay
                await websocket.send_json({
                    "task_id": task_id,
                    "status": "processing",
                    "current_agent": stage,
                    "progress": int(((i+1)/len(stages)) * 100)
                })
            await websocket.send_json({"task_id": task_id, "status": "completed", "progress": 100})
        except WebSocketDisconnect:
            pass

    return app

app = create_app()
