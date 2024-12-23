import pytest

from tests.blackjack.test_configs import initial_game_blackjack
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs, PlayerOutcome
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

    @pytest.mark.parametrize(
        "dealer_sum, player_sum, dealer_blackjack, player_blackjack, expected_outcome",
        [
            (18, 20, False, False, PlayerOutcome.WIN),  # Player beats dealer
            (20, 18, False, False, PlayerOutcome.LOSE),  # Dealer beats player
            (21, 21, False, False, PlayerOutcome.PUSH),  # Player ties with dealer
            (18, 22, False, False, PlayerOutcome.LOSE),  # Player busts
            (22, 20, False, False, PlayerOutcome.WIN),  # Dealer busts
            (22, 22, False, False, PlayerOutcome.LOSE),  # Both bust; player still loses
            (19, 19, False, False, PlayerOutcome.PUSH),  # Tie on lower values
            (21, 21, True, False, PlayerOutcome.LOSE),  # Dealer has Blackjack, player ties
            (21, 21, False, True, PlayerOutcome.WIN),  # Player has Blackjack, dealer ties
            (21, 21, True, True, PlayerOutcome.PUSH),  # Both have Blackjack, push
            (21, 22, True, False, PlayerOutcome.LOSE),  # Dealer has Blackjack, player busts
            (22, 21, False, True, PlayerOutcome.WIN),  # Player has Blackjack, dealer busts
        ]
    )
    def test_determine_outcome(self, dealer_sum, player_sum, dealer_blackjack, player_blackjack, expected_outcome):
        result = BlackjackModel._determine_outcome(dealer_sum, player_sum, dealer_blackjack, player_blackjack)
        assert result == expected_outcome

    # Todo: fix this if necessary. This might require an integration test since no dependency injection
    @pytest.mark.parametrize('test_input, expected_output', (
                                                             ([Card('3', 'C'), Card('3', 'C')], 6),
                                                             ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25)))
    def test_resolve_dealer_turn(self, test_input, expected_output):
        return
        model = BlackjackModel(GameConfigs)
        model.resolve_dealer_turn(test_input)
        assert model.dealer_sum >= expected_output
