import celery 
from .config import BaseConfig

celery_app = celery.Celery('celery',broker=BaseConfig)