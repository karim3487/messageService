import celery
from src import config_reader as cfg

celery_service = celery.Celery("mailing tasks", broker=cfg.BROKER, backend=cfg.BACKEND)
