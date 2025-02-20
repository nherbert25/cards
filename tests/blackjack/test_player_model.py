import pytest

from tests.blackjack.test_configs import example_hand_total_KQ, example_hand_total_KK, example_hand_KQ, example_hand_KK, example_hand_total_QQQ
from cards.blackjack.hand_model import Hand
from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card


class TestPlayerModel:
    @pytest.fixture
    def mock_player(self, mocker):
        mock_player = Player()
        # mock_player.add_hand(example_hand_total_KK)
        # mock_player.add_hand(example_hand_total_KQ)
        return mock_player

    # TODO: Test is breaking, I believe it's because example_hand_total_KK is one instance, manipulated across tests.
    @pytest.mark.parametrize('test_input, expected_output', (
            (example_hand_total_KK, 2),
            (example_hand_total_KQ, 1),

    ))
    def test_split_pair(self, test_input, expected_output, mock_player):
        # print(f"Hand before adding: {test_input.cards}")
        mock_player.add_hand(test_input)
        mock_player.split_pair(0)
        assert len(mock_player.hands) == expected_output
