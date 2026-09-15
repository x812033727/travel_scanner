"""Record the native follow-up revision while preserving the initial author review."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REVIEW = HERE / "verification/authoring-review.json"
ORIGINAL = HERE / "verification/authoring-review-initial-20260914.json"


def digest(file: Path) -> str:
    return hashlib.sha256(file.read_bytes()).hexdigest()


def record(file: Path) -> dict:
    return {"path": file.relative_to(ROOT).as_posix(), "sha256": digest(file)}


def refresh(value):
    if isinstance(value, dict):
        if "path" in value and "sha256" in value:
            file = (ROOT / value["path"]).resolve()
            if not file.is_relative_to(ROOT):
                raise ValueError("Review path escaped workspace")
            value["sha256"] = digest(file)
        for child in value.values():
            refresh(child)
    elif isinstance(value, list):
        for child in value:
            refresh(child)


if __name__ == "__main__":
    data = json.loads(REVIEW.read_text(encoding="utf-8"))
    if data.get("revision") or ORIGINAL.exists():
        raise FileExistsError("This one-time review already exists; retain it and create another revision.")
    ORIGINAL.write_bytes(REVIEW.read_bytes())
    refresh(data)
    data["checkedAt"] = datetime.now(timezone.utc).isoformat()
    data["revision"] = 2
    data["supersedes"] = record(ORIGINAL)
    data["publishable"] = False
    data["boundaries"]["nativeExtensionTerminal"] = "Node 22.23.2: original CLI and PowerShell gemini.cmd passed; Node 24.13.0/24.19.0 assertion remains. Redirected stdio, no visible console or model session."
    build = json.loads((HERE / "verification/build.json").read_text(encoding="utf-8"))
    for article in data["articles"]:
        current = next(row for row in build if row["number"] == article["number"])
        article.update(current)
    files = [HERE / "verify-native.py", Path(__file__).resolve(), HERE / "README.md"]
    files += [HERE / "verification" / name for name in ("native-cli-followup-20260914.json", "native-cli-powershell-20260914.json", "native-followup.md")]
    files += [HERE / "examples/73" / name for name in ("native-cli-followup-20260914.json", "native-cli-powershell-20260914.json", "native-followup.md")]
    data["nativeFollowup"] = {"files": [record(file) for file in files], "observations": 34,
                              "passedNode22Steps": 28, "node24Failures": 2,
                              "allGoogleModelCalls": 0, "temporaryHomesRemoved": True}
    data["checks"].append({"name": "Windows original CLI and PowerShell npm shim lifecycle (Node 22.23.2)", "passed": 28,
                           "limits": "Two separate redirected-stdio runs; Node 24 failures retained."})
    REVIEW.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Saved revision 2 and preserved the initial author review.")
