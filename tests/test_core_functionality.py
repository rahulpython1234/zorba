
import os, pytest

def test_zorba_reply_exists(import_app):
    app = import_app
    assert hasattr(app, "zorba_query") or hasattr(app, "zorba_reply"),         "Main query function not found"

def test_zorba_reply_with_mock(import_app, sample_history):
    app = import_app
    if not hasattr(app, "zorba_query") and not hasattr(app, "zorba_reply"):
        pytest.skip("Query function not implemented")

    query_func = getattr(app, "zorba_query", None) or getattr(app, "zorba_reply", None)

    try:
        # Ensure we're calling the function correctly and unpacking the result if it's a tuple
        if hasattr(app, "zorba_query"):
            result = query_func("What are eco bricks?")
        else:
            # Assuming zorba_reply returns (reply_text, audio_path, convo_id)
            result, audio_path, convo_id = query_func("What are eco bricks?", sample_history)

        assert isinstance(result, str)
        assert len(result) > 0
    except Exception as e:
        if "API key" in str(e) and os.getenv("MOCK_LLM") != "1":
            pytest.skip("API key required for this test")
        raise

def test_conversation_context(import_app):
    app = import_app
    if not hasattr(app, "ZorbaConversation"):
        pytest.skip("ZorbaConversation class not found in app.py")

    conv = app.ZorbaConversation(voice_enabled=False, use_groq=False) # use_groq=False as we mock both
    response1 = conv.chat("My name is Lakshay")
    response2 = conv.chat("What is my name?")
    assert "Lakshay" in response2 # Simple check for context
    assert len(conv.conversation_history) >= 2 # At least 2 entries (user, assistant)

def test_financial_analysis(import_app, sample_financial_data):
    app = import_app
    if not hasattr(app, "FinancialAnalyzer"):
        pytest.skip("FinancialAnalyzer class not found in app.py")
    analyzer = app.FinancialAnalyzer()
    result = analyzer.comprehensive_analysis(sample_financial_data)
    assert "historical_analysis" in result
    assert "forward_projections" in result
    assert result["historical_analysis"]["latest_revenue"] > 0

def test_dashboard_generation(import_app):
    app = import_app
    if not hasattr(app, "generate_dashboard"):
        pytest.skip("generate_dashboard function not found in app.py")

    fig, status = app.generate_dashboard()
    assert status # Check if status is returned
