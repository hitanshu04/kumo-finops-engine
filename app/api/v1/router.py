"""API v1 router - aggregate all v1 route modules."""

from fastapi import APIRouter

from app.api.v1.routes import health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
