# adapters/mongodb.py

from typing import List, Dict, Any, Optional
from .base import DatabaseAdapter

class MongoDBAdapter(DatabaseAdapter):
    """MongoDB adapter"""
    
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self, config: Dict[str, Any]) -> None:
        # NOTE: Requires `pymongo`
        from pymongo import MongoClient
        uri = config.get('uri', 'mongodb://localhost:27017/')
        db_name = config.get('database')
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    
    def fetch_data(self, collection: str, filters: Optional[Dict] = None) -> List[Dict]:
        filters = filters or {}
        data = list(self.db[collection].find(filters))
        # Convert ObjectId to string
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
        return data
    
    def close(self) -> None:
        if self.client:
            self.client.close()
