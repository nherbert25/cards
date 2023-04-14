from flask import Flask, render_template, request, redirect, session
from networking.client import Client
import socket
import random

app = Flask(__name__)
app.secret_key = 'anA194$38@na.dn0832A'


# @app.route('/')
def hello_world():  # put application's code here
    print('testing')
    print('pls work')
    print('test3')
    print('hi taylor!!')
    return 'Hello World!'


# this defines the entrance to your code. my_website.com goes HERE (because @app.route('/')) as well as my_website.com/home (because @app.route('/home'))
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
        client = Client(server_ip=ip_address, server_port=port)

        # Ask for player name
        session['player_name'] = input("Enter your player name: ")
        client.send_data(session['player_name'])

        # Receive a response from the server
        data = client.receive_data()

        return render_template('black_jack.html', player_name=session['player_name'])
    except Exception as e:
        return 'Error: {}'.format(e)


@app.route('/player_choice', methods=['POST'])
def player_choice():
    player_card = "{{ url_for('static', filename='cards2/BACK.png') }}"
    if request.form.get('hit') == 'Hit':
        hit = True
        print('Player chose to hit!')
        player_name = session.get('player_name')
        return render_template('black_jack.html', player_name=session['player_name'], hit=hit)

    elif request.form.get('stay') == 'Stay':
        print('Player chose to stay!')
        player_name = session.get('player_name')
        return render_template('black_jack.html', player_name=session['player_name'])


if __name__ == '__main__':
    app.run()
