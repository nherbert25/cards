import pytest
from cards.forms import RegistrationForm, LoginForm
from cards.app import app


class TestRegistrationForm:
    @pytest.fixture
    def app_context(self):
        """Create Flask application context for form testing"""
        with app.app_context():
            with app.test_request_context():
                yield

    def test_registration_form_valid_data(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is True

    def test_registration_form_username_too_short(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'a',  # Too short (min 2 chars)
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'username' in form.errors

    def test_registration_form_username_too_long(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'a' * 21,  # Too long (max 20 chars)
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'username' in form.errors

    def test_registration_form_invalid_email(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'email': 'not-an-email',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'email' in form.errors

    def test_registration_form_password_too_short(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'pass',  # Too short (min 8 chars)
                'confirm_password': 'pass'
            }
        )
        assert form.validate() is False
        assert 'password' in form.errors

    def test_registration_form_password_mismatch(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'different123'
            }
        )
        assert form.validate() is False
        assert 'confirm_password' in form.errors

    def test_registration_form_missing_username(self, app_context):
        form = RegistrationForm(
            data={
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'username' in form.errors

    def test_registration_form_missing_email(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'email' in form.errors

    def test_registration_form_missing_password(self, app_context):
        form = RegistrationForm(
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'confirm_password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'password' in form.errors

    def test_registration_form_empty_data(self, app_context):
        form = RegistrationForm(data={})
        assert form.validate() is False
        assert 'username' in form.errors
        assert 'email' in form.errors
        assert 'password' in form.errors


class TestLoginForm:
    @pytest.fixture
    def app_context(self):
        """Create Flask application context for form testing"""
        with app.app_context():
            with app.test_request_context():
                yield

    def test_login_form_valid_data(self, app_context):
        form = LoginForm(
            data={
                'email': 'test@example.com',
                'password': 'password123',
                'remember': True
            }
        )
        assert form.validate() is True

    def test_login_form_valid_without_remember(self, app_context):
        form = LoginForm(
            data={
                'email': 'test@example.com',
                'password': 'password123',
                'remember': False
            }
        )
        assert form.validate() is True

    def test_login_form_invalid_email(self, app_context):
        form = LoginForm(
            data={
                'email': 'not-an-email',
                'password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'email' in form.errors

    def test_login_form_password_too_short(self, app_context):
        form = LoginForm(
            data={
                'email': 'test@example.com',
                'password': 'pass'  # Too short (min 8 chars)
            }
        )
        assert form.validate() is False
        assert 'password' in form.errors

    def test_login_form_missing_email(self, app_context):
        form = LoginForm(
            data={
                'password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'email' in form.errors

    def test_login_form_missing_password(self, app_context):
        form = LoginForm(
            data={
                'email': 'test@example.com'
            }
        )
        assert form.validate() is False
        assert 'password' in form.errors

    def test_login_form_empty_data(self, app_context):
        form = LoginForm(data={})
        assert form.validate() is False
        assert 'email' in form.errors
        assert 'password' in form.errors

    def test_login_form_email_with_spaces(self, app_context):
        form = LoginForm(
            data={
                'email': '  test@example.com  ',
                'password': 'password123'
            }
        )
        # Email validator rejects emails with leading/trailing spaces
        assert form.validate() is False
        assert 'email' in form.errors

    def test_login_form_minimum_valid_password(self, app_context):
        form = LoginForm(
            data={
                'email': 'test@example.com',
                'password': '12345678'  # Exactly 8 characters
            }
        )
        assert form.validate() is True

    @pytest.mark.parametrize('email', [
        'user@domain.com',
        'user.name@domain.co.uk',
        'user+tag@example.com',
        'user123@test-domain.com'
    ])
    def test_login_form_valid_email_formats(self, app_context, email):
        form = LoginForm(
            data={
                'email': email,
                'password': 'password123'
            }
        )
        assert form.validate() is True

    @pytest.mark.parametrize('email', [
        'notanemail',
        '@example.com',
        'user@',
        'user @example.com',
        'user@domain',
    ])
    def test_login_form_invalid_email_formats(self, app_context, email):
        form = LoginForm(
            data={
                'email': email,
                'password': 'password123'
            }
        )
        assert form.validate() is False
        assert 'email' in form.errors
