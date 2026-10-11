from pathlib import Path
import chromadb
from config.settings import VECTORSTORE_DIR

class FinancialVectorStore:
    """Store and retrieve financial document chunks using chromaDb"""

    def __init__(
            self,
            collection_name: str ="investiq_financial_documents",
            persist_directory: str | Path = VECTORSTORE_DIR
        ):

        self.client = chromadb.PersistentClient(
            path=str(persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name = collection_name,
            metadata = {"hnsw:space": "cosine"}
        )


    def add_documents(
            self,
            chunks: list[str],
            embeddings: list[list[float]],
            document_id: str,
    ) -> None:
        """Save text chunks and their embeddings."""

        if not chunks:
            raise ValueError("Chunks cannot empty.")

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Each chunk must have a corresponding embedding."
            )

        if not document_id or not document_id.strip():
            raise ValueError("document_id cannot be empty.")

        if any(not chunk or not chunk.strip() for chunk in chunks):
            raise ValueError("Chunks cannot contain empty text.")

        if any(not embedding for embedding in embeddings):
            raise ValueError("Enmmbeddings cannot be empty.")

        ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        metadatas = [
            {
                "document_id": document_id,
                "chunk_index": index,
            }

            for index in range(len(chunks))
        ]

        self.collection.upsert(
            ids = ids,
            documents = chunks,
            embeddings = embeddings,
            metadatas = metadatas
        )


    def search(
            self,
            query_embedding: list[float],
            n_results: int=3,
    ) -> list[dict]:
        """Retrieve the most relevant chunks for a query embedding."""

        if not query_embedding:
            raise ValueError("Query embedding cannot be empty.")

        if n_results <=0:
            raise ValueError("n_results must be greater than zero.")

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results = n_results,
            include = ["documents", "metadatas","distances"]
        )

        matches = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for document, metadata, distance in zip(
            documents, metadatas, distances
        ):
            matches.append(
                {
                    "text":document,
                    "metadata":metadata,
                    "distance": distances,
                }
            )

        return matches




    