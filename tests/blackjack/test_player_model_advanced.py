import pytest
from uuid import UUID, uuid4
from cards.blackjack.player_model import Player
from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card


class TestPlayerModelAdvanced:
    @pytest.fixture
    def mock_dao(self, mocker):
        mock = mocker.Mock()
        mock.get_user_by_uuid.return_value = None
        mock.add_user_to_database.return_value = None
        mock.update_coins.return_value = None
        return mock

    def test_player_initialization_defaults(self, mock_dao):
        player = Player(dao=mock_dao)
        assert player.user_id is not None
        assert isinstance(player.user_id, UUID)
        assert player.player_name == 'Guest'
        assert player.bet == 50
        assert player.hands == []
        assert player.coins == 500

    def test_player_initialization_with_custom_values(self, mock_dao):
        custom_uuid = uuid4()
        player = Player(
            user_id=custom_uuid,
            player_name='TestPlayer',
            bet=100,
            dao=mock_dao
        )
        assert player.user_id == custom_uuid
        assert player.player_name == 'TestPlayer'
        assert player.bet == 100

    def test_player_repr(self, mock_dao):
        player = Player(player_name='TestPlayer', dao=mock_dao)
        repr_str = repr(player)
        assert 'TestPlayer' in repr_str
        assert str(player.user_id) in repr_str

    def test_get_coins_from_db_when_user_exists(self, mocker):
        mock_dao = mocker.Mock()
        mock_entry = mocker.Mock()
        mock_entry.coins = 750
        mock_dao.get_user_by_uuid.return_value = mock_entry

        player = Player(dao=mock_dao)
        assert player.coins == 750

    def test_get_coins_from_db_when_user_not_exists(self, mock_dao):
        player = Player(dao=mock_dao)
        assert player.coins == 500

    def test_add_new_user_to_blackjack_table_called(self, mock_dao):
        player = Player(dao=mock_dao)
        mock_dao.add_user_to_database.assert_called_once()

    def test_get_hand_valid_index(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand()
        hand2 = Hand()
        player.add_hand(hand1)
        player.add_hand(hand2)

        assert player.get_hand(0) == hand1
        assert player.get_hand(1) == hand2

    def test_get_hand_invalid_index_raises_error(self, mock_dao):
        player = Player(dao=mock_dao)
        player.add_hand(Hand())

        with pytest.raises(IndexError):
            player.get_hand(5)

    def test_add_hand_appends_by_default(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand()
        hand2 = Hand()

        player.add_hand(hand1)
        player.add_hand(hand2)

        assert len(player.hands) == 2
        assert player.hands[0] == hand1
        assert player.hands[1] == hand2

    def test_add_hand_at_specific_index(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand()
        hand2 = Hand()
        hand3 = Hand()

        player.add_hand(hand1)
        player.add_hand(hand2)
        player.add_hand(hand3, index=1)

        assert len(player.hands) == 3
        assert player.hands[0] == hand1
        assert player.hands[1] == hand3
        assert player.hands[2] == hand2

    def test_stay_hand_valid_index(self, mock_dao):
        player = Player(dao=mock_dao)
        hand = Hand()
        player.add_hand(hand)

        assert not hand.has_stayed
        player.stay_hand(0)
        assert hand.has_stayed

    def test_stay_hand_invalid_index_logs_error(self, mock_dao, mocker):
        mock_logging = mocker.patch('cards.blackjack.player_model.logging')
        player = Player(dao=mock_dao)
        player.add_hand(Hand())

        player.stay_hand(5)  # Invalid index
        mock_logging.error.assert_called()

    def test_split_pair_success(self, mock_dao):
        player = Player(dao=mock_dao)
        hand = Hand([Card('K', 'H'), Card('K', 'D')])
        player.add_hand(hand)

        result = player.split_pair(0)

        assert result is True
        assert len(player.hands) == 2
        assert len(player.hands[0].cards) == 1
        assert len(player.hands[1].cards) == 1

    def test_split_pair_failure(self, mock_dao):
        player = Player(dao=mock_dao)
        hand = Hand([Card('K', 'H'), Card('Q', 'D')])
        player.add_hand(hand)

        result = player.split_pair(0)

        assert result is False
        assert len(player.hands) == 1

    def test_split_pair_inserts_at_correct_position(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand([Card('8', 'H'), Card('8', 'D')])
        hand2 = Hand([Card('K', 'H'), Card('Q', 'D')])
        player.add_hand(hand1)
        player.add_hand(hand2)

        player.split_pair(0)

        assert len(player.hands) == 3
        # Original split hand at index 0, new split hand at index 1, original second hand at index 2

    def test_evaluate_round_end_all_wins(self, mock_dao, mocker):
        player = Player(dao=mock_dao)
        hand1 = Hand(bet=50)
        hand1.evaluate_outcome(HandOutcome.WIN)
        hand2 = Hand(bet=50)
        hand2.evaluate_outcome(HandOutcome.WIN)
        player.add_hand(hand1)
        player.add_hand(hand2)

        initial_coins = player.coins
        # Mock _get_coins_from_db to return updated coins value
        mocker.patch.object(player, '_get_coins_from_db', return_value=initial_coins + 100)
        player.evaluate_round_end()

        assert player.coins == initial_coins + 100
        assert 'win' in player.win_or_lose_message.lower()

    def test_evaluate_round_end_all_losses(self, mock_dao, mocker):
        player = Player(dao=mock_dao)
        hand1 = Hand(bet=50)
        hand1.evaluate_outcome(HandOutcome.LOSE)
        hand2 = Hand(bet=50)
        hand2.evaluate_outcome(HandOutcome.LOSE)
        player.add_hand(hand1)
        player.add_hand(hand2)

        initial_coins = player.coins
        # Mock _get_coins_from_db to return updated coins value
        mocker.patch.object(player, '_get_coins_from_db', return_value=initial_coins - 100)
        player.evaluate_round_end()

        assert player.coins == initial_coins - 100
        assert 'lose' in player.win_or_lose_message.lower()

    def test_evaluate_round_end_push(self, mock_dao):
        player = Player(dao=mock_dao)
        hand = Hand(bet=50)
        hand.evaluate_outcome(HandOutcome.PUSH)
        player.add_hand(hand)

        initial_coins = player.coins
        player.evaluate_round_end()

        assert player.coins == initial_coins
        assert 'Push' in player.win_or_lose_message

    def test_evaluate_round_end_mixed_outcomes(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand(bet=50)
        hand1.evaluate_outcome(HandOutcome.WIN)
        hand2 = Hand(bet=50)
        hand2.evaluate_outcome(HandOutcome.LOSE)
        player.add_hand(hand1)
        player.add_hand(hand2)

        initial_coins = player.coins
        player.evaluate_round_end()

        assert player.coins == initial_coins  # +50 -50 = 0

    def test_evaluate_round_end_pushes_coins_to_db(self, mock_dao):
        player = Player(dao=mock_dao)
        hand = Hand(bet=50)
        hand.evaluate_outcome(HandOutcome.WIN)
        player.add_hand(hand)

        player.evaluate_round_end()

        mock_dao.update_coins.assert_called_once_with(str(player.user_id), 50)

    def test_new_round_resets_hands(self, mock_dao):
        player = Player(dao=mock_dao)
        player.add_hand(Hand())
        player.add_hand(Hand())

        assert len(player.hands) == 2

        player.new_round(50)

        assert len(player.hands) == 0

    def test_new_round_resets_bet(self, mock_dao):
        player = Player(dao=mock_dao)
        player.bet = 100

        player.new_round(75)

        assert player.bet == 75

    def test_new_round_resets_message(self, mock_dao):
        player = Player(dao=mock_dao)
        player.win_or_lose_message = 'You win!'

        player.new_round(50)

        assert 'Current bet: 50' in player.win_or_lose_message

    def test_to_dict_contains_all_fields(self, mock_dao):
        player = Player(player_name='TestPlayer', dao=mock_dao)
        player.add_hand(Hand())

        result = player.to_dict()

        assert 'player_name' in result
        assert 'hands' in result
        assert 'bet' in result
        assert 'coins' in result
        assert 'win_or_lose_message' in result

    def test_to_dict_serializes_hands(self, mock_dao):
        player = Player(dao=mock_dao)
        hand1 = Hand([Card('K', 'H'), Card('Q', 'D')])
        hand2 = Hand([Card('A', 'H'), Card('5', 'D')])
        player.add_hand(hand1)
        player.add_hand(hand2)

        result = player.to_dict()

        assert len(result['hands']) == 2
        assert isinstance(result['hands'][0], dict)
        assert isinstance(result['hands'][1], dict)

    def test_to_dict_values(self, mock_dao):
        player = Player(
            player_name='TestPlayer',
            bet=100,
            dao=mock_dao
        )

        result = player.to_dict()

        assert result['player_name'] == 'TestPlayer'
        assert result['bet'] == 100
        assert result['coins'] == 500

    def test_player_multiple_hands_management(self, mock_dao):
        player = Player(dao=mock_dao)

        for i in range(5):
            player.add_hand(Hand())

        assert len(player.hands) == 5

        for i in range(5):
            assert isinstance(player.get_hand(i), Hand)
