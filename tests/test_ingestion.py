from unittest.mock import patch 
from rag.ingestion import ingest_pdf

def test_ingest_pdf_processes_and_stores_chunks():
    sample_chunks= [
        "Higher interest rates can reduce bomd prices.",
        "Revenue growth measures an increase in sales"

    ]

    sample_embeddings = [
        [0.1,0.2,0.3],
        [0.4,0.5,0.6]
    ]

    with (
        patch(
            "rag.ingestion.process_pdf",
            return_value = sample_chunks,
        ) as mock_process,
        patch(
            "rag.ingestion.embed_texts",
            return_value = sample_embeddings,
        ) as mock_embed,
        patch(
            "rag.ingestion.FinancialVectorStore"
        ) as mock_store_class,
    ):
        result = ingest_pdf(
            file_path="financial_report.pdf",
            document_id="report_001",
        )


    mock_process.assert_called_once()
    mock_embed.assert_called_once_with(sample_chunks)

    mock_store = mock_store_class.return_value
    mock_store.add_documents.assert_called_once_with(
        chunks = sample_chunks,
        embeddings = sample_embeddings,
        document_id ="report_001"
    )

    assert result =={
    "document_id": "report_001",
    "chunks_created":2,
    "chunks_stored" : 2
    }

def test_ingest_pdf_returns_zero_chunks_when_no_chunks_created():
    with(
        patch(
            "rag.ingestion.process_pdf",
            return_value=[],

        ),
        patch(
            "rag.ingestion.embed_texts",
            return_value = []
        ) as mock_embed,
        patch(
            "rag.ingestion.FinancialVectorStore"
        ) as mock_store_class,
    ):
        result = ingest_pdf(
            file_path="empty_report.pdf",
            document_id="report_002"
        )

    mock_embed.assert_not_called()
    mock_store_class.assert_not_called()

    assert result== {
        "document_id": "report_002",
        "chunks_created": 0,
        "chunks_stored":0
    }