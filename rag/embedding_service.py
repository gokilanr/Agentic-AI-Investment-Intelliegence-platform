import os

from dotenv import load_dotenv

from config.settings import BASE_DIR
from utils.llm import get_client

load_dotenv(BASE_DIR/ ".env")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "gemini-embedding-001"
)

def embed_texts(texts:list[str]) -> list[list[float]]:
    """Convert a list of text chunks into embedding vectors."""

    if not texts:
        raise ValueError("Texts cannot be empty.")

    if any(not text or not text.strip() for text in texts):
        raise ValueError("Each text must contain readable content.")

    client = get_client()

    response = client.models.embed_content(
        model = EMBEDDING_MODEL,
        contents = texts,
    )

    embeddings = response.embeddings

    if not embeddings or len(embeddings) !=  len(texts):
        raise RuntimeError(
            "The embedding API returned an unexpected number of vectors."
        )

    vectors = [embedding.values for embedding in embeddings]

    if any(not vector for vector in vectors):
        raise RuntimeError("The API returned an empty embedding vector.")

    return vectors


def embed_text(text:str) -> list[float]:
    """Convert a single text into an embedding vector."""

    return embed_texts([text])[0]