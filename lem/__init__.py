import logging
import os
import sys

from flask import Flask
from flask_argon2 import Argon2
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_principal import Principal
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound

db = SQLAlchemy(session_options={'autoflush': False})

logger = logging.getLogger(__name__)

bootstrap = Bootstrap()

login_manager = LoginManager()

migrate = Migrate()


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')):
    app = Flask(__name__)
    app.config.from_object('lem.config.%sConfig' % config_var)
    app.config['DEPLOY_ENV'] = config_var

    configure_logger(app)

    app.argon2 = Argon2(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)
    setup_login_manager()

    Principal(app)

    db.init_app(app)

    _module_dir = os.path.dirname(os.path.abspath(__file__))
    migrate.init_app(app, db, directory=os.path.join(_module_dir, '..', 'migrations'))

    register_blueprints_and_error_handling(app)

    return app


def configure_logger(app):
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(app.config['LOGS_LEVEL'])
        logger.addHandler(ch)


def register_blueprints_and_error_handling(app):
    from lem.views.common import common, forbidden, internal_server_error, not_found
    app.register_blueprint(common)

    app.register_error_handler(Forbidden.code, forbidden)
    app.register_error_handler(InternalServerError.code, internal_server_error)
    app.register_error_handler(NotFound.code, not_found)


def setup_login_manager():
    from lem.models import User
    login_manager.user_callback = User.load_user
    login_manager.login_view = 'common.login'
    login_manager.login_message = 'Efetue o login para continuar'
    login_manager.login_message_category = 'warning'