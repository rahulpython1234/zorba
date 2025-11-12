
import os, pytest, pkgutil

def test_openai_key_present():
    """Test that API keys are set (unless in mock mode)."""
    if os.getenv("MOCK_LLM", "0") == "1":
        pytest.skip("Running in mock mode")

    key = os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")
    assert key, "No API key found. Set OPENAI_API_KEY or GROQ_API_KEY, or run with MOCK_LLM=1"

def test_required_packages_importable():
    """Test that all required packages can be imported."""
    required = [
        "langchain_openai",
        "langchain_groq",
        "langchain_chroma",
        "langchain_huggingface",
        "gtts",
        "pandas",
        "chromadb",
        "plotly"
    ]

    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    assert not missing, f"Missing packages: {missing}"

def test_python_version():
    """Test Python version is 3.8+."""
    import sys
    assert sys.version_info >= (3, 8), "Python 3.8+ required"
