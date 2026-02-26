from pydantic import BaseModel, EmailStr
from typing import List


# user schema
class UserCreate(BaseModel):
    email: EmailStr


# question schema
class QuestionRequest(BaseModel):
    user_id: str
    tech_stack: List[str]


# evaluation schema
class EvaluationRequest(BaseModel):
    user_id: str
    question: str
    answer: str