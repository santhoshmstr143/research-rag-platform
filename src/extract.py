import fitz

def extract_text(pdf_path):
    pdf = fitz.open(pdf_path)

    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    return full_text