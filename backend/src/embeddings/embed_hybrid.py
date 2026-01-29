# src/embeddings/embed_hybrid.py
from pathlib import Path
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
        self.index_path = Path(index_path).resolve()
        self.metadata_path = Path(metadata_path).resolve()

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
            print("[DEBUG] LM Studio not configured, returning zeros")
            return np.zeros((len(texts), 1536), dtype="float32")

        if isinstance(texts, str):
            texts = [texts]

        try:
            resp = requests.post(
                f"{self.lmstudio_url}/v1/embeddings",
                json={"model": self.lmstudio_model, "input": texts},
                timeout=(10, 180)
            )
            resp.raise_for_status()
            data = resp.json()
            print("[DEBUG] LM Studio raw response:", data)

            if "data" not in data or not isinstance(data["data"], list):
                print("[WARN] 'data' key missing or invalid. Returning zeros.")
                return np.zeros((len(texts), 1536), dtype="float32")

            emb_list = [item.get("embedding") for item in data["data"]]
            print("[DEBUG] LM Studio embedding list:", emb_list)

            if not emb_list or any(e is None for e in emb_list):
                print("[WARN] Some embeddings are None. Returning zeros.")
                return np.zeros((len(texts), 1536), dtype="float32")

            emb_array = np.array(emb_list, dtype="float32")
            print("[DEBUG] LM Studio array shape before fix:", emb_array.shape, "ndim:", emb_array.ndim)

            # Force 2D
            if emb_array.ndim == 1:
                emb_array = emb_array.reshape(1, -1)
                print("[DEBUG] Reshaped to 2D:", emb_array.shape)

            # Ensure row count = len(texts)
            if emb_array.shape[0] != len(texts):
                print(f"[WARN] LM Studio returned {emb_array.shape[0]} embeddings, expected {len(texts)}. Filling with zeros.")
                emb_array = np.zeros((len(texts), emb_array.shape[1]), dtype="float32")

            return emb_array

        except Exception as e:
            print(f"[ERROR] LM Studio embedding failed: {e}")
            return np.zeros((len(texts), 1536), dtype="float32")

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate hybrid embeddings (SentenceTransformer + LM Studio)
        """
        # SentenceTransformer embeddings
        st_embs = self.st_model.encode(
            texts, convert_to_numpy=True, show_progress_bar=True
        ).astype("float32")
        print(f"[DEBUG] ST embeddings shape: {st_embs.shape}, ndim: {st_embs.ndim}")

        # LM Studio embeddings
        lm_embs = self.get_lmstudio_embeddings(texts)
        print(f"[DEBUG] LM Studio embeddings shape: {lm_embs.shape}, ndim: {lm_embs.ndim}")

        # Safety check before concatenation
        if lm_embs is None:
            print("[ERROR] LM Studio returned None, replacing with zeros")
            lm_embs = np.zeros((len(texts), 1536), dtype="float32")

        if st_embs.shape[0] != lm_embs.shape[0]:
            print(f"[ERROR] Row mismatch! ST: {st_embs.shape}, LM: {lm_embs.shape}, forcing zeros")
            lm_dim = lm_embs.shape[1] if lm_embs.ndim == 2 else 1536
            lm_embs = np.zeros((st_embs.shape[0], lm_dim), dtype="float32")

        # Concatenate embeddings
        hybrid_embs = np.concatenate([st_embs, lm_embs], axis=1)
        print(f"[DEBUG] Hybrid embeddings shape: {hybrid_embs.shape}, ndim: {hybrid_embs.ndim}")

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

        # Convert Path -> str
        faiss.write_index(self.index, str(self.index_path))
        with open(self.metadata_path, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        print("Looking for FAISS at:", self.index_path)
        print("Exists (Path.exists()):", self.index_path.exists())
        print("Exists (os.path.exists()):", os.path.exists(self.index_path))

        if not os.path.exists(self.index_path):
            raise FileNotFoundError("FAISS index not found")
        if not os.path.exists(self.metadata_path):
            raise FileNotFoundError("Metadata file not found")

        # Convert Path -> str
        self.index = faiss.read_index(str(self.index_path))
        with open(self.metadata_path, "rb") as f:
            self.metadata = pickle.load(f)
