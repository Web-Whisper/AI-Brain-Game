import streamlit as st
import random
import json
import os
import time

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Brain Game", layout="wide")

# -----------------------------
# DARK UI (extra CSS)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.stApp {
    background-color: #0e1117;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠🔥 AI Brain Booster Game PRO")

# -----------------------------
# LEADERBOARD FILE
# -----------------------------
LEADERBOARD_FILE = "leaderboard.json"

if not os.path.exists(LEADERBOARD_FILE):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump([], f)

# -----------------------------
# SESSION STATE
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "question" not in st.session_state:
    st.session_state.question = ""
if "answer" not in st.session_state:
    st.session_state.answer = ""

# -----------------------------
# AI QUESTION GENERATOR
# -----------------------------
def generate_question(level):
    if level <= 2:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        return f"{a} + {b}", str(a + b)

    elif level <= 4:
        a = random.randint(2, 10)
        return f"{a} × 2", str(a * 2)

    elif level <= 6:
        a = random.randint(5, 20)
        return f"{a} - {random.randint(1, 5)}", str(a - 2)

    else:
        a = random.randint(2, 10)
        b = random.randint(2, 5)
        return f"{a} × {b} + {b}", str(a * b + b)

# -----------------------------
# LOAD QUESTION
# -----------------------------
if st.session_state.question == "":
    q, ans = generate_question(st.session_state.level)
    st.session_state.question = q
    st.session_state.answer = ans

# -----------------------------
# UI SECTION
# -----------------------------
st.subheader("🧩 Solve This AI Question")
st.markdown(f"### {st.session_state.question}")

user_ans = st.text_input("Your Answer:")

progress = st.progress(st.session_state.score % 100)

# -----------------------------
# CHECK ANSWER
# -----------------------------
if st.button("Submit Answer"):

    if user_ans == st.session_state.answer:
        st.success("Correct! 🎉")

        st.session_state.score += 10
        st.session_state.level += 1

        st.balloons()  # animation

    else:
        st.error(f"Wrong! Correct answer: {st.session_state.answer}")

        if st.session_state.level > 1:
            st.session_state.level -= 1

    # new question
    q, ans = generate_question(st.session_state.level)
    st.session_state.question = q
    st.session_state.answer = ans

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📊 Player Stats")
st.sidebar.write(f"⭐ Score: {st.session_state.score}")
st.sidebar.write(f"📈 Level: {st.session_state.level}")

# -----------------------------
# LEADERBOARD SAVE
# -----------------------------
def save_score(name, score):
    with open(LEADERBOARD_FILE, "r") as f:
        data = json.load(f)

    data.append({"name": name, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

# -----------------------------
# SAVE SCORE UI
# -----------------------------
st.subheader("🏆 Save Score")

name = st.text_input("Enter your name:")

if st.button("Save to Leaderboard"):
    if name:
        save_score(name, st.session_state.score)
        st.success("Saved to leaderboard!")

# -----------------------------
# SHOW LEADERBOARD
# -----------------------------
st.subheader("🏅 Leaderboard")

with open(LEADERBOARD_FILE, "r") as f:
    leaders = json.load(f)

for i, player in enumerate(leaders):
    st.write(f"{i+1}. {player['name']} - {player['score']}")
