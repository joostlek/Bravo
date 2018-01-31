import os


class Config(object):
    DEBUG = False
    TESTING = False
    THREADS_PER_PAGE = 2
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = 'secret'
    DATABASE_CONNECT_OPTIONS = {}


class LocalConfig(Config):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')


class RemoteConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:project@192.168.42.10:5432/postgres'


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:project@192.168.42.10:5432/postgres'

