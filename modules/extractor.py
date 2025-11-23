import io
import PyPDF2
import requests

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts text from PDF bytes.
    """
    pdf_file = io.BytesIO(pdf_bytes)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def download_pdf_from_url(url: str) -> bytes:
    """
    Downloads a PDF from a given URL and returns its content as bytes.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    return response.content
