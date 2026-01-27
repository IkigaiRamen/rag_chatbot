from typing import List, Dict


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 200
) -> List[str]:
    """
    Split text into overlapping chunks.
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
        if start < 0:
            start = 0

    return chunks


def chunk_documents(documents: List[Dict]) -> List[Dict]:
    """
    Chunk documents and attach chunk-level metadata.
    """
    chunked_docs = []

    for doc in documents:
        text = doc["text"]
        metadata = doc["metadata"]

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "text": chunk,
                "metadata": {
                    **metadata,
                    "chunk_id": f"{metadata['doc_id']}_p{metadata['page']}_c{i}"
                }
            })

    return chunked_docs
