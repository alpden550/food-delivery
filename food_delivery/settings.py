import os


class Config:
    DEBUG = os.getenv('DEBUG') in {'1', 'yes', 'true', 'True'}
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
