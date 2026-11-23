import json
import shutil
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest


@pytest.mark.parametrize(
    ("source", "status"),
    [
        ("def double(n): return n * 2", "pass"),
        ("def double(n): return n", "fail"),
        ("def double(n): return", "fail"),
        ("def double(:", "test_error"),
    ],
)
def test_judge_runs_pytest_against_the_candidate(tmp_path, source, status):
    from runner import Challenge, judge

    task = tmp_path / "task.md"
    task.write_text("# Double\n", encoding="utf-8")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_double.py").write_text(
        "from solution import double\ndef test_double(): assert double(5) == 10\n",
        encoding="utf-8",
    )
    result = judge(Challenge("double", "Double", "algorithm", "easy", task), source, 5)
    assert result.status == status
    assert not (tmp_path / "solution.py").exists()


def test_process_timeout_and_log_bound():
    from runner import run_process

    result = run_process([sys.executable, "-c", "while True: pass"], 0.2)
    assert result.timed_out
    result = run_process([sys.executable, "-c", "print('A' * 30000)"], 5)
    assert result.truncated and len(result.output.encode("utf-8")) <= 16_384


def test_live_provider_sends_only_the_public_task(tmp_path):
    from runner import Challenge, OpenAICompatible, submission_source

    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            requests.append((
                self.path,
                self.headers.get("Authorization"),
                json.loads(self.rfile.read(int(self.headers["Content-Length"]))),
            ))
            body = json.dumps({"choices": [{"finish_reason": "stop", "message": {
                "content": "```python\ndef double(n): return 2 * n\n```"
            }}]}).encode()
            self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    task = tmp_path / "task.md"
    task.write_text("Return twice the input. Signature: double(n).", encoding="utf-8")
    (tmp_path / "reference.py").write_text("# grader material", encoding="utf-8")
    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            provider = OpenAICompatible(f"http://127.0.0.1:{server.server_port}/v1/", "fixture", "")
            result = provider.generate(Challenge("double", "Double", "algorithm", "easy", task))
        finally:
            server.shutdown()
            thread.join()
    assert submission_source(result) == "def double(n): return 2 * n\n"
    path, authorization, body = requests[0]
    assert path == "/v1/chat/completions"
    assert authorization is None
    assert body["model"] == "fixture"
    assert body["messages"][1] == {"role": "user", "content": task.read_text(encoding="utf-8")}
    assert "grader material" not in json.dumps(body)


@pytest.mark.parametrize("value", ["", "Here is code:\n```python\npass\n```", "```js\npass\n```"])
def test_ambiguous_provider_output_is_rejected(value):
    from runner import ProviderError, submission_source

    with pytest.raises(ProviderError):
        submission_source(value)


def test_live_requires_docker_before_endpoint_contact(monkeypatch):
    from runner import main

    monkeypatch.setattr(shutil, "which", lambda executable: None)
    monkeypatch.setenv("BENCHMARK_BASE_URL", "http://127.0.0.1:1/v1")
    monkeypatch.setenv("BENCHMARK_MODEL", "fixture")
    assert main(["--live"]) == 2


def test_sandbox_command_limits_resources_and_mounts_one_submission(tmp_path):
    from runner import docker_command

    command = docker_command("benchmark-judge", tmp_path, "job-abc")
    assert ["--network", "none"] == command[command.index("--network"):command.index("--network") + 2]
    assert "--read-only" in command
    assert command[command.index("--cap-drop") + 1] == "ALL"
    assert command[command.index("--security-opt") + 1] == "no-new-privileges"
    assert command[command.index("--user") + 1] == "65534:65534"
    mount = command[command.index("--mount") + 1]
    assert mount == f"type=bind,source={tmp_path},target=/work,readonly"
    assert command.count("--mount") == 1
    assert "--memory" in command and "--pids-limit" in command


def test_report_counts_each_question_once(tmp_path):
    from report import write_reports

    results = [
        {"id": "a01", "title": "One", "category": "algorithm", "difficulty": "easy",
         "status": "pass", "detail": "", "duration_seconds": 0.1},
        {"id": "b01", "title": "Two", "category": "bugfix", "difficulty": "easy",
         "status": "timeout", "detail": "5 seconds", "duration_seconds": 5.0},
        {"id": "b02", "title": "Three", "category": "bugfix", "difficulty": "medium",
         "status": "provider_error", "detail": "HTTP 429", "duration_seconds": 0.0},
    ]
    write_reports(tmp_path, mode="mock", model="stub", results=results)
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["overall"] == {"passed": 1, "total": 3, "pass_rate": 0.3333}
    assert report["by_category"]["bugfix"]["passed"] == 0
    assert report["by_difficulty"]["easy"]["pass_rate"] == 0.5
    assert len(report["results"]) == 3
    markdown = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "Mock run" in markdown and "HTTP 429" in markdown

