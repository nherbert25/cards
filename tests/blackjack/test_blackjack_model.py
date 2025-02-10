import pytest

from tests.blackjack.test_configs import initial_game_blackjack
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs
from cards.blackjack.player_model import Player
from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card


def generate_test_players():
    player_1 = Player(player_name='Taylor')
    hand = Hand()
    cards = [Card('3', 'C'), Card('3', 'C')]
    for card in cards:
        hand.hit(card, BlackjackModel.calculate_blackjack_sum())
    player_1.add_hand(hand)

    player_2 = Player(player_name='Nate')
    hand = Hand()
    cards = [Card('10', 'C'), Card('A', 'C')]
    for card in cards:
        hand.hit(card, BlackjackModel.calculate_blackjack_sum())
    player_2.add_hand(hand)

    player_3 = Player(player_name='Travis')
    hand = Hand()
    cards = [Card('3', 'C'), Card('3', 'C')]
    for card in cards:
        hand.hit(card, BlackjackModel.calculate_blackjack_sum())
    player_3.add_hand(hand)

    return player_1, player_2, player_3


class TestBlackjackModel:
    @pytest.fixture
    def mock_game(self, mocker):
        mock_create_game = mocker.patch('cards.blackjack.controller.BlackjackController.serialize_blackjack_data',
                                        return_value=initial_game_blackjack)
        blackjack_game = BlackjackModel(GameConfigs)

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
        model = BlackjackModel(GameConfigs)
        result = model.calculate_blackjack_sum(test_input)
        assert result == expected_output

    @pytest.mark.parametrize(
        "dealer_sum, player_sum, dealer_blackjack, player_blackjack, expected_outcome",
        [
            (18, 20, False, False, HandOutcome.WIN),  # Player beats dealer
            (20, 18, False, False, HandOutcome.LOSE),  # Dealer beats player
            (21, 21, False, False, HandOutcome.PUSH),  # Player ties with dealer
            (18, 22, False, False, HandOutcome.LOSE),  # Player busts
            (22, 20, False, False, HandOutcome.WIN),  # Dealer busts
            (22, 22, False, False, HandOutcome.LOSE),  # Both bust; player still loses
            (19, 19, False, False, HandOutcome.PUSH),  # Tie on lower values
            (21, 21, True, False, HandOutcome.LOSE),  # Dealer has Blackjack, player ties
            (21, 21, False, True, HandOutcome.WIN),  # Player has Blackjack, dealer ties
            (21, 21, True, True, HandOutcome.PUSH),  # Both have Blackjack, push
            (21, 22, True, False, HandOutcome.LOSE),  # Dealer has Blackjack, player busts
            (22, 21, False, True, HandOutcome.WIN),  # Player has Blackjack, dealer busts
        ]
    )
    def test_determine_outcome(self, dealer_sum, player_sum, dealer_blackjack, player_blackjack, expected_outcome):
        result = BlackjackModel._determine_outcome(dealer_sum, player_sum, dealer_blackjack, player_blackjack)
        assert result == expected_outcome

    @pytest.mark.parametrize('test_input, expected_output', (
            ([Card('3', 'C'), Card('3', 'C')], 17),
            ([Card('5', 'C'), Card('K', 'C'), Card('Q', 'C')], 25)))
    def test_resolve_dealer_turn(self, test_input, expected_output):
        mock_game = BlackjackModel(GameConfigs)
        # mock_game.players = generate_test_players()
        mock_game.resolve_dealer_turn(test_input)
        assert mock_game.dealer_sum == expected_output



