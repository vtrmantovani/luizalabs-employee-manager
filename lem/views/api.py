from flask import Blueprint, jsonify, request

from lem.models import Employee


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    return jsonify({"service": "Luizalabs Employee Manager",
                    "version": "1.0"})

