import pytest
from unittest.mock import patch, MagicMock
from database.models import User
from database.user_table_DAO import UserTableDAO
from sqlalchemy.orm import Session

# @pytest.fixture
# def mock_get_user_details():
#     with patch('get_user_by_username') as mock:
#         mock.return_value = {
#             'username': 'testuser',
#             'password': 'password123',
#             'email': 'testuser@example.com'
#         }
#         yield mock


@patch("database.user_service.UserService.get_user_by_username", return_value='nate')
def test_get_user_by_username(mock_get_user_by_username):
    my_service = UserTableDAO(Session)
    assert my_service.get_user_by_username('test') == 'naate'

#
#
# def test_get_user_by_username():
#     testUserService = UserService()
#     user_id = 1  # The user_id doesn't matter because we are mocking the return value
#     result = testUserService.get_user_by_username(username='user_id')
#     expected_result = "Username: testuser, Email: testuser@example.com"
#     assert result == expected_result



# def test_get_user_by_username(mock_get_user_details):
#     user_id = 1  # The user_id doesn't matter because we are mocking the return value
#     result = User.format_user_details(user_id)
#     expected_result = "Username: testuser, Email: testuser@example.com"
#     assert result == expected_result

###############

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client
#
# @pytest.fixture
# def mock_user_service():
#     with patch('app.user_service') as mock:
#         yield mock
#
# def test_login_success(client, mock_user_service):
#     # Set up mock user
#     mock_user = MagicMock()
#     mock_user.email = 'testuser@example.com'
#     mock_user.password = 'hashedpassword'
#
#     # Configure the mock service to return the mock user and validate password
#     mock_user_service.get_user_by_email.return_value = mock_user
#     mock_user_service.verify_password.return_value = True
#
#     # Simulate a login POST request
#     response = client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'}, follow_redirects=True)
#
#     assert response.status_code == 200
#     assert b'You have been logged in!' in response.data
#
# def test_login_failure(client, mock_user_service):
#     # Configure the mock service to return None (user not found)
#     mock_user_service.get_user_by_email.return_value = None
#
#     # Simulate a login POST request
#     response = client.post('/login', data={'email': 'wronguser@example.com', 'password': 'wrongpassword'}, follow_redirects=True)
#
#     assert response.status_code == 200
#     assert b'Invalid login. Please check username and password' in response.data
