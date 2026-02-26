import google.genai as genai
import json
from config import GEMINI_API_KEY
from pathlib import Path

client = genai.Client(api_key=GEMINI_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


def load_prompt(filename: str) -> str:
    with open(PROMPTS_DIR / filename, "r", encoding="utf-8") as file:
        return file.read()


def safe_json_parse(text: str | None):
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            cleaned = text[text.index("{"): text.rindex("}") + 1]
            return json.loads(cleaned)
        except:
            return None


def generate_from_gemini(prompt: str) -> str | None:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def extract_resume_data(resume_text: str):
    template = load_prompt("resume_extraction_prompt.txt")
    prompt = template.replace("{resume_text}", resume_text)

    output = generate_from_gemini(prompt)
    return safe_json_parse(output)


def evaluate_answer(question: str, answer: str):
    template = load_prompt("evaluation_prompt.txt")
    prompt = (
        template
        .replace("{question}", question)
        .replace("{answer}", answer)
    )

    output = generate_from_gemini(prompt)
    return safe_json_parse(output)