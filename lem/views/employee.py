import flask
from flask import Blueprint, jsonify, request

employee = Blueprint('employee', __name__, url_prefix='/employee')


@employee.route('/', methods=['GET'])
def index():
    return flask.render_template('employee/list.html')
