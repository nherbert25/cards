from flask import Blueprint, request
from flask_socketio import emit
from cards.app_setup import socketio

from cards.blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)

# initialize blueprint
# blackjack_blueprint.game_exists = False


blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():
    # Create an instance of the BlackjackController if not already in session
    # if 'blackjack_controller' not in session:
    #     session['blackjack_controller'] = BlackjackController()
    # return session['blackjack_controller'].blackjack()
    return blackjack_controller.blackjack()


@blackjack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return blackjack_controller.buttons(request)


@socketio.on('press_button_1')
def press_button_1(data):
    button_number = data['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)


@socketio.on('press_button_2')
def press_button_2(data):
    button_number = data['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)


@socketio.on("connect")
def handle_connection():
    print("Client connected! Python output.")
