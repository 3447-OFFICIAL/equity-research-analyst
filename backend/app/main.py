from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return app


app = create_app()
