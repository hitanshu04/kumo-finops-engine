"""Health and readiness endpoints under API v1."""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("")
async def api_health() -> dict:
    """API-level health check."""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "v1",
    }
