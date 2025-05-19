import pytest
import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from index import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_classify_valid_url(client):
    """Test classification of a valid URL"""
    response = client.post('/api/classify',
                          json={'url': 'https://www.google.com'},
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'category' in data
    assert isinstance(data['category'], str)

def test_classify_invalid_url(client):
    """Test classification of an invalid URL"""
    response = client.post('/api/classify',
                          json={'url': 'not-a-valid-url'},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_classify_empty_url(client):
    """Test classification with empty URL"""
    response = client.post('/api/classify',
                          json={'url': ''},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_classify_missing_url(client):
    """Test classification with missing URL parameter"""
    response = client.post('/api/classify',
                          json={},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data 