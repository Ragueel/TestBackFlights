from re import M
from .config import BaseConfig
from celery.schedules import crontab
import celery 
from celery._state import _set_current_app
from .tasks import *
from .services.flight_services.flights_service import find_cheapest_flight_schedule
celery_app = celery.Celery('celery',broker=BaseConfig.CELERY_BROKER, backend=BaseConfig.CELERY_BACKEND)
celery_app.conf.task_serializer = 'json'
# celery_app.autodiscover_tasks(force=True)
# celery_app.conf.update(result_expires=3600,enable_utc=True)
collect_flights.delay()
celery_app.conf.beat_schedule={
    'collect_flights':{
        'task': 'collect_flights',
        'schedule': 500,
        # 'args':(0)
    }
}