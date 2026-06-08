from celery import Celery

from backend.core.config import settings

celery_app = Celery(
    "equity_research",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)

# Optional: Auto-discover tasks in specific modules
celery_app.autodiscover_tasks(["backend.agents"])
