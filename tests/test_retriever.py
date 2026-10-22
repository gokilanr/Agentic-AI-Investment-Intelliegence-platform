from unittest.mock import patch
import pytest 
from rag.retriever import retrieve_context

def test_retrieve_context_returns_relevant_chunks():
    sample_results=[
        {
            "text": "Higher interest can be reduce bond prices.",
            "metadata" : {
                "document_id" : "report_001",
                "chunk_index" : 0
            },
            "distance" : 0.1,
        }
    ]

    with (
        patch(
            "rag.retriever.embed_text",
            return_value=[0.1,0.2,0.3],
        ) as mock_embed,
        patch(
            "rag.retriever.FinancialVectorStore"
        ) as mock_store_class,
    ):
        mock_store_class.return_value.search.return_value = sample_results

        results = retrieve_context("How do interest rates affect bonds?")

    mock_embed.assert_called_once_with(
        "How do interest rates affect bonds?"
    )

    mock_store_class.return_value.search.assert_called_once_with(
        query_embedding = [0.1,0.2,0.3],
        n_results = 3,
    )

    assert results == sample_results

def test_retrieve_context_rejects_empty_question():
    with pytest.raises(ValueError):
        retrieve_context("")

def test_retrieve_context_rejects_whitespaces_question():
    with pytest.raises(ValueError):
        retrieve_context("  ")

def test_retrieve_context_rejects_invalid_result_count():
    with pytest.raises(ValueError):
        retrieve_context("Explain Bond duration", n_results=0)