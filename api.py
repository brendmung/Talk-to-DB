# api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import TYPE_CHECKING, Dict, Any

# Avoid circular imports and dependency issues by using TYPE_CHECKING
if TYPE_CHECKING:
    from main import NLQueryDB

def create_app(nlquerydb: 'NLQueryDB') -> Flask:
    """Create Flask API server, requiring an initialized NLQueryDB instance."""
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})
    
    @app.route('/query', methods=['POST'])
    def query():
        data = request.get_json()
        question = data.get('question')
        num_results = data.get('num_results', 5)
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        try:
            # Access the instance passed to the factory function
            result = nlquerydb.query(question, num_results)
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Error during query: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/search', methods=['POST'])
    def search():
        """Direct semantic search without AI response"""
        data = request.get_json()
        question = data.get('question')
        num_results = data.get('num_results', 5)
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        try:
            results = nlquerydb.search_engine.search(question, k=num_results)
            return jsonify({'question': question, 'results': results})
        except Exception as e:
            app.logger.error(f"Error during search: {e}")
            return jsonify({'error': str(e)}), 500
    
    return app
