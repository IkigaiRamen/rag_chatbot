
# 🧠 Hybrid RAG Chatbot

An **end-to-end hybrid Retrieval-Augmented Generation (RAG) chatbot** built with **Python**, **FastAPI**, **FAISS**, and **LM Studio** for embeddings and large language model responses. This system can answer questions over your document corpus by combining **local semantic embeddings** (Sentence Transformers) with **LM Studio embeddings**.

---

## 🚀 Features

* **Hybrid embeddings**: Combines local SentenceTransformer embeddings with LM Studio embeddings for better semantic search.
* **FAISS-based retrieval**: Efficient vector search for large document corpora.
* **Chunked document ingestion**: Handles large documents by splitting them into overlapping chunks.
* **RAG pipeline**: Retrieves top-k relevant chunks and generates answers using a large language model (Mistral 3B).
* **FastAPI server**: Provides a REST API for querying the chatbot.
* **Persistence**: Saves and loads FAISS index and chunk metadata.
* **Logging**: Tracks queries, latency, and errors for monitoring.

---

## 🛠 Tech Stack & Libraries

| Layer                     | Libraries / Tools                             |
| ------------------------- | --------------------------------------------- |
| **Backend API**           | FastAPI, Pydantic, Uvicorn                    |
| **Embedding / Retrieval** | Sentence Transformers, FAISS, NumPy, Requests |
| **LLM Integration**       | LM Studio (Mistral 3B)                        |
| **Data Processing**       | Python, pathlib, tqdm                         |
| **Persistence**           | Pickle, FAISS binary index files              |
| **Logging**               | Python `logging` module                       |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd rag_chatbot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare documents

Place your PDF or text documents in the `data/` directory. The ingestion script will extract text and metadata.

### 5. Build embeddings & FAISS index

**For hybrid embeddings** (SentenceTransformer + LM Studio):

```bash
python build_index.py
```

> ⚠️ Make sure LM Studio API is running. For large documents, LM Studio requests may time out — chunking helps reduce request size.

**For local embeddings only** (fallback):

```python
from src.embeddings.embed import EmbeddingStore
```

---

### 6. Run the FastAPI server

```bash
uvicorn src.api.main:app --reload
```

* API endpoints:

  * `POST /ask` – Ask a question: `{"question": "your question", "top_k": 3}`
  * `GET /health` – Health check: returns `{"status": "ok"}`

---

## 📝 Project Structure

```
rag_chatbot/
│
├─ src/
│   ├─ api/
│   │   └─ main.py           # FastAPI server
│   ├─ embeddings/
│   │   ├─ embed.py          # Local embeddings
│   │   └─ embed_hybrid.py   # Hybrid embeddings
│   ├─ retrieval/
│   │   ├─ retriever.py
│   │   └─ retriever_hybrid.py
│   ├─ rag/
│   │   └─ rag.py            # RAG engine
│   ├─ llm/
│   │   └─ llm.py            # LM Studio integration
│   └─ ingestion/
│       └─ loader.py         # Document loading / chunking
│
├─ data/
│   ├─ index/                # FAISS index & metadata
│   └─ pdfs/                 # Documents to ingest
│
├─ build_index.py            # Script to build embeddings & FAISS
├─ requirements.txt
└─ README.md
```

---

## ⚡ How it Works

1. **Load documents** → Chunk text into overlapping segments.
2. **Embed text** → Hybrid embeddings (local ST + LM Studio).
3. **Build FAISS index** → Stores embeddings & metadata.
4. **Query API** → User question → Embed → Retrieve top-k chunks → LLM generates answer.
5. **Return** → JSON with answer, sources, and latency.

---

## ✅ Notes / Tips

* Chunking large documents is essential to prevent LM Studio embedding timeouts.
* Clearing `data/index` before rebuilding ensures no old embeddings cause dimension mismatch.
* If LM Studio is unavailable, fallback to local SentenceTransformer embeddings is supported.
* Embedding dimension for hybrid embeddings = `ST_dim + LMStudio_dim` (e.g., 384 + 1536 = 1920).

---

This README is ready for **GitHub**, **portfolio**, or **documentation** purposes.
