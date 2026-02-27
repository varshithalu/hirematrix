import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def resume_upload_flow():
    st.subheader("Upload Your Resume")

    email = st.text_input("Enter Your Email")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if st.button("Process Resume"):

        if not email:
            st.error("Email is required")
            return

        if not uploaded_file:
            st.error("Please upload a resume")
            return

        # Create or get user
        user_response = requests.post(
            f"{BACKEND_URL}/users",
            json={"email": email}
        )

        if user_response.status_code != 200:
            st.error("User creation failed")
            return

        user_data = user_response.json()[0]
        user_id = user_data["id"]

        # Upload resume
        with st.spinner("Extracting resume information..."):
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                )
            }

            data = {"user_id": user_id}

            resume_response = requests.post(
                f"{BACKEND_URL}/resume/upload",
                files=files,
                data=data
            )

        if resume_response.status_code != 200:
            st.error("Resume processing failed")
            return

        extracted = resume_response.json()

        st.session_state.user_id = user_id
        st.session_state.extracted_data = extracted
        st.session_state.stage = "confirm"

        st.rerun()


def confirm_profile_and_generate():
    extracted = st.session_state.extracted_data

    st.subheader("Confirm Your Profile")

    st.write("### Extracted Information")

    st.write("**Name:**", extracted.get("full_name", ""))
    st.write("**Email:**", extracted.get("email", ""))
    st.write("**Experience:**", extracted.get("years_of_experience", ""))
    st.write("**Location:**", extracted.get("location", ""))

    tech_stack = extracted.get("tech_stack", [])

    if not tech_stack:
        st.error("No technologies detected in resume.")
        return

    st.write("### Select 4–5 Technologies for Assessment")

    selected_tech = st.multiselect(
        "Choose technologies",
        tech_stack,
        max_selections=5
    )

    experience_level = st.selectbox(
        "Select Your Experience Level",
        ["Fresher", "2-5 Years", "Above 5 Years"]
    )

    if st.button("Generate Questions"):

        if len(selected_tech) < 1:
            st.error("Please select at least one technology.")
            return

        generate_questions(selected_tech, experience_level)


def generate_questions(selected_tech, experience_level):

    response = requests.post(
        f"{BACKEND_URL}/questions/generate",
        json={
            "user_id": st.session_state.user_id,
            "tech_stack": selected_tech,
            "experience_level": experience_level
        }
    )

    if response.status_code != 200:
        st.error("Question generation failed")
        return

    data = response.json()

    questions = data.get("final questions", [])

    st.session_state.questions = questions
    st.session_state.question_index = 0
    st.session_state.stage = "screening"

    st.rerun()