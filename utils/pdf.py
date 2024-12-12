from io import BytesIO
from pypdf import PdfReader
from fastapi.exceptions import HTTPException
from typing import List

def read_pdf(file_bytes: BytesIO) -> List[str]:
    """
    Convert PDF bytes to text. Returns a list of strings (one string per page)
    """
    
    reader = PdfReader(file_bytes)

    # Iterate through the pages and extract text
    return [page.extract_text() for page in reader.pages]