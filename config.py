import os


class Config(object):
    FLASK_ENV = "development"
    DEBUG = False
    TESTING = False
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = 27017
    DB_NAME = os.getenv("DB_NAME")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DB_NAME = os.getenv("TEST_DB_NAME")
