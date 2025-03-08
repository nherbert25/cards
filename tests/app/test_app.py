import pytest
from cards.app import app


class TestApp:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    def test_home(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b"Welcome to our demo web page!" in response.data
        assert b"Blackjack" in response.data
        assert b"Register" in response.data
        assert b"Login" in response.data

        response = client.get('/home')
        assert response.status_code == 200
        assert b"Welcome to our demo web page!" in response.data
        assert b"Blackjack" in response.data
        assert b"Register" in response.data
        assert b"Login" in response.data

    def test_blackjack(self, client):
        response = client.get('/blackjack')
        assert response.status_code == 200
        assert b"<title>Blackjack</title>" in response.data

    def test_register_get(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    # TODO: change this test to actually register a user (right now it returns 200 even though it doesn't even
    #  contain the correct data to create an account)
    def test_register_post(self, client):
        data = {'email': 'fakeemail123@gmail.com', 'password': 'password'}
        response = client.post('/register', data=data)
        assert response.status_code == 200

    def test_login_get(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    # TODO: make tests create in memory DBs
    def test_login_post_success(self, client):
        data = {'email': 'fakeemail123@gmail.com', 'password': 'password'}
        response = client.post('/login', data=data)
        assert response.status_code == 302

    def test_login_post_invalid_data(self, client):
        data = {'email': 'bad_email_syntax', 'password': 'password'}
        response = client.post('/login', data=data)
        assert response.status_code == 400

    def test_login_post_bad_username_and_password(self, client):
        data = {'email': 'test@example.com', 'password': 'password'}
        response = client.post('/login', data=data)
        assert response.status_code == 401
