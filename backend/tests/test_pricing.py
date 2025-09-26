import pytest
import json
from src.app import create_app, db
from src.app.models import User, Project

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
    user_data = {
        'email': 'test@example.com',
        'password': 'TestPass123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    client.post('/api/auth/register', json=user_data)
    
    login_data = {
        'email': 'test@example.com',
        'password': 'TestPass123'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = json.loads(response.data)['access_token']
    
    return {'Authorization': f'Bearer {token}'}

def test_analyze_project(client, auth_headers):
    project_data = {
        'description': 'Build a e-commerce website with payment integration',
        'project_type': 'ecommerce',
        'complexity': 'medium',
        'timeline': 'standard',
        'team_size': 'small'
    }
    
    response = client.post('/api/pricing/analyze', 
                          json=project_data, 
                          headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'project_id' in data
    assert 'pricing' in data
    assert 'technical_recommendations' in data
    assert data['pricing']['currency'] == 'ZAR'

def test_analyze_project_missing_fields(client, auth_headers):
    project_data = {
        'description': 'Test project',
        # Missing required fields
    }
    
    response = client.post('/api/pricing/analyze', 
                          json=project_data, 
                          headers=auth_headers)
    assert response.status_code == 400

def test_get_project(client, auth_headers):
    # First create a project
    project_data = {
        'description': 'Test project',
        'project_type': 'web',
        'complexity': 'simple',
        'timeline': 'flexible',
        'team_size': 'solo'
    }
    response = client.post('/api/pricing/analyze', 
                          json=project_data, 
                          headers=auth_headers)
    project_id = json.loads(response.data)['project_id']
    
    # Get the project
    response = client.get(f'/api/pricing/projects/{project_id}', 
                         headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'project' in data
    assert data['project']['id'] == project_id

def test_get_nonexistent_project(client, auth_headers):
    response = client.get('/api/pricing/projects/nonexistent', 
                         headers=auth_headers)
    assert response.status_code == 404

def test_get_user_projects(client, auth_headers):
    # Create multiple projects
    for i in range(3):
        project_data = {
            'description': f'Test project {i}',
            'project_type': 'web',
            'complexity': 'simple',
            'timeline': 'flexible',
            'team_size': 'solo'
        }
        client.post('/api/pricing/analyze', 
                   json=project_data, 
                   headers=auth_headers)
    
    response = client.get('/api/pricing/projects', headers=auth_headers)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'projects' in data
    assert len(data['projects']) == 3

def test_pricing_accuracy():
    from src.app.ai_team.pricing_engine import PricingEngine
    pricing_engine = PricingEngine()
    
    test_project = {
        'description': 'Simple website with contact form',
        'project_type': 'web',
        'complexity': 'simple',
        'timeline': 'standard',
        'team_size': 'solo'
    }
    
    result = pricing_engine.calculate_price(test_project)
    
    assert 'final_price_zar' in result
    assert result['final_price_zar'] > 0
    assert result['confidence_score'] > 0
    assert 'price_breakdown' in result
