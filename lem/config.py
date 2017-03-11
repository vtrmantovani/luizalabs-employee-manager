import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    LOGS_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGS_LEVEL = logging.DEBUG
    SECRET_KEY = 'b21032d50cbf2bbfe56a'


class StagingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass
