from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)])
