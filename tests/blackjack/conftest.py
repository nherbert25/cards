# TODO: MAKE THIS WORK

import pytest
from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card


# pytest automatically loads fixtures from a file named conftest.py if it is in the same directory or a parent directory of your test files.


################################################
################################################
# EXAMPLE 1
# conftest.py
@pytest.fixture
def input_data(request):
    return request.param


# test_example.py
import pytest


@pytest.mark.parametrize(
    "input_data, expected",
    [
        pytest.param(2, 4, id="square_2"),
        pytest.param(3, 9, id="square_3"),
        pytest.param(4, 16, id="square_4"),
    ],
    indirect=["input_data"],
)
def test_square(input_data, expected):
    assert input_data * input_data == expected


################################################
################################################


################################################
################################################
# EXAMPLE 2
# Define a fixture that takes an argument
@pytest.fixture
def square(request):
    return request.param * 2


# Use indirect parametrization to pass arguments to the fixture
@pytest.mark.parametrize("square", [1, 2, 3], indirect=True)
def test_square(square):
    assert square in [2, 4, 6]


################################################
################################################


@pytest.fixture
def example_hand_KK():
    """Returns a hand with two Kings."""
    return Hand([Card('K', 'C'), Card('K', 'D')])


@pytest.fixture
def example_hand_KQ():
    """Returns a hand with King and Queen."""
    return Hand([Card('K', 'C'), Card('Q', 'D')])


@pytest.fixture(params=[
    [Card('K', 'C'), Card('Q', 'D')],
    [Card('K', 'C'), Card('K', 'D')],
    [Card('Q', 'C'), Card('Q', 'D'), Card('Q', 'H')]
])
def generate_hands(request):
    list_of_cards = request.param
    test_hand = Hand()

    for card in list_of_cards:
        test_hand.hit(card)

    return test_hand


@pytest.fixture
def test_hands():
    return {
        "KQ": Hand([Card('K', 'C'), Card('Q', 'D')]),
        "KK": Hand([Card('K', 'C'), Card('K', 'D')]),
        "QQQ": Hand([Card('Q', 'C'), Card('Q', 'D'), Card('Q', 'H')]),
    }


@pytest.fixture(scope="session")
def hand_factory():
    """scope defaults to "function" which means this would get ran during every single unit test. hand_factory is only
    defining *how* to create hands, so it only needs to be defined once."""

    def _create_hand(name):
        hands = {
            "empty_hand": lambda: Hand(),
            "9": lambda: Hand([Card('9', 'C')]),
            "AA": lambda: Hand([Card('A', 'C'), Card('A', 'D')]),
            "AAA": lambda: Hand([Card('A', 'C'), Card('A', 'D'), Card('A', 'D')]),
            "AJ": lambda: Hand([Card('A', 'C'), Card('J', 'D')]),
            "AAQ": lambda: Hand([Card('A', 'C'), Card('A', 'D'), Card('Q', 'D')]),
            "KQ": lambda: Hand([Card('K', 'C'), Card('Q', 'D')]),
            "KK": lambda: Hand([Card('K', 'C'), Card('K', 'D')]),
            "QQQ": lambda: Hand([Card('Q', 'C'), Card('Q', 'D'), Card('Q', 'H')]),
            "33": lambda: Hand([Card('3', 'C'), Card('3', 'C')]),
            "333": lambda: Hand([Card('3', 'C'), Card('3', 'C'), Card('3', 'C')]),
            "5KQ": lambda: Hand([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')]),
        }
        return hands[name]()  # Lazily initialize only the requested hand

    return _create_hand
