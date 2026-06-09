from fastapi import APIRouter

from backend.app.v1 import companies, filings, health, reports, auth

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(companies.router, prefix="/company", tags=["companies"])
api_router.include_router(filings.router, prefix="/filings", tags=["filings"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
