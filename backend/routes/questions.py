from fastapi import APIRouter, HTTPException
from services.question_generator import generate_questions
from schemas.schema import QuestionRequest
from database.queries import save_questions

router = APIRouter()



@router.post("/generate")
def create_questions(data: QuestionRequest):

    if not data.tech_stack:
        raise HTTPException(status_code=400, detail="Tech stack required")

    if not hasattr(data, "experience_level"):
        raise HTTPException(status_code=400, detail="Experience level required")

    # NEW VALIDATION
    if not getattr(data, "desired_role", None):
        raise HTTPException(status_code=400, detail="Desired role must be provided")

    questions = generate_questions(
        data.tech_stack,
        data.experience_level
    )

    return questions