"""
BetterPrompt Flask Application
A web application for optimizing AI prompts using Azure OpenAI.
"""

import os
import logging
from typing import Dict, Any, Tuple
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class."""
    
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    MODEL_NAME = os.getenv('MODEL_NAME', 'o1-mini')
    MAX_COMPLETION_TOKENS = int(os.getenv('MAX_COMPLETION_TOKENS', '2048'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        # Skip validation in testing environment
        if os.getenv('TESTING') == 'true':
            return
            
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required")
        if not cls.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY environment variable is required")

class PromptOptimizer:
    """Handles prompt optimization using Azure OpenAI."""
    
    def __init__(self):
        self.endpoint = Config.AZURE_OPENAI_ENDPOINT
        self.api_key = Config.AZURE_OPENAI_API_KEY
        self.model = Config.MODEL_NAME
        self.max_tokens = Config.MAX_COMPLETION_TOKENS
        self.timeout = Config.REQUEST_TIMEOUT
        
        self.system_prompt = """You are a prompt optimization specialist. Your job is to take a rough or poorly structured prompt and transform it into a well-formatted, clear, and effective prompt that will get better results from AI models.

Focus on:
1. Clear structure and formatting
2. Specific instructions and context
3. Expected output format
4. Removing ambiguity
5. Adding relevant details that improve results
6. Proper grammar and clarity

Return ONLY the improved prompt - do not chat, ask questions, or provide explanations. Just return the optimized version ready to use."""
    
    def optimize_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Optimize a user prompt using Azure OpenAI.
        
        Args:
            user_prompt: The original prompt to optimize
            
        Returns:
            Dictionary containing the improved prompt or error information
        """
        if not user_prompt or not user_prompt.strip():
            return {'error': 'Prompt cannot be empty'}
        
        headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Please improve this prompt and make it well-structured and effective:\n\n{user_prompt.strip()}"}
            ],
            "max_completion_tokens": self.max_tokens,
            "model": self.model
        }
        
        try:            
            response = requests.post(
                self.endpoint, 
                headers=headers, 
                json=payload, 
                timeout=self.timeout
            )
            
            if response.status_code != 200:
                return {'error': f'Service temporarily unavailable (Error {response.status_code})'}
            
            result = response.json()
            
            # Validate response structure
            choices = result.get('choices')
            if not choices or not isinstance(choices, list) or not choices:
                return {'error': 'Invalid response from optimization service'}
            
            message = choices[0].get('message')
            if not message:
                return {'error': 'No response from optimization service'}
            
            improved_prompt = message.get('content', '').strip()
            if not improved_prompt:
                return {'error': 'No optimized prompt returned'}
            
            return {'improved_prompt': improved_prompt}
            
        except requests.exceptions.Timeout:
            return {'error': 'Request timeout - please try again'}
        except requests.exceptions.RequestException as e:
            return {'error': 'Network error - please check your connection'}
        except Exception as e:
            return {'error': 'An unexpected error occurred'}

def create_app() -> Flask:
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    Config.validate()
      # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s: %(message)s'
        )
    
    # Initialize the prompt optimizer
    optimizer = PromptOptimizer()
    
    @app.route('/')
    def index():
        """Render the main application page."""
        return render_template('index.html')
    
    @app.route('/api/fix-prompt', methods=['POST'])
    def fix_prompt():
        """API endpoint to optimize prompts."""
        try:
            # Handle cases where no JSON data is provided
            try:
                data = request.get_json()
            except Exception:
                return jsonify({'error': 'No data provided'}), 400
                
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            user_prompt = data.get('prompt', '')
            if not user_prompt or not user_prompt.strip():
                return jsonify({'error': 'Prompt cannot be empty'}), 400
            
            # Limit prompt length for security
            if len(user_prompt) > 10000:
                return jsonify({'error': 'Prompt too long (max 10,000 characters)'}), 400
            
            result = optimizer.optimize_prompt(user_prompt)
            
            if 'error' in result:
                return jsonify(result), 500
            
            return jsonify(result)
            
        except Exception as e:
            app.logger.error(f"Error in fix_prompt endpoint: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify({'status': 'healthy', 'service': 'BetterPrompt'})

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Create the main app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
