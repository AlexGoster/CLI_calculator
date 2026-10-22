import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "calculator.py"


def run(tmp_path, *args, text=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=tmp_path, input=text,
                          text=True, capture_output=True, encoding="utf-8", timeout=10)


def test_cli_history_and_clear(tmp_path):
    assert run(tmp_path, "5", "+", "3").returncode == 0
    assert "8.0" in run(tmp_path, "--history").stdout
    assert run(tmp_path, "--clear").returncode == 0
    assert not (tmp_path / "calculator_history.json").exists()


def test_interactive_recovers_after_error(tmp_path):
    result = run(tmp_path, text="1 / 0\n2 + 3\nq\n")
    assert result.returncode == 0
    assert "5.0" in result.stdout


def test_incomplete_args_and_eof(tmp_path):
    result = run(tmp_path, "1")
    assert result.returncode != 0 and "Traceback" not in result.stderr
    assert run(tmp_path, text="").returncode == 0


def test_corrupt_history_is_preserved(tmp_path):
    history = tmp_path / "calculator_history.json"
    history.write_text("broken", encoding="utf-8")
    result = run(tmp_path, "1", "+", "2")
    assert result.returncode != 0 and "Traceback" not in result.stderr
    assert history.read_text() == "broken"


def test_nonfinite_rejected(tmp_path):
    for args in [("nan", "+", "1"), ("1e308", "*", "1e308")]:
        assert run(tmp_path, *args).returncode != 0
