import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from unittest import mock
from datetime import datetime, timedelta
import sqlite3
import jwt

client = TestClient(app)

# Assume this is your DTO class (define it if it's not imported)
class UserNamePassword:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "healthy"

# Helper function to mock database calls
def mock_db_calls(user_exists=True, user_permissions=None):
    if user_permissions is None:
        user_permissions = []

    def mock_connect(*args, **kwargs):
        mock_cursor = patch('sqlite3.Connection.cursor').start()
        mock_connection = mock.Mock(sqlite3.Connection)
        mock_connection.cursor.return_value = mock_cursor

        if user_exists:
            mock_cursor.fetchall.side_effect = [
                [(1, 'John', 'Doe')],
                [(1,)],
                [(permission,) for permission in user_permissions]
            ]
        else: 
            mock_cursor.fetchall.side_effect = [[]]

        return mock_connection

    return mock_connect

@patch('sqlite3.connect', new_callable=mock_db_calls(user_exists=False))
def test_get_token_user_not_found(mock_connect):
    data = {"username": "nonexistent_user", "password": "wrong_password"}
    response = client.post("/get_token", json=data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

@patch('sqlite3.connect', new_callable=mock_db_calls(user_permissions=['admin', 'user']))
def test_get_token_success(mock_connect):
    data = {"username": "existing_user", "password": "correct_password"}
    response = client.post("/get_token", json=data)
    assert response.status_code == 200
    json_response = response.json()
    
    token = json_response['token']
    decoded_token = jwt.decode(token, "simple_token", algorithms=["HS256"])

    assert decoded_token['user_id'] == 1
    assert decoded_token['user_firstName'] == 'John'
    assert decoded_token['user_lastName'] == 'Doe'
    assert decoded_token['user_permissions'] == ['admin', 'user']

    record_creation = datetime.strptime(decoded_token['created_at'], "%m/%d/%Y, %H:%M:%S")
    expires_at = datetime.strptime(decoded_token['expires_at'], "%m/%d/%Y, %H:%M:%S")
    expected_expires_at = record_creation + timedelta(days=1)

    assert expected_expires_at == expires_at

@pytest.fixture(autouse=True)
def unstub():
    """ Cleanup to unstub mock objects after each test """
    yield
    patch.stopall()

if __name__ == "__main__":
    pytest.main()