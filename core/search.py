# core/search.py

from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os # For optional loading checks

# NOTE: Requires `sentence-transformers`, `faiss-cpu`, and `numpy`

class SemanticSearchEngine:
    """Handles embedding generation and semantic search"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.data = None
        self.embeddings = None
    
    def build_index(self, data: List[Dict], text_fields: List[str]) -> None:
        """Build FAISS index from data"""
        self.data = data
        
        # Convert documents to text
        texts = [self._doc_to_text(item, text_fields) for item in data]
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} documents...")
        self.embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Build FAISS index
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)
        print(f"✓ Built FAISS index with dimension {dim}")
    
    def _doc_to_text(self, doc: Dict, text_fields: List[str]) -> str:
        """Convert document to searchable text"""
        parts = []
        for field in text_fields:
            if field in doc:
                value = doc[field]
                parts.append(f"{field}: {value}")
        return " | ".join(parts)
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Perform semantic search"""
        if self.index is None:
            raise ValueError("Index not built. Call build_index first.")
        
        # Encode query
        qvec = self.model.encode([query], convert_to_numpy=True)
        
        # Search
        distances, indices = self.index.search(qvec, k)
        
        # Format results
        results = []
        for i, idx in enumerate(indices[0]):
            result = self.data[idx].copy()
            # Convert distance to a relevance score (inverse of distance)
            result['relevance_score'] = float(1 / (1 + distances[0][i])) 
            results.append(result)
        
        return results
