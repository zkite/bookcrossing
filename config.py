import os

from sqlalchemy import create_engine

root_path = os.path.abspath(os.path.dirname(__file__))
template_folder = os.path.join(root_path, 'bookcrossing/templates')
static_folder = os.path.join(root_path, 'bookcrossing/static')


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = "postgresql://dima:dima@localhost/bookcrossing"
    DATABASE_URL = "postgresql://localhost/bookcrossing"

    @staticmethod
    def create_psql_engine():
        engine = create_engine('postgresql://localhost/bookcrossing')
        return engine


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
