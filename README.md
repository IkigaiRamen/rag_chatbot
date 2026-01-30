# 🧠 Hybrid RAG Chatbot

An **end-to-end hybrid Retrieval-Augmented Generation (RAG) chatbot** built with **Python**, **FastAPI**, **FAISS**, and **LM Studio** for embeddings and large language model responses.

This system can answer questions over your document corpus by combining **local semantic embeddings** (Sentence Transformers) with **LM Studio embeddings**, and features a **modern React frontend** similar to ChatGPT’s UI.

---

## 🚀 Features

* **Hybrid embeddings**: Combines local SentenceTransformer embeddings with LM Studio embeddings for better semantic search.
* **FAISS-based retrieval**: Efficient vector search for large document corpora.
* **Chunked document ingestion**: Handles large documents by splitting them into overlapping chunks.
* **RAG pipeline**: Retrieves top-k relevant chunks and generates answers using a large language model (Mistral 3B).
* **FastAPI server**: Provides a REST API for querying the chatbot.
* **React frontend**: Chat interface with scrollable conversation, bottom-aligned input, and sidebar for conversation history.
* **Persistence**: Saves and loads FAISS index and chunk metadata.
* **Logging & monitoring**: Tracks queries, latency, and errors for easier debugging.
* **File upload support**: Users can upload PDFs or text files to expand the chatbot’s knowledge.

---

## 🛠 Tech Stack & Libraries

| Layer                     | Libraries / Tools                                                     |
| ------------------------- | --------------------------------------------------------------------- |
| **Backend API**           | FastAPI, Pydantic, Uvicorn                                            |
| **Embedding / Retrieval** | Sentence Transformers, FAISS, NumPy, Requests                         |
| **LLM Integration**       | LM Studio (Mistral 3B)                                                |
| **Frontend**              | React, Vite, TailwindCSS, Framer Motion, React Markdown, Lucide Icons |
| **Data Processing**       | Python, pathlib, tqdm                                                 |
| **Persistence**           | Pickle, FAISS binary index files                                      |
| **Logging**               | Python `logging` module                                               |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd rag_chatbot
```

---

### 2. Backend Setup

#### Create a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

#### Install backend dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

* The frontend runs on `http://localhost:5173/` (or another port displayed in terminal).
* Connects to FastAPI backend to send questions and retrieve RAG responses.

---

### 4. Prepare Documents

Place your PDF or text documents in the `data/pdfs/` directory.

---

### 5. Build embeddings & FAISS index

**Hybrid embeddings** (SentenceTransformer + LM Studio):

```bash
python build_index.py
```

> ⚠️ Make sure LM Studio API is running. Chunking large documents is essential to avoid timeouts.

**Fallback to local embeddings only**:

```python
from src.embeddings.embed import EmbeddingStore
```

---

### 6. Run FastAPI server

```bash
uvicorn src.api.main:app --reload
```

* API endpoints:

  * `POST /ask` – Ask a question:

    ```json
    {"question": "Your question", "top_k": 3}
    ```
  * `POST /upload` – Upload documents (PDF / TXT) for embedding.
  * `GET /health` – Health check: returns `{"status": "ok"}`

---

## 🌐 Frontend Usage

* Chat UI with scrollable conversation area.
* Input box fixed at the bottom, toolbar at the top.
* Sidebar shows conversation history.
* Supports Markdown formatting in AI responses, including code blocks, lists, links, and blockquotes.
* File upload button allows users to extend the chatbot knowledge in real-time.

**Tech highlights:**

* **Framer Motion** – Smooth animations for messages and typing indicators.
* **Tailwind CSS** – Modern responsive UI with dark/light theme support.
* **React Markdown** – Render AI-generated content with formatting.
* **Lucide Icons** – Clean, lightweight icons.

---

## 📝 Project Structure

```
rag_chatbot/
│
├─ backend/
│   ├─ src/
│   │   ├─ api/
│   │   │   └─ main.py          # FastAPI server
│   │   ├─ embeddings/
│   │   │   ├─ embed.py         # Local embeddings
│   │   │   └─ embed_hybrid.py  # Hybrid embeddings
│   │   ├─ retrieval/
│   │   │   ├─ retriever.py
│   │   │   └─ retriever_hybrid.py
│   │   ├─ rag/
│   │   │   └─ rag.py           # RAG engine
│   │   ├─ llm/
│   │   │   └─ llm.py           # LM Studio integration
│   │   └─ ingestion/
│   │       └─ loader.py        # Document loading / chunking
│   │
│   ├─ data/
│   │   ├─ index/               # FAISS index & metadata
│   │   └─ pdfs/                # Documents to ingest
│   │
│   ├─ build_index.py           # Script to build embeddings & FAISS
│   └─ requirements.txt
│
├─ frontend/
│   ├─ src/
│   │   ├─ components/
│   │   │   ├─ ChatContainer.tsx
│   │   │   ├─ ChatMessage.tsx
│   │   │   ├─ ChatInput.tsx
│   │   │   ├─ ChatSidebar.tsx
│   │   │   ├─ TypingIndicator.tsx
│   │   │   └─ WelcomeScreen.tsx
│   │   └─ types/chat.ts
│   ├─ package.json
│   ├─ vite.config.ts
│   └─ tailwind.config.cjs
│
└─ README.md
```

---

## ⚡ How it Works

1. **User uploads documents** → Text extraction → Split into chunks.
2. **Embedding** → Hybrid embeddings (local + LM Studio).
3. **FAISS Index** → Stores embeddings & metadata.
4. **Query API** → User question → Embed → Retrieve top-k chunks → LLM generates answer.
5. **Frontend** → React chat UI displays conversation with Markdown formatting.
6. **Return** → JSON with answer, sources, and latency.

---

## ✅ Notes / Tips

* Hybrid embedding dimension = `ST_dim + LMStudio_dim` (e.g., 384 + 1536 = 1920).
* Chunking large documents prevents LM Studio timeouts.
* Clearing `data/index` before rebuilding prevents dimension mismatches.
* LM Studio unavailable → fallback to local SentenceTransformer embeddings.
* Frontend can be replaced or customized with your own React/Vite project.




