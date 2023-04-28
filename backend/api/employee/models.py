from api.core import Mixin
from ..db import db


class Employee(Mixin, db.Model):
    """Employee Table"""

    __tablename__ = "employee"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    first_name = db.Column(db.String, nullable=False, default='')
    surname = db.Column(db.String, nullable=False, default='')
    other_names = db.Column(db.String, nullable=False, default='')
    login = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)

    def __init__(self, email, password, name):
        if name:
            res = name.split(' ')
            self.first_name = '' if len(res) == 1 else res[0]
            self.surname = res[0] if len(res) == 1 else ' '.join(res[1:])
        self.surname = None
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<Employee {self.first_name} {self.surname}>"
