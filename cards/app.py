from cards.app_setup import create_app, socketio

# Create app using the factory function
app = create_app()


if __name__ == '__main__':
    # Run the app with SocketIO support
    socketio.run(app, allow_unsafe_werkzeug=True)