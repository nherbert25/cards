from flask import render_template
from cards.blackjack.blackjack_model import BlackjackModel


class BlackjackController:
    def __init__(self):
        self.blackjack_model = BlackjackModel()
        self.counts = {'button1': 0, 'button2': 0}

    # TODO: since the controller should pull variables from the routes and send them to the model, NOT modify it
    #  directly... it should likely not have logic such as "if not self.blackjack_model.game_exists" either?
    #  or is it okay to have the 'brain' direct traffic based on the state of the model?
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

    def prepare_blackjack_socket_data(self):
        """WebSockets require data to be in a format that can be transmitted over the network. This means the data must be serialized to a format like JSON.
        Not all Python objects are directly serializable to JSON. For example, custom objects need to be converted to basic data types (dicts, lists, strings, numbers, etc.) before they can be serialized."""

        result = {
            'dealer_cards': [card.to_dict() for card in self.blackjack_model.dealer_cards],
            'dealer_sum': self.blackjack_model.dealer_sum,
            'button1_count': self.counts['button1'],
            'button2_count': self.counts['button2'],
            'players_data_object': {},
        }

        for player in self.blackjack_model.players.values():
            result['players_data_object'][str(player.user_id)] = player.to_dict()
        return result

    def buttons(self, button_name: str, user_id: str) -> None:
        player_object = self.blackjack_model.get_player(user_id)

        if button_name == 'hit':
            self.blackjack_model.hit(player_object)

        if button_name == 'stay':
            self.blackjack_model.stay(player_object)

        if button_name == 'new_game':
            self.blackjack_model.start_new_game()

        # the following will render the blackjack.html BUT leave the url as http://127.0.0.1:5000/buttons?hit=Hit,
        # meaning if you refresh the page it will rerun this route
        # return render_template("blackjack.html", deck=self.blackjack_model.deck, etc.)
