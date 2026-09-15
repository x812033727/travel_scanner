"""Check the actual downloadable files, then re-run their isolated CLI experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import zipfile
from pathlib import Path

import tomllib

HERE = Path(__file__).resolve().parent


def main(node: str, cli: str) -> dict:
    examples = HERE / "examples"
    checked = []
    for file in sorted(examples.glob("*.zip")):
        with zipfile.ZipFile(file) as archive:
            if archive.testzip() is not None:
                raise ValueError("ZIP CRC failed")
            if not archive.namelist() or len(archive.namelist()) != len(set(archive.namelist())):
                raise ValueError("Empty archive or duplicate members")
            for name in archive.namelist():
                if name.startswith("/") or ".." in Path(name).parts or ".git" in Path(name).parts:
                    raise ValueError("Unexpected archive path")
                if file.name == "md-verification.zip":
                    source = HERE / name if name != "README.md" else HERE / "verification/README.md"
                else:
                    source = examples / name
                if archive.read(name) != source.read_bytes():
                    raise ValueError(f"Archive differs from reviewed source: {name}")
            checked.append({"name": file.name, "members": len(archive.namelist()), "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
    syntax_count = 0
    for file in sorted(examples.rglob("*.mjs")):
        subprocess.run([node, "--check", str(file)], check=True, capture_output=True, timeout=30)
        syntax_count += 1
    for file in examples.rglob("*.toml"):
        data = tomllib.loads(file.read_text(encoding="utf-8"))
        if not isinstance(data.get("prompt"), str):
            raise TypeError("TOML command is missing prompt")
    invalid_json = []
    for file in examples.rglob("*.json"):
        try:
            json.loads(file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            invalid_json.append(str(file.relative_to(examples)).replace("\\", "/"))
    if invalid_json != ["71/settings-cases/07-invalid-json/workspace.json"]:
        raise ValueError(f"Unexpected invalid JSON files: {invalid_json}")
    with tempfile.TemporaryDirectory(prefix="gemini-delivery-verify-") as directory:
        target = Path(directory).resolve()
        with zipfile.ZipFile(examples / "md-verification.zip") as archive:
            for name in archive.namelist():
                destination = (target / name).resolve()
                if not destination.is_relative_to(target):
                    raise ValueError("Archive escaped isolated output")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(archive.read(name))
        result = subprocess.run([node, str(target / "verify-cli.mjs"), cli], cwd=target,
                                capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)
        if result.returncode:
            raise RuntimeError(result.stderr[-2000:])
        report = json.loads((target / "verification/local-cli.json").read_text(encoding="utf-8"))
        counts = {number: len(rows) for number, rows in report["results"].items()}
        if counts != {"69": 5, "70": 4, "71": 8, "72": 19, "73": 9, "74": 3}:
            raise ValueError("Unexpected extracted exercise result counts")
    receipt = {"checkedOn": "2026-09-14", "status": "local-delivery-verified-not-published",
               "archives": checked, "javascriptSyntaxFiles": syntax_count, "tomlCommands": 3,
               "intentionalInvalidJson": invalid_json, "extractedBundleObservations": counts,
               "cli": report["cli"], "node": report["node"], "platform": report["platform"],
               "notTested": report["notTested"]}
    (HERE / "verification/delivery.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", required=True)
    parser.add_argument("--cli", required=True)
    args = parser.parse_args()
    print(json.dumps(main(args.node, args.cli), ensure_ascii=False, indent=2))
