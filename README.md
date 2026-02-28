----------------- 🧠 HIREMATRIX: AI- DRIVEN HIRING ASSISTANT ---------------

HireMatrix is an AI-powered technical hiring assistant designed to automate early-stage candidate screening.
It collects candidate details, extracts structured information from resumes, generates context-aware technical questions based on declared technologies and experience level, and evaluates responses using a structured AI scoring framework.

The system ensures:
Context-aware interaction flow
Experience-calibrated question difficulty
Resume-aware question personalization
Structured evaluation with scoring and recommendation band
HireMatrix combines backend orchestration with prompt-engineered LLM outputs to simulate a structured technical interview workflow.


 -------- System Architecture ----------
Frontend :
Streamlit
Stateful session management using st.session_state
Multi-stage flow --
- Greeting
- Resume Upload
- Profile Confirmation
- Technical Assessment
- Review Answers
- Results
- Exit

Backend : 
FastAPI
Modular route structure -- 
- resume
- questions
- screening
- system
Service layer for AI calls (gemini_service.py)
Structured schema validation using Pydantic
Batch evaluation architecture

AI Model :
Gemini 2.5 Flash
Strict JSON-only response enforcement
Defensive parsing and fallback handling

 -------- AI & Prompt Engineering  -------

HireMatrix uses carefully engineered prompts to ensure reliability and control.

Resume Extraction Prompt:
Extracts only explicitly mentioned technologies
Conservative experience calculation
Strict JSON return format
No hallucinated tools

Question Generation Prompt:
Generates 3–4 scenario-based technical questions
Calibrated by --
- Selected tech stack
- Candidate experience level
- Resume project context
Strict anti-hallucination constraints
No textbook questions
JSON-only output

Evaluation Prompt:
Structured scoring rubric (0–10 scale)
Penalizes vague answers
No encouragement allowed
Strict JSON output ----
- Per-question evaluation
- Overall average
- Percentage
- Recommendation band

This ensures deterministic behavior and reduces LLM unpredictability.


 -------Installation Instructions ---------

Prerequisites
- Python 3.10+
- API Key (Gemini)

1️⃣ Create folder :
cd hirematrix

2️⃣ Create Virtual Environment:
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

3️⃣ Install Dependencies:
pip install -r requirements.txt

4️⃣ Configure Environment Variables:
- Create a .env file or update your config.py
GEMINI_API_KEY=your_api_key_here
SUPABASE_URL= 'supabase_url'
SUPABASE_KEY= 'supabase_key'

5️⃣ Run Backend:
cd backend
uvicorn main:app --reload

- Backend runs at --
http://127.0.0.1:8000

6️⃣ Run Frontend:
cd frontend
python -m streamlit run app.py

- Frontend runs at --
http://localhost:8501


📖 Usage Guide:
Start Assessment
Upload Resume
Confirm Extracted Profile
Select Technologies
Answer Generated Questions
Review Answers
Submit Assessment
View Evaluation & Recommendation

📊 Evaluation Output:
- The system returns --
Per-question score (0–10)
Justified feedback
Overall average score
Percentage
Recommendation band --
- Strong Hire
- Hire
- Borderline
- No Hire


