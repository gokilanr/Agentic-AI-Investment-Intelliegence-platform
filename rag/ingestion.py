from pathlib import Path

from rag.document_processor import process_pdf
from rag.embedding_service import embed_texts
from rag.vector_store import FinancialVectorStore

def ingest_pdf(
        file_path: str | Path,
        document_id:str,
        chunk_size: int =1000,
        overlap: int=150
) -> dict:
    """Extract, embed, and store a financial PDF."""

    chunks = process_pdf(
        file_path= file_path,
        chunk_size=chunk_size,
        overlap=overlap
    )

    if not chunks:
        return {
            "document_id":document_id,
            "chunks_created":0,
            "chunks_stored":0,
        }

    embeddings = embed_texts(chunks)

    store = FinancialVectorStore()

    store.add_documents(
        chunks=chunks,
        embeddings=embeddings,
        document_id=document_id,
    )

    return {
        "document_id": document_id,
        "chunks_created": len(chunks),
        "chunks_stored" : len(embeddings)
    }