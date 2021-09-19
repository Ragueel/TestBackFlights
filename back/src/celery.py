from re import M
from .config import BaseConfig
from celery.schedules import crontab

import celery 

class CeleryController:

    def __init__(self) -> None:
        self.session_maker = None
        self.app = None

    def make_celery_app(self, config: BaseConfig, session_maker)->celery.Celery:

        self.session_maker = session_maker
        self.app = celery.Celery('celery',broker=config.CELERY_BROKER, backend=config.CELERY_BACKEND)
        self.app.conf.task_serializer = 'json'

        self.app.conf.beat_schedule={
            'collect_flights':{
                'task': 'collect_flights',
                'schedule': crontab(hour='23', minute=59),
                # 'args':(0)
            }
        }
        return self.app


celery_controller = CeleryController()