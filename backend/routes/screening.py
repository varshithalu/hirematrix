from fastapi import APIRouter
from schemas.schema import BatchEvaluationRequest
from services.gemini_service import evaluate_batch
from database.queries import save_evaluation

router = APIRouter()

@router.post("/evaluate-batch")
async def evaluate_batch_route(data: BatchEvaluationRequest):

    result = evaluate_batch(data.responses)

    if not result or "evaluations" not in result:
        return {"error": "Evaluation failed"}

    # Save each evaluation
    for idx, eval_item in enumerate(result["evaluations"]):
        save_evaluation(
            data.user_id,
            data.responses[idx].question,
            data.responses[idx].answer,
            eval_item,
            eval_item.get("score", 0)
        )

    return result