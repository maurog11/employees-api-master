from .auth.controllers import bp as auth_bp
from .employee.controllers import bp as employee_bp


def register_blueprints(app):
    for bp in [auth_bp, employee_bp]:
        if app.config['API_ROOT']:
            bp.url_prefix = app.config['API_ROOT'] + bp.url_prefix
        app.register_blueprint(bp)
