workers = 1  # Adjust the number of workers based on your application's needs. Gunicorn can only support 1 worker for web sockets! See https://flask-socketio.readthedocs.io/en/latest/deployment.html#gunicorn-web-server for details
timeout = 300  # Set a reasonable timeout value.
worker_class = 'eventlet'

# to run: "gunicorn -c gunicorn_config.py app:app"
# to run with eventlet "gunicorn --worker-class eventlet -w 1 app:app"
# to find zombie processes on port 8000 "sudo lsof -i :8000"
# to kill those zombie processes "kill -9 <pid>"
