"""Aggregate per-challenge verdicts into JSON and GitHub-flavored Markdown."""

from collections import Counter, defaultdict
import html
import json
from pathlib import Path


MODE_LABELS = {
    "mock": ("Mock run", "Bundled synthetic submissions · no model was called."),
    "reference": ("Reference check", "Bundled reference implementations · no model was called."),
    "live": ("Live run", "One endpoint completion per challenge."),
}
LABELS = {
    "algorithm": "Algorithms", "bugfix": "Bug fixes", "practical": "Practical tasks",
    "easy": "Easy", "medium": "Medium", "hard": "Hard",
}


def score(results):
    passed = sum(row["status"] == "pass" for row in results)
    total = len(results)
    return {"passed": passed, "total": total, "pass_rate": round(passed / total, 4) if total else 0.0}


def by_field(results, field):
    groups = defaultdict(list)
    for row in results:
        groups[row[field]].append(row)
    return {key: score(rows) for key, rows in sorted(groups.items())}


def cell(value):
    cleaned = " ".join(str(value).split())
    return html.escape(cleaned).replace("|", "&#124;").replace(chr(96), "&#96;")


def markdown(summary):
    title, subtitle = MODE_LABELS[summary["mode"]]
    overall = summary["overall"]
    lines = [
        f"# Programming Benchmark · {title}", "", f"> {subtitle}", "",
        f"**{overall['passed']} / {overall['total']} passed · {overall['pass_rate']:.1%}**",
        "", f"Submission source: {cell(summary['model'])}", "",
        "Each challenge is worth one point and passes only if all its tests pass. "
        "Every challenge is included in the denominator.", "",
        "## Score breakdown", "", "| Group | Passed | Total | Pass rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for field, label in (("by_category", "Category"), ("by_difficulty", "Difficulty")):
        groups = summary[field]
        keys = [key for key in LABELS if key in groups] + [key for key in groups if key not in LABELS]
        for key in keys:
            group = groups[key]
            lines.append(
                f"| {label} · {cell(LABELS.get(key, key))} | {group['passed']} | "
                f"{group['total']} | {group['pass_rate']:.1%} |"
            )
    lines.extend(["", "## Challenge results", "",
                  "| ID | Challenge | Difficulty | Verdict | First failure |",
                  "| --- | --- | --- | --- | --- |"])
    for row in summary["results"]:
        detail = cell(row["detail"]) if row["detail"] else "—"
        lines.append(
            f"| {cell(row['id'])} | {cell(row['title'])} | {cell(row['difficulty'])} | "
            f"{cell(row['status'])} | {detail} |"
        )
    lines.extend(["", "See report.json for status counts, category labels and judge timings.", ""])
    return "\n".join(lines)


def write_reports(directory: Path, *, mode, model, results):
    summary = {
        "schema_version": 1,
        "mode": mode,
        "model": model,
        "overall": score(results),
        "by_category": by_field(results, "category"),
        "by_difficulty": by_field(results, "difficulty"),
        "status_counts": dict(sorted(Counter(row["status"] for row in results).items())),
        "results": results,
    }
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (directory / "report.md").write_text(markdown(summary), encoding="utf-8")
    return summary
