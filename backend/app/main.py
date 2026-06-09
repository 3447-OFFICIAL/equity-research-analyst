from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter

from backend.app.routes import api_router
from backend.core.config import settings
from backend.core.logger import setup_logging, get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Starting up API...")
    redis_conn = redis.from_url(settings.celery_broker_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_conn)
    yield
    await redis_conn.aclose()

def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Equity Research Analyst API",
        version="0.1.0",
        description="Research automation API for filings, transcripts, RAG, valuation, and recommendations.",
        lifespan=lifespan
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
    async def websocket_endpoint(websocket: WebSocket, task_id: str, token: str):
        import jwt
        from backend.core.security import ALGORITHM
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
            if not payload.get("sub"):
                await websocket.close(code=1008)
                return
        except Exception:
            await websocket.close(code=1008)
            return

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
