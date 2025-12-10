# adapters/postgresql.py

from typing import List, Dict, Any, Optional
from .base import DatabaseAdapter

class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL adapter"""
    
    def __init__(self):
        self.conn = None
    
    def connect(self, config: Dict[str, Any]) -> None:
        # NOTE: Requires `psycopg2`
        import psycopg2
        import psycopg2.extras
        self.conn = psycopg2.connect(
            host=config.get('host', 'localhost'),
            port=config.get('port', 5432),
            database=config.get('database'),
            user=config.get('user'),
            password=config.get('password')
        )
    
    def fetch_data(self, collection: str, filters: Optional[Dict] = None) -> List[Dict]:
        import psycopg2.extras
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Security note: Using f-string for table/collection name is generally safe 
        # since table names are configured, but parameterized queries are used for filters.
        query = f"SELECT * FROM {collection}"
        params = []
        
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = %s")
                params.append(value)
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
