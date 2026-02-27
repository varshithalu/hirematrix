from fastapi import APIRouter
from schemas.schema import BatchEvaluationRequest
from services.gemini_service import evaluate_batch
from database.queries import save_evaluation

router = APIRouter()

@router.post("/evaluate-batch")
async def evaluate_batch_route(data: BatchEvaluationRequest):

    result = evaluate_batch(data.responses)

    # Validate AI output
    if not isinstance(result, dict):
        return {"error": "AI evaluation failed. Please retry later."}

    if "evaluations" not in result:
        return {"error": "Malformed AI response."}

    # Save each evaluation
    for idx, eval_item in enumerate(result["evaluations"]):

        if not isinstance(eval_item, dict):
            continue

        save_evaluation(
            data.user_id,
            data.responses[idx].question,
            data.responses[idx].answer,
            eval_item,
            eval_item.get("score", 0)
        )

    # ✅ ALWAYS return result
    return result