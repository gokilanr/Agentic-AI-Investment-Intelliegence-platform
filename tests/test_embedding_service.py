
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from rag.embedding_service import embed_text, embed_texts


def test_embed_texts_returns_vectors():
    fake_response = SimpleNamespace(
        embeddings=[
            SimpleNamespace(values=[0.1, 0.2, 0.3]),
            SimpleNamespace(values=[0.4, 0.5, 0.6]),
        ]
    )

    with patch("rag.embedding_service.get_client") as mock_get_client:
        mock_get_client.return_value.models.embed_content.return_value = (
            fake_response
        )

        vectors = embed_texts(["Stock returns", "Bond duration"])

    assert len(vectors) == 2
    assert vectors[0] == [0.1, 0.2, 0.3]
    assert vectors[1] == [0.4, 0.5, 0.6]


def test_embed_text_returns_one_vector():
    fake_response = SimpleNamespace(
        embeddings=[
            SimpleNamespace(values=[0.1, 0.2, 0.3])
        ]
    )

    with patch("rag.embedding_service.get_client") as mock_get_client:
        mock_get_client.return_value.models.embed_content.return_value = (
            fake_response
        )

        vector = embed_text("Explain bond duration")

    assert vector == [0.1, 0.2, 0.3]


def test_embed_texts_rejects_empty_list():
    with pytest.raises(ValueError):
        embed_texts([])


def test_embed_texts_rejects_blank_text():
    with pytest.raises(ValueError):
        embed_texts(["Stock returns", "   "])
