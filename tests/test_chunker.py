import pytest

from rag.chunker import chunk_text


def test_chunk_text_splits_long_text():
    text = "A" * 2500

    chunks = chunk_text(text, chunk_size=1000, overlap=150)

    assert len(chunks) == 3
    assert all(len(chunk) <= 11000 for chunk in chunks)

def text_chunk_text_preserves_overlap():
    text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    chunks = chunk_text(text, chunk_size=10, overlaap=3)

    assert chunks[0][-3:] == chunks[1][:3]

def test_chunk_text_rejects_empty_text():
    with pytest.raises(ValueError):
        chunk_text("")

def test_chunk_text_rejects_ivalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("Example text", chunk_size= 10, overlap=10)