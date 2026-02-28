import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def technical_screening():

    questions = st.session_state.questions
    index = st.session_state.question_index

    if "answers" not in st.session_state:
        st.session_state.answers = [
            {"question": q, "answer": ""} for q in questions
        ]

    total_questions = len(questions)

    st.progress((index + 1) / total_questions)

    question = questions[index]

    st.subheader(f"Question {index + 1} of {total_questions}")
    st.write(question)

    current_answer = st.session_state.answers[index]["answer"]

    answer = st.text_area(
        "Your Answer",
        value=current_answer,
        key=f"answer_box_{index}",
        height=150
    )

    col1, col2 = st.columns(2)

    if col1.button("Previous", disabled=index == 0):
        st.session_state.question_index -= 1
        st.rerun()

    if col2.button("Next"):
        if not answer or answer.strip() == "":
            st.warning("Answer cannot be empty")
            return

        st.session_state.answers[index]["answer"] = answer

        if index < total_questions - 1:
            st.session_state.question_index += 1
            st.rerun()

    all_answered = all(
        item["answer"].strip() != "" for item in st.session_state.answers
    )

    if all_answered and index == total_questions - 1:
        st.success("All questions answered.")

        if st.button("Review Answers"):
            st.session_state.stage = "review"
            st.rerun()


def review_answers():

    st.subheader("Review Your Answers")

    for i, item in enumerate(st.session_state.answers):
        st.write(f"### Question {i+1}")
        st.write(item["question"])
        st.write("**Your Answer:**")
        st.write(item["answer"])
        st.markdown("---")

    col1, col2 = st.columns(2)

    if col1.button("Back to Questions"):
        st.session_state.stage = "screening"
        st.session_state.question_index = 0
        st.rerun()

    if col2.button("Submit Assessment"):

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