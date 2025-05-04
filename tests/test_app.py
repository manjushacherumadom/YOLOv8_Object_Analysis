import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  
    return app.test_client()

def test_home_route(client):
    """Test if home route loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
