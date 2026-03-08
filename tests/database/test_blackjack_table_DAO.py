import pytest
from unittest.mock import MagicMock
from cards.database.blackjack_table_DAO import BlackjackTableDAO
from cards.database.models import Blackjack


class TestBlackjackTableDAO:
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()

    @pytest.fixture
    def blackjack_table_dao(self, mock_db_session):
        return BlackjackTableDAO(mock_db_session)

    def test_get_user_by_uuid_success(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '11111111-1111-1111-1111-111111111111'
        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=500)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        result = blackjack_table_dao.get_user_by_uuid(mock_uuid)

        # Assert
        assert result is not None
        assert result.user_uuid == mock_uuid
        assert result.coins == 500
        mock_db_session.query.assert_called_once_with(Blackjack)
        mock_query.filter_by.assert_called_once_with(user_uuid=mock_uuid)
        mock_query.filter_by.return_value.first.assert_called_once()

    def test_get_user_by_uuid_not_found(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = 'nonexistent-uuid'
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = None

        # Act
        result = blackjack_table_dao.get_user_by_uuid(mock_uuid)

        # Assert
        assert result is None
        mock_db_session.query.assert_called_once_with(Blackjack)
        mock_query.filter_by.assert_called_once_with(user_uuid=mock_uuid)

    def test_add_user_to_database(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '22222222-2222-2222-2222-222222222222'
        new_user = Blackjack(user_uuid=mock_uuid, coins=500)

        # Act
        result = blackjack_table_dao.add_user_to_database(new_user)

        # Assert
        assert result is None
        mock_db_session.add.assert_called_once_with(new_user)
        mock_db_session.commit.assert_called_once()

    def test_update_coins_user_exists(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '33333333-3333-3333-3333-333333333333'
        initial_coins = 500
        coin_change = 100

        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=initial_coins)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        result = blackjack_table_dao.update_coins(mock_uuid, coin_change)

        # Assert
        assert result is None
        assert mock_blackjack_entry.coins == initial_coins + coin_change
        mock_db_session.add.assert_called_once_with(mock_blackjack_entry)
        mock_db_session.commit.assert_called_once()

    def test_update_coins_negative_change(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '44444444-4444-4444-4444-444444444444'
        initial_coins = 500
        coin_change = -50

        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=initial_coins)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        blackjack_table_dao.update_coins(mock_uuid, coin_change)

        # Assert
        assert mock_blackjack_entry.coins == 450

    def test_update_coins_user_not_found(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = 'nonexistent-uuid'
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = None

        # Act
        result = blackjack_table_dao.update_coins(mock_uuid, 100)

        # Assert
        assert result is None
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()

    def test_blackjack_table_dao_uses_default_session(self):
        # Test that DAO can be initialized without explicitly passing a session
        dao = BlackjackTableDAO()
        assert dao.db_session is not None

    def test_update_coins_zero_change(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '55555555-5555-5555-5555-555555555555'
        initial_coins = 500
        coin_change = 0

        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=initial_coins)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        blackjack_table_dao.update_coins(mock_uuid, coin_change)

        # Assert
        assert mock_blackjack_entry.coins == initial_coins

    def test_update_coins_large_positive_change(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '66666666-6666-6666-6666-666666666666'
        initial_coins = 100
        coin_change = 10000

        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=initial_coins)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        blackjack_table_dao.update_coins(mock_uuid, coin_change)

        # Assert
        assert mock_blackjack_entry.coins == 10100

    def test_update_coins_large_negative_change(self, blackjack_table_dao, mock_db_session):
        # Arrange
        mock_uuid = '77777777-7777-7777-7777-777777777777'
        initial_coins = 500
        coin_change = -1000  # Going negative

        mock_blackjack_entry = Blackjack(user_uuid=mock_uuid, coins=initial_coins)
        mock_query = mock_db_session.query.return_value
        mock_query.filter_by.return_value.first.return_value = mock_blackjack_entry

        # Act
        blackjack_table_dao.update_coins(mock_uuid, coin_change)

        # Assert
        assert mock_blackjack_entry.coins == -500  # Allows negative balance
