import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def technical_screening():

    questions = st.session_state.questions
    index = st.session_state.question_index

    if "answers" not in st.session_state:
        st.session_state.answers = []

    if index < len(questions):

        question = questions[index]

        st.subheader(f"Question {index + 1}")
        st.write(question)

        answer = st.text_area("Your Answer", key=f"answer_{index}")

        col1, col2 = st.columns(2)

        if col1.button("Previous") and index > 0:
            st.session_state.question_index -= 1
            st.rerun()

        if col2.button("Next"):
            if answer.strip() == "":
                st.warning("Answer cannot be empty")
                return

            if len(st.session_state.answers) > index:
                st.session_state.answers[index] = {
                    "question": question,
                    "answer": answer
                }
            else:
                st.session_state.answers.append({
                    "question": question,
                    "answer": answer
                })

            st.session_state.question_index += 1
            st.rerun()
    else:

        st.success("All questions answered.")

        if st.button("Submit Assessment", key="submit_final"):

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

            st.write("Status Code:", response.status_code)
            st.write("Raw Response:", response.text)

            if response.status_code != 200:
                st.error("Evaluation failed.")
                return

            try:
                result = response.json()
            except Exception as e:
                st.error(f"JSON decode error: {e}")
                return

            if not isinstance(result, dict):
                st.error("Unexpected server response.")
                return

            if "error" in result:
                st.error(result["error"])
                return

            st.session_state.evaluation_result = result
            st.session_state.stage = "results"
            st.rerun()