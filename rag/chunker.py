def chunk_text(
        text:str,
        chunk_size: int = 1000,
        overlap : int =150,
) -> list[str]:
    """Split text into chunks with a small overlap."""

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if chunk_size <=0:
        raise ValueError("chunk_size must be greater thann zero.")

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk_size.")

    text = text.strip()
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap


    return chunks