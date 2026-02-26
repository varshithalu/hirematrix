import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"


def technical_screening():

    questions = st.session_state.questions
    index = st.session_state.question_index

    if index < len(questions):

        question = questions[index]

        st.subheader(f"Question {index + 1}")
        st.write(question)

        answer = st.text_area("Your Answer", key=f"answer_{index}")

        if st.button("Submit Answer"):

            if not answer.strip():
                st.error("Please provide an answer.")
                return

            response = requests.post(
                f"{BACKEND_URL}/screening/evaluate",
                json={
                    "user_id": st.session_state.user_id,
                    "question": question,
                    "answer": answer
                }
            )

            if response.status_code != 200:
                st.error("Evaluation failed")
                return

            result = response.json()

            st.success("Evaluation Complete")

            st.write("### Score:", result.get("score"))
            st.write("### Feedback:")
            st.write(result.get("feedback"))

            st.session_state.question_index += 1
            st.rerun()

    else:
        st.success("Screening Completed 🎉")
        st.balloons()