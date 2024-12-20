import pytest
from cards.blackjack.blackjack_model import Card, BlackjackModel


class TestBlackjackModel:
    # working test with parametrization (allows you to run the same test with multiple inputs) note that 'test_input, expected_output' is a SINGLE string!
    # also note the class must be instantiated first. pytest methods do not take the 'self' keyword, you must *always* instantiate your test class.
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
        model = BlackjackModel()
        result = model.calculate_blackjack_sum(test_input)
        assert result == expected_output

    # Todo: fix
    @pytest.mark.parametrize('test_input, expected_output', ((5, 10), (10, 10), (18,10), (21,10), (21,21), (22,10), (22,22)))
    def test_determine_winner(self, test_input, expected_output):
        return
        model = BlackjackModel()
        result = model.determine_winner(test_input)
        assert result == expected_output

    # Todo: fix
    @pytest.mark.parametrize('test_input, expected_output', (
                                                             ([Card('3', 'C'), Card('3', 'C')], 6),
                                                             ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25)))
    def test_resolve_dealer_turn(self, test_input, expected_output):
        return
        model = BlackjackModel()
        model.resolve_dealer_turn(test_input)
        assert model.dealer_sum >= expected_output
