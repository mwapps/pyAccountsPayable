import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from flasgger import Swagger, swag_from
from src.constants.swagger import template, swagger_config

from .controllers.accounts_payable import accounts_payable_api
from .controllers.auth import auth
from .controllers.companies import companies_api
from .controllers.rules import rules_api
from .controllers.suppliers import suppliers_api
from .controllers.reports import report_api

def create_app(settings_module):
    app = Flask(__name__, instance_relative_config=True)
    # Load the config file specified by the APP environment variable
    app.config.from_object(settings_module)
    # Load the configuration from the instance folder
    if app.config.get('TESTING', False):
        app.config.from_pyfile('config-testing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)

    configure_logging(app)
    JWTManager(app)

    app.register_blueprint(accounts_payable_api)
    app.register_blueprint(auth)
    app.register_blueprint(companies_api)
    app.register_blueprint(rules_api)
    app.register_blueprint(suppliers_api)
    app.register_blueprint(report_api)

    db = SQLAlchemy()
    db.app = app
    db.init_app(app)

    Swagger(app, config=swagger_config, template=template)
    
    return app

def configure_logging(app):
    """
    Configura el módulo de logs. Establece los manejadores para cada logger.
    :param app: Instancia de la aplicación Flask
    """

    # Elimina los manejadores por defecto de la app
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    fileHandler = logging.FileHandler(app.config['APP_LOG_FILE_LOCATION'])
    fileHandler.setFormatter(verbose_formatter())
    fileHandler.setLevel(logging.DEBUG)
    handlers.append(fileHandler)

    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        mail_handler = SMTPHandler((app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                                   app.config['DONT_REPLY_FROM_EMAIL'],
                                   app.config['ADMINS'],
                                   '[Error][{}] La aplicación falló'.format(app.config['APP_ENV']),
                                   (app.config['MAIL_USERNAME'],
                                    app.config['MAIL_PASSWORD']),
                                   ())
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )


def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

