from database.supabase_client import supabase
from datetime import datetime
import uuid


def store_candidate(profile: dict):
    candidate_data = {
        "id": str(uuid.uuid4()),
        "full_name": profile.get("full_name"),
        "email": profile.get("email"),
        "phone": profile.get("phone"),
        "years_experience": profile.get("years_of_experience"),
        "desired_role": profile.get("desired_role"),
        "location": profile.get("location"),
        "tech_stack": profile.get("tech_stack"),
        "status": "profile_confirmed",
        "created_at": datetime.utcnow().isoformat()
    }

    supabase.table("candidates").insert(candidate_data).execute()

    return candidate_data["id"]