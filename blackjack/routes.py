from flask import Blueprint, render_template, redirect, url_for, request
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
