# Programming Benchmark Demo

An end-to-end evaluation pipeline for Python code generation. The benchmark contains 12 original tasks and 48 pytest cases. The runner requests one code submission per task, tests it in a fresh workspace, and writes human-readable Markdown and machine-readable JSON.

[Read the mock score report](reports/report.md) · [Inspect the JSON results](reports/report.json)

## Run the offline demo

Requires Python 3.11 or newer. In a fresh Python environment, run these commands from the repository root.

```sh
python -m pip install -r requirements.txt
python runner.py --mock --out-dir runs/mock
python -m pytest -q
python runner.py --reference --out-dir runs/reference
```

The first command installs pytest. Subsequent mock and reference runs work offline without credentials or Docker. The mock returns seven bundled reference answers and five deliberately defective answers. The judge runs each answer against its test suite to derive the scores.

## Mock run · 7 of 12 passed (58.3%)

| Category | Passed | Total |
| --- | ---: | ---: |
| Algorithms | 2 | 4 |
| Bug fixes | 2 | 4 |
| Practical tasks | 3 | 4 |

The cursor pagination fixture drops an event that shares the cursor's timestamp. The invoice fixture uses a naive CSV parser and raises a value error on a quoted comma. Both failures are visible in the [generated report](reports/report.md). The scores describe synthetic submissions.

## Run with an OpenAI-compatible endpoint

Build the judge image on a machine running Docker in Linux container mode.

```sh
docker build -t benchmark-judge .
```

Set these environment variables in the shell that will launch the runner.

| Variable | Value |
| --- | --- |
| `BENCHMARK_BASE_URL` | API root, for example `http://127.0.0.1:8000/v1`. The runner appends `/chat/completions`. |
| `BENCHMARK_MODEL` | Model ID accepted by your endpoint. |
| `BENCHMARK_API_KEY` | Optional bearer credential for endpoints that require authentication. Use HTTPS for authenticated non-loopback endpoints. |

```sh
python runner.py --live --out-dir runs/live --timeout 20
```

The runner sends the public `task.md` and a response-format instruction as chat messages. Grading tests, reference solutions and mock fixtures stay out of the request. The API adapter accepts raw Python or a single Python code fence. Each returned submission is graded in a non-root Linux container with networking disabled, a read-only root filesystem and a read-only mount containing only the submission and its tests. CPU, memory, PID count, judge time and captured output are bounded. Use a local Docker engine that can mount the host's temporary directory. [Docker run options](https://docs.docker.com/reference/cli/docker/container/run/) · [Docker bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

## Scoring and layout

| Path | Contents |
| --- | --- |
| `challenges/` | Twelve task folders, with the prompt, category, difficulty and four pytest cases each. Bug-fix prompts include starter code. |
| `solutions/` | Twelve reference implementations, used offline to verify the test suites. |
| `mock_submissions/` | Five defective submissions that the offline fixture provider uses in place of references. |
| `runner.py`, `Dockerfile` | Dataset loading, fixture and HTTP adapters, and the local and containerized judges. |
| `report.py`, `reports/` | Report generator and a checked-in mock run. |
| `harness_tests/` | Tests for the provider boundary, judge verdicts, timeout, Docker options and report aggregation. |

Each task is worth one point. A submission earns that point only when all its tests pass. Every task counts in the denominator. The reports include overall, category and difficulty breakdowns. The JSON also includes status counts and per-task judge duration, which excludes endpoint latency.

| Verdict | Meaning |
| --- | --- |
| `pass` | All tests passed. |
| `fail` | A test failed an assertion or raised an exception. |
| `test_error` | Pytest could not collect the tests or exited without a passing result. |
| `timeout` | The judge exceeded the per-task time limit. |
| `provider_error` | The endpoint failed or returned unusable content. |

Exit code 0 means the run finished and wrote its reports. Exit code 1 means a reference check finished with failures. Exit code 2 means the runner could not finish because of configuration or infrastructure.

## Scope and verification

- This small public dataset measures functional correctness against included cases. The tests and reference answers are public, so the dataset is suitable for a pipeline demonstration and smoke tests.
- The judge imports the submission into the pytest process. The Docker configuration isolates that process from the host for this demo. Tamper-resistant grading for adversarial submissions would require a separate trust boundary between the test controller and submitted code.
- The demo makes one request per task and has no provider retries, concurrency or cross-model statistics.
- Verified in Python 3.11 on Windows with 12 passing harness tests, 12 passing reference submissions and two matching mock scorecards. The HTTP adapter was exercised against a local stub. The live Docker path requires a Linux container engine and was not executed in this verification environment.
