import pytest
import json
from src.app import create_app, db
from src.app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Register user
    user_data = {
        'email': 'test@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/api/auth/register', json=user_data)
    
    # Login user
    login_data = {
        'email': 'test@example.com',
        'password': 'TestPass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = json.loads(response.data)['access_token']
    
    return {'Authorization': f'Bearer {token}'}

def test_register_user(client):
    user_data = {
        'email': 'newuser@example.com',
        'password': 'NewPass123',
        'first_name': 'New',
        'last_name': 'User'
    }
    
    response = client.post('/api/auth/register', json=user_data)
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'newuser@example.com'

def test_register_existing_user(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    # First registration
    client.post('/api/auth/register', json=user_data)
    
    # Second registration with same email
    response = client.post('/api/auth/register', json=user_data)
    assert response.status_code == 409

def test_login_success(client):
    # Register user first
    user_data = {
        'email': 'test@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/api/auth/register', json=user_data)
    
    # Login
    login_data = {
        'email': 'test@example.com',
        'password': 'TestPass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_invalid_credentials(client):
    login_data = {
        'email': 'nonexistent@example.com',
        'password': 'WrongPass'
    }
    response = client.post('/api/auth/login', json=login_data)
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    response = client.get('/api/auth/me', headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'

def test_change_password(client, auth_headers):
    password_data = {
        'current_password': 'TestPass123',
        'new_password': 'NewPass123'
    }
    response = client.post('/api/auth/change-password', 
                          json=password_data, 
                          headers=auth_headers)
    assert response.status_code == 200

def test_change_password_wrong_current(client, auth_headers):
    password_data = {
        'current_password': 'WrongPass',
        'new_password': 'NewPass123'
    }
    response = client.post('/api/auth/change-password', 
                          json=password_data, 
                          headers=auth_headers)
    assert response.status_code == 401

def test_password_validation(client):
    weak_password_data = {
        'email': 'test@example.com',
        'password': '123',  # Too short
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post('/api/auth/register', json=weak_password_data)
    assert response.status_code == 400
