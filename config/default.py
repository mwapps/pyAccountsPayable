from os.path import abspath, dirname
from datetime import timedelta

# Define the application directory
BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = 'modificar aquí'
JWT_SECRET_KEY = 'modificar aquí'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

# Database configuration
SQLALCHEMY_TRACK_MODIFICATIONS = False

# App environments
APP_ENV_LOCAL = 'local'
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV_STAGING = 'staging'
APP_ENV_PRODUCTION = 'production'
APP_ENV = ''
APP_LOG_FILE_LOCATION = "aplication.log"

# Configuración del email
MAIL_SERVER = 'tu servidor smtp'
MAIL_PORT = 587
MAIL_USERNAME = 'tu correo'
MAIL_PASSWORD = 'tu contraseña'
DONT_REPLY_FROM_EMAIL = 'dirección from'
ADMINS = ('manriquewebapps@gmail.com', )
MAIL_USE_TLS = True
MAIL_DEBUG = False
