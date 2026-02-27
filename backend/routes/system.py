from fastapi import APIRouter

router = APIRouter()

@router.get("/greeting")
def get_greeting():
    return {
        "message": "Welcome to HireMatrix: AI- Driven Hiring Assistant",
        "overview": "This system will collect your profile details and conduct a structured technical assessment based on your selected technologies."
    }

@router.get("/exit")
def exit_message():
    return {
        "message": "Thank you for completing the assessment.",
        "next_steps": "Our team will review your responses and contact you regarding the next steps."
    }