from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config["DEBUG"] = True  # comment out for pycharm debug mode (ironic, isn't it?)
    app.config["SECRET_KEY"] = 'anA194$38@na.dn0832A'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    from blackjack.routes import blackjack_blueprint
    app.register_blueprint(blackjack_blueprint)

    socketio.init_app(app)
    return app
