import streamlit as st
import requests
from resume_upload import resume_upload_flow, confirm_profile_and_generate
from screening_ui import technical_screening

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="TalentScout AI", layout="centered")

# Initialize state
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"

# Greeting Stage
if st.session_state.stage == "greeting":

    response = requests.get(f"{BACKEND_URL}/system/greeting")

    if response.status_code == 200:
        data = response.json()
        st.title("TalentScout AI Hiring Assistant")
        st.success(data.get("message"))
        st.write(data.get("overview"))

        if st.button("Start Assessment"):
            st.session_state.stage = "upload"
            st.rerun()
    else:
        st.error("System unavailable.")

# Upload Stage
elif st.session_state.stage == "upload":
    resume_upload_flow()

# Confirm Stage
elif st.session_state.stage == "confirm":
    confirm_profile_and_generate()

# Screening Stage
elif st.session_state.stage == "screening":
    technical_screening()

elif st.session_state.stage == "results":

    result = st.session_state.get("evaluation_result")

    if not result:
        st.error("No evaluation data available.")
        st.stop()

    st.success("Evaluation Complete 🎉")

    st.write("### Overall Summary")
    st.write(result.get("overall_summary"))
    st.write("**Average Score:**", result.get("overall_average_score"))
    st.write("**Percentage:**", result.get("overall_percentage"), "%")
    st.write("**Recommendation:**", result.get("recommendation_band"))

    if st.button("Finish"):
        st.session_state.stage = "exit"
        st.rerun()

# Exit Stage
elif st.session_state.stage == "exit":

    response = requests.get(f"{BACKEND_URL}/system/exit")

    if response.status_code == 200:
        data = response.json()
        st.success(data.get("message"))
        st.write(data.get("next_steps"))
    else:
        st.success("Thank you for completing the assessment.")