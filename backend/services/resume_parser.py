import PyPDF2
from docx import Document
from fastapi import UploadFile

def parse_resume(file: UploadFile) -> str:
    text = ""

    if file.filename and file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif file.filename and file.filename.endswith(".docx"):
        doc = Document(file.file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

    return text.strip()