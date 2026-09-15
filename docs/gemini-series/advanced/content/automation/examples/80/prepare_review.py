"""Validate candidate docs in a separate tree; produce a patch for human review."""
import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ALLOWED = {f"doc{i:02d}.md" for i in range(1, 11)}


def links(text: str) -> list[str]:
    # This lesson supports simple inline Markdown links outside fenced code blocks.
    plain = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.findall(r"\[[^\]\n]+\]\(([^\s)]+)\)", plain)


def check(tree: dict[str, str]) -> list[dict]:
    problems = []
    for name, text in tree.items():
        if not re.search(r"^# .+", text, flags=re.MULTILINE) or not re.search(r"^## 來源\s*$", text, flags=re.MULTILINE):
            problems.append({"file": name, "reason": "missing_title_or_sources"})
        for target in links(text):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                problems.append({"file": name, "target": target, "reason": "external_url_needs_separate_review"})
                continue
            destination = unquote(url.path) or name
            if destination not in ALLOWED or destination not in tree:
                problems.append({"file": name, "target": target, "reason": "missing_or_outside_target"})
                continue
            # Explicit markers avoid guessing a site's heading-to-anchor rules.
            if url.fragment and f'<a id="{unquote(url.fragment)}"></a>' not in tree[destination]:
                problems.append({"file": name, "target": target, "reason": "missing_anchor"})
    return problems


def prepare(source: Path, proposals: dict, output: Path) -> dict:
    source = source.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {"publishable": False, "ready_for_human_review": False, "applied": False}
    report_file = output / "review.json"
    report_file.write_text(json.dumps(report) + "\n", encoding="utf-8", newline="\n")
    try:
        if not isinstance(proposals, dict) or any(name not in ALLOWED for name in proposals):
            raise ValueError("proposal_outside_scope")
        before = {}
        for name in sorted(ALLOWED):
            file = source / name
            if file.is_symlink() or not file.resolve().is_relative_to(source):
                raise ValueError("linked_source_not_allowed")
            before[name] = file.read_text(encoding="utf-8")
        after = dict(before)
        for name, text in proposals.items():
            if not isinstance(text, str) or len(text) > 16000:
                raise ValueError("invalid_proposal_text")
            after[name] = text
        problems = check(after)
        report["original_problems"] = check(before)
        report["remaining_problems"] = problems
        if problems:
            report["reason"] = "candidate_validation_failed"
        else:
            patch, changes = [], []
            for name in sorted(ALLOWED):
                if before[name] == after[name]:
                    continue
                patch += list(difflib.unified_diff(before[name].splitlines(keepends=True), after[name].splitlines(keepends=True), fromfile="a/" + name, tofile="b/" + name))
                changes.append({"file": name, "beforeHash": hashlib.sha256(before[name].encode()).hexdigest(),
                                "afterHash": hashlib.sha256(after[name].encode()).hexdigest()})
                candidate = output / "candidates" / name
                candidate.parent.mkdir(exist_ok=True)
                candidate.write_text(after[name], encoding="utf-8", newline="\n")
            (output / "changes.patch").write_text("".join(patch), encoding="utf-8", newline="\n")
            report.update({"ready_for_human_review": True, "changes": changes})
    except (ValueError, OSError) as error:
        report["reason"] = str(error)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("proposals", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = prepare(args.source, json.loads(args.proposals.read_text(encoding="utf-8")), args.output)
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(0 if report["ready_for_human_review"] else 1)
