from pathlib import Path
from rag.loader import load_pdf
from rag.chunker import chunk_text

def process_pdf(
        file_path:str | Path,
        chunk_size: int= 1000,
        overlap: int = 150,
) -> list[str]:
    """"Extract text from a PDF and split it into chunks."""

    document_text  = load_pdf(file_path)

    chunks = chunk_text(
        document_text,
        chunk_size=chunk_size,
        overlap=overlap,
    )

    return chunks