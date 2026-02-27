from services.gemini_service import (
    load_prompt,
    safe_json_parse,
    generate_from_gemini
)

def generate_questions(tech_stack: list, experience_level: str):

    template = load_prompt("question_generation_prompt.txt")

    tech_string = ", ".join(tech_stack)

    prompt = (
        template
        .replace("{selected_tech_stack}", tech_string)
        .replace("{experience_level}", experience_level)
    )

    output = generate_from_gemini(prompt)

    parsed = safe_json_parse(output)

    if not parsed or "final questions" not in parsed:
        return {"final questions": []}

    return parsed