import configparser
import logging
import marshmallow
from typing import Tuple, List
from functools import wraps

from werkzeug.local import LocalProxy
from flask import current_app, jsonify, request
from flask.wrappers import Response
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt import PyJWTError

logger = LocalProxy(lambda: current_app.logger)
core_logger = logging.getLogger("core")


class Mixin:

    def to_dict(self) -> dict:
        d_out = dict((key, val) for key, val in self.__dict__.items())
        d_out.pop("_sa_instance_state", None)
        d_out["_id"] = d_out.pop("id", None)  
        return d_out


def init_jtw_security(app):
    @app.before_request
    def before_request():
        if request.endpoint and request.endpoint not in app.config['NO_AUTH_ENDPOINTS']:
            try:
                verify_jwt_in_request()
            except JWTExtendedException as e:
                return create_response(message='Not authorized', status=401)
            except PyJWTError as e:
                return create_response(message='Not authorized', status=401)


def create_response(
        data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary")

    response = {"success": 200 <= status < 300, "message": message, "result": data}
    return jsonify(response), status


def serialize_list(items: List) -> List:
    if not items or items is None:
        return []
    return [x.to_dict() for x in items]


def all_exception_handler(error: Exception) -> Tuple[Response, int]:
    if isinstance(error, marshmallow.ValidationError):
        return create_response(message='Validation error', data=error.messages, status=400)
    if isinstance(error, HTTPException):
        return create_response(message=error.description, status=error.code)
    else:
        core_logger.error(error)
        return create_response(message=str(error), status=500)


def validate_json_body(schema, unknown=marshmallow.INCLUDE, partial=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = request.get_json()
            schema().load(data, unknown=unknown, partial=partial)

            return f(*args, **kwargs)

        return wrapped

    return decorator
