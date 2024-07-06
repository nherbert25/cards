from flask import render_template, redirect, url_for
from cards.blackjack.blackjack_model import BlackjackModel


# Controller class for Blackjack game
class BlackjackController:
    def __init__(self):
        self.blackjack_model = BlackjackModel()
        self.counts = {'button1': 0, 'button2': 0}

    # TODO: since the controller should pull variables from the routes and send them to the model, NOT modify it
    #  directly... it should likely not have logic such as "if not self.blackjack_model.game_exists" either?
    #  or is it okay to have the 'brain' direct traffic based on the state of the model?
    # TODO: rewrite the buttons scripts and frontend displayed variables with javascript
    # TODO: rewrite these endpoints to return JSON, to then be picked up by javascript
    # TODO: write the 'Stay' button as a javascript ajax thing that returns JSON from the server
    # TODO: how to unit test these buttons, make sure the page still loads, etc.?
    # https://testdriven.io/blog/flask-server-side-sessions/
    # flask session tutorial:  https://www.youtube.com/watch?v=lvKjQhQ8Fwk&t=14s
    def blackjack(self):
        # blackjack_controller = session['blackjack_controller']
        if not self.blackjack_model.game_exists:
            self.blackjack_model.start_new_game()
        return render_template("blackjack.html", **self.prepare_blackjack_socket_data())

    def update_page_data(self):
        return render_template("blackjack.html", **self.prepare_blackjack_socket_data())

    def prepare_blackjack_html_data(self):
        result = {
            # 'dealer_cards': self.blackjack_model.dealer_cards,
            # 'dealer_sum': self.blackjack_model.dealer_sum,
            # 'your_cards': self.blackjack_model.your_cards,
            # 'your_sum': self.blackjack_model.your_sum,
            # 'player_name': self.blackjack_model.player_name,
            # 'your_coins': self.blackjack_model.your_coins,
            # 'has_stayed': self.blackjack_model.has_stayed,
            # 'button1_count': self.counts['button1'],
            # 'button2_count': self.counts['button2'],
        }
        return result

    def prepare_blackjack_socket_data(self):
        """WebSockets require data to be in a format that can be transmitted over the network. This means the data must be serialized to a format like JSON.
        Not all Python objects are directly serializable to JSON. For example, custom objects need to be converted to basic data types (dicts, lists, strings, numbers, etc.) before they can be serialized."""
        result = {
            'dealer_cards': [card.to_dict() for card in self.blackjack_model.dealer_cards],
            'your_cards': [card.to_dict() for card in self.blackjack_model.your_cards],
            'dealer_sum': self.blackjack_model.dealer_sum,
            'your_sum': self.blackjack_model.your_sum,
            'player_name': self.blackjack_model.player_name,
            'your_coins': self.blackjack_model.your_coins,
            'has_stayed': self.blackjack_model.has_stayed,
            'button1_count': self.counts['button1'],
            'button2_count': self.counts['button2'],
            'testing_coins': 200
        }
        return result

    def buttons(self, request):

        if request.method == 'POST':

            if request.form.get('button_pressed') == 'Hit':
                self.blackjack_model.hit()

            if request.form.get('button_pressed') == 'Stay':
                self.blackjack_model.stay()

            if request.form.get('button_pressed') == 'New Game':
                self.blackjack_model.start_new_game()

        return redirect(url_for('blackjack.blackjack'))

    # the following will render the blackjack.html BUT leave the url as http://127.0.0.1:5000/buttons?hit=Hit,
    # meaning if you refresh the page it will rerun this route
    # return render_template("blackjack.html", deck=self.blackjack_model.deck, etc.)
