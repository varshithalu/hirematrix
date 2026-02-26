from services.gemini_service import (
    load_prompt,
    safe_json_parse,
    generate_from_gemini
)

def generate_questions(tech_stack: list):
    template = load_prompt("question_generation_prompt.txt")

    tech_string = ", ".join(tech_stack)
    prompt = template.replace("{tech_stack}", tech_string)

    output = generate_from_gemini(prompt)
    parsed = safe_json_parse(output)

    if not parsed:
        return {}

    return parsed