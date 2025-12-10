# adapters/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class DatabaseAdapter(ABC):
    """Base class for database adapters"""
    
    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> None:
        """Connect to the database"""
        pass
    
    @abstractmethod
    def fetch_data(self, collection: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Fetch data from database"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close database connection"""
        pass
