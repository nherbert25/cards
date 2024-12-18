import pytest
from cards.app import app, socketio
from tests.blackjack.test_configs import initial_game_blackjack


class TestBlackjackRoutes:
    @pytest.fixture
    def client(self, mocker):
        client = socketio.test_client(app)
        mock_create_game = mocker.patch('cards.blackjack.controller.BlackjackController.serialize_blackjack_data',
                                        return_value=initial_game_blackjack)
        yield client
        client.disconnect()

    # TODO: add test for http route /blackjack
    def test_blackjack(self, client):
        pass

    def test_socketio_connection(self, client):
        assert client.is_connected()

    def test_press_socket_testing_buttons(self, client):
        client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
        client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
        client.emit('press_socket_testing_buttons', {'buttonNumber': 2})
        received = client.get_received()

        assert len(received) > 0
        assert received[0]['name'] == 'update_button_counts'
        assert received[0]['args'][0]['counts'] == {'button1': 1, 'button2': 0}
        assert received[1]['args'][0]['counts'] == {'button1': 2, 'button2': 0}
        assert received[2]['args'][0]['counts'] == {'button1': 2, 'button2': 1}

    def test_update_page_data(self, client, mocker):
        client.emit('update_page_data')
        received = client.get_received()

        assert len(received) > 0
        assert received[0]['name'] == 'update_page_data'
        assert received[0]['args'][0]['dealer_cards'] == [
            {'image_path': 'images/playing_cards/BACK.png', 'rank': '0', 'suit': 'None'},
            {'image_path': 'images/playing_cards/8-S.png ', 'rank': '8', 'suit': 'S'}]
        assert received[0]['args'][0]['dealer_sum'] == 8

    def test_hit(self, client, mocker):
        mock_hit = mocker.patch('cards.blackjack.controller.BlackjackController.hit')
        client.emit('hit', '2290c4b3-5f33-498b-85f1-92da8da356b1')
        mock_hit.assert_called_once_with('2290c4b3-5f33-498b-85f1-92da8da356b1')

    def test_stay(self, client, mocker):
        mock_stay = mocker.patch('cards.blackjack.controller.BlackjackController.stay')
        client.emit('stay', '2290c4b3-5f33-498b-85f1-92da8da356b1')
        mock_stay.assert_called_once_with('2290c4b3-5f33-498b-85f1-92da8da356b1')

    def test_new_game(self, client, mocker):
        mock_new_game = mocker.patch('cards.blackjack.controller.BlackjackController.new_game')
        client.emit('new_game')
        mock_new_game.assert_called_once()

    def test_handle_request_game_data(self, client, mocker):
        mock_serialize = mocker.patch('cards.blackjack.controller.BlackjackController.serialize_blackjack_data',
                                      return_value=initial_game_blackjack)
        client.emit('request_game_data')
        received = client.get_received()

        assert len(received) > 0
        assert received[0]['name'] == 'request_game_data'
        assert received[0]['args'][0] == initial_game_blackjack
        mock_serialize.assert_called_once()
