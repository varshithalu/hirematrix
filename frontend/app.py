import streamlit as st
import requests
from resume_upload import resume_upload_flow, confirm_profile_and_generate
from screening_ui import technical_screening, review_answers

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="HireMatrix",
    page_icon="🧠",
    layout="centered"
)

# Modern UI Styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0b1220 0%, #0e1625 100%);
        color: white;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -1px;
    }

    .hero-sub {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 2.5rem;
        font-size: 1.15rem;
    }

    .card {
        background: #1e293b;
        padding: 2.2rem;
        border-radius: 18px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 2rem;
    }

    .welcome-banner {
        background: linear-gradient(90deg, #14532d, #166534);
        padding: 14px 18px;
        border-radius: 10px;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: 16px;
        color: #dcfce7;
    }

    .stButton>button {
        border-radius: 14px;
        height: 50px;
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0 25px;
    }

    .stButton>button:hover {
        opacity: 0.92;
    }
</style>
""", unsafe_allow_html=True)


# Initialize state
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"


# Greeting Stage
if st.session_state.stage == "greeting":

    response = requests.get(f"{BACKEND_URL}/system/greeting")

    if response.status_code == 200:
        data = response.json()

        st.markdown('<div class="hero-title">🧠 HireMatrix</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">AI-Driven Technical Hiring Platform</div>', unsafe_allow_html=True)

        st.markdown(
            f'<div class="welcome-banner">{data.get("message")}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"<p style='font-size:17px; color:#e2e8f0;'>{data.get('overview')}</p>",
            unsafe_allow_html=True
        )

        if st.button("🚀 Start Assessment"):
            st.session_state.stage = "upload"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("System unavailable.")


# Upload Stage
elif st.session_state.stage == "upload":

    st.markdown('<div class="hero-title">📄 Resume Upload</div>', unsafe_allow_html=True)
    resume_upload_flow()
    st.markdown('</div>', unsafe_allow_html=True)


# Confirm Stage
elif st.session_state.stage == "confirm":

    st.markdown('<div class="hero-title">👤 User Profile</div>', unsafe_allow_html=True)
    confirm_profile_and_generate()
    st.markdown('</div>', unsafe_allow_html=True)


# Screening Stage
elif st.session_state.stage == "screening":

    st.markdown('<div class="hero-title"> Technical Assessment💻</div>', unsafe_allow_html=True)
    technical_screening()
    st.markdown('</div>', unsafe_allow_html=True)


# ✅ NEW REVIEW STAGE (only addition)
elif st.session_state.stage == "review":

    st.markdown('<div class="hero-title">Review Your Answers</div>', unsafe_allow_html=True)
    review_answers()
    st.markdown('</div>', unsafe_allow_html=True)


# Results Stage
elif st.session_state.stage == "results":

    result = st.session_state.get("evaluation_result")

    if not result:
        st.error("No evaluation data available.")
        st.stop()

    st.markdown('<div class="hero-title">🎉 Assessment Completed</div>', unsafe_allow_html=True)
    st.markdown("### Overall Summary")
    st.write(result.get("overall_summary"))

    col1, col2, col3 = st.columns(3)

    col1.metric("Average Score", result.get("overall_average_score"))
    col2.metric("Percentage", f"{result.get('overall_percentage')} %")
    col3.metric("Recommendation", result.get("recommendation_band"))

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Finish"):
        st.session_state.stage = "exit"
        st.rerun()


# Exit Stage
elif st.session_state.stage == "exit":

    response = requests.get(f"{BACKEND_URL}/system/exit")

    st.markdown('<div class="hero-title">Final Review </div>', unsafe_allow_html=True)

    if response.status_code == 200:
        data = response.json()
        st.markdown(
            f'<div class="welcome-banner">{data.get("message")}</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"<p style='color:#e2e8f0;'>{data.get('next_steps')}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.success("Thank you for completing the assessment.")