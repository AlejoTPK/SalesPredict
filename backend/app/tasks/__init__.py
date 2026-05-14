from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "salespredict",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer=settings.celery_task_serializer,
    result_serializer=settings.celery_result_serializer,
    accept_content=settings.celery_accept_content,
    timezone=settings.celery_timezone,
    enable_utc=settings.celery_enable_utc,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

celery_app.autodiscover_tasks(
    ["app.tasks.etl_tasks", "app.tasks.training_tasks", "app.tasks.prediction_tasks"]
)
