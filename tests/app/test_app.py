import pytest
from cards.app import app
from cards.database.models import User
from cards.database.database import db


class TestApp:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def cleanup_db(self):
        yield  # The yield is just a placeholder here to indicate the point where the test will run.
        user = User.query.filter_by(username="test_user").first()
        if user:
            db.session.delete(user)
            db.session.commit()

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

    def test_register_post_success(self, client, cleanup_db):
        data = {'email': 'fakeemail123@gmail.com', 'username': 'test_user', 'password': 'password',
                'confirm_password': 'password'}
        response = client.post('/register', data=data)
        assert response.status_code == 302

    def test_register_post_fails_on_existing_user(self, client, cleanup_db):
        data = {'email': 'fakeemail123@gmail.com', 'username': 'test_user', 'password': 'password',
                'confirm_password': 'password'}
        register_1 = client.post('/register', data=data)
        register_2 = client.post('/register', data=data)
        assert register_1.status_code == 302
        assert register_2.status_code == 400

    def test_register_post_invalid_data(self, client):
        data = {'email': 'fakeemail123@gmail.com', 'password': 'password'}
        response = client.post('/register', data=data)
        assert response.status_code == 400

    def test_login_get(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_login_post_success(self, client, cleanup_db):
        register_data = {'email': 'fakeemail123@gmail.com', 'username': 'test_user', 'password': 'password',
                         'confirm_password': 'password'}
        client.post('/register', data=register_data)

        login_data = {'email': 'fakeemail123@gmail.com', 'password': 'password'}
        response = client.post('/login', data=login_data)
        assert response.status_code == 302

    def test_login_post_invalid_data(self, client):
        data = {'email': 'bad_email_syntax', 'password': 'password'}
        response = client.post('/login', data=data)
        assert response.status_code == 400

    def test_login_post_bad_username_and_password(self, client):
        data = {'email': 'test@example.com', 'password': 'password'}
        response = client.post('/login', data=data)
        assert response.status_code == 401
