import os


class Config:
    """
    Base Configuration
    """

    APP_NAME = 'Backend Bundle App'
    FRONT_END_DOMAIN = 'http://localhost:4200'
    SECRET_KEY = "testkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "api.log"  
    JWT_SECRET_KEY = "super-secr3t"
    API_ROOT = "/api"
    PASSWORD_RECOVERY_SECRET = u"password recovery secret here"
    PASSWORD_RECOVERY_TTL = 86400
    NO_AUTH_ENDPOINTS = ['auth.signin', 'auth.sign_up', 'auth.reset_pass', 'auth.request_pass']

    SMTP_SETTINGS = {
        'DEBUG': True,
        'HOST': 'smtp.dreamhost.com',
        'PORT': 587,
        'PASSWORD': 'top_secr3t',
        'FROM': 'noreply@email.com'
    }


class DevelopmentConfig(Config):
    db_path = os.path.join(os.path.dirname(__file__), 'bundle.db')
    url = (
            "sqlite:///%s" % db_path
    )  
    SQLALCHEMY_DATABASE_URI = url
    DEBUG = True
    
config = {"dev": DevelopmentConfig}
