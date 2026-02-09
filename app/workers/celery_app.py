"""Celery application configuration."""

from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "kumo",
    broker=settings.celery_broker,
    backend=settings.celery_result,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
