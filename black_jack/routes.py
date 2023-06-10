from flask import Blueprint, render_template, redirect, url_for, request
import black_jack.black_jack as bj

black_jack_blueprint = Blueprint('black_jack', __name__)

# initialize blueprint
black_jack_blueprint.game_exists = False


@black_jack_blueprint.route('/black_jack')
def black_jack():
    if not black_jack_blueprint.game_exists:
        bj.deck, bj.dealer_cards, bj.dealer_sum, bj.your_cards, bj.your_sum = bj.start_new_game()
        black_jack_blueprint.game_exists = True
    # print(type(bj.your_sum), bj.your_sum)
    return render_template("black_jack.html", deck=bj.deck, dealer_cards=bj.dealer_cards, dealer_sum=bj.dealer_sum,
                           your_sum=bj.your_sum, player_name=bj.player_name, your_cards=bj.your_cards)


@black_jack_blueprint.route('/buttons', methods=['GET', 'POST'])
def buttons():
    if request.method == 'POST':

        # uncomment for debugging
        # print(request.form, request.form.get('button_pressed'))

        if request.form.get('button_pressed') == 'Hit':
            bj.your_cards.append(bj.deck.cards.pop())
            bj.your_sum = bj.calculate_black_jack_sum(bj.your_cards)

        if request.form.get('button_pressed') == 'Stay':
            pass

        if request.form.get('button_pressed') == 'New Game':
            black_jack_blueprint.game_exists = False

    return redirect(url_for('black_jack.black_jack'))

    # the following will render the black_jack.html BUT leave the url as http://127.0.0.1:5000/buttons?hit=Hit, meaning if you refresh the page it will rerun this route
    # return render_template("black_jack.html", deck=bj.deck, etc.)