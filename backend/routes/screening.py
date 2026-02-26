from fastapi import APIRouter
from schemas.schema import EvaluationRequest
from services.gemini_service import evaluate_answer
from database.queries import save_evaluation

router = APIRouter()

@router.post("/evaluate")
async def evaluate(data: EvaluationRequest):
    result = evaluate_answer(data.question, data.answer)

    if not result:
        return {"error": "Evaluation failed"}

    score = result.get("score", 0)

    save_evaluation(
        data.user_id,
        data.question,
        data.answer,
        result,
        score
    )

    return result