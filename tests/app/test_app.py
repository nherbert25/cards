import pytest
from cards.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to our demo web page!" in response.data
    assert b"Blackjack" in response.data
    assert b"Register" in response.data
    assert b"Login" in response.data

# TODO: add test that when you click the home button it takes you to that url
# TODO: add test that when you click the blackjack button it takes you to that url
