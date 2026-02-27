from fastapi import FastAPI
from routes import resume, questions, screening
from schemas.schema import UserCreate
from database.queries import create_or_get_user
from routes import resume, questions, screening, system


app = FastAPI()

@app.post("/users")
def register_user(user: UserCreate):
    return create_or_get_user(user.email)

app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(system.router, prefix="/system", tags=["System"])
app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(screening.router, prefix="/screening", tags=["Screening"])

