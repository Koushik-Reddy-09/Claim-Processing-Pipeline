
import fitz


def extract_pages(pdf_bytes: bytes) -> list:
    """
    Extract text from each page of an uploaded PDF.
    Page numbering starts at 1.
    """
    pages = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        if pdf.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        for page_number, page in enumerate(pdf, start=1):
            pages.append({
                "page_number": page_number,
                "text": page.get_text("text").strip()
            })

    if not pages:
        raise ValueError("The PDF contains no pages.")

    return pages
