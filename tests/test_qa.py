
from unittest.mock import patch

import pytest

from rag.qa import answer_question


def test_answer_question_uses_retrieved_context():
    retrieved_chunks = [
        {
            "text": "Higher interest rates can reduce bond prices.",
            "metadata": {
                "document_id": "report_001",
                "chunk_index": 0,
            },
            "distance": 0.1,
        }
    ]

    with (
        patch(
            "rag.qa.retrieve_context",
            return_value=retrieved_chunks,
        ) as mock_retrieve,
        patch(
            "rag.qa.generate_text",
            return_value="Higher interest rates can reduce bond prices. [Source 1]",
        ) as mock_generate,
    ):
        result = answer_question(
            "How do interest rates affect bonds?"
        )

    mock_retrieve.assert_called_once_with(
        question="How do interest rates affect bonds?",
        n_results=3,
    )

    assert mock_generate.called
    assert "Higher interest rates" in result["answer"]
    assert result["sources"][0]["document_id"] == "report_001"


def test_answer_question_handles_no_retrieved_context():
    with (
        patch(
            "rag.qa.retrieve_context",
            return_value=[],
        ),
        patch("rag.qa.generate_text") as mock_generate,
    ):
        result = answer_question("Explain bond duration")

    assert "couldn't find relevant information" in result["answer"]
    assert result["sources"] == []
    mock_generate.assert_not_called()


def test_answer_question_rejects_empty_question():
    with pytest.raises(ValueError):
        answer_question("")


def test_answer_question_rejects_invalid_result_count():
    with pytest.raises(ValueError):
        answer_question(
            "Explain bond duration",
            n_results=0,
        )
