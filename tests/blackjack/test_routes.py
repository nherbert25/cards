import pytest
from cards.app import app, socketio


@pytest.fixture
def client():
    client = socketio.test_client(app)
    yield client
    client.disconnect()


def test_socketio_connection(client):
    assert client.is_connected()


def test_press_socket_testing_buttons(client):
    client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
    client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
    client.emit('press_socket_testing_buttons', {'buttonNumber': 2})
    received = client.get_received()

    assert len(received) > 0
    assert received[0]['name'] == 'update_button_counts'
    assert received[0]['args'][0]['counts'] == {'button1': 1, 'button2': 0}
    assert received[1]['args'][0]['counts'] == {'button1': 2, 'button2': 0}
    assert received[2]['args'][0]['counts'] == {'button1': 2, 'button2': 1}


def test_update_page_data(client):
    client.emit('update_page_data')
    received = client.get_received()

    assert len(received) > 0
    assert received[0]['name'] == 'update_page_data'
    assert received[0]['args'][0]['dealer_cards'] == []
    assert received[0]['args'][0]['dealer_sum'] == 0
    assert received[0]['args'][0]['button1_count'] == 0
    assert received[0]['args'][0]['button2_count'] == 0
    assert received[0]['args'][0]['players_data_object'] == {}