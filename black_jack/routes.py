from flask import Blueprint, render_template, redirect, url_for, request
from black_jack.controller import BlackjackController

black_jack_blueprint = Blueprint('black_jack', __name__)

# initialize blueprint
# black_jack_blueprint.game_exists = False

# Create an instance of the BlackjackController
blackjack_controller = BlackjackController()


@black_jack_blueprint.route('/black_jack')
def black_jack():  # black_jack_route
    return blackjack_controller.blackjack()


@black_jack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    return blackjack_controller.buttons(request)
