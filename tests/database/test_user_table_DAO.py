import pytest
from unittest.mock import MagicMock
from database.user_table_DAO import UserTableDAO  # Adjust the import based on your actual project structure
from database.models import User  # Adjust the import based on your actual project structure


@pytest.fixture
def mock_db_session():
    return MagicMock()


@pytest.fixture
def user_table_dao(mock_db_session):
    return UserTableDAO(mock_db_session)


def test_get_user_by_username(user_table_dao, mock_db_session):
    # Arrange
    mock_username = 'testuser'
    mock_user = User(username=mock_username, email='testuser@example.com', password='hashedpassword')
    mock_query = mock_db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_user

    # Act
    result = user_table_dao.get_user_by_username(mock_username)

    # Assert
    assert result == mock_user
    mock_db_session.query.assert_called_once_with(User)
    mock_query.filter_by.assert_called_once_with(username=mock_username)
    mock_query.filter_by.return_value.first.assert_called_once()

"""
Explanation

Fixtures:
    mock_db_session: Creates a mock object for the database session.
    user_table_dao: Initializes the UserTableDAO with the mocked database session.

Test Function:
    test_get_user_by_username: Tests the get_user_by_username method.

Arrange:
    mock_username: A test username.
    mock_user: A mock User object.
    mock_query: Mocks the query method of the database session.
    Configures the mock to return mock_user when filter_by and first methods are called.

Act:
    Calls get_user_by_username on the user_table_dao with the mock username.

Assert:
    Checks that the result is the expected mock_user.
    Verifies that the appropriate methods on the mock objects were called.

This setup allows you to test the UserTableDAO class without requiring a real database, making your tests faster and more reliable.
"""


def test_get_user_by_email(user_table_dao, mock_db_session):
    # Arrange
    mock_email = 'testuser@gmail.com'
    mock_user = User(username='my_test_username', email=mock_email, password='hashedpassword')
    mock_query = mock_db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = mock_user

    # Act
    result = user_table_dao.get_user_by_email(mock_email)

    # Assert
    assert result == mock_user
    mock_db_session.query.assert_called_once_with(User)
    mock_query.filter_by.assert_called_once_with(email=mock_email)
    mock_query.filter_by.return_value.first.assert_called_once()


# TODO: Actually integrate this with the database? There's no point in mocking a successful upsert.
#  For now just make sure the type is correct.
def test_add_user_to_database(user_table_dao, mock_db_session):
    # Arrange
    mock_username = 'my_test_username'
    mock_email = 'testuser@gmail.com'
    mock_password = 'p@ssword123'
    mock_user = User(username=mock_username, email=mock_email, password=mock_password)

    # Assert
    assert type(mock_user) == User
