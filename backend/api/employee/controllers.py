from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields

from flask_jwt_extended import get_jwt_identity

from .services import get_employee_by_id, update_employee
from api.core import validate_json_body

bp = Blueprint('employee', __name__, url_prefix='/employees')


@bp.route('/current', methods=['GET'])
def get_employee():
    employee_id = get_jwt_identity()
    employee = get_employee_by_id(employee_id)
    return jsonify(__serialize_employee(employee))


class UpdateEmployeeSchema(Schema):
    firstName = fields.String(required=True, allow_none=True)
    surname = fields.String(required=True, allow_none=True)


@bp.route('/current', methods=['PUT'])
@validate_json_body(UpdateEmployeeSchema)
def update_current_employee():
    employee_id = get_jwt_identity()
    data = request.get_json()

    employee = get_employee_by_id(employee_id)

    employee.first_name = data['firstName']
    employee.surname = data['surname']
    employee.login = data['userName']
    employee.country = data['country']

    update_employee(employee)

    return jsonify(__serialize_employee(employee))


def __serialize_employee(employee):
    return {
        'id': employee.id,
        'email': employee.email,
        'firstName': employee.first_name,
        'surname': employee.last_name,
        'userName': employee.login,
        'country': employee.country
    }
