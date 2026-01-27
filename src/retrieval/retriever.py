from typing import List, Dict
import numpy as np

from src.embeddings.embed import EmbeddingStore


class Retriever:
    def __init__(self, embedding_store: EmbeddingStore, top_k: int = 5):
        if not embedding_store.is_loaded():
            raise ValueError("EmbeddingStore must be loaded before retrieval")
        self.store = embedding_store
        self.model = embedding_store.model
        self.top_k = top_k

    def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve top-k most relevant chunks for a query.
        Returns list of dicts with:
        - rank
        - score (cosine similarity)
        - metadata
        """
        # 1️⃣ Embed the query
        query_embedding = self.model.encode([query], convert_to_numpy=True).astype("float32")
        # Normalize for cosine similarity
        import faiss
        faiss.normalize_L2(query_embedding)

        # 2️⃣ FAISS search
        distances, indices = self.store.index.search(query_embedding, self.top_k)

        results = []
        for rank, idx in enumerate(indices[0]):
            metadata = self.store.metadata[idx]
            results.append({
                "rank": rank,
                "score": float(distances[0][rank]),
                "metadata": metadata
            })

        return results
