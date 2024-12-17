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
    # Emit an event and test the response
    client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
    received = client.get_received()
    assert len(received) > 0
    assert received[0]['name'] == 'update_button_counts'
    assert received[0]['args'][0]['counts'] == {'button1': 1, 'button2': 0}

    # Emit another event and test the response
    client.emit('press_socket_testing_buttons', {'buttonNumber': 1})
    received = client.get_received()
    assert received[0]['args'][0]['counts'] == {'button1': 2, 'button2': 0}

    # Emit another event and test the response
    client.emit('press_socket_testing_buttons', {'buttonNumber': 2})
    received = client.get_received()
    assert received[0]['args'][0]['counts'] == {'button1': 2, 'button2': 1}
