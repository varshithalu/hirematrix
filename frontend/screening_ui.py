import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def technical_screening():

    questions = st.session_state.questions
    index = st.session_state.question_index

    # Initialize answers list with empty placeholders
    if "answers" not in st.session_state:
        st.session_state.answers = [
            {"question": q, "answer": ""} for q in questions
        ]

    total_questions = len(questions)

    # Progress indicator
    st.progress((index + 1) / total_questions)

    question = questions[index]

    st.subheader(f"Question {index + 1} of {total_questions}")
    st.write(question)

    # Pre-fill answer if already exists
    current_answer = st.session_state.answers[index]["answer"]

    answer = st.text_area(
        "Your Answer",
        value=current_answer,
        key=f"answer_box_{index}",
        height=150
    )

    col1, col2 = st.columns(2)

    # Previous Button
    if col1.button("Previous", disabled=index == 0):
        st.session_state.question_index -= 1
        st.rerun()

    # Next Button
    if col2.button("Next"):
        if not answer or answer.strip() == "":
            st.warning("Answer cannot be empty")
            return

        # Save answer
        st.session_state.answers[index]["answer"] = answer

        if index < total_questions - 1:
            st.session_state.question_index += 1
            st.rerun()

    # ---- After Last Question Logic ----

    all_answered = all(
        item["answer"].strip() != "" for item in st.session_state.answers
    )

    if all_answered and index == total_questions - 1:

        st.success("All questions answered.")

        col3, col4 = st.columns(2)

        # Review Button
        if col3.button("Review Answers"):
            st.session_state.question_index = 0
            st.rerun()

        # Submit Button
        if col4.button("Submit Assessment", key="submit_final"):

            try:
                response = requests.post(
                    f"{BACKEND_URL}/screening/evaluate-batch",
                    json={
                        "user_id": st.session_state.user_id,
                        "responses": st.session_state.answers
                    }
                )
            except Exception as e:
                st.error(f"Connection error: {e}")
                return

            if response.status_code != 200:
                st.error("Evaluation failed.")
                return

            try:
                result = response.json()
            except Exception:
                st.error("Invalid server response.")
                return

            if not isinstance(result, dict) or "error" in result:
                st.error(result.get("error", "Unexpected server response"))
                return

            st.session_state.evaluation_result = result
            st.session_state.stage = "results"
            st.rerun()