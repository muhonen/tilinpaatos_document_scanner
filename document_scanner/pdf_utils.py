from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyPDF2.
    Returns a string containing the text from all pages.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def convert_pdf_to_images(pdf_path, dpi=200):
    """
    Converts each page of a PDF file to an image using pdf2image.
    Returns a list of PIL Image objects.
    """
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        return images
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []