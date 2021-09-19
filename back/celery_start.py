from src.config import BaseConfig
from src.celery import celery_controller
from src.db import get_session_maker
if __name__=='__main__':
    app = celery_controller.make_celery_app(BaseConfig(), get_session_maker(BaseConfig))

    app.worker_main(argv=['worker', '-B', '--loglevel=info'])
