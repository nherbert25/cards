from flask import Blueprint, current_app
from cards.app_setup import socketio

from cards.blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)


# @blackjack_blueprint.before_request
# def initialize_blackjack():
#     current_app.config['BLACKJACK_GAME'] = BlackjackController()


blackjack_controller = None


def get_blackjack_controller():
    global blackjack_controller
    if not blackjack_controller:
        blackjack_controller = BlackjackController()
    return blackjack_controller


@blackjack_blueprint.route('/blackjack')
def blackjack():
    blackjack_controller = get_blackjack_controller()
    return blackjack_controller.blackjack()


@socketio.on('hit')
def hit(user_id=None, hand_index=0):
    blackjack_controller = get_blackjack_controller()
    blackjack_controller.hit(user_id, hand_index)
    socketio.emit('update_page_data', blackjack_controller.serialize_blackjack_data(), to=None)


@socketio.on('stay')
def stay(user_id=None, hand_index=0):
    blackjack_controller = get_blackjack_controller()
    blackjack_controller.stay(user_id, hand_index)
    socketio.emit('update_page_data', blackjack_controller.serialize_blackjack_data(), to=None)


@socketio.on('double_down')
def double_down(user_id=None, hand_index=0):
    blackjack_controller = get_blackjack_controller()
    blackjack_controller.double_down(user_id, hand_index)
    socketio.emit('update_page_data', blackjack_controller.serialize_blackjack_data(), to=None)


@socketio.on('split_pair')
def split_pair(user_id=None, hand_index=0):
    blackjack_controller = get_blackjack_controller()
    if blackjack_controller.split_pair(user_id, hand_index):
        data = blackjack_controller.serialize_blackjack_data()
        player_data = data['players'][user_id]
        socketio.emit('player_added_hand', {'player_id': user_id, 'player_data': player_data}, to=None)

    socketio.emit('update_page_data', blackjack_controller.serialize_blackjack_data(), to=None)


# TODO: add ability to change bet amount
@socketio.on('bet')
def bet(user_id=None, hand_index=0):
    pass


@socketio.on('new_game')
def new_game():
    blackjack_controller = get_blackjack_controller()
    blackjack_controller.new_game()
    socketio.emit('rebuild_entire_page', blackjack_controller.serialize_blackjack_data(), to=None)


@socketio.on('rebuild_entire_page')
def handle_rebuild_entire_page():
    try:
        blackjack_controller = get_blackjack_controller()
        socketio.emit('rebuild_entire_page', blackjack_controller.serialize_blackjack_data(), to=None)
    except Exception as e:
        socketio.emit('request_game_data_error', str(e))


@socketio.on('request_game_data')
def handle_request_game_data():
    try:
        blackjack_controller = get_blackjack_controller()
        socketio.emit('request_game_data', blackjack_controller.serialize_blackjack_data(), to=None)
    except Exception as e:
        socketio.emit('request_game_data_error', str(e))


@socketio.on('update_page_data')
def update_page_data():
    try:
        blackjack_controller = get_blackjack_controller()
        socketio.emit('update_page_data', blackjack_controller.serialize_blackjack_data(), to=None)
    except Exception as e:
        socketio.emit('request_game_data_error', str(e))


@socketio.on('press_socket_testing_buttons')
def press_socket_testing_buttons(button_data_from_client):
    blackjack_controller = get_blackjack_controller()
    button_number = button_data_from_client['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    socketio.emit('update_button_counts', {'counts': blackjack_controller.counts}, to=None)


@socketio.on("connect")
def handle_connection():
    print("Client connected!")
