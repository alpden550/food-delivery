import os


class BaseConfig:
    DEBUG = os.getenv('DEBUG') in {'1', 'yes', 'true', 'True'}
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(BaseConfig):
    TESTING = True
    SECRET_KEY = 'extrasecretstring'  # noqa:S105
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


config = {
    'testing': TestingConfig,
    'production': ProductionConfig,
}
