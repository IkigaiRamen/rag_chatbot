# test_rag.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.embeddings.embed import EmbeddingStore
from src.retrieval.retriever import Retriever
from src.llm.llm import LLM
from src.rag.rag import RAG

# Load FAISS index + metadata
store = EmbeddingStore()
store.load()

# Initialize Retriever
retriever = Retriever(store, top_k=3)

# Initialize LLM
llm = LLM(model_path="models/ggml-gpt4all-j-v1.3-groovy.bin")

# Initialize RAG
rag = RAG(retriever, llm)

# Ask a question
question = "What rights does the Tunisian Constitution guarantee?"
result = rag.ask(question)

print("Answer:\n", result["answer"])
print("\nSources:")
for src in result["sources"]:
    print(f"- {src['doc_id']} page {src.get('page', 'N/A')}")
