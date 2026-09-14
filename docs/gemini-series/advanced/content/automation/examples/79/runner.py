"""A one-document adapter for the example workflow; no git writes or comments."""
import json
import os
import shutil
from pathlib import Path

from pipeline import atomic_json, run_batch


def run(root: Path, env: dict) -> dict:
    root = root.resolve()
    mode, document = env.get("LESSON_MODE", "fixture"), env.get("LESSON_DOCUMENT", "doc01.md")
    out = root / "out"
    out.mkdir(parents=True, exist_ok=True)
    report = {"mode": mode, "document": document, "status": "failed", "remote_actions_run": False}
    try:
        if mode not in {"fixture", "live"} or document not in {"doc01.md", "doc02.md"}:
            raise ValueError("unsupported_mode_or_document")
        if mode == "live" and (not env.get("GEMINI_API_KEY") or not env.get("LESSON_MODEL")):
            raise ValueError("live_mode_requires_model_and_api_key")
        selected = out / "selected"
        selected.mkdir(exist_ok=False)
        shutil.copyfile(root / "docs" / document, selected / document)
        result = run_batch(selected, out / "report", fixture=mode == "fixture",
                           config={"command": ["gemini"], "model": env.get("LESSON_MODEL")})
        report.update({"status": "failed" if result["failed"] else "complete", "batch": result,
                       "remote_actions_run": bool(env.get("GITHUB_ACTIONS"))})
    except (ValueError, OSError) as error:
        report["errorType"] = type(error).__name__
        report["reason"] = str(error)[:160]
    atomic_json(out / "workflow.json", report)
    return report


if __name__ == "__main__":
    result = run(Path(__file__).parent, dict(os.environ))
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(0 if result["status"] == "complete" else 1)
