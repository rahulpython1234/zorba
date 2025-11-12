
import subprocess, sys, datetime, os, textwrap
from pathlib import Path

def run_pytest_and_report(output_path="test_reports/test_report.txt"):
    t0 = datetime.datetime.now()

    # --- Ensure output directory exists ---
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # -------------------------------------

    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "--maxfail=5",
        "--html=test_reports/test_report.html",
        "--self-contained-html"
    ]
    # Using textwrap.dedent for the print statement to avoid SyntaxError
    print(textwrap.dedent(f"""
================================================================================
⚙️ ZORBA AI TEST SUITE
================================================================================
Started: {t0.strftime('%Y-%m-%d %H:%M:%S')}
Command: {' '.join(cmd)}
================================================================================
"""))

    proc = subprocess.run(cmd, capture_output=True, text=True)
    Path(output_path).write_text(proc.stdout, encoding="utf-8")
    print(proc.stdout)
    print(f"HTML report saved at test_reports/test_report.html")
    return proc.returncode

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Zorba AI tests")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (no API calls)")
    # Use parse_known_args() to ignore arguments passed by the Colab environment
    args, unknown = parser.parse_known_args()

    if args.mock:
        os.environ["MOCK_LLM"] = "1"
        # Using textwrap.dedent for the print statement to avoid SyntaxError
        print(textwrap.dedent("""
Running in MOCK mode (no API calls)
"""))

    rc = run_pytest_and_report()
    sys.exit(rc)
