from flask import Blueprint
from flask_socketio import emit
from cards.app_setup import socketio

from cards.blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)
blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():
    return blackjack_controller.blackjack()


@socketio.on('hit')
def hit(user_id=None):
    blackjack_controller.hit(user_id)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('stay')
def stay(user_id=None):
    blackjack_controller.stay(user_id)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('double_down')
def double_down(user_id=None):
    blackjack_controller.double_down(user_id)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('new_game')
def new_game():
    blackjack_controller.new_game()
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


# TODO: add ability to change bet amount
@socketio.on('bet')
def bet(user_id=None):
    pass


@socketio.on('request_game_data')
def handle_request_game_data():
    try:
        emit('request_game_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)
    except Exception as e:
        emit('request_game_data_error', str(e))


@socketio.on('update_page_data')
def update_page_data():
    try:
        emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)
    except Exception as e:
        emit('request_game_data_error', str(e))


@socketio.on('press_socket_testing_buttons')
def press_socket_testing_buttons(button_data_from_client):
    button_number = button_data_from_client['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)


@socketio.on("connect")
def handle_connection():
    print("Client connected!")
