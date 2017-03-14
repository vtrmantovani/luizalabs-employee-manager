import json

import flask
from flask import Blueprint, request

from lem import db
from lem.forms import NewEmployee
from lem.models import Employee
from utils.decorators import requires_json

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


@requires_json
@employee.route('/remove', methods=['POST'])
def remove():
    data = json.loads(request.data.decode('utf-8'))
    employee = Employee.query.filter_by(id=data['employee_id']).first_or_404()
    db.session.delete(employee)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return '', 400

    return ''
