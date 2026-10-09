"""scripts/status.py: a step's first speed measurement must not count the hours it waited in the queue."""
import importlib.util
import time
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "scripts" / "status.py"
spec = importlib.util.spec_from_file_location("status", SRC)
status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status)


def _render(monkeypatch, tmp_path, lines_now: int, prev_entry: dict) -> dict:
    f = tmp_path / "probes_x.jsonl"
    f.write_text("{}\n" * lines_now)
    monkeypatch.setattr(status, "OUT", tmp_path)
    monkeypatch.setattr(status, "gpu_line", lambda: "GPU: n/a")
    monkeypatch.setattr(status, "steps", lambda: [
        {"name": "S", "file": f, "total": 300, "exp": 10.0, "kind": "items", "group": "G"}])
    return status.render({"S": prev_entry}, False)


def test_first_measurement_ignores_the_queue_wait(monkeypatch, tmp_path, capsys):
    # the step was first seen idle (0 lines) 10.5 h ago and now has 143 lines: that is not 143 items per 10.5 h
    cur = _render(monkeypatch, tmp_path, 143, {"lines": 0, "t": time.time() - 38000, "rate": None})
    assert cur["S"]["rate"] is None  # no measurement yet; the ETA falls back to the expected seconds per item
    assert "est." in capsys.readouterr().out


def test_second_measurement_uses_the_delta(monkeypatch, tmp_path):
    # 143 -> 203 lines in 15 min = 4 items per minute
    cur = _render(monkeypatch, tmp_path, 203, {"lines": 143, "t": time.time() - 900, "rate": None})
    assert abs(60 * cur["S"]["rate"] - 4.0) < 0.05
