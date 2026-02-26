import streamlit as st
from resume_upload import resume_upload_flow, confirm_profile_and_generate
from screening_ui import technical_screening

st.set_page_config(page_title="TalentScout AI", layout="centered")

st.title("TalentScout AI Hiring Assistant")

if "stage" not in st.session_state:
    st.session_state.stage = "upload"

if st.session_state.stage == "upload":
    resume_upload_flow()

elif st.session_state.stage == "confirm":
    confirm_profile_and_generate()

elif st.session_state.stage == "screening":
    technical_screening()