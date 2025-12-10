# main.py

import os
import json
from typing import Dict, Any

# Imports from modular files
from adapters import DatabaseAdapter, ADAPTER_MAP
from core.search import SemanticSearchEngine
from core.ai import AIResponseGenerator
from api import create_app

class NLQueryDB:
    """Main class for natural language database queries"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db_adapter = self._create_adapter()
        self.search_engine = SemanticSearchEngine(
            model_name=config.get('embedding_model', 'all-MiniLM-L6-v2')
        )
        self.ai_generator = AIResponseGenerator(
            api_url=config.get('ai_api_url', 'https://grey-api.vercel.app/api/chat'),
            model=config.get('ai_model', 'gpt-4o')
        )
    
    def _create_adapter(self) -> DatabaseAdapter:
        """Create appropriate database adapter based on configuration."""
        db_type = self.config.get('database_type', '').lower()
        
        adapter_class = ADAPTER_MAP.get(db_type)
        if not adapter_class:
            raise ValueError(f"Unsupported database type: {db_type}. Available types: {list(ADAPTER_MAP.keys())}")
        
        return adapter_class()
    
    def initialize(self) -> None:
        """Initialize database connection and build search index"""
        print("Connecting to database...")
        self.db_adapter.connect(self.config['database_config'])
        
        print("Fetching data...")
        data = self.db_adapter.fetch_data(
            collection=self.config['collection'],
            filters=self.config.get('filters')
        )
        
        if not data:
            raise ValueError("No data found in database")
        
        print(f"✓ Loaded {len(data)} records")
        
        # Build search index
        self.search_engine.build_index(
            data=data,
            text_fields=self.config.get('text_fields', [])
        )
    
    def query(self, question: str, num_results: int = 5) -> Dict[str, Any]:
        """Query database using natural language"""
        # Semantic search
        results = self.search_engine.search(question, k=num_results)
        
        # Generate AI response
        answer = self.ai_generator.generate_response(
            question=question,
            results=results,
            context=self.config.get('ai_context', '')
        )
        
        return {
            'question': question,
            'answer': answer,
            'results': results
        }
    
    def close(self) -> None:
        """Close database connection"""
        self.db_adapter.close()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Example configuration - users should customize this
    # Configuration can be loaded from a YAML or JSON file in a real app
    config = {
        'database_type': 'mongodb',  # REQUIRED: mongodb, supabase, firebase, postgresql
        'database_config': {
            'uri': os.getenv('MONGO_URI', 'mongodb://localhost:27017/'),
            'database': os.getenv('DB_NAME', 'your_database')
            # For Postgres/Supabase, use: 'host', 'user', 'password', 'port'
        },
        'collection': os.getenv('COLLECTION', 'your_collection'),
        'text_fields': ['title', 'description', 'category', 'type', 'price', 'location'],
        'filters': {},
        'embedding_model': 'all-MiniLM-L6-v2',
        'ai_api_url': os.getenv('AI_API_URL', 'https://grey-api.vercel.app/api/chat'),
        'ai_model': 'gpt-4o',
        'ai_context': ''
    }
    
    try:
        # Initialize NLQueryDB
        nlquerydb = NLQueryDB(config)
        nlquerydb.initialize()
    except Exception as e:
        print(f"FATAL INITIALIZATION ERROR: {e}")
        exit(1)
    
    # Run as CLI or API server
    mode = os.getenv('MODE', 'cli').lower()
    
    if mode == 'api':
        # Start Flask API server
        app = create_app(nlquerydb)
        port = int(os.getenv('PORT', 5000))
        print(f"\n🚀 Starting API server on port {port}...")
        print(f"📍 Endpoints:")
        print(f"   - POST /query - Natural language query with AI response")
        print(f"   - POST /search - Direct semantic search")
        print(f"   - GET /health - Health check")
        
        # Use a proper production server like Waitress or Gunicorn for deployment
        app.run(host='0.0.0.0', port=port, debug=False)
        
    else:
        # Interactive CLI mode
        print("\n" + "="*60)
        print("🎯 NLQueryDB - Interactive Mode")
        print("="*60)
        print("Type your questions or 'quit' to exit\n")
        
        while True:
            try:
                question = input("🔎 Your question: ").strip()
                if question.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if question:
                    result = nlquerydb.query(question)
                    print(f"\n💬 Answer:\n{result['answer']}\n")
                    print("-"*60 + "\n")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                
        nlquerydb.close()
