from cards.app_setup import create_app, socketio

# Create app using the factory function
app = create_app()

# todo: remove allow_unsafe_werkzeug for prod
if __name__ == '__main__':
    # Run the app with SocketIO support
    host = app.config.get('SERVER_HOST', '127.0.0.1')
    port = app.config.get('SERVER_PORT', 5000)
    debug = app.config.get('DEBUG', False)

    print(f"Starting Flask-SocketIO server on http://{host}:{port}")
    print(f"Debug mode: {debug}")
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)