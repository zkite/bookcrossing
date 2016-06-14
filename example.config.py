import os

from sqlalchemy import create_engine

root_path = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(root_path, 'bookcrossing/templates')
static_folder = os.path.join(root_path, 'bookcrossing/static')


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_LOG_LEVEL = 'DEBUG'

    # EMAIL SETTINGS
    MAIL_SERVER = 'smtp.yandex.ua'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class ProductionConfig(Config):
    DEBUG = False

    #  TODO set up DB
    #  http://killtheyak.com/use-postgresql-with-django-flask/
    #  http://eax.me/postgresql-install/  --> just look how to create db, user
    SQLALCHEMY_DATABASE_URI = "postgresql://{{test_user}}:{{password}}@localhost/{{test_database}}"
    DATABASE_URL = "postgresql://localhost/{{test_database}}"

    @staticmethod
    def create_psql_engine():
        engine = create_engine('postgresql://localhost/{{test_database}}')
        return engine


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
