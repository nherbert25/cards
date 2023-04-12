from flask import Flask, render_template, request
import socket

app = Flask(__name__)


# @app.route('/')
def hello_world():  # put application's code here
    print('testing')
    print('pls work')
    print('test3')
    print('hi taylor!!')
    return 'Hello World!'


# this defines the entrance to your code. my_website.com goes HERE as well as my_website.com/home
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]

    return render_template('index.html', name=name)


@app.route('/black_jack')
def black_jack():
    return render_template("black_jack.html")


@app.route('/join_game', methods=['POST'])
def join_game():
    ip_address = request.form['ip_address']
    port = int(request.form['port'])

    # Connect to the game server
    try:
        # Create a socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((ip_address, port))

        # Ask player for their name
        player_name = input("Enter your player name: ")
        client_socket.sendall(player_name.encode())

        # Receive a response from the server
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

        return render_template('black_jack.html', player_name=player_name)
    except Exception as e:
        return 'Error: {}'.format(e)


if __name__ == '__main__':
    app.run()
