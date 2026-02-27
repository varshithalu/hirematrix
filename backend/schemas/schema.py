from pydantic import BaseModel, EmailStr
from typing import List


class UserCreate(BaseModel):
    email: EmailStr


class QuestionRequest(BaseModel):
    user_id: str
    tech_stack: List[str]
    experience_level: str  # ADD THIS


class QAItem(BaseModel):
    question: str
    answer: str


class BatchEvaluationRequest(BaseModel):
    user_id: str
    responses: List[QAItem]