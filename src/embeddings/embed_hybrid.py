# src/embeddings/embed_hybrid.py
import os
import pickle
from typing import List, Dict
import numpy as np
import requests
import faiss
from sentence_transformers import SentenceTransformer


class HybridEmbeddingStore:
    def __init__(
        self,
        st_model_name: str = "all-MiniLM-L6-v2",
        lmstudio_url: str = None,
        lmstudio_model: str = None,
        index_path: str = "data/index/faiss.index",
        metadata_path: str = "data/index/metadata.pkl"
    ):
        self.st_model_name = st_model_name
        self.lmstudio_url = lmstudio_url
        self.lmstudio_model = lmstudio_model
        self.index_path = index_path
        self.metadata_path = metadata_path

        # Load SentenceTransformer model for FAISS
        self.st_model = SentenceTransformer(st_model_name)

        # FAISS index placeholder
        self.index = None
        self.metadata = []

    # -----------------------------
    # Helpers
    # -----------------------------
    def is_loaded(self) -> bool:
        return self.index is not None and len(self.metadata) > 0

    def get_lmstudio_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Query LM Studio API to get embeddings for multiple texts.
        Always returns a 2D array (n_texts, embedding_dim)
        """
        if not self.lmstudio_url or not self.lmstudio_model:
            # fallback: zero embeddings
            return np.zeros((len(texts), 1536), dtype="float32")

        # Ensure we always have a list
        if isinstance(texts, str):
            texts = [texts]

        try:
            resp = requests.post(
                f"{self.lmstudio_url}/v1/embeddings",
                json={"model": self.lmstudio_model, "input": texts},
                timeout=30
            )
            resp.raise_for_status()
            emb_list = [item["embedding"] for item in resp.json()["data"]]
            emb_array = np.array(emb_list, dtype="float32")

            # Ensure 2D array
            if emb_array.ndim == 1:
                emb_array = emb_array[np.newaxis, :]
            return emb_array
        except Exception as e:
            print(f"LM Studio embedding failed: {e}")
            return np.zeros((len(texts), 1536), dtype="float32")

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate hybrid embeddings (SentenceTransformer + LM Studio)
        """
        # SentenceTransformer embeddings
        st_embs = self.st_model.encode(
            texts, convert_to_numpy=True, show_progress_bar=True
        ).astype("float32")
        print(f"[DEBUG] ST embeddings shape: {st_embs.shape}")

        # LM Studio embeddings
        lm_embs = self.get_lmstudio_embeddings(texts)
        print(f"[DEBUG] LM Studio embeddings shape: {lm_embs.shape}")

        # Safety check
        if lm_embs.shape[0] != len(texts):
            print(f"[WARNING] LM Studio embeddings row count {lm_embs.shape[0]} != number of texts {len(texts)}. Replacing with zeros.")
            lm_dim = lm_embs.shape[1] if lm_embs.ndim == 2 else 1536
            lm_embs = np.zeros((len(texts), lm_dim), dtype="float32")
            print(f"[DEBUG] LM Studio embeddings shape after fix: {lm_embs.shape}")

        # Concatenate embeddings
        hybrid_embs = np.concatenate([st_embs, lm_embs], axis=1)
        print(f"[DEBUG] Hybrid embeddings shape: {hybrid_embs.shape}")

        # Normalize
        faiss.normalize_L2(hybrid_embs)
        return hybrid_embs


    # -----------------------------
    # Build / add embeddings
    # -----------------------------
    def build(self, chunks: List[Dict]):
        """
        chunks: list of dicts with keys:
            - text
            - metadata
        """
        if not chunks:
            raise ValueError("No chunks provided for embedding")

        texts = [c["text"] for c in chunks]
        embeddings = self.embed_texts(texts)

        # Create FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # Store metadata
        self.metadata = [c["metadata"] for c in chunks]

    # -----------------------------
    # Persistence
    # -----------------------------
    def save(self):
        if self.index is None:
            raise ValueError("No index to save")

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("FAISS index not found")
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError("Metadata file not found")

        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)
