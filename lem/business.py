from datetime import datetime

from flask_login import current_user
from flask_principal import identity_loaded, Permission, RoleNeed, UserNeed

from lem import db
from lem.models import User


class UserDisabledException(Exception):
    pass


def auth_user(email, password) -> User:
    user = User.query.filter_by(email=email).first()
    if user and not user.enabled:
        raise UserDisabledException()
    if not user or not user.check_password(password):
        return False

    user.last_login_dt = datetime.utcnow()
    db.session.commit()

    return user


def create_user(email, password):
    user = User(email=email, password=password)
    user.enabled = True

    db.session.add(user)
    db.session.commit()


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
