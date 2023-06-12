from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from black_jack.blackjack_model import BlackjackModel


# Controller class for Blackjack game
class BlackjackController:
    def __init__(self):
        self.blackjack_model = BlackjackModel()

    # TODO: the controller should pull variables from the routes and SEND them to the model. NOT modify the model
    #  directly!!!!
    def blackjack(self):
        if not self.blackjack_model.game_exists:
            self.blackjack_model.deck, self.blackjack_model.dealer_cards, self.blackjack_model.dealer_sum, self.blackjack_model.your_cards, self.blackjack_model.your_sum = self.blackjack_model.start_new_game()
            self.blackjack_model.game_exists = True
        # print(type(self.blackjack_model.your_sum), self.blackjack_model.your_sum)
        return render_template("black_jack.html", deck=self.blackjack_model.deck, dealer_cards=self.blackjack_model.dealer_cards, dealer_sum=self.blackjack_model.dealer_sum,
                               your_sum=self.blackjack_model.your_sum, player_name=self.blackjack_model.player_name, your_cards=self.blackjack_model.your_cards)

    def buttons(self, request):
        if request.method == 'POST':

            # uncomment for debugging
            # print(request.form, request.form.get('button_pressed'))

            if request.form.get('button_pressed') == 'Hit':
                self.blackjack_model.your_cards.append(self.blackjack_model.deck.cards.pop())
                self.blackjack_model.your_sum = self.blackjack_model.calculate_black_jack_sum(self.blackjack_model.your_cards)

            if request.form.get('button_pressed') == 'Stay':
                pass

            if request.form.get('button_pressed') == 'New Game':
                self.blackjack_model.game_exists = False

        return redirect(url_for('black_jack.black_jack'))

        # the following will render the black_jack.html BUT leave the url as http://127.0.0.1:5000/buttons?hit=Hit,
        # meaning if you refresh the page it will rerun this route return render_template("black_jack.html",
        # deck=self.blackjack_model.deck, etc.)
