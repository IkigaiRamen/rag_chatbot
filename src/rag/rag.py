# src/rag/rag.py
from typing import Dict
from src.retrieval.retriever import Retriever
from src.llm.llm import LLM

class RAG:
    def __init__(self, retriever: Retriever, llm: LLM):
        self.retriever = retriever
        self.llm = llm

    def ask(self, question: str, top_k: int = 3) -> Dict:
        # 1️⃣ Retrieve chunks
        retrieved = self.retriever.retrieve(question)[:top_k]

        # 2️⃣ Build context string
        context_chunks = ""
        for r in retrieved:
            meta = r["metadata"]
            context_chunks += f"[{meta['doc_id']}|page {meta['page']}] {meta.get('text', '')}\n"

        # 3️⃣ Build prompt
        prompt = f"""
You are a helpful assistant. Use the context below to answer the question.
Provide an answer and include source references.

Context:
{context_chunks}

Question:
{question}

Answer:
"""
        # 4️⃣ Generate
        answer = self.llm.generate_answer(prompt)
        return {
            "answer": answer,
            "sources": [r["metadata"] for r in retrieved]
        }
