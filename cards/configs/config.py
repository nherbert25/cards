import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# running application locally
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'development_database.db')


# running test suite (clean database, etc.)
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'test_database.db')


# running production application
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../instance', 'production_database.db')

# running AWS RDS Postgres DB
class AWSPostgresConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # ex: postgres://user:password@host:5432/db or f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    # app.config['SQLALCHEMY_DATABASE_URI'] =

