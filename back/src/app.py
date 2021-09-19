import falcon.asgi
from .config import BaseConfig
from .resources.health import HealthResource
from .db import get_session_maker
from .models.all_models import create_all
from .celery import celery_controller
from .middleware.session_manager_middleware import SQLAlchemySessionManager
import os

def create_file(file_path):
    if not os.path.exists(file_path):
        f = open(file_path, 'w+')
        f.close()
    else:
        print('file exists')


class BackendApp:

    def __init__(self) -> None:
        self.config = None
        self.falcon_app = None
        self.session_maker = None
        self.celery = celery_controller

    def register_resources(self, app: falcon.asgi.App)-> None:
        app.add_route('/health', HealthResource())

    def migrate_db(self, session):
        create_all(session.get_bind())

    def prepare_db(self):
        db_path = './test.sqlite'
        create_file(db_path)


    def create_app(self, config=None) -> falcon.asgi.App:

        self.config = config
        
        self.falcon_app = falcon.asgi.App()

        self.prepare_db()

        self.session_maker = get_session_maker(self.config)
        
        self.migrate_db(self.session_maker())

        self.falcon_app.add_middleware(SQLAlchemySessionManager(self.session_maker))

        self.celery.make_celery_app(config, self.session_maker)

        self.register_resources(self.falcon_app)

        return self.falcon_app

backend_app = BackendApp()