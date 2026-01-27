# src/retrieval/retriever_hybrid.py
from typing import List, Dict
import numpy as np
import faiss

from src.embeddings.embed_hybrid import HybridEmbeddingStore


class Retriever:
    def __init__(self, embedding_store: HybridEmbeddingStore, top_k: int = 5):
        if not embedding_store.is_loaded():
            raise ValueError("HybridEmbeddingStore must be loaded before retrieval")
        self.store = embedding_store
        self.st_model = embedding_store.st_model  # SentenceTransformers part
        self.lmstudio_url = embedding_store.lmstudio_url
        self.top_k = top_k

    def get_hybrid_query_embedding(self, query: str) -> np.ndarray:
        """
        Generate hybrid embedding for the query:
        SentenceTransformer + LM Studio embeddings
        """
        # 1️⃣ ST embedding
        st_emb = self.st_model.encode([query], convert_to_numpy=True).astype("float32")

        # 2️⃣ LM Studio embedding via API
        import requests
        try:
            resp = requests.post(self.lmstudio_url, json={"input": query})
            resp.raise_for_status()
            lm_emb = np.array(resp.json()["data"][0]["embedding"], dtype="float32")
        except Exception as e:
            print(f"LM Studio embedding failed: {e}")
            lm_emb = np.zeros(1536, dtype="float32")  # fallback size, adjust if needed

        # 3️⃣ Concatenate
        hybrid_emb = np.concatenate([st_emb, lm_emb], axis=1)

        # 4️⃣ Normalize
        faiss.normalize_L2(hybrid_emb)
        return hybrid_emb

    def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve top-k most relevant chunks for a query.
        Returns list of dicts with:
        - rank
        - score (cosine similarity)
        - metadata
        """
        query_embedding = self.get_hybrid_query_embedding(query)

        # FAISS search
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
