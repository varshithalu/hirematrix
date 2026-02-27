import fitz
from docx import Document
from fastapi import UploadFile

def parse_resume(file: UploadFile) -> str:
    text = ""

    if file.filename and file.filename.endswith(".pdf"):
        file_bytes = file.file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        for page in doc:
            page_text = page.get_text("text")
            if page_text:
                text += str(page_text) + "\n"

    elif file.filename and file.filename.endswith(".docx"):
        doc = Document(file.file)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"

    return text.strip()