from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(ping_interval=50, ping_timeout=50)


# create app pattern:  https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config["DEBUG"] = True  # comment out for pycharm debug mode (ironic, isn't it?)
    app.config["SECRET_KEY"] = 'anA194$38@na.dn0832A'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SESSION_TYPE'] = 'sqlalchemy'

    from app import sess
    from app import db
    from app import bcrypt
    db.init_app(app)
    bcrypt.init_app(app)
    app.config['SESSION_SQLALCHEMY'] = db
    sess.init_app(app)

    with app.app_context():
        db.create_all()

    from blackjack.routes import blackjack_blueprint
    app.register_blueprint(blackjack_blueprint)

    socketio.init_app(app)
    return app
