from flask import Blueprint, render_template
import black_jack.black_jack as bj

black_jack_blueprint = Blueprint('black_jack', __name__)


@black_jack_blueprint.route('/black_jack')
def black_jack():
    return render_template("black_jack.html", dealer_sum=bj.dealer_sum)

@black_jack_blueprint.route('/hit')
def hit():
    pass