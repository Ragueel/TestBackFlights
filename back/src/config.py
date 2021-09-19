import os
import pathlib
import uuid


class BaseConfig:
    DEFAULT_CONFIG_PATH = '/tmp/asgilook'
    DEFAULT_UUID_GENERATOR = uuid.uuid4
    CELERY_BROKER='redis'
    CELERY_BACKEND='redis'
    SKY_API_PARTNER=os.environ.get('SKY_API_PARTNER', 'ragueelnomad')


    def __init__(self):
        self.storage_path = pathlib.Path(
            os.environ.get('ASGI_LOOK_STORAGE_PATH', self.DEFAULT_CONFIG_PATH))
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.uuid_generator = BaseConfig.DEFAULT_UUID_GENERATOR