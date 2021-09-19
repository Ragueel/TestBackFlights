from src.config import BaseConfig
from src.tasks import *
from src.celery import celery_controller
from src.db import get_session_maker
from src.app import create_file

if __name__=='__main__':
    create_file(BaseConfig().TEST_DB_PATH)
    app = celery_controller.make_celery_app(BaseConfig(), get_session_maker(BaseConfig))
    collect_flights.delay()
    app.worker_main(argv=['worker', '-B', '--loglevel=info'])
