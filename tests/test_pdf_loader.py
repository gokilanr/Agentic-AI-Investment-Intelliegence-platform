from pathlib import Path
from pypdf import PdfWriter
import pytest 
from rag.loader import load_pdf

def test_missing_pdf_raises_error():
    with pytest.raises(FileNotFoundError):
        load_pdf("missing_financial_report.pdf")

def test_pdf_loader_rejects_empty_pdf(tmp_path):
    

    pdf_path = tmp_path / "empty.pdf"
    writer = PdfWriter()

    writer.add_blank_page(width=300, height=300)

    with pdf_path.open("wb") as file:
        writer.write(file)

    with pytest.raises(ValueError):
        load_pdf(pdf_path)