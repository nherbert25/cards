import pytest

from tests.blackjack.test_configs import example_hand_total_KQ, example_hand_total_KK, example_hand_total_QQQ
from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card


class TestBlackjackModel:
    @pytest.fixture
    def mock_game(self, mocker):
        pass

    # working test with parametrization (allows you to run the same test with multiple inputs) note that 'test_input,
    # expected_output' is a SINGLE string! also note the class must be instantiated first. pytest methods do not take
    # the 'self' keyword, you must *always* instantiate your test class.
    @pytest.mark.parametrize('test_input, expected_output', (
            ([], 0),
            ([Card('10', 'C')], 10),
            ([Card('3', 'C'), Card('3', 'C')], 6),
            ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25),
            ([Card('A', 'C'), Card('A', 'D')], 12),
            ([Card('A', 'C'), Card('A', 'D'), Card('A', 'D')], 13),
            ([Card('A', 'C'), Card('J', 'D')], 21),
            ([Card('A', 'C'), Card('A', 'D'), Card('Q', 'D')], 12)))
    def test_calculate_blackjack_sum(self, test_input, expected_output):
        model = Hand()
        result = model.calculate_blackjack_sum(test_input)
        assert result == expected_output

    @pytest.mark.parametrize('test_input, expected_output', (
            (example_hand_total_KQ, False),
            (example_hand_total_KK, True),
            (example_hand_total_QQQ, False),
    ))
    def test_can_split_pairs(self, test_input, expected_output):
        assert test_input.can_split_pairs == expected_output

    @pytest.mark.parametrize('test_input, expected_output', (
            (example_hand_total_KK, (Card('K', 'C'), (Card('K', 'D')))),
            (example_hand_total_KQ, None),

    ))
    def test_split_pairs(self, test_input, expected_output):
        if not test_input.can_split_pairs:
            assert test_input.split_pairs() is None

        else:
            hand_1, hand_2 = test_input.split_pairs()
            assert hand_1[0] == expected_output[0]
            assert hand_2[0] == expected_output[1]
