from fastapi import APIRouter, UploadFile, File, Form
from services.resume_parser import parse_resume
from services.gemini_service import extract_resume_data
from database.queries import save_resume

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    if not file:
        return {"error": "No file uploaded"}

    text = parse_resume(file)
    print("==== RESUME TEXT START ====")
    print(text[:1000])
    print("==== RESUME TEXT END ====")

    if not text:
        return {"error": "Unable to extract text from resume"}

    structured = extract_resume_data(text)

    if not structured:
        return {"error": "AI extraction failed"}

    save_resume(user_id, text, structured)

    return structured




