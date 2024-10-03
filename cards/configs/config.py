import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# running application locally
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'development_database.db')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'development_database.db')

import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '..', 'instance', 'development_database.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(db_path)


# running test suite (clean database, etc.)
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'test_database.db')


# running production application
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'production_database.db')
