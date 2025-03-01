from flask import Flask
from flask_socketio import SocketIO
from flask_session import Session
from flask_bcrypt import Bcrypt
import os
from cards.database.models import db
from cards.configs.config import DevelopmentConfig, TestingConfig, ProductionConfig

# Initialize extensions
bcrypt = Bcrypt()
session = Session()
socketio = SocketIO(ping_interval=50, ping_timeout=50)


# Application factory pattern:  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
def create_app() -> Flask:
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

    initialize_db(app)
    initialize_session(app, db)
    initialize_bcrypt(app)
    initialize_socketio(app)

    # Blueprints must be imported here to avoid circular imports. See Flask documentation
    from cards.blackjack.routes import blackjack_blueprint
    from cards.landing_page_blueprint import landing_page_blueprint
    app.register_blueprint(blackjack_blueprint)
    app.register_blueprint(landing_page_blueprint)

    return app


def initialize_db(app):
    """Initialize Database."""
    db.init_app(app)
    with app.app_context():
        db.create_all()


def initialize_session(app, session_db):
    """Initialize Session."""
    # Load Session configurations
    app.config['SESSION_SQLALCHEMY'] = session_db
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    session.init_app(app)


def initialize_bcrypt(app):
    """Initialize Bcrypt."""
    bcrypt.init_app(app)


def initialize_socketio(app):
    """Initialize SocketIO."""
    socketio.init_app(app)


# if __name__ == '__main__':
#     # socketio.run encapsulates app.run but includes web socket functionality
#     app = create_app()
#     socketio.run(app, allow_unsafe_werkzeug=True)