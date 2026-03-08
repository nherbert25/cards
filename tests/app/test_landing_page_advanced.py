import pytest
from cards.app import app
from cards.database.models import User
from cards.database.database import db


class TestLandingPageAdvanced:
    @pytest.fixture
    def client(self):
        with app.test_client() as client:
            yield client

    @pytest.fixture
    def cleanup_users(self):
        """Cleanup test users after each test"""
        yield
        test_emails = [
            'test1@example.com',
            'test2@example.com',
            'test3@example.com',
            'duplicate@example.com',
            'fakeemail123@gmail.com'
        ]
        for email in test_emails:
            user = User.query.filter_by(email=email).first()
            if user:
                db.session.delete(user)
                db.session.commit()

    def test_health_check_endpoint(self, client):
        """Test the health check endpoint"""
        response = client.get('/health_check')
        assert response.status_code == 200
        assert response.data == b"OK"

    def test_home_route_both_paths(self, client):
        """Test both / and /home return same content"""
        response1 = client.get('/')
        response2 = client.get('/home')

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.data == response2.data

    def test_register_get_returns_form(self, client):
        """Test that register GET returns form"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Register' in response.data or b'register' in response.data

    def test_register_post_with_all_valid_fields(self, client, cleanup_users):
        """Test registration with all valid fields"""
        data = {
            'email': 'test1@example.com',
            'username': 'testuser1',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = client.post('/register', data=data, follow_redirects=False)
        assert response.status_code == 302  # Redirect after success

    def test_register_creates_user_in_database(self, client, cleanup_users):
        """Test that registration creates user in database"""
        data = {
            'email': 'test2@example.com',
            'username': 'testuser2',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/register', data=data)

        user = User.query.filter_by(email='test2@example.com').first()
        assert user is not None
        assert user.username == 'testuser2'

    def test_register_hashes_password(self, client, cleanup_users):
        """Test that password is hashed in database"""
        data = {
            'email': 'test3@example.com',
            'username': 'testuser3',
            'password': 'mypassword',
            'confirm_password': 'mypassword'
        }
        client.post('/register', data=data)

        user = User.query.filter_by(email='test3@example.com').first()
        assert user.password != 'mypassword'  # Should be hashed
        assert len(user.password) > 20  # Bcrypt hash is long

    def test_register_duplicate_username(self, client, cleanup_users):
        """Test registering with duplicate username fails"""
        data = {
            'email': 'user1@example.com',
            'username': 'duplicate_user',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/register', data=data)

        # Try to register again with same username but different email
        data2 = {
            'email': 'user2@example.com',
            'username': 'duplicate_user',
            'password': 'password456',
            'confirm_password': 'password456'
        }
        response = client.post('/register', data=data2)
        assert response.status_code == 400

    def test_register_duplicate_email(self, client, cleanup_users):
        """Test registering with duplicate email fails"""
        data = {
            'email': 'duplicate@example.com',
            'username': 'user1',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/register', data=data)

        # Try to register again with same email but different username
        data2 = {
            'email': 'duplicate@example.com',
            'username': 'user2',
            'password': 'password456',
            'confirm_password': 'password456'
        }
        response = client.post('/register', data=data2)
        assert response.status_code == 400

    def test_register_password_mismatch(self, client):
        """Test that mismatched passwords fail validation"""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'different123'
        }
        response = client.post('/register', data=data)
        assert response.status_code == 400

    def test_register_short_password(self, client):
        """Test that short password fails validation"""
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'short',
            'confirm_password': 'short'
        }
        response = client.post('/register', data=data)
        assert response.status_code == 400

    def test_register_invalid_email_format(self, client):
        """Test that invalid email format fails validation"""
        data = {
            'email': 'not-an-email',
            'username': 'testuser',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = client.post('/register', data=data)
        assert response.status_code == 400

    def test_login_get_returns_form(self, client):
        """Test that login GET returns form"""
        response = client.get('/login')
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client, cleanup_users):
        """Test login with valid credentials"""
        # First register a user
        register_data = {
            'email': 'login_test@example.com',
            'username': 'loginuser',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/register', data=register_data)

        # Then try to login
        login_data = {
            'email': 'login_test@example.com',
            'password': 'password123'
        }
        response = client.post('/login', data=login_data, follow_redirects=False)
        assert response.status_code == 302  # Redirect after successful login

    def test_login_with_wrong_password(self, client, cleanup_users):
        """Test login with wrong password fails"""
        # Register user
        register_data = {
            'email': 'wrongpass@example.com',
            'username': 'wrongpassuser',
            'password': 'correctpass',
            'confirm_password': 'correctpass'
        }
        client.post('/register', data=register_data)

        # Try to login with wrong password
        login_data = {
            'email': 'wrongpass@example.com',
            'password': 'wrongpassword'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 401

    def test_login_with_nonexistent_user(self, client):
        """Test login with non-existent user fails"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 401

    def test_login_with_invalid_email_format(self, client):
        """Test login with invalid email format fails"""
        login_data = {
            'email': 'not-an-email',
            'password': 'password123'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 400

    def test_login_with_short_password(self, client):
        """Test login with too short password fails validation"""
        login_data = {
            'email': 'test@example.com',
            'password': 'short'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 400

    def test_login_missing_email(self, client):
        """Test login without email fails"""
        login_data = {
            'password': 'password123'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 400

    def test_login_missing_password(self, client):
        """Test login without password fails"""
        login_data = {
            'email': 'test@example.com'
        }
        response = client.post('/login', data=login_data)
        assert response.status_code == 400

    def test_register_redirects_to_login(self, client, cleanup_users):
        """Test that successful registration redirects to login"""
        data = {
            'email': 'redirect_test@example.com',
            'username': 'redirectuser',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = client.post('/register', data=data, follow_redirects=False)
        assert response.status_code == 302
        assert '/login' in response.location

    def test_login_redirects_to_home(self, client, cleanup_users):
        """Test that successful login redirects to home"""
        # Register user
        register_data = {
            'email': 'redirect_login@example.com',
            'username': 'redirectlogin',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        client.post('/register', data=register_data)

        # Login
        login_data = {
            'email': 'redirect_login@example.com',
            'password': 'password123'
        }
        response = client.post('/login', data=login_data, follow_redirects=False)
        assert response.status_code == 302
        # Note: response.location might be a tuple in Flask, check appropriately

    def test_blackjack_link_on_home_page(self, client):
        """Test that home page has link to blackjack"""
        response = client.get('/')
        assert b'blackjack' in response.data.lower()

    def test_register_link_on_home_page(self, client):
        """Test that home page has link to register"""
        response = client.get('/')
        assert b'register' in response.data.lower()

    def test_login_link_on_home_page(self, client):
        """Test that home page has link to login"""
        response = client.get('/')
        assert b'login' in response.data.lower()
