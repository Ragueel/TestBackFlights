from src.app import backend_app
from src.config import BaseConfig
app = backend_app.create_app(BaseConfig())
    