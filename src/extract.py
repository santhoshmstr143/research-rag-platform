from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent.parent

def extract_text(pdf_name):

    pdf_path = BASE_DIR / "data" / pdf_name

    pdf = fitz.open(str(pdf_path))

    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    pdf.close()

    return full_text