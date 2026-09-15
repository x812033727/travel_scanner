"""Validate exact evidence and expose disagreements; never modify reviewed files."""
import argparse
import json
from pathlib import Path


def merge(root: Path, reports: list[dict]) -> dict:
    root = root.resolve()
    allowed = {"src/limit.mjs", "docs/limits.md"}
    accepted, rejected, groups = [], [], {}
    for report in reports:
        if report.get("status") != "complete":
            rejected.append({"agent": report.get("agent"), "reason": "agent_incomplete"})
            continue
        for finding in report.get("findings", []):
            try:
                name, line = finding["file"], finding["line"]
                if name not in allowed or isinstance(line, bool) or not isinstance(line, int):
                    raise ValueError("outside_scope_or_bad_line")
                file = (root / name).resolve()
                if not file.is_relative_to(root):
                    raise ValueError("symlink_outside_scope")
                lines = file.read_text(encoding="utf-8").splitlines()
                if line < 1 or line > len(lines) or lines[line - 1] != finding["quote"]:
                    raise ValueError("evidence_mismatch")
                if not all(isinstance(finding.get(k), str) and finding[k] for k in ("check", "recommendation")):
                    raise ValueError("missing_contract_fields")
                key = (name, line, finding["check"])
                groups.setdefault(key, []).append({**finding, "agent": report["agent"]})
            except (KeyError, ValueError, OSError) as error:
                rejected.append({"finding": finding, "reason": str(error)})
    conflicts = []
    for rows in groups.values():
        if len({r["recommendation"] for r in rows}) != 1:
            conflicts.append(rows)
        else:
            accepted.append({**rows[0], "agents": sorted({r["agent"] for r in rows})})
    return {"accepted": accepted, "conflicts": conflicts, "rejected": rejected,
            "ready_for_human_review": True, "automatically_applied": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("reports", nargs="+", type=Path)
    args = parser.parse_args()
    print(json.dumps(merge(args.root, [json.loads(f.read_text(encoding="utf-8")) for f in args.reports]), ensure_ascii=False, indent=2))
