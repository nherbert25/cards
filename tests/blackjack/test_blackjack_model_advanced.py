import pytest
from uuid import UUID
from cards.blackjack.blackjack_model import BlackjackModel, GameConfigs, get_default_players
from cards.blackjack.player_model import Player
from cards.blackjack.hand_model import Hand, HandOutcome
from cards.blackjack.card_model import Card
from cards.blackjack.deck_model import Deck


class TestBlackjackModelAdvanced:
    @pytest.fixture
    def mock_game(self, mocker):
        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
        return BlackjackModel(GameConfigs, get_default_players())

    def test_start_new_game_creates_dealer_hand(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        assert mock_game.dealer is None

        mock_game.start_new_game()

        assert mock_game.dealer is not None
        assert len(mock_game.dealer.cards) == 2
        assert mock_game.dealer.cards[0].hidden is True
        assert mock_game.dealer.cards[1].hidden is False

    def test_start_new_game_deals_cards_to_all_players(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        for player in mock_game.players.values():
            assert len(player.hands) == 1
            assert len(player.get_hand(0).cards) == 2

    def test_start_new_game_sets_game_exists_flag(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        assert mock_game.game_exists is False

        mock_game.start_new_game()

        assert mock_game.game_exists is True

    def test_start_new_game_shuffles_deck(self, mock_game, mocker):
        # Patch the Deck class's shuffle method since start_new_game creates a new Deck
        mock_shuffle = mocker.patch('cards.blackjack.deck_model.Deck.shuffle')

        mock_game.start_new_game()

        mock_shuffle.assert_called_once()

    def test_hit_adds_card_to_player_hand(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        initial_card_count = len(player.get_hand(0).cards)

        mock_game.hit(player, 0)

        assert len(player.get_hand(0).cards) == initial_card_count + 1

    def test_stay_marks_hand_as_stayed(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        assert not player.get_hand(0).has_stayed

        mock_game.stay(player, 0)

        assert player.get_hand(0).has_stayed

    def test_double_down_doubles_bet(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        initial_bet = player.get_hand(0).bet

        mock_game.double_down(player, 0)

        assert player.get_hand(0).bet == initial_bet * 2

    def test_double_down_marks_hand_as_stayed(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]

        mock_game.double_down(player, 0)

        assert player.get_hand(0).has_stayed

    def test_double_down_hits_once(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        initial_card_count = len(player.get_hand(0).cards)

        mock_game.double_down(player, 0)

        assert len(player.get_hand(0).cards) == initial_card_count + 1

    def test_split_pair_with_valid_pair(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        player.hands[0] = Hand([Card('K', 'H'), Card('K', 'D')])

        result = mock_game.split_pair(player, 0)

        assert result is True
        assert len(player.hands) == 2

    def test_split_pair_with_invalid_pair(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        player.hands[0] = Hand([Card('K', 'H'), Card('Q', 'D')])

        result = mock_game.split_pair(player, 0)

        assert result is False
        assert len(player.hands) == 1

    def test_split_pair_deals_card_to_each_split_hand(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        player = list(mock_game.players.values())[0]
        player.hands[0] = Hand([Card('8', 'H'), Card('8', 'D')])

        mock_game.split_pair(player, 0)

        assert len(player.hands[0].cards) == 2
        assert len(player.hands[1].cards) == 2

    def test_get_player_returns_correct_player(self, mock_game):
        player_uuid = list(mock_game.players.keys())[0]

        result = mock_game.get_player(str(player_uuid))

        assert result is not None
        assert result.user_id == player_uuid

    def test_get_player_returns_none_for_invalid_uuid(self, mock_game):
        result = mock_game.get_player('invalid-uuid-string')

        assert result is None

    def test_if_all_hands_have_stayed_all_stayed(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        for player in mock_game.players.values():
            for hand in player.hands:
                hand.stay()

        assert mock_game._if_all_hands_have_stayed() is True

    def test_if_all_hands_have_stayed_one_not_stayed(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        # Stay all but one
        players = list(mock_game.players.values())
        for player in players[:-1]:
            player.get_hand(0).stay()

        assert mock_game._if_all_hands_have_stayed() is False

    def test_resolve_dealer_turn_flips_hidden_card(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        # Mock push_coins_to_db to avoid database operations
        for player in mock_game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)
            player.get_hand(0).stay()

        assert mock_game.dealer.cards[0].hidden is True

        mock_game._resolve_dealer_turn(mock_game.dealer)

        assert mock_game.dealer.cards[0].hidden is False

    def test_resolve_dealer_turn_draws_until_threshold(self, mock_game, mocker):
        mocker.patch.object(mock_game.deck, 'shuffle')
        mock_game.start_new_game()

        # Mock push_coins_to_db to avoid database operations
        for player in mock_game.players.values():
            mocker.patch.object(player, '_push_coins_to_db', return_value=None)

        # Force dealer to have low hand
        mock_game.dealer.cards = [Card('2', 'H'), Card('3', 'D')]

        # Ensure deck has cards
        mock_game.deck = Deck()

        mock_game._resolve_dealer_turn(mock_game.dealer)

        assert mock_game.dealer.sum >= BlackjackModel.DEALER_HOLD_THRESHOLD or mock_game.dealer.has_bust

    def test_determine_outcome_player_wins_higher_sum(self, mock_game):
        result = mock_game._determine_outcome(18, 20, False, False)
        assert result == HandOutcome.WIN

    def test_determine_outcome_dealer_wins_higher_sum(self, mock_game):
        result = mock_game._determine_outcome(20, 18, False, False)
        assert result == HandOutcome.LOSE

    def test_determine_outcome_push_same_sum(self, mock_game):
        result = mock_game._determine_outcome(19, 19, False, False)
        assert result == HandOutcome.PUSH

    def test_determine_outcome_player_busts(self, mock_game):
        result = mock_game._determine_outcome(18, 22, False, False)
        assert result == HandOutcome.LOSE

    def test_determine_outcome_dealer_busts(self, mock_game):
        result = mock_game._determine_outcome(22, 20, False, False)
        assert result == HandOutcome.WIN

    def test_determine_outcome_both_bust(self, mock_game):
        result = mock_game._determine_outcome(22, 22, False, False)
        assert result == HandOutcome.LOSE

    def test_determine_outcome_dealer_blackjack_player_21(self, mock_game):
        result = mock_game._determine_outcome(21, 21, True, False)
        assert result == HandOutcome.LOSE

    def test_determine_outcome_player_blackjack_dealer_21(self, mock_game):
        result = mock_game._determine_outcome(21, 21, False, True)
        assert result == HandOutcome.WIN

    def test_determine_outcome_both_blackjack(self, mock_game):
        result = mock_game._determine_outcome(21, 21, True, True)
        assert result == HandOutcome.PUSH

    def test_game_configs_defaults(self):
        assert GameConfigs.NUMBER_OF_DECKS == 1
        assert GameConfigs.BLACKJACK_RATIO == 1.5
        assert GameConfigs.DEALER_HITS_ON_SOFT_17 is False
        assert GameConfigs.ALLOW_SPLIT_PAIR is True

    def test_get_default_players_returns_three_players(self, mocker):
        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
        players = get_default_players()
        assert len(players) == 3

    def test_get_default_players_returns_dict_keyed_by_uuid(self, mocker):
        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
        players = get_default_players()
        for uuid, player in players.items():
            assert isinstance(uuid, UUID)
            assert player.user_id == uuid

    def test_blackjack_max_constant(self):
        assert BlackjackModel.BLACKJACK_MAX == 21

    def test_dealer_hold_threshold_constant(self):
        assert BlackjackModel.DEALER_HOLD_THRESHOLD == 17

    def test_double_down_ratio_constant(self):
        assert BlackjackModel.DOUBLE_DOWN_RATIO == 2
