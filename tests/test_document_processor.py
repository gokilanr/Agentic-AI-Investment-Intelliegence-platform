from unittest.mock import patch

from rag.document_processor import process_pdf

def test_process_pdf_extracts_and_chunks_text():
    sample_text = "Financial report content. " * 100

    with patch(
        "rag.document_processor.load_pdf",
        return_value = sample_text,
    ):
        chunks = process_pdf("sample.pdf",
                             chunk_size=100,
                             overlap=20,)


    assert len(chunks) > 1
    assert all(len(chunk) <=100 for chunk in chunks)