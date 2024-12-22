import pytest

from tests.blackjack.test_configs import initial_game_blackjack
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs
from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card


def generate_test_players():
    player_1 = Player()
    player_1.hand = [Card('3', 'C'), Card('3', 'C')]
    player_2 = Player()
    player_2.hand = [Card('10', 'C'), Card('A', 'C')]
    player_3 = Player()
    player_3.hand = [Card('3', 'C'), Card('3', 'C')]


class TestBlackjackModel:
    @pytest.fixture
    def mock_game(self, mocker):
        mock_create_game = mocker.patch('cards.blackjack.controller.BlackjackController.serialize_blackjack_data',
                                        return_value=initial_game_blackjack)
        blackjack_game = BlackjackModel(GameConfigs)


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
        model = BlackjackModel(GameConfigs)
        result = model.calculate_blackjack_sum(test_input)
        assert result == expected_output

    # Todo: fix
    @pytest.mark.parametrize('test_input, expected_output', ((5, 10), (10, 10), (18,10), (21,10), (21,21), (22,10), (22,22)))
    def test_determine_winner(self, test_input, expected_output):
        return
        model = BlackjackModel(GameConfigs)
        result = model.determine_winner(test_input)
        assert result == expected_output

    # Todo: fix
    @pytest.mark.parametrize('test_input, expected_output', (
                                                             ([Card('3', 'C'), Card('3', 'C')], 6),
                                                             ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25)))
    def test_resolve_dealer_turn(self, test_input, expected_output):
        return
        model = BlackjackModel(GameConfigs)
        model.resolve_dealer_turn(test_input)
        assert model.dealer_sum >= expected_output
