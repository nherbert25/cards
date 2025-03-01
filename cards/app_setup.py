from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from flask_bcrypt import Bcrypt
import os
from cards.database.models import db
from cards.configs.config import DevelopmentConfig, TestingConfig, ProductionConfig


# Initialize extensions
bcrypt = Bcrypt()
sess = Session()
socketio = SocketIO(ping_interval=50, ping_timeout=50)


# create app pattern:  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
def create_app():
    """Create an application."""
    app = Flask(__name__)

    # Load configuration based on environment
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Load database configurations
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Load Session configurations
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    sess.init_app(app)

    # Load bcrypt configurations
    bcrypt.init_app(app)


    socketio.init_app(app)

    # Load blueprints, these must be imported here to avoid circular imports. See Flask documentation
    from cards.blackjack.routes import blackjack_blueprint
    app.register_blueprint(blackjack_blueprint)

    return app, db, sess, bcrypt
