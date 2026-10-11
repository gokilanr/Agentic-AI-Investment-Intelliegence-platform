from pathlib import Path
from pypdf import PdfReader

from utils.logger import get_logger

logger = get_logger(__name__)

def load_pdf(file_path: str | Path) -> str:
    """
    Extra text from a pdf file.
    
    Args:
    File_path: Path to the pdf file.
    
    Returns:
    Extracted text from the pdf.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    reader = PdfReader(str(file_path))

    pages=[]

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            pages.append(
                f"Page {page_number}\n{page_text}"
            )

    document_text = "\n\n".join(pages).strip()

    if not document_text:
        raise ValueError(
            f"No readable text found in {file_path.name}"
        )

    logger.info(
        f"sucessfully extracted text from {file_path.name}"
    )

    return document_text
