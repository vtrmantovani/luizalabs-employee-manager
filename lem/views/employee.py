import flask
from flask import Blueprint

from lem import db
from lem.forms import NewEmployee
from lem.models import Employee

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/', methods=['GET'])
def index():
    return flask.render_template('employee/list.html')


@employee.route('/create', methods=['GET', 'POST'])
def create():
    formNewEmployee = NewEmployee()
    if formNewEmployee.validate_on_submit():
        employee = Employee()
        employee.name = formNewEmployee.data['name']
        employee.email = formNewEmployee.data['email']
        employee.department = formNewEmployee.data['department']

        db.session.add(employee)
        try:
            db.session.commit()
            flask.flash('Empregado cadastrado com sucesso', 'success')
            return flask.render_template('employee/list.html')
        except Exception as e:
            db.session.rollback()
            flask.flash('Erro ao criar empregado', 'error')

    return flask.render_template('employee/create.html', form=formNewEmployee)
