import os

from src import create_app

settings_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(settings_module)
