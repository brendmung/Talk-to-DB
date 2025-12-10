# app_runner.py

import os
from main import NLQueryDB, create_app # Import NLQueryDB and create_app

# --- Configuration (Load from environment variables or a config file) ---
config = {
    'database_type': os.getenv('DB_TYPE', 'mongodb'),
    'database_config': {
        'uri': os.getenv('MONGO_URI', 'mongodb://localhost:27017/'),
        'database': os.getenv('DB_NAME', 'your_database')
    },
    'collection': os.getenv('COLLECTION', 'your_collection'),
    'text_fields': ['title', 'description', 'category', 'type', 'price', 'location'],
    'embedding_model': 'all-MiniLM-L6-v2',
    'ai_api_url': os.getenv('AI_API_URL', 'https://grey-api.vercel.app/api/chat'),
    'ai_model': 'gpt-4o',
    'ai_context': ''
}
# ------------------------------------------------------------------------

print("--- Starting NLQueryDB Initialization ---")
try:
    # 1. Initialize the core NLQueryDB logic
    nlquerydb_instance = NLQueryDB(config)
    nlquerydb_instance.initialize()
    
    # 2. Create the Flask app, passing the initialized instance
    app = create_app(nlquerydb_instance)
    print("--- Flask App created successfully ---")

except Exception as e:
    print(f"FATAL INITIALIZATION ERROR during startup: {e}")
    # In production, crashing here is often desired if the DB connection is mandatory
    raise SystemExit(e)

# Gunicorn will look for 'app' and run it.
