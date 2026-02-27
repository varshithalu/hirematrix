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
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def safe_json_parse(text: str | None):
    if not text:
        return None

    text = text.strip()

    # Remove markdown fencing
    if text.startswith("```"):
        text = text.split("```")[1]

    # Remove leading 'json'
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
        return "__AI_FAILURE__"

    except Exception as e:
        print("UNEXPECTED GEMINI ERROR:", e)
        return "__AI_FAILURE__"


# -----------------------
# Resume Extraction
# -----------------------

def extract_resume_data(resume_text: str):
    try:
        template = load_prompt("resume_extraction_prompt.txt")
        prompt = template.replace("{resume_text}", resume_text)

        output = generate_from_gemini(prompt)

        if output == "__AI_FAILURE__":
            return {
                "error": "AI service temporarily unavailable. Please try again later."
            }

        print("=== RAW GEMINI OUTPUT ===")
        print(output)
        print("=========================")

        parsed = safe_json_parse(output)

        if not parsed:
            return {
                "error": "AI response parsing failed."
            }

        return parsed

    except Exception as e:
        print("RESUME EXTRACTION ERROR:", e)
        return {
            "error": "Resume extraction failed due to internal error."
        }


# -----------------------
# Batch Evaluation
# -----------------------

def evaluate_batch(responses: list):

    try:
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

        if output == "__AI_FAILURE__":
            return {
                "error": "AI evaluation service unavailable."
            }

        print("=== BATCH RAW OUTPUT ===")
        print(output)
        print("========================")

        parsed = safe_json_parse(output)

        if not parsed:
            return {
                "error": "AI evaluation parsing failed."
            }

        return parsed

    except Exception as e:
        print("BATCH EVALUATION ERROR:", e)
        return {
            "error": "Batch evaluation failed due to internal error."
        }