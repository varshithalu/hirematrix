from fastapi import APIRouter
from services.question_generator import generate_questions
from schemas.schema import QuestionRequest
from database.queries import save_questions

router = APIRouter()

@router.post("/generate")
async def create_questions(data: QuestionRequest):
    questions = generate_questions(data.tech_stack)
    save_questions(data.user_id, data.tech_stack, questions)
    return questions