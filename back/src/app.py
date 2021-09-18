import falcon.asgi
from .config import BaseConfig
from .resources.health import HealthResource

def register_resources(app: falcon.asgi.App)-> None:
    app.add_route('/health', HealthResource())

def create_app(config=None) -> falcon.asgi.App:
    config = config or BaseConfig()
    app = falcon.asgi.App()

    register_resources(app)

    return app

