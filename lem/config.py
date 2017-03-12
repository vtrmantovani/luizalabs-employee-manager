import logging
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    LOGS_LEVEL = logging.INFO
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_SIZE = 40
    SQLALCHEMY_POOL_RECYCLE = 100


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOGS_LEVEL = logging.DEBUG
    SECRET_KEY = 'b21032d50cbf2bbfe56a'

    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/employee-manager'


class StagingConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass
