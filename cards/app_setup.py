from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_bcrypt import Bcrypt
import os
from cards.configs.config import DevelopmentConfig, TestingConfig, ProductionConfig, AWSPostgresConfig

socketio = SocketIO(ping_interval=50, ping_timeout=50)


# create app pattern:  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config["DEBUG"] = True  # comment out for pycharm debug mode (ironic, isn't it?)
    app.config["SECRET_KEY"] = 'anA194$38@na.dn0832A'
    app.config['SESSION_TYPE'] = 'sqlalchemy'

    # Load configuration based on environment
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    elif env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'aws-postgres':
        app.config.from_object(AWSPostgresConfig)

    # Load database configurations
    from cards.database.models import db
    db.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db

    # Load Session configurations
    sess = Session()
    sess.init_app(app)

    # Load bcrypt configurations
    bcrypt = Bcrypt()
    bcrypt.init_app(app)

    # Not sure how app_context works
    with app.app_context():
        db.create_all()

    # Load blueprints, these must be imported here to avoid circular imports. See Flask documentation
    from cards.blackjack.routes import blackjack_blueprint
    app.register_blueprint(blackjack_blueprint)

    socketio.init_app(app)
    return app, db, sess, bcrypt
