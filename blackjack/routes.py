from flask import Blueprint, render_template, redirect, url_for, request
from flask_socketio import emit
from app_setup import socketio

from blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)

# initialize blueprint
# blackjack_blueprint.game_exists = False

# Create an instance of the BlackjackController
blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():  # blackjack_route
    return blackjack_controller.blackjack()


@blackjack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return blackjack_controller.buttons(request)


@socketio.on('press_button_1')
def handle_press_button_1(data):
    # Handle the event here
    button_number = data['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)


@socketio.on('press_button_2')
def handle_press_button_2(data):
    # Handle the event here
    button_number = data['buttonNumber']
    blackjack_controller.counts[f'button{button_number}'] += 1
    emit('update_button_counts', {'counts': blackjack_controller.counts}, broadcast=True)
