from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Conflict

from lem import db
from lem.models import Employee
from utils.decorators import requires_json, requires_fields_validation

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return jsonify({"service": "Luizalabs Employee Manager",
                    "version": "1.0"})


@api.route('/employee', methods=['GET'])
def get_employee_list():
    employees = Employee.query.all()
    return jsonify(employees=[i.serialize for i in employees])


@requires_fields_validation
@requires_json
@api.route('/employee', methods=['POST'])
def post_employee():
    r = request.json
    employee = Employee()
    employee.name = r['name']
    employee.email = r['email']
    employee.department = r['department']

    db.session.add(employee)

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        raise Conflict("Integrity error: {0}".format(str(e)))

    return jsonify(employee.serialize)


@api.route('/employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    employee = Employee.query.filter_by(id=employee_id).first_or_404()
    db.session.delete(employee)
    db.session.commit()
    return ''
