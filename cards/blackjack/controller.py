from flask import render_template
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs


class BlackjackController:
    def __init__(self):
        self.blackjack_model = BlackjackModel(GameConfigs)
        self.counts = {'button1': 0, 'button2': 0}

    # TODO: since the controller should pull variables from the routes and send them to the model, NOT modify it
    #  directly... it should likely not have logic such as "if not self.blackjack_model.game_exists" either?
    #  or is it okay to have the 'brain' direct traffic based on the state of the model?
    # https://testdriven.io/blog/flask-server-side-sessions/
    # flask session tutorial:  https://www.youtube.com/watch?v=lvKjQhQ8Fwk&t=14s
    def blackjack(self):
        # blackjack_controller = session['blackjack_controller']
        if not self.blackjack_model.game_exists:
            self.blackjack_model.start_new_game()
        return render_template("blackjack.html", **self.serialize_blackjack_data())

    def update_page_data(self):
        return render_template("blackjack.html", **self.serialize_blackjack_data())

    def serialize_blackjack_data(self) -> dict:
        result = {
            'BLACKJACK_MAX': self.blackjack_model.BLACKJACK_MAX,
            'dealer_cards': [card.to_dict() for card in self.blackjack_model.dealer_cards],
            'dealer_sum': self.blackjack_model.dealer_sum,
            'button1_count': self.counts['button1'],
            'button2_count': self.counts['button2'],
            'players_data_object': {},
        }

        for player in self.blackjack_model.players.values():
            result['players_data_object'][str(player.user_id)] = player.to_dict()
        return result

    def hit(self, user_id: str) -> None:
        player_object = self.blackjack_model.get_player(user_id)
        self.blackjack_model.hit(player_object)

    def stay(self, user_id: str) -> None:
        player_object = self.blackjack_model.get_player(user_id)
        self.blackjack_model.stay(player_object)

    def double_down(self, user_id: str) -> None:
        player_object = self.blackjack_model.get_player(user_id)
        self.blackjack_model.double_down(player_object)

    def new_game(self) -> None:
        self.blackjack_model.start_new_game()
