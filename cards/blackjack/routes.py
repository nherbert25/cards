from flask import Blueprint
from flask_socketio import emit
from cards.app_setup import socketio

from cards.blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)
blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():
    return blackjack_controller.blackjack()


@socketio.on('press_buttons')
def press_buttons(button_name):
    blackjack_controller.buttons(button_name)
    emit('update_page_data', blackjack_controller.prepare_blackjack_socket_data(), broadcast=True)


@socketio.on('update_page_data')
def update_page_data():
    print('pressed refresh on server')
    emit('update_page_data', blackjack_controller.prepare_blackjack_socket_data(), broadcast=True)


@socketio.on('press_socket_testing_buttons')
def press_socket_testing_buttons(button_data_from_client):
    button_number = button_data_from_client['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)


@socketio.on("connect")
def handle_connection():
    print("Client connected! Python output.")
