import json

import flask
from flask import Blueprint, request, redirect, url_for

from lem import db
from lem.forms import EmployeeForm
from lem.models import Employee
from utils.decorators import requires_json

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/', methods=['GET'])
def index():
    return flask.render_template('employee/list.html')


@employee.route('/create', methods=['GET', 'POST'])
def create():
    employeeForm = EmployeeForm()
    if request.method == 'POST':
        if employeeForm.validate_on_submit():
            employee = Employee()
            employee.name = employeeForm.data['name']
            employee.email = employeeForm.data['email']
            employee.department = employeeForm.data['department']
            db.session.add(employee)
            try:
                db.session.commit()
                flask.flash('Empregado cadastrado com sucesso', 'success')
                return redirect(url_for('employee.index'))
            except Exception as e:
                db.session.rollback()
                flask.flash('Erro ao criar empregado', 'error')

    return flask.render_template('employee/create.html', form=employeeForm)


@employee.route('/edit', methods=['GET', 'POST'])
@employee.route('/edit/<employee_id>',  methods=['GET'])
def edit(employee_id=None):
    employeeForm = EmployeeForm()
    if not employee_id:
        employee_id = request.args.get('id')
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    if request.method == 'POST':
        if employeeForm.validate_on_submit():
            employee.name = employeeForm.data['name']
            employee.email = employeeForm.data['email']
            employee.department = employeeForm.data['department']
            db.session.add(employee)
            try:
                db.session.commit()
                flask.flash('Empregado atualizado com sucesso', 'success')
                return redirect(url_for('employee.index'))
            except Exception as e:
                db.session.rollback()
                flask.flash('Erro ao atualizar empregado', 'error')

    employeeForm.name.data = employee.name
    employeeForm.email.data = employee.email
    employeeForm.department.data = employee.department
    return flask.render_template('employee/edit.html', employee=employee, form=employeeForm)


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
