from pathlib import Path
from typing import List, Dict
import PyPDF2


def load_txt(file_path: Path) -> List[Dict]:
    """
    Load a TXT file and return text with metadata.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return [{
        "text": text,
        "metadata": {
            "doc_id": file_path.name,
            "page": None,
            "source": "txt"
        }
    }]


def load_pdf(file_path: Path) -> List[Dict]:
    """
    Load a PDF file and return page-level text with metadata.
    """
    documents = []

    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                documents.append({
                    "text": text,
                    "metadata": {
                        "doc_id": file_path.name,
                        "page": page_number,
                        "source": "pdf"
                    }
                })

    return documents


def load_documents(data_dir: Path) -> List[Dict]:
    """
    Load all PDF and TXT documents from data directory.
    """
    all_docs = []

    for txt_file in (data_dir / "txt").glob("*.txt"):
        all_docs.extend(load_txt(txt_file))

    for pdf_file in (data_dir / "pdfs").glob("*.pdf"):
        all_docs.extend(load_pdf(pdf_file))

    return all_docs
