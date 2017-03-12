from flask import Blueprint, jsonify, request

from lem.models import Employee


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return jsonify({"service": "Luizalabs Employee Manager",
                    "version": "1.0"})


@api.route('/employee', methods=['GET'])
def get_employee_list():
    employees = Employee.query.all()
    return jsonify(employees=[i.serialize for i in employees])
