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

        if col1.button("Next"):

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


        if col2.button("Previous") and index > 0:
            st.session_state.question_index -= 1
            st.rerun()

    else:

        st.success("All questions answered.")

        if st.button("Submit Assessment"):

            response = requests.post(
                f"{BACKEND_URL}/screening/evaluate-batch",
                json={
                    "user_id": st.session_state.user_id,
                    "responses": st.session_state.answers
                }
            )

            if response.status_code != 200:
                st.error("Evaluation failed")
                return

            result = response.json()

            st.success("Evaluation Complete 🎉")

            for eval_item in result["evaluations"]:
                st.write("Score:", eval_item["score"])
                st.write("Feedback:", eval_item["feedback"])
                st.markdown("---")