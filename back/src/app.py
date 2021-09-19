from src.services.flight_services.flights_service import FlightsService
from src.services.flight_services.flight_get import FlightGetSerivce
from src.services.flight_services.flight_validator import FlightValidatorService
from src.repository.flights_repository import FlightsRepository
import falcon.asgi
from .config import BaseConfig
from .resources.health import HealthResource
from .db import get_session_maker
from .models.all_models import create_all
from .celery import celery_controller
from .middleware.session_manager_middleware import SQLAlchemySessionManager
from .resources.flights_resource import FlightsResource
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
        flights_service = FlightsService(FlightGetSerivce(), FlightValidatorService(), FlightsRepository())
        app.add_route('/api/v1/flights', FlightsResource(flights_service))

    def migrate_db(self, session):
        create_all(session.get_bind())

    def prepare_db(self, config):
        create_file(config.TEST_DB_PATH)


    def create_app(self, config=None) -> falcon.asgi.App:

        self.config = config
        
        self.falcon_app = falcon.asgi.App()

        self.prepare_db(config)

        self.session_maker = get_session_maker(self.config)
        self.falcon_app.add_middleware(SQLAlchemySessionManager(self.session_maker))
        
        self.migrate_db(self.session_maker())


        self.celery.make_celery_app(config, self.session_maker)

        self.register_resources(self.falcon_app)

        return self.falcon_app

backend_app = BackendApp()