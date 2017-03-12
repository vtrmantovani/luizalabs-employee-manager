import datetime
import re

from flask import current_app as app
from sqlalchemy.orm import validates

from lem import db, login_manager

rx_email = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


class User(db.Model):
    __tablename__ = 'user'

    DATA_GROUPS = 'groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, index=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    last_login_dt = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, nullable=False)
    created_dt = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_dt = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow, nullable=True)

    def __init__(self, *args, **kwargs):
        self.email = kwargs['email'] if 'email' in kwargs else None
        self.password = kwargs['password'] if 'password' in kwargs else None

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError('Email is required')
        if not rx_email.match(value):
            raise ValueError('Email is invalid')
        return value

    @validates('password')
    def validate_password(self, key, value):
        if value:
            return app.argon2.generate_password_hash(value)
        raise ValueError('Email is required')

    def check_password(self, password):
        return app.argon2.check_password_hash(self.password, password)

    # Flask-Login integration
    def is_authenticated(self):
        return self.id is not None

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.id is None

    def get_id(self):
        return self.id

    def reload(self):
        User.query.get(self.id)

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)