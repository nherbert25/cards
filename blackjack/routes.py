from flask import Blueprint, render_template, redirect, url_for, request
from blackjack.controller import BlackjackController

blackjack_blueprint = Blueprint('blackjack', __name__)

# initialize blueprint
# black_jack_blueprint.game_exists = False

# Create an instance of the BlackjackController
blackjack_controller = BlackjackController()


@blackjack_blueprint.route('/blackjack')
def blackjack():  # black_jack_route
    return blackjack_controller.blackjack()


@blackjack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return blackjack_controller.buttons(request)
