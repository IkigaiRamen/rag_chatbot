# src/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import time
from fastapi.middleware.cors import CORSMiddleware
from src.api.upload import router as upload_router


# -----------------------------
# RAG components
# -----------------------------
from src.rag.rag import RAG
from src.embeddings.embed_hybrid import HybridEmbeddingStore
from src.retrieval.retriever_hybrid import Retriever
from src.llm.llm import LLM

# -----------------------------
# FastAPI app (CREATE FIRST)
# -----------------------------
app = FastAPI(title="Hybrid RAG Chatbot")

# -----------------------------
# Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------------
# Request model
# -----------------------------
class AskRequest(BaseModel):
    question: str
    top_k: int = 3

# -----------------------------
# Initialize Hybrid Embeddings
# -----------------------------
embedding_store = HybridEmbeddingStore(
    st_model_name="all-MiniLM-L6-v2",
    lmstudio_url="http://127.0.0.1:1234",
    lmstudio_model="text-embedding-nomic-embed-text-v1.5",
    index_path="data/index/faiss.index",
    metadata_path="data/index/metadata.pkl"
)

# -----------------------------
# Load or fail fast
# -----------------------------
try:
    embedding_store.load()
    print("✅ Hybrid FAISS index loaded")
except FileNotFoundError:
    raise RuntimeError(
        "Hybrid FAISS index not found.\n"
        "👉 Run ingestion first to build hybrid embeddings."
    )

# -----------------------------
# 🔐 DIMENSION SAFETY CHECK
# -----------------------------
dummy = embedding_store.embed_texts(["dimension check"])
faiss_dim = embedding_store.index.d
embed_dim = dummy.shape[1]

if faiss_dim != embed_dim:
    raise RuntimeError(
        f"Embedding dimension mismatch:\n"
        f"  FAISS dim: {faiss_dim}\n"
        f"  Embed dim: {embed_dim}\n"
        f"Delete index and rebuild."
    )

print(f"✅ Hybrid embedding dimension OK ({faiss_dim})")

# -----------------------------
# Retriever + LLM
# -----------------------------
retriever = Retriever(embedding_store, top_k=5)

llm = LLM(
    api_url="http://127.0.0.1:1234/v1/chat/completions",
    model_name="mistral-3-3b"
)

rag = RAG(retriever, llm)

# -----------------------------
# API
# -----------------------------
@app.post("/ask")
def ask_question(request: AskRequest):
    start = time.time()
    try:
        response = rag.ask(request.question, top_k=request.top_k)
        latency = time.time() - start

        return {
            "question": request.question,
            "answer": response["answer"],
            "sources": response["sources"],
            "latency_seconds": round(latency, 2)
        }

    except Exception as e:
        logging.exception("RAG failure")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(upload_router)


@app.get("/health")
def health():
    return {"status": "ok"}
