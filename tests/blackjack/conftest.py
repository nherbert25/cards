import pytest
from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card

"""Pytest automatically loads fixtures from a file named conftest.py
if it is in the same directory or a parent directory of your test files."""


################################################
################################################
# EXAMPLE
@pytest.fixture
def square(request):
    """
    Define a fixture that takes an argument. 'Request' is a built-in fixture,
    find parameters using request.param
    """
    return request.param * 2


@pytest.mark.parametrize("square", [1, 2, 3], indirect=True)
def test_square(square):
    """Use indirect parametrization to pass arguments to the fixture"""
    assert square in [2, 4, 6]


################################################
################################################


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
