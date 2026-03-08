import pytest
from cards.app_setup import socketio
from cards.app import app
from cards.blackjack.routes import get_blackjack_controller, blackjack_controller


class TestBlackjackRoutesAdvanced:
    @pytest.fixture
    def socket_client(self, mocker):
        # Reset global controller
        import cards.blackjack.routes as routes_module
        routes_module.blackjack_controller = None

        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)

        client = socketio.test_client(app)
        yield client
        client.disconnect()

    @pytest.fixture
    def http_client(self, mocker):
        # Reset global controller
        import cards.blackjack.routes as routes_module
        routes_module.blackjack_controller = None

        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)

        client = app.test_client()
        yield client

    def test_get_blackjack_controller_creates_instance(self, mocker):
        import cards.blackjack.routes as routes_module
        routes_module.blackjack_controller = None

        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)

        controller = get_blackjack_controller()
        assert controller is not None
        assert routes_module.blackjack_controller is not None

    def test_get_blackjack_controller_returns_same_instance(self, mocker):
        import cards.blackjack.routes as routes_module
        routes_module.blackjack_controller = None

        mocker.patch('cards.blackjack.player_model.Player._get_coins_from_db', return_value=500)
        mocker.patch('cards.blackjack.player_model.Player._add_new_user_to_blackjack_table', return_value=None)

        controller1 = get_blackjack_controller()
        controller2 = get_blackjack_controller()
        assert controller1 is controller2

    def test_blackjack_route_returns_200(self, http_client):
        response = http_client.get('/blackjack')
        assert response.status_code == 200

    def test_blackjack_route_starts_game(self, http_client, mocker):
        response = http_client.get('/blackjack')

        # Verify game was started
        import cards.blackjack.routes as routes_module
        assert routes_module.blackjack_controller.blackjack_model.game_exists is True

    def test_socketio_hit_emits_update(self, socket_client, mocker):
        # Start game first
        socket_client.emit('new_game')
        socket_client.get_received()  # Clear queue

        # Get a valid player ID
        import cards.blackjack.routes as routes_module
        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])

        socket_client.emit('hit', player_id)
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'update_page_data' for msg in received)

    def test_socketio_stay_emits_update(self, socket_client, mocker):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module
        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])

        socket_client.emit('stay', player_id)
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'update_page_data' for msg in received)

    def test_socketio_double_down_emits_update(self, socket_client, mocker):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module
        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])

        socket_client.emit('double_down', player_id)
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'update_page_data' for msg in received)

    def test_socketio_split_pair_emits_player_added_hand(self, socket_client, mocker):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module
        from cards.blackjack.hand_model import Hand
        from cards.blackjack.card_model import Card

        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])
        player = routes_module.blackjack_controller.blackjack_model.get_player(player_id)

        # Give player a splittable hand
        player.hands[0] = Hand([Card('K', 'H'), Card('K', 'D')])

        socket_client.emit('split_pair', player_id)
        received = socket_client.get_received()

        assert any(msg['name'] == 'player_added_hand' for msg in received)
        assert any(msg['name'] == 'update_page_data' for msg in received)

    def test_socketio_new_game_emits_rebuild(self, socket_client):
        socket_client.emit('new_game')
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'rebuild_entire_page' for msg in received)

    def test_socketio_rebuild_entire_page(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        socket_client.emit('rebuild_entire_page')
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'rebuild_entire_page' for msg in received)

    def test_socketio_request_game_data(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        socket_client.emit('request_game_data')
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'request_game_data' for msg in received)

    def test_socketio_update_page_data_event(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        socket_client.emit('update_page_data')
        received = socket_client.get_received()

        assert len(received) > 0
        assert any(msg['name'] == 'update_page_data' for msg in received)

    def test_socketio_connection_message(self, socket_client, capsys):
        # Connection happens in fixture, check that handler runs
        assert socket_client.is_connected()

    def test_multiple_hits_in_sequence(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module
        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])
        player = routes_module.blackjack_controller.blackjack_model.get_player(player_id)

        initial_cards = len(player.get_hand(0).cards)

        socket_client.emit('hit', player_id)
        socket_client.get_received()

        socket_client.emit('hit', player_id)
        socket_client.get_received()

        socket_client.emit('hit', player_id)
        socket_client.get_received()

        assert len(player.get_hand(0).cards) == initial_cards + 3

    def test_all_players_stay_triggers_dealer_resolution(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module

        # Make all players stay
        for player_id in routes_module.blackjack_controller.blackjack_model.players.keys():
            socket_client.emit('stay', str(player_id))
            socket_client.get_received()

        # After all players stay, dealer should have resolved
        dealer = routes_module.blackjack_controller.blackjack_model.dealer
        assert dealer.cards[0].hidden is False  # Dealer's hidden card should be revealed

    def test_hit_with_hand_index_parameter(self, socket_client):
        socket_client.emit('new_game')
        socket_client.get_received()

        import cards.blackjack.routes as routes_module
        from cards.blackjack.hand_model import Hand
        from cards.blackjack.card_model import Card

        player_id = str(list(routes_module.blackjack_controller.blackjack_model.players.keys())[0])
        player = routes_module.blackjack_controller.blackjack_model.get_player(player_id)

        # Add a second hand
        player.add_hand(Hand([Card('5', 'H'), Card('6', 'D')]))

        initial_cards_hand0 = len(player.get_hand(0).cards)
        initial_cards_hand1 = len(player.get_hand(1).cards)

        socket_client.emit('hit', {'user_id': player_id, 'hand_index': 1})
        socket_client.get_received()

        # Only second hand should have new card
        assert len(player.get_hand(0).cards) == initial_cards_hand0
        assert len(player.get_hand(1).cards) == initial_cards_hand1 + 1

    def test_button_count_increments(self, socket_client):
        socket_client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
        received = socket_client.get_received()

        assert len(received) > 0
        assert received[0]['name'] == 'update_button_counts'
        assert received[0]['args'][0]['counts']['button1'] == 1
