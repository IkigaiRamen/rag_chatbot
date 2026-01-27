# build_index.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.embeddings.embed_hybrid import HybridEmbeddingStore
from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents  # <- import your chunker

# 1️⃣ Load documents
data_dir = Path("data")
documents = load_documents(data_dir)
print(f"Loaded {len(documents)} documents")

# 2️⃣ Chunk documents
chunked_documents = chunk_documents(documents)
print(f"Total chunks after splitting: {len(chunked_documents)}")

# 3️⃣ Initialize HYBRID embedding store
store = HybridEmbeddingStore(
    st_model_name="all-MiniLM-L6-v2",
    lmstudio_url="http://127.0.0.1:1234",
    lmstudio_model="text-embedding-nomic-embed-text-v1.5",
    index_path="data/index/faiss.index",
    metadata_path="data/index/metadata.pkl"
)

# 4️⃣ Build FAISS index (HYBRID)
store.build(chunked_documents)
print(f"Built FAISS index with {store.index.ntotal} vectors")
print(f"Embedding dimension = {store.index.d}")

# 5️⃣ Save index & metadata
store.save()
print("Hybrid FAISS index and metadata saved to disk")
