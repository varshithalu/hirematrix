import google.genai as genai
import json
from config import GEMINI_API_KEY
from pathlib import Path
from google.genai.errors import ClientError

client = genai.Client(api_key=GEMINI_API_KEY)

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPTS_DIR = BASE_DIR / "prompts"


# -----------------------
# Utility Functions
# -----------------------

def load_prompt(filename: str) -> str:
    with open(PROMPTS_DIR / filename, "r", encoding="utf-8") as file:
        return file.read()


def safe_json_parse(text: str | None):
    if not text:
        return None

    text = text.strip()

    if text.startswith("```"):
        text = text.split("```")[1]

    if text.strip().startswith("json"):
        text = text.strip()[4:].strip()

    try:
        return json.loads(text)
    except:
        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except:
            return None


def generate_from_gemini(prompt: str) -> str | None:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except ClientError as e:
        print("GEMINI ERROR:", e)
        return None


# -----------------------
# Resume Extraction
# -----------------------

def extract_resume_data(resume_text: str):
    template = load_prompt("resume_extraction_prompt.txt")
    prompt = template.replace("{resume_text}", resume_text)

    output = generate_from_gemini(prompt)

    print("=== RAW GEMINI OUTPUT ===")
    print(output)
    print("=========================")

    parsed = safe_json_parse(output)

    if not parsed:
        return {
            "full_name": "",
            "email": "",
            "phone": "",
            "years_of_experience": "",
            "desired_role": "",
            "location": "",
            "tech_stack": []
        }

    return parsed


# -----------------------
# Batch Evaluation
# -----------------------

def evaluate_batch(responses: list):

    template = load_prompt("evaluation_prompt.txt")

    formatted_block = ""

    for i, item in enumerate(responses):
        formatted_block += f"""
Question {i+1}:
{item.question}

Answer:
{item.answer}

------------------------
"""

    prompt = template.replace("{qa_list}", formatted_block)

    output = generate_from_gemini(prompt)

    print("=== BATCH RAW OUTPUT ===")
    print(output)
    print("========================")

    return safe_json_parse(output)