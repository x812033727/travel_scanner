"""Check every ZIP member against source, then rerun from the delivered archive."""
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent


def verify(python: str, node: str, cli: str, mcp_python: str) -> None:
    packages = []
    for archive_path in sorted((HERE / "examples").glob("*.zip")):
        with zipfile.ZipFile(archive_path) as archive:
            assert archive.testzip() is None, archive_path.name
            names = archive.namelist()
            assert len(names) == len(set(names)), "duplicate_members"
            base = HERE if archive_path.name == "automation-verification.zip" else HERE / "examples"
            for name in names:
                relative = PurePosixPath(name)
                assert not relative.is_absolute() and ".." not in relative.parts
                assert not any(p in {".venv", "__pycache__", ".git", ".env"} for p in relative.parts)
                assert archive.read(name) == (base / name).read_bytes(), name
            packages.append({"file": archive_path.relative_to(HERE).as_posix(), "members": len(names),
                             "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(), "crc": "passed", "sourceBytes": "matched"})
    assert len(packages) == 7, "expected_seven_archives"
    temporary = Path(tempfile.mkdtemp(prefix="gemini-automation-delivery-"))
    try:
        with zipfile.ZipFile(HERE / "examples/automation-verification.zip") as archive:
            archive.extractall(temporary)
        commands = [[python, "-X", "utf8", "verification/test_exercises.py"], [node, "verify-cli.mjs", cli, mcp_python]]
        runs = []
        for command in commands:
            result = subprocess.run(command, cwd=temporary, text=True, encoding="utf-8", capture_output=True, timeout=150, check=False)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
            runs.append({"entrypoint": command[3] if command[0] == python else command[1], "exitCode": result.returncode})
        fixture = json.loads((temporary / "verification/fixtures.json").read_text(encoding="utf-8"))
        cli_result = json.loads((temporary / "verification/local-cli.json").read_text(encoding="utf-8"))
        receipt = {"checkedOn": "2026-09-14", "status": "downloaded-archive-local-verification-passed",
                   "packages": packages, "extractedRuns": runs, "fixture": fixture, "cli": cli_result,
                   "cloudCalls": 0, "remoteActionsRuns": 0, "publication": "unpublished"}
        (HERE / "verification/delivery.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(json.dumps({"packages": len(packages), "fixtureTests": fixture["tests"], "extractedRuns": runs}, ensure_ascii=False))
    finally:
        shutil.rmtree(temporary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--python", required=True)
    parser.add_argument("--node", required=True)
    parser.add_argument("--cli", required=True)
    parser.add_argument("--mcp-python", required=True)
    args = parser.parse_args()
    verify(args.python, args.node, args.cli, args.mcp_python)
