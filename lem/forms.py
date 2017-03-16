from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', validators=[validators.DataRequired(), validators.Length(min=6)])


class EmployeeForm(FlaskForm):
    name = StringField('Nome', validators=[validators.DataRequired()])
    email = StringField('E-mail', validators=[validators.DataRequired(), validators.Email()])
    department = StringField('Departamento', validators=[validators.DataRequired()])
