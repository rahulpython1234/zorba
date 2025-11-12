
import os, sqlite3, pytest, importlib, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
MOCK_LLM = os.getenv("MOCK_LLM", "0") == "1"

@pytest.fixture(scope="session")
def temp_db_path(tmp_path_factory):
    p = tmp_path_factory.mktemp("data") / "test_zorba.sqlite"
    return str(p)

@pytest.fixture(scope="session")
def init_temp_db(temp_db_path):
    conn = sqlite3.connect(temp_db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL,
        user_text TEXT,
        zorba_reply TEXT,
        audio_path TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts REAL,
        convo_id INTEGER,
        rating INTEGER,
        comment TEXT
    )""")
    conn.commit()
    yield temp_db_path
    conn.close()

@pytest.fixture(autouse=True) # Autouse to apply mocking globally
def mock_llm(monkeypatch):
    """Mock LLM for testing without API calls."""
    if MOCK_LLM:
        class FakeLLM:
            def invoke(self, messages):
                # Simulates LLM response based on prompt structure
                content = messages[0].content if messages and hasattr(messages[0], 'content') else ""
                if "name" in content.lower():
                    return type("Response", (), {"content": "My name is Lakshay."})
                return type("Response", (), {"content": "MOCK LLM: This is a test response from Zorba AI."})

        monkeypatch.setattr("langchain_openai.ChatOpenAI", lambda **kwargs: FakeLLM())
        monkeypatch.setattr("langchain_groq.ChatGroq", lambda **kwargs: FakeLLM())

@pytest.fixture
def import_app(monkeypatch, init_temp_db):
    monkeypatch.setenv("DB_PATH", init_temp_db)
    try:
        if "app" in sys.modules:
            importlib.reload(sys.modules["app"])
        app = importlib.import_module("app")
    except ImportError:
        pytest.skip("app.py not found - create it first")
    setattr(app, "__MOCK_LLM__", MOCK_LLM)

    # Ensure db_conn is available for tests that need it
    if hasattr(app, 'setup_db_connection'):
        app.setup_db_connection(init_temp_db)
    else:
        # Fallback for apps not explicitly setting up DB connection
        app.db_conn = sqlite3.connect(init_temp_db)

    return app

@pytest.fixture
def sample_history():
    return [("hello", "hi there"), ("how are you", "fine")]

@pytest.fixture
def sample_financial_data():
    import pandas as pd
    return pd.DataFrame({
        'year': [2021, 2022, 2023, 2024],
        'revenue': [1000000, 1250000, 1600000, 2100000],
        'cogs': [600000, 725000, 920000, 1200000],
        'opex': [300000, 350000, 420000, 550000]
    })
