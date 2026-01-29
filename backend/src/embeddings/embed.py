import os
import pickle
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingStore:
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        index_path: str = "data/index/faiss.index",
        metadata_path: str = "data/index/metadata.pkl"
    ):
        self.model_name = model_name
        self.index_path = index_path
        self.metadata_path = metadata_path

        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadata = []

    # -----------------------------
    # State helpers
    # -----------------------------
    def is_loaded(self) -> bool:
        return self.index is not None and len(self.metadata) > 0

    # -----------------------------
    # Build index
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

        # 1. Generate embeddings
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        ).astype("float32")

        # 2. Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        # 3. Create FAISS index
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

        # 4. Store metadata
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
