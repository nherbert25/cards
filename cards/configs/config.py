import os

basedir = os.path.abspath(os.path.dirname(__file__))

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '..', 'instance', 'development_database.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(db_path)


class Config:
    SECRET_KEY = 'your_secret_key_here'
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# running application locally
class DevelopmentConfig(Config):
    """Per official flask documentation:
    The DEBUG config value is special because it may behave inconsistently
        if changed after the app has begun setting up.
    In order to set debug mode reliably, use the --debug option on the flask or flask run command
    Aka: enable DEBUG in Pycharm's run/debug config or envoke it on the run command: 'flask --app hello run --debug'
    """
    # DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'development_database.db')


# running test suite (clean database, etc.)
class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# running production application
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'production_database.db')
