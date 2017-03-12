from functools import wraps

from flask import request

from werkzeug.exceptions import UnsupportedMediaType
from utils.api_exceptions import (
    BadRequestInvalidParam,
    BadRequestInvalidParamValue,
    BadRequestMissingParams
)


def requires_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.mimetype not in ('application/json',):
            raise UnsupportedMediaType(
                "You must send a raw body in JSON format with the Content-Type"
                " header properly set to application/json.")

        return f(*args, **kwargs)

    return decorated


def requires_fields_validation(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyError as e:
            raise BadRequestMissingParams(e.message)
        except ValueError as e:
            raise BadRequestInvalidParamValue(e.message)
        except AttributeError as e:
            raise BadRequestInvalidParam(e.message)
    return decorated
