"""Celery tasks - import here so Celery discovers them."""

from app.workers.celery_app import celery_app


@celery_app.task
def ping() -> str:
    """Example task for worker health checks."""
    return "pong"
