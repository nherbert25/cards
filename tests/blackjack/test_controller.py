import pytest
from uuid import UUID
from cards.blackjack.controller import BlackjackController
from cards.blackjack.player_model import Player
from cards.blackjack.hand_model import Hand
from cards.blackjack.card_model import Card


class TestBlackjackController:
    @pytest.fixture
    def app_context(self):
        from cards.app import app
        with app.app_context():
            yield

    @pytest.fixture
    def controller(self, mocker):
        # Mock database operations to avoid DB dependencies
        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)
        return BlackjackController()

    def test_controller_initialization(self, controller):
        assert controller is not None
        assert controller.blackjack_model is not None
        assert controller.counts == {'button1': 0, 'button2': 0}

    def test_controller_has_default_players(self, controller):
        assert len(controller.blackjack_model.players) == 3
        player_names = [player.player_name for player in controller.blackjack_model.players.values()]
        assert 'Taylor' in player_names
        assert 'Nate' in player_names
        assert 'Travis' in player_names

    def test_serialize_blackjack_data_structure(self, controller, mocker):
        # Start a new game to populate data
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        data = controller.serialize_blackjack_data()

        # Check top-level structure
        assert 'BLACKJACK_MAX' in data
        assert 'dealer' in data
        assert 'button_counts' in data
        assert 'players' in data

        # Check dealer structure
        assert 'cards' in data['dealer']
        assert 'sum' in data['dealer']
        assert isinstance(data['dealer']['cards'], list)
        assert isinstance(data['dealer']['sum'], int)

        # Check button counts
        assert data['button_counts']['button1'] == 0
        assert data['button_counts']['button2'] == 0

        # Check players structure
        assert isinstance(data['players'], dict)
        assert len(data['players']) == 3

    def test_serialize_blackjack_data_dealer_cards(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        data = controller.serialize_blackjack_data()
        dealer_cards = data['dealer']['cards']

        assert len(dealer_cards) >= 2  # Dealer starts with 2 cards
        for card in dealer_cards:
            assert 'rank' in card
            assert 'suit' in card
            assert 'image_path' in card

    def test_serialize_blackjack_data_players(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        data = controller.serialize_blackjack_data()

        for player_id, player_data in data['players'].items():
            assert 'player_name' in player_data
            assert 'hands' in player_data
            assert 'bet' in player_data
            assert 'coins' in player_data
            assert 'win_or_lose_message' in player_data

    def test_hit_method(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        # Get a player UUID
        player_id = str(list(controller.blackjack_model.players.keys())[0])
        player = controller.blackjack_model.get_player(player_id)
        initial_card_count = len(player.get_hand(0).cards)

        controller.hit(player_id, 0)

        assert len(player.get_hand(0).cards) == initial_card_count + 1

    def test_stay_method(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        player_id = str(list(controller.blackjack_model.players.keys())[0])
        player = controller.blackjack_model.get_player(player_id)

        assert not player.get_hand(0).has_stayed

        controller.stay(player_id, 0)

        assert player.get_hand(0).has_stayed

    def test_double_down_method(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        player_id = str(list(controller.blackjack_model.players.keys())[0])
        player = controller.blackjack_model.get_player(player_id)
        initial_bet = player.get_hand(0).bet
        initial_card_count = len(player.get_hand(0).cards)

        controller.double_down(player_id, 0)

        assert player.get_hand(0).bet == initial_bet * 2
        assert len(player.get_hand(0).cards) == initial_card_count + 1
        assert player.get_hand(0).has_stayed

    def test_split_pair_success(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        player_id = str(list(controller.blackjack_model.players.keys())[0])
        player = controller.blackjack_model.get_player(player_id)

        # Create a splittable hand
        player.hands[0] = Hand([Card('K', 'H'), Card('K', 'D')])

        assert len(player.hands) == 1
        result = controller.split_pair(player_id, 0)

        assert result is True
        assert len(player.hands) == 2

    def test_split_pair_failure(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        player_id = str(list(controller.blackjack_model.players.keys())[0])
        player = controller.blackjack_model.get_player(player_id)

        # Create a non-splittable hand
        player.hands[0] = Hand([Card('K', 'H'), Card('Q', 'D')])

        assert len(player.hands) == 1
        result = controller.split_pair(player_id, 0)

        assert result is False
        assert len(player.hands) == 1

    def test_new_game_resets_game_state(self, controller, mocker):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        # Modify game state
        player_id = str(list(controller.blackjack_model.players.keys())[0])
        controller.hit(player_id, 0)

        # Start new game
        controller.new_game()

        # Verify reset
        for player in controller.blackjack_model.players.values():
            assert len(player.hands) == 1
            assert len(player.get_hand(0).cards) == 2

    def test_blackjack_method_starts_game_if_not_exists(self, controller, mocker, app_context):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        mocker.patch('cards.blackjack.controller.render_template', return_value='<html></html>')
        assert controller.blackjack_model.game_exists is False

        result = controller.blackjack()

        assert controller.blackjack_model.game_exists is True
        assert result == '<html></html>'

    def test_update_page_data_returns_rendered_template(self, controller, mocker, app_context):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        mocker.patch('cards.blackjack.controller.render_template', return_value='<html></html>')
        controller.blackjack_model.start_new_game()

        result = controller.update_page_data()
        assert result == '<html></html>'

    def test_hit_with_invalid_user_id(self, controller, mocker, app_context):
        mocker.patch.object(controller.blackjack_model.deck, 'shuffle')
        controller.blackjack_model.start_new_game()

        # Should handle gracefully - returns None when player not found
        result = controller.hit('invalid-uuid', 0)
        assert result is None

    def test_controller_button_counts_increment(self, controller):
        assert controller.counts['button1'] == 0
        assert controller.counts['button2'] == 0

        controller.counts['button1'] += 1
        controller.counts['button2'] += 3

        assert controller.counts['button1'] == 1
        assert controller.counts['button2'] == 3
