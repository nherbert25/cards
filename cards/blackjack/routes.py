from flask import Blueprint
# TODO: I think this socketio should be from app_setup instead
from flask_socketio import emit
from cards.app_setup import socketio

from cards.blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)
blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():
    return blackjack_controller.blackjack()


@socketio.on('hit')
def hit(user_id=None, hand_index=0):
    blackjack_controller.hit(user_id, hand_index)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('stay')
def stay(user_id=None, hand_index=0):
    blackjack_controller.stay(user_id, hand_index)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('double_down')
def double_down(user_id=None, hand_index=0):
    blackjack_controller.double_down(user_id, hand_index)
    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('split_pair')
def split_pair(user_id=None, hand_index=0):
    if blackjack_controller.split_pair(user_id, hand_index):
        data = blackjack_controller.serialize_blackjack_data()
        player_data = data['players'][user_id]
        emit('player_added_hand', {'player_id': user_id, 'player_data': player_data}, broadcast=True)

    emit('update_page_data', blackjack_controller.serialize_blackjack_data(), broadcast=True)


# TODO: add ability to change bet amount
@socketio.on('bet')
def bet(user_id=None, hand_index=0):
    pass


@socketio.on('new_game')
def new_game():
    blackjack_controller.new_game()
    emit('rebuild_entire_page', blackjack_controller.serialize_blackjack_data(), broadcast=True)


@socketio.on('rebuild_entire_page')
def handle_rebuild_entire_page():
    try:
        emit('rebuild_entire_page', blackjack_controller.serialize_blackjack_data(), broadcast=True)
    except Exception as e:
        emit('request_game_data_error', str(e))


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
