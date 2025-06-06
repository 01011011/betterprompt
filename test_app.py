import os
import json
import pytest
from unittest.mock import patch, Mock
from app import create_app, PromptOptimizer

@pytest.fixture
def app():
    """Create application for testing."""
    os.environ['AZURE_OPENAI_ENDPOINT'] = 'test-endpoint'
    os.environ['AZURE_OPENAI_API_KEY'] = 'test-key'
    
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_index_route(client):
    """Test the main page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'BetterPrompt' in response.data
    assert b'AI Prompt Optimizer' in response.data

def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'BetterPrompt'

@patch('app.requests.post')
def test_fix_prompt_success(mock_post, client):
    """Test successful prompt optimization."""
    # Mock Azure OpenAI API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [
            {'message': {'content': 'Write a comprehensive guide about dog training that includes: 1. Basic commands, 2. House training methods, 3. Behavioral tips. Format as a structured article with clear headings.'}}
        ]
    }
    mock_post.return_value = mock_response
    
    response = client.post('/api/fix-prompt', 
                          json={'prompt': 'write about dog training'},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'improved_prompt' in data
    assert 'comprehensive guide' in data['improved_prompt']

@patch('app.requests.post')
def test_fix_prompt_api_error(mock_post, client):
    """Test API error handling."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = 'Internal server error'
    mock_post.return_value = mock_response
    
    response = client.post('/api/fix-prompt', 
                          json={'prompt': 'test prompt'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Service temporarily unavailable' in data['error']

@patch('app.requests.post')
def test_fix_prompt_timeout(mock_post, client):
    """Test timeout handling."""
    mock_post.side_effect = Exception('Request timeout - please try again')
    
    response = client.post('/api/fix-prompt', 
                          json={'prompt': 'test prompt'},
                          content_type='application/json')
    
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data

def test_fix_prompt_empty_prompt(client):
    """Test empty prompt validation."""
    response = client.post('/api/fix-prompt', 
                          json={'prompt': ''},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'cannot be empty' in data['error']

def test_fix_prompt_no_data(client):
    """Test missing data validation."""
    response = client.post('/api/fix-prompt', 
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'No data provided' in data['error']

def test_fix_prompt_too_long(client):
    """Test prompt length validation."""
    long_prompt = 'x' * 10001  # Exceed 10,000 character limit
    
    response = client.post('/api/fix-prompt', 
                          json={'prompt': long_prompt},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'too long' in data['error']

def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'not found' in data['error'].lower()

def test_prompt_optimizer_class():
    """Test PromptOptimizer class initialization."""
    optimizer = PromptOptimizer()
    assert optimizer.model == 'o1-mini'
    assert optimizer.max_tokens == 2048
    assert optimizer.timeout == 30
    assert 'prompt optimization specialist' in optimizer.system_prompt

@patch('app.requests.post')
def test_prompt_optimizer_optimize_prompt(mock_post):
    """Test PromptOptimizer.optimize_prompt method."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'choices': [
            {'message': {'content': 'Optimized prompt result'}}
        ]
    }
    mock_post.return_value = mock_response
    
    optimizer = PromptOptimizer()
    result = optimizer.optimize_prompt('test prompt')
    
    assert 'improved_prompt' in result
    assert result['improved_prompt'] == 'Optimized prompt result'

def test_prompt_optimizer_empty_prompt():
    """Test PromptOptimizer with empty prompt."""
    optimizer = PromptOptimizer()
    result = optimizer.optimize_prompt('')
    
    assert 'error' in result
    assert 'cannot be empty' in result['error']
