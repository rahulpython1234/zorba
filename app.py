"""
Zorba AI - Mock App (Clean Version)
-----------------------------------
A fully functional placeholder app used for testing.
This file contains all functions/classes expected by the Zorba AI test suite.
"""

import sqlite3
import os
import time
import plotly.graph_objects as go

# ===============================
# DATABASE SETUP
# ===============================
DB_PATH = os.getenv("DB_PATH", "zorba.sqlite")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    user_text TEXT,
    zorba_reply TEXT,
    audio_path TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    convo_id INTEGER,
    rating INTEGER,
    comment TEXT
)
""")
conn.commit()
db_conn = conn


# ===============================
# CORE CHAT HANDLER
# ===============================
def zorba_reply(user_text, history=None):
    """Simulate a chatbot reply and store in DB."""
    reply = f"Zorba AI mock reply: You said '{user_text}'."
    audio_path = "/tmp/mock_audio.mp3"
    convo_id = save_convo(user_text, reply, audio_path)
    return reply, audio_path, convo_id


def save_convo(user_text, reply, audio_path):
    """Save a conversation record."""
    ts = time.time()
    cur = db_conn.cursor()
    cur.execute(
        "INSERT INTO conversations (ts, user_text, zorba_reply, audio_path) VALUES (?, ?, ?, ?)",
        (ts, user_text, reply, audio_path)
    )
    db_conn.commit()
    return cur.lastrowid


def save_feedback(convo_id, rating, comment):
    """Save feedback for a conversation."""
    ts = time.time()
    cur = db_conn.cursor()
    cur.execute(
        "INSERT INTO feedback (ts, convo_id, rating, comment) VALUES (?, ?, ?, ?)",
        (ts, convo_id, rating, comment)
    )
    db_conn.commit()


# ---------------------------
# MOCK RETRIEVER & DASHBOARD
# ---------------------------
class MockRetriever:
    """Simple retriever mock."""
    def invoke(self, query):
        return [{"text": f"Mock document for '{query}'"}]

retriever = MockRetriever()


def generate_dashboard():
    """Create a sample dashboard figure."""
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Chats", "Feedback"], y=[12, 5]))
    return fig, "Dashboard generated successfully."


# ---------------------------
# CONVERSATION CONTEXT HANDLER
# ---------------------------
class ZorbaConversation:
    """Conversation handler with basic memory."""
    def __init__(self, voice_enabled=False, use_groq=False):
        self.conversation_history = []
        self.memory = {}

    def chat(self, message):
        msg_lower = message.lower()

        if "my name is" in msg_lower:
            name = message.split("is")[-1].strip()
            self.memory["name"] = name
            response = f"Nice to meet you, {name}!"
        elif "what is my name" in msg_lower:
            name = self.memory.get("name")
            if name:
                response = f"Your name is {name}."
            else:
                response = "I don’t know your name yet."
        else:
            response = f"Zorba remembers you said '{message}'"

        self.conversation_history.append(("user", message))
        self.conversation_history.append(("zorba", response))
        return response


# ===============================
# FINANCIAL ANALYZER
# ===============================
class FinancialAnalyzer:
    """Performs mock financial analysis."""
    def comprehensive_analysis(self, df):
        latest_revenue = float(df["revenue"].iloc[-1])
        growth_rate = (df["revenue"].iloc[-1] - df["revenue"].iloc[-2]) / df["revenue"].iloc[-2]
        return {
            "historical_analysis": {"latest_revenue": latest_revenue},
            "forward_projections": {"growth_rate": round(growth_rate, 2)}
        }
