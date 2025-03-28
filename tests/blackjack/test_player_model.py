import pytest

from cards.database.blackjack_table_DAO import BlackjackTableDAO
from tests.blackjack.test_configs import example_hand_total_KQ, example_hand_total_KK, example_hand_KQ, example_hand_KK, \
    example_hand_total_QQQ
from cards.blackjack.hand_model import Hand
from cards.blackjack.player_model import Player
from cards.blackjack.card_model import Card
from cards.app_setup import create_app, db  # Import your Flask app factory and db


class TestPlayerModel:

    @pytest.fixture
    def mock_db_session(mocker):
        return mocker.Mock()

    @pytest.fixture
    def mock_player(mock_db_session, mocker):
        """Mock Player instance with a mocked database session."""
        """Create a real Player instance but mock only its database dependencies."""
        from cards.blackjack.player_model import Player

        # mocker.patch.object(Player, "coins", new=1000)
        mocker.patch.object(Player, "_get_coins_from_db", return_value=1000)  # Mocks a method, not an attribute
        mocker.patch.object(Player, "_add_new_user_to_blackjack_table",
                            return_value=None)  # Mocks a method, not an attribute

        mock_player = Player()

        return mock_player

    @pytest.mark.parametrize('hand_name, expected_output', (
            ("KK", 2),
            ("KQ", 1),

    ))
    def test_split_pair(self, hand_factory, hand_name, expected_output, mock_player):
        mock_player.add_hand(hand_factory(hand_name))
        mock_player.split_pair(0)
        assert len(mock_player.hands) == expected_output
