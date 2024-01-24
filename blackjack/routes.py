from flask import Blueprint, render_template, redirect, url_for, request
from flask_socketio import emit
from app_setup import socketio

from blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)

# initialize blueprint
# blackjack_blueprint.game_exists = False

# Create an instance of the BlackjackController
blackjack_controller = BlackjackController()
counts = 0


@blackjack_blueprint.route('/blackjack')
def blackjack():  # blackjack_route
    return blackjack_controller.blackjack()


@blackjack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return blackjack_controller.buttons(request)


@blackjack_blueprint.route('/press_button_1', methods=['POST'])
def handle_press_button_1(counts):
    data = request.get_json()
    player_name = data['player_name']
    game_id = data['game_id']
    counts += 1
    # Perform necessary actions for button 1 press here
    # ...
    # Emit 'update_button_counts' event with updated counts
    emit('update_button_counts', {'game_id': game_id, 'counts': counts}, broadcast=True)
    return {}, 200


@socketio.on('press_button_1')
def handle_press_button_1(data):
    # Handle the event here
    global counts
    counts += 1
    print('Button 1 pressed with data:', data)
    emit('update_button_counts', {'game_id': data['game_id'], 'counts': counts}, broadcast=True)

@socketio.on('press_button_2')
def handle_press_button_2(data):
    # Handle the event here
    global counts
    counts += 1
    print('Button 2 pressed with data:', data)
    emit('update_button_counts', {'game_id': data['game_id'], 'counts': counts}, broadcast=True)
