import streamlit as st
import sqlite3
import time
from datetime import datetime
import pandas as pd
from movie_recommender import recommend, recommend_similar # already built
from intent_classifier import predict_intent # already built
from chatbot_reply import generate_bot_reply # already built
from entity_extraction import cleaned_directors #actor_names

# --- SQLite Setup ---
def create_feedback_db():
    conn = sqlite3.connect("chat_feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            generate_bot_reply TEXT,
            predict_intent TEXT,
            timestamp DATETIME,
            feedback TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_feedback(user_input, bot_response, intent, feedback):
    conn = sqlite3.connect("chat_feedback.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO feedback (user_input, generate_bot_reply, predict_intent, timestamp, feedback)
        VALUES (?, ?, ?, ?, ?)
    """, (user_input, bot_response, intent, datetime.now(), feedback))
    conn.commit()
    conn.close()

# Load movie data for autocomplete
movies_df = pd.read_csv("South_Indian_movies_cleaned.csv")
movie_titles = sorted(movies_df['title'].dropna().unique())

# ---- Streamlit Layout ----
# UI setup
st.set_page_config(page_title="🎬 Movie Recommender + Chatbot", layout="wide")
st.title("🎥 South Indian Movie Recommender + Chatbot")

# Create two columns: Recommender (left), Chatbot (right)
col1, col2 = st.columns(2)

# --- Left: Movie Recommender ---
with col1:
    st.header("🎞️ South Indian Movie Recommender")
    selected_movie = st.selectbox("Type or select a movie title", movie_titles)

    if st.button("Recommend Similar Movies"):
        recommendations = recommend(selected_movie)
        if recommendations:
            for title, year, lang in recommendations:
                st.markdown(f"✅ **{title}** ({year}) — *{lang}*")
        else:
            st.warning("No recommendations found. Try another movie.")

# --- Right: Movie Chatbot ---
with col2:
    st.header("🤖 Movie Chatbot")

    # Load actor and director names
    #actor_names = actor_names
    director_names = cleaned_directors
    #all_names = sorted(set(actor_names + director_names + movie_titles)) 

    # Init state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = ""
    if "last_bot_response" not in st.session_state:
        st.session_state.last_bot_response = ""
    if "last_intent" not in st.session_state:
        st.session_state.last_intent = ""

    # Clear Chat
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    # User input box
    user_input = st.chat_input("Type your message...")
    if user_input:
        bot_response = generate_bot_reply(user_input)

        # FIX: Convert list response to string
        if isinstance(bot_response, list):
            bot_response = ", ".join(str(x) for x in bot_response)
        bot_response = str(bot_response) if not isinstance(bot_response, str) else bot_response

        intent = predict_intent(user_input)

        st.session_state.last_user_input = user_input
        st.session_state.last_bot_response = bot_response
        st.session_state.last_intent = intent

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", bot_response))

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(
                f"""
                <div style="text-align: right; margin-bottom: 10px;">
                    <span style="
                        background-color: #dcf8c6;
                        padding: 10px 15px;
                        border-radius: 15px;
                        display: inline-block;
                        max-width: 70%;
                        word-wrap: break-word;
                        ">
                        {msg}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="text-align: left; margin-bottom: 10px;">
                    <span style="
                        background-color: #f1f0f0;
                        padding: 10px 15px;
                        border-radius: 15px;
                        display: inline-block;
                        max-width: 70%;
                        word-wrap: break-word;
                        ">
                        {msg}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Feedback Buttons
        # if st.session_state.chat_history and "last_user_input" in st.session_state:
        #     feedback = st.radio("Was my response helpful?", ("👍 Yes", "👎 No"), horizontal=True)
        #     if feedback:
        #         if feedback == "👍 Yes":
        #             store_feedback(
        #                 st.session_state.last_user_input,
        #                 st.session_state.last_bot_response,
        #                 st.session_state.last_intent,
        #                 "positive"
        #             )
        #         else:
        #             store_feedback(
        #                 st.session_state.last_user_input,
        #                 st.session_state.last_bot_response,
        #                 st.session_state.last_intent,
        #                 "negative"
        #             )
        #         st.success("Thanks for your feedback!")

    if st.session_state.chat_history and "last_user_input" in st.session_state:
        feedback_col1, feedback_col2 = st.columns([1, 1])
        with feedback_col1:
            if st.button("👍"):
                store_feedback(
                    st.session_state.last_user_input,
                    st.session_state.last_bot_response,
                    st.session_state.last_intent,
                    "positive"
                )
                st.success("Thanks for your feedback!")
        with feedback_col2:
            if st.button("👎"):
                store_feedback(
                    st.session_state.last_user_input,
                    st.session_state.last_bot_response,
                    st.session_state.last_intent,
                    "negative"
                )
                st.success("Thanks for your feedback!")

# Initialize feedback database
create_feedback_db()

# if st.checkbox("Show feedback log"):
#     conn = sqlite3.connect("chat_feedback.db")
#     feedback_df = pd.read_sql("SELECT * FROM feedback ORDER BY timestamp DESC", conn)
#     st.dataframe(feedback_df)
#     conn.close()

import streamlit as st
import sqlite3
import pandas as pd

st.title("📊 Admin Feedback Dashboard")

# Simple password protection
password = st.text_input("Enter admin password:", type="password")

if password == st.secrets["admin"]["admin_password"]:   # set this in Streamlit Cloud secrets
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM feedback", conn)
    
    st.write(f"✅ Total feedback collected: {len(df)}")
    st.dataframe(df)
    
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Feedback (CSV)", data=csv, file_name="feedback.csv")
    
    with open("feedback.db", "rb") as f:
        st.download_button("⬇️ Download Feedback Database", data=f, file_name="feedback.db")
else:
    st.warning("🔒 Enter password to access the feedback dashboard")


