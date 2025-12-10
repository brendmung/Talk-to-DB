# adapters/firebase.py

from typing import List, Dict, Any, Optional
from .base import DatabaseAdapter

class FirebaseAdapter(DatabaseAdapter):
    """Firebase Firestore adapter"""
    
    def __init__(self):
        self.db = None
    
    def connect(self, config: Dict[str, Any]) -> None:
        # NOTE: Requires `firebase-admin`
        import firebase_admin
        from firebase_admin import credentials, firestore
        
        cred_path = config.get('credentials_path')
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
    
    def fetch_data(self, collection: str, filters: Optional[Dict] = None) -> List[Dict]:
        ref = self.db.collection(collection)
        if filters:
            for key, value in filters.items():
                ref = ref.where(key, '==', value)
        docs = ref.stream()
        return [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    def close(self) -> None:
        pass
