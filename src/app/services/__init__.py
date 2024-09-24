import celery
from src import config_reader as cfg

celery_service = celery.Celery("mailing tasks", broker=cfg.BROKER, backend=cfg.BACKEND)

celery_service.conf.update(
    broker_connection_retry_on_startup=True,
    result_backend="rpc://",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
