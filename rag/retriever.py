from rag.embedding_service import embed_text
from rag.vector_store import FinancialVectorStore

def retrieve_context(
        question: str,
        n_results: int =3,
) -> list[dict]:
    """Retrieve relevant financial document chunks for a question."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if n_results <=0:
        raise ValueError("n_results must be greater than zero.")

    query_embedding = embed_text(question)

    store =  FinancialVectorStore()

    results = store.search(
        query_embedding=query_embedding,
        n_results=n_results
    )

    return results