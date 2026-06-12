import streamlit as st
import json
import random
from utils import evaluate_answer

# Load data
with open("data.json") as f:
    data = json.load(f)

st.title("🤖 AI Interview Simulator")

# Get all roles
roles = [item["role"] for item in data]

# Select role
role = st.selectbox("Select Job Role", roles)

# Get selected role data
selected_role_data = next(item for item in data if item["role"] == role)
questions = selected_role_data["questions"]

# Session state initialization
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

if "score_history" not in st.session_state:
    st.session_state.score_history = []

if "answered" not in st.session_state:
    st.session_state.answered = False

current_q = st.session_state.current_question

# Show question
st.subheader("Question:")
st.write(current_q["question"])

# Input
answer = st.text_area("Your Answer:")

# Evaluate
if st.button("Evaluate Answer"):
    if answer.strip() == "":
        st.warning("Please enter your answer!")
    else:
        score, feedback = evaluate_answer(
            answer,
            current_q["keywords"],
            current_q.get("ideal_answer", None)
        )

        st.session_state.score_history.append(score)
        st.session_state.answered = True

        st.subheader(f"Score: {score}/10")

        st.subheader("Feedback:")
        for f in feedback:
            st.write("-", f)

# Next Question (only after answering)
if st.session_state.answered:
    if st.button("➡️ Next Question"):
        st.session_state.current_question = random.choice(questions)
        st.session_state.answered = False
        st.rerun()

# Show performance
if st.session_state.score_history:
    st.subheader("📊 Performance Summary")
    avg_score = sum(st.session_state.score_history) / len(st.session_state.score_history)
    st.write(f"Average Score: {round(avg_score,2)}")

    st.write("Scores:", st.session_state.score_history)