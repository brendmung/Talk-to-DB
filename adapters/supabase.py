# adapters/supabase.py

from typing import List, Dict, Any, Optional
from .base import DatabaseAdapter

class SupabaseAdapter(DatabaseAdapter):
    """Supabase adapter"""
    
    def __init__(self):
        self.client = None
    
    def connect(self, config: Dict[str, Any]) -> None:
        # NOTE: Requires `supabase-py`
        from supabase import create_client
        url = config.get('url')
        key = config.get('key')
        self.client = create_client(url, key)
    
    def fetch_data(self, collection: str, filters: Optional[Dict] = None) -> List[Dict]:
        query = self.client.table(collection).select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data
    
    def close(self) -> None:
        pass
