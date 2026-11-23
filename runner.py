"""Generate one Python submission per challenge and score it with pytest."""

import argparse
from dataclasses import asdict, dataclass
from http.client import HTTPException
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from threading import Thread
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4

from report import write_reports

ROOT = Path(__file__).resolve().parent
LOG_LIMIT = 16_384
RESPONSE_LIMIT = 256 * 1024
PYTEST_ARGS = (
    "-m", "pytest", "-q", "--tb=short", "--color=no", "-p", "no:cacheprovider",
    "--confcutdir=.", "tests",
)


@dataclass(frozen=True)
class Challenge:
    id: str
    title: str
    category: str
    difficulty: str
    task_file: Path


@dataclass(frozen=True)
class ProcessResult:
    returncode: int
    output: str
    timed_out: bool
    truncated: bool


@dataclass(frozen=True)
class Verdict:
    status: str
    detail: str
    duration_seconds: float


class ProviderError(Exception):
    """The endpoint failed or returned an unusable completion."""


class NoRedirect(HTTPRedirectHandler):
    """Keep credentials on the configured endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class OpenAICompatible:
    def __init__(self, base_url, model, api_key, timeout=45):
        parsed = urlsplit(base_url)
        if (
            parsed.scheme not in {"http", "https"} or not parsed.hostname
            or parsed.username is not None or parsed.query or parsed.fragment
        ):
            raise ValueError("BENCHMARK_BASE_URL must be an HTTP(S) API root without credentials or a query.")
        loopback = parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        if api_key and parsed.scheme != "https" and not loopback:
            raise ValueError("Use HTTPS when sending a credential to a non-loopback endpoint.")
        self.url = base_url.rstrip("/") + "/chat/completions"
        self.model = model
        self.timeout = timeout
        self.opener = build_opener(NoRedirect())
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def generate(self, challenge):
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": (
                    "Return one complete Python 3.11 source file. "
                    "Use the standard library only. Keep all required function signatures. "
                    "Return raw code or one Python fenced block without explanations."
                )},
                {"role": "user", "content": challenge.task_file.read_text(encoding="utf-8")},
            ],
        }
        request = Request(self.url, data=json.dumps(payload).encode("utf-8"), headers=self.headers)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read(RESPONSE_LIMIT + 1)
        except HTTPError as error:
            error.close()
            raise ProviderError(f"Endpoint returned HTTP {error.code}.") from None
        except (URLError, OSError, HTTPException) as error:
            raise ProviderError(f"Endpoint connection failed ({type(error).__name__}).") from None
        if len(raw) > RESPONSE_LIMIT:
            raise ProviderError("Endpoint response exceeded the 256 KiB limit.")
        try:
            choice = json.loads(raw)["choices"][0]
            content = choice["message"]["content"]
            finish_reason = choice.get("finish_reason")
        except (ValueError, KeyError, IndexError, TypeError, AttributeError):
            raise ProviderError("Endpoint returned an unexpected completion schema.") from None
        if finish_reason is not None and finish_reason != "stop":
            raise ProviderError("Endpoint ended without a complete response.")
        if not isinstance(content, str):
            raise ProviderError("Endpoint completion contained no text.")
        return content


def submission_source(content):
    source = content.strip()
    fence = chr(96) * 3
    fenced = re.fullmatch(rf"{fence}(?:python|py)?[ \t]*\r?\n(.*?)\r?\n{fence}", source, re.S | re.I)
    if fenced:
        source = fenced.group(1).strip("\r\n")
    if not source.strip() or any(line.lstrip().startswith(fence) for line in source.splitlines()):
        raise ProviderError("Expected one Python submission without surrounding prose.")
    return source + "\n"


def load_challenges():
    challenges = []
    for metadata_file in sorted((ROOT / "challenges").glob("*/metadata.json")):
        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        task_file = metadata_file.with_name("task.md")
        if metadata["id"] != metadata_file.parent.name or not task_file.is_file():
            raise ValueError(f"Invalid challenge directory: {metadata_file.parent.name}")
        challenges.append(Challenge(**metadata, task_file=task_file))
    if not challenges:
        raise ValueError("No challenges found.")
    return challenges


def fixture_source(challenge, mode):
    path = ROOT / "solutions" / f"{challenge.id}.py"
    if mode == "mock":
        alternative = ROOT / "mock_submissions" / path.name
        if alternative.is_file():
            path = alternative
    return path.read_text(encoding="utf-8")


def run_process(command, timeout, *, cwd=None, env=None):
    """Drain merged output while retaining at most LOG_LIMIT bytes."""
    with subprocess.Popen(
        command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    ) as process:
        captured = bytearray()
        truncated = False

        def drain():
            nonlocal truncated
            while chunk := process.stdout.read1(4096):
                remaining = LOG_LIMIT - len(captured)
                captured.extend(chunk[:remaining])
                truncated |= len(chunk) > remaining

        reader = Thread(target=drain, daemon=True)
        reader.start()
        timed_out = False
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
            reader.join()
        return ProcessResult(
            process.returncode, captured.decode("utf-8", errors="replace").replace("\r\n", "\n"), timed_out, truncated,
        )


def docker_command(image, scratch, name):
    return [
        "docker", "run", "--rm", "--name", name, "--pull", "never",
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--user", "65534:65534",
        "--memory", "256m", "--memory-swap", "256m", "--cpus", "1", "--pids-limit", "64",
        "--log-driver", "none", "--tmpfs", "/tmp:rw,noexec,nosuid,nodev,size=32m",
        "--mount", f"type=bind,source={scratch},target=/work,readonly",
        "--workdir", "/work", "--env", "PYTEST_DISABLE_PLUGIN_AUTOLOAD=1",
        "--entrypoint", "python", image, "-B", *PYTEST_ARGS,
    ]


def local_environment():
    allowed = ("SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "PATH", "TEMP", "TMP", "TMPDIR")
    env = {key: os.environ[key] for key in allowed if key in os.environ}
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def failure_detail(output):
    error = next((line[3:].strip() for line in output.splitlines() if line.startswith("E ")), "")
    failed = next((line.partition(" - ")[0] for line in output.splitlines() if line.startswith(("FAILED ", "ERROR "))), "")
    return " — ".join(part for part in (failed, error) if part)[:600] or output.strip()[-600:]


def judge(challenge, source, timeout, *, image=None):
    started = perf_counter()
    with tempfile.TemporaryDirectory(prefix="benchmark-judge-") as folder:
        scratch = Path(folder).resolve()
        if image and "," in str(scratch):
            raise RuntimeError("Docker bind paths must not contain commas. Set TMP or TMPDIR to another folder.")
        scratch.chmod(0o755)
        code = scratch / "solution.py"
        code.write_text(source, encoding="utf-8")
        code.chmod(0o644)
        tests = scratch / "tests"
        tests.mkdir(mode=0o755)
        for item in sorted((challenge.task_file.parent / "tests").glob("test_*.py")):
            destination = tests / item.name
            shutil.copyfile(item, destination)
            destination.chmod(0o644)

        if image:
            name = f"benchmark-judge-{uuid4().hex}"
            result = None
            try:
                result = run_process(docker_command(image, scratch, name), timeout)
            finally:
                if result is None or result.timed_out or result.returncode == 125:
                    cleanup = run_process(["docker", "rm", "-f", name], 10)
                    if cleanup.returncode and "No such container" not in cleanup.output:
                        raise RuntimeError(f"Docker could not confirm cleanup for {name}.")
        else:
            result = run_process(
                [sys.executable, "-B", *PYTEST_ARGS], timeout, cwd=scratch, env=local_environment(),
            )

    elapsed = round(perf_counter() - started, 3)
    if result.timed_out:
        return Verdict("timeout", f"Exceeded the {timeout:g}-second judge limit.", elapsed)
    if image and result.returncode in {125, 126, 127}:
        raise RuntimeError("Docker could not launch the judge. Check the image and the bind-mount path.")
    if result.returncode == 0 and re.search(r"(?m)^[1-9]\d* passed in [\d.]+s$", result.output):
        return Verdict("pass", "", elapsed)
    status = "fail" if result.returncode == 1 else "test_error"
    detail = failure_detail(result.output) or f"Pytest exited with code {result.returncode}."
    if result.truncated:
        detail += " [log truncated]"
    return Verdict(status, detail, elapsed)


def prepare_docker(image):
    if shutil.which("docker") is None:
        raise RuntimeError("Live scoring requires Docker with Linux containers.")
    engine = run_process(["docker", "info", "--format", "{{.OSType}}"], 15)
    if engine.returncode or engine.output.strip() != "linux":
        raise RuntimeError("Start a local Docker engine in Linux container mode.")
    check_image = run_process(["docker", "image", "inspect", "--format", "{{.Id}}", image], 15)
    if check_image.returncode:
        raise RuntimeError("Judge image missing. Build it with: docker build -t benchmark-judge .")


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("expected a positive number of seconds")
    return seconds


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--mock", dest="mode", action="store_const", const="mock", help="Run bundled fixtures (default).")
    modes.add_argument("--live", dest="mode", action="store_const", const="live", help="Call an endpoint and require Docker.")
    modes.add_argument("--reference", dest="mode", action="store_const", const="reference", help="Verify all bundled references.")
    parser.set_defaults(mode="mock")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"), help="Directory for report.md and report.json.")
    parser.add_argument("--timeout", type=positive_seconds, default=10, help="Maximum seconds per judge process.")
    parser.add_argument("--api-timeout", type=positive_seconds, default=45, help="Endpoint socket timeout in seconds.")
    parser.add_argument("--image", default="benchmark-judge", help="Trusted local Docker judge image (live mode).")
    args = parser.parse_args(argv)

    model = {"mock": "offline-fixture", "reference": "bundled-references"}.get(args.mode)
    provider = None
    try:
        if args.mode == "live":
            base_url = os.environ.get("BENCHMARK_BASE_URL", "").strip()
            model = os.environ.get("BENCHMARK_MODEL", "").strip()
            if not base_url or not model:
                raise ValueError("Set BENCHMARK_BASE_URL and BENCHMARK_MODEL for live scoring.")
            prepare_docker(args.image)
            provider = OpenAICompatible(
                base_url, model, os.environ.get("BENCHMARK_API_KEY", ""), args.api_timeout,
            )

        results = []
        for challenge in load_challenges():
            try:
                if provider:
                    source = submission_source(provider.generate(challenge))
                else:
                    source = fixture_source(challenge, args.mode)
                verdict = judge(challenge, source, args.timeout, image=args.image if provider else None)
            except ProviderError as error:
                verdict = Verdict("provider_error", str(error), 0.0)
            results.append({
                "id": challenge.id, "title": challenge.title, "category": challenge.category,
                "difficulty": challenge.difficulty, **asdict(verdict),
            })
            print(f"{challenge.id}: {verdict.status}")
        overall = write_reports(args.out_dir, mode=args.mode, model=model, results=results)["overall"]
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Benchmark stopped. {error}", file=sys.stderr)
        return 2

    print(f"{args.mode}: {overall['passed']}/{overall['total']} passed. Reports in {args.out_dir}")
    if args.mode == "reference" and overall["passed"] != overall["total"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
