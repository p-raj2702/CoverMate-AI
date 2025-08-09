# backend/utils.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_url):
    import requests
    from io import BytesIO

    response = requests.get(pdf_url)
    doc = fitz.open(stream=BytesIO(response.content), filetype="pdf")

    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text