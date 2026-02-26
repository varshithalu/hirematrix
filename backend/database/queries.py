from database.supabase_client import supabase


USERS_TABLE = "users"
RESUMES_TABLE = "resumes"
QUESTIONS_TABLE = "questions"
EVALUATIONS_TABLE = "evaluations"

# ------------------------
# Helper for safe execution
# ------------------------

def _execute(query):
    response = query.execute()

    if response.data is None:
        raise Exception(f"Database Error: {response.error}")

    return response.data


# ------------------------
# USERS
# ------------------------

def create_or_get_user(email: str):
    # Check if user already exists
    existing = (
        supabase
        .table(USERS_TABLE)
        .select("*")
        .eq("email", email)
        .execute()
    )

    if existing.data:
        return existing.data

    # Otherwise create new user
    response = (
        supabase
        .table(USERS_TABLE)
        .insert({"email": email})
        .execute()
    )

    if response.data is None:
        raise Exception(response.error)

    return response.data


def get_user_by_email(email: str):
    return _execute(
        supabase
        .table(USERS_TABLE)
        .select("*")
        .eq("email", email)
        .single()
    )

# ------------------------
# RESUMES
# ------------------------

def save_resume(user_id: str, resume_text: str, extracted_data: dict):
    response = (
        supabase
        .table(RESUMES_TABLE)
        .insert({
            "user_id": user_id,
            "resume_text": resume_text,
            "extracted_data": extracted_data
        })
        .execute()
    )

    if response.data is None:
        raise Exception(response.error)

    return response.data



def get_latest_resume(user_id: str):
    return _execute(
        supabase
        .table(RESUMES_TABLE)
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )


# ------------------------
# QUESTIONS
# ------------------------

def save_questions(user_id: str, tech_stack: list, generated_questions: dict):
    return _execute(
        supabase
        .table(QUESTIONS_TABLE)
        .insert({
            "user_id": user_id,
            "tech_stack": tech_stack,
            "generated_questions": generated_questions
        })
    )


def get_user_questions(user_id: str):
    return _execute(
        supabase
        .table(QUESTIONS_TABLE)
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
    )


# ------------------------
# EVALUATIONS
# ------------------------

def save_evaluation(
    user_id: str,
    question: str,
    answer: str,
    evaluation_result: dict,
    score: int
):
    return _execute(
        supabase
        .table(EVALUATIONS_TABLE)
        .insert({
            "user_id": user_id,
            "question": question,
            "answer": answer,
            "evaluation_result": evaluation_result,
            "score": score
        })
    )


def get_user_evaluations(user_id: str):
    return _execute(
        supabase
        .table(EVALUATIONS_TABLE)
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
    )