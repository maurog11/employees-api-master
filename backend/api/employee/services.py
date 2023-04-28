import flask_bcrypt

from .models import Employee
from ..db import db


def get_employee_by_id(id):
    if not id:
        raise Exception('No email provided.')
    return Employee.query.filter_by(id=id).first()


def check_employee_exists(email):
    return True if get_employee_by_id(email) else False


def generate_password_hash(password):
    return flask_bcrypt.generate_password_hash(password, 10)


def check_password(employee, password):
    return flask_bcrypt.check_password_hash(employee.password, password) if employee else False


def create_employee(email, password, fullname):
    u = Employee(email, generate_password_hash(password), fullname)
    db.session.add(u)
    db.session.commit()


def update_employee_password(employee, new_password):
    employee.password = generate_password_hash(new_password)
    update_employee(employee)


def update_employee(employee):
    db.session.merge(employee)
    db.session.commit()
