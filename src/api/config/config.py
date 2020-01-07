class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flask_api:flask_api_test@localhost:3306/landing"
    SECRET_KEY = "MY_SECRET_KEY"
    SECURITY_PASSWORD_SALT = "MY_SECURITY_PASSWORD_SALT_FOR_PRODUCTION"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flask_api:flask_api_test@localhost:3306/landing"
    SECRET_KEY = "MY_SECRET_KEY"
    SECURITY_PASSWORD_SALT = "MY_SECURITY_PASSWORD_SALT_FOR_DEVELOPMENT"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://flask_api:flask_api_test@localhost:3306/landing"
    SECRET_KEY = "MY_SECRET_KEY"
    SECURITY_PASSWORD_SALT = "MY_SECURITY_PASSWORD_SALT_FOR_TESTING"
