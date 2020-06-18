import os
import logging
import logging.config
import yaml

from flask import Flask
from flask_cors import CORS
from healthcheck import HealthCheck
from dynaconf import FlaskDynaconf, settings


from .blueprint import ConfigBluePrint
from .exception_handler import ConfigErrorHandler


class Server:

    def config(self):
        return self.__config_Flask()

    def __config_Flask(self):
        app = Flask(__name__)
        url = os.getenv('DATABASE_URL')
        if url:
            app.config['SQLALCHEMY_DATABASE_URI'] = url
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = (
                'postgresql+psycopg2://raven_adm:'
                'raven_adm@localhost:5405/db_raven')
        self.__config_enviroments(app, settings.LOG_CONFIG_PATH)
        self.__config_health(app, settings.HEALTH_PATH)
        self.__config_cors(app)

        ConfigBluePrint().config(app)
        ConfigErrorHandler().config(app)

        return app

    def __config_enviroments(self, app, config_file_path):
        FlaskDynaconf(app)
        settings.from_env(os.getenv('FLASK_ENV', 'default'))

        logging.basicConfig(level=settings.LOG_LEVEL)

        with open(config_file_path, 'rt') as config_file:
            config = yaml.safe_load(config_file.read())
            logging.config.dictConfig(config)

    def __config_health(self, app, config_file_path):
        HealthCheck(app, config_file_path)

    def __config_cors(self, app):
        CORS(app, resources={r"/*": {"origins": "*"}})
