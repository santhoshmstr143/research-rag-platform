from pathlib import Path
import fitz

BASE_DIR = Path(__file__).resolve().parent.parent


def extract_text(pdf_path):

    pdf_path = Path(pdf_path)

    if not pdf_path.is_absolute():
        pdf_path = BASE_DIR / pdf_path

    pdf = fitz.open(str(pdf_path))

    full_text = ""

    for page in pdf:
        full_text += page.get_text()

    return full_text