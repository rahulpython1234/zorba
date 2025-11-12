
import sqlite3, time, pytest

def test_db_connection(init_temp_db):
    conn = sqlite3.connect(init_temp_db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    assert "conversations" in tables
    assert "feedback" in tables
    conn.close()

def test_db_write_and_read(init_temp_db):
    conn = sqlite3.connect(init_temp_db)
    c = conn.cursor()
    ts = time.time()
    c.execute("INSERT INTO conversations (ts, user_text, zorba_reply, audio_path) VALUES (?, ?, ?, ?)", (ts, "test question", "test answer", "/tmp/test.mp3"))
    conn.commit()
    c.execute("SELECT user_text, zorba_reply FROM conversations ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    assert row[0] == "test question"
    assert row[1] == "test answer"
    conn.close()

def test_feedback_write_and_read(init_temp_db):
    conn = sqlite3.connect(init_temp_db)
    c = conn.cursor()
    ts = time.time()
    c.execute("INSERT INTO conversations (ts, user_text, zorba_reply, audio_path) VALUES (?, ?, ?, ?)", (ts, "initial q", "initial a", "/tmp/temp.mp3"))
    conn.commit()
    convo_id = c.lastrowid
    c.execute("INSERT INTO feedback (ts, convo_id, rating, comment) VALUES (?, ?, ?, ?)", (ts, convo_id, 4, "ok"))
    conn.commit()
    c.execute("SELECT rating, comment FROM feedback ORDER BY id DESC LIMIT 1")
    r = c.fetchone()
    assert r[0] == 4
    conn.close()

def test_db_data_integrity(init_temp_db):
    conn = sqlite3.connect(init_temp_db)
    c = conn.cursor()
    c.execute("INSERT INTO conversations (ts, user_text, zorba_reply) VALUES (?, ?, ?)", (time.time(), "q1", "a1"))
    convo_id = c.lastrowid
    c.execute("INSERT INTO feedback (ts, convo_id, rating, comment) VALUES (?, ?, ?, ?)", (time.time(), convo_id, 4, "good"))
    conn.commit()
    c.execute("SELECT f.rating FROM feedback f JOIN conversations c ON f.convo_id = c.id WHERE c.id = ?", (convo_id,))
    rating = c.fetchone()[0]
    assert rating == 4
    conn.close()
