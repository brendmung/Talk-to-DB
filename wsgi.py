# wsgi.py

import os
from main import NLQueryDB, create_app, config

# 1. Initialize NLQueryDB instance
try:
    nlquerydb_instance = NLQueryDB(config)
    nlquerydb_instance.initialize()
except Exception as e:
    # Log error or handle failure
    print(f"WSGI Initialization Failed: {e}")
    # In a real scenario, you might want to raise the exception or exit
    import sys
    sys.exit(1)

# 2. Create the Flask app instance
app = create_app(nlquerydb_instance)

# Note: Gunicorn will run 'app' from this file.
