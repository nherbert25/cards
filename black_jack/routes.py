from flask import Blueprint, render_template, redirect, url_for
import black_jack.black_jack as bj

black_jack_blueprint = Blueprint('black_jack', __name__)


@black_jack_blueprint.route('/black_jack')
def black_jack():
    deck = bj.Deck()
    deck.shuffle()
    return render_template("black_jack.html", dealer_sum=bj.dealer_sum, player_name=bj.player_name, your_cards=bj.your_cards, test_cards=bj.test_cards)


@black_jack_blueprint.route('/hit', methods=['GET'])
def hit():
    bj.dealer_sum += 1
    bj.your_cards.append(bj.Card(rank='A', suit='S'))
    return redirect(url_for('black_jack.black_jack'))

