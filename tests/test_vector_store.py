import pytest 

from rag.vector_store import FinancialVectorStore

def test_add_and_search_documents(tmp_path):
    store = FinancialVectorStore(
        collection_name="test_financial_documents",
        persist_directory= tmp_path/ "chroma"
    )

    chunks = [
        "Higher interest rates can reduce bond prices",
        "revenue growth measures ab=n increase in sales."
    ]

    embeddings = [
        [1.0,0.0,0.0],
        [0.0,1.0,0.0]
    ]

    store.add_documents(
        chunks=chunks,
        embeddings=embeddings,
        document_id="report_001"
    )

    results = store.search(
        query_embedding=[0.99,0.01,0.0],
        n_results=1,
    )

    assert len(results) ==1
    assert results[0]["text"] == chunks[0]
    assert results[0]['metadata']['document_id'] == "report_001"

def test_add_documents_rejects_mismatched_lengths(tmp_path):
    store = FinancialVectorStore(
        collection_name="test_mismatched_documents",
        persist_directory=tmp_path/"chroma"
    )

    with pytest.raises(ValueError):
        store.add_documents(
            chunks=["A financial report"],
            embeddings=[],
            document_id="report_002"
        )

def test_search_rejects_empty_embedding(tmp_path):
    store = FinancialVectorStore(
        collection_name="Test_empty_query",
        persist_directory=tmp_path/"chroma"
    )

    with pytest.raises(ValueError):
        store.search(query_embedding=[])


def test_search_rejects_invalid_result_count(tmp_path):
    store=FinancialVectorStore(
        collection_name= "test_invalidd_count",
        persist_directory= tmp_path/ "chroma"
    )

    with pytest.raises(ValueError):
        store.search(
            query_embedding=[1.0,0.0],
            n_results=0
        )
