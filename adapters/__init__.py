# adapters/__init__.py

from .base import DatabaseAdapter
from .mongodb import MongoDBAdapter
from .supabase import SupabaseAdapter
from .firebase import FirebaseAdapter
from .postgresql import PostgreSQLAdapter

ADAPTER_MAP = {
    'mongodb': MongoDBAdapter,
    'supabase': SupabaseAdapter,
    'firebase': FirebaseAdapter,
    'postgresql': PostgreSQLAdapter,
    'postgres': PostgreSQLAdapter
}

__all__ = [
    'DatabaseAdapter', 
    'ADAPTER_MAP',
    'MongoDBAdapter', 
    'SupabaseAdapter', 
    'FirebaseAdapter', 
    'PostgreSQLAdapter'
]
