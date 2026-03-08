import pytest
from cards.app_setup import create_app
from cards.configs.config import DevelopmentConfig, TestingConfig, ProductionConfig
import os


class TestAppSetup:
    def test_create_app_returns_flask_app(self):
        app = create_app()
        assert app is not None
        assert hasattr(app, 'config')

    def test_create_app_testing_config(self):
        os.environ['FLASK_ENV'] = 'testing'
        app = create_app()
        assert app.config['TESTING'] is True

    def test_create_app_development_config(self):
        os.environ['FLASK_ENV'] = 'development'
        app = create_app()
        assert app.config['DEBUG'] is True

    def test_create_app_production_config(self):
        os.environ['FLASK_ENV'] = 'production'
        app = create_app()
        assert app.config['DEBUG'] is False

    def test_app_has_blueprints_registered(self):
        app = create_app()
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'blackjack' in blueprint_names
        assert 'landing_page' in blueprint_names

    def test_app_has_database_extension(self):
        app = create_app()
        assert hasattr(app, 'extensions')
        assert 'sqlalchemy' in app.extensions

    def test_app_has_socketio_extension(self):
        from cards.app_setup import socketio
        assert socketio is not None

    def test_testing_config_values(self):
        config = TestingConfig()
        assert config.TESTING is True
        assert 'sqlite:///:memory:' in config.SQLALCHEMY_DATABASE_URI

    def test_development_config_values(self):
        config = DevelopmentConfig()
        assert config.DEBUG is True
        assert 'development_database.db' in config.SQLALCHEMY_DATABASE_URI

    def test_production_config_values(self):
        config = ProductionConfig()
        assert config.DEBUG is False
        assert 'production_database.db' in config.SQLALCHEMY_DATABASE_URI


class TestAppRoutes:
    @pytest.fixture
    def app(self):
        from cards.app import app
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    def test_app_has_home_route(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_app_has_blackjack_route(self, client):
        response = client.get('/blackjack')
        assert response.status_code == 200

    def test_app_has_register_route(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_app_has_login_route(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_app_has_health_check(self, client):
        response = client.get('/health_check')
        assert response.status_code == 200
