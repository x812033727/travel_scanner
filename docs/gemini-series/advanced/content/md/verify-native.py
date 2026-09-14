"""Exercise the unmodified Windows Gemini CLI entry point without an AI account."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAME = "mokaair-doc-check"


def verify(node: Path, cli: Path, powershell: Path | None = None) -> dict:
    package = json.loads((cli / "package.json").read_text(encoding="utf-8"))
    if package["name"] != "@google/gemini-cli" or package["version"] != "0.59.0":
        raise ValueError("This experiment is pinned to the original CLI 0.59.0.")
    version = subprocess.check_output([node, "--version"], text=True).strip()
    report = {"node": version, "cli": package["version"], "platform": os.name,
              "entrySha256": hashlib.sha256((cli / "bundle/gemini.js").read_bytes()).hexdigest(),
              "entryModified": False, "modelCalls": 0, "steps": [],
              "entryMode": "PowerShell npm gemini.cmd" if powershell else "node bundle/gemini.js"}
    with tempfile.TemporaryDirectory(prefix="gemini-native-lifecycle-") as directory:
        root = Path(directory).resolve()
        user = root / "user"
        workspace = root / "workspace"
        workspace.mkdir()
        (user / ".gemini").mkdir(parents=True)
        (workspace / ".git").mkdir()
        (user / ".gemini/settings.json").write_text(json.dumps({
            "telemetry": {"enabled": False}, "security": {"folderTrust": {"enabled": False}},
            "general": {"disableAutoUpdate": True, "disableUpdateNag": True},
        }), encoding="utf-8")
        for name in ("system.json", "defaults.json"):
            (root / name).write_text("{}", encoding="utf-8")
        source = workspace / "extension-source"
        shutil.copytree(HERE / "examples/73/doc-check-1.0.0", source)
        wrapper = root / "entry.ps1"
        shim = cli.parent.parent / ".bin/gemini.cmd"
        if powershell:
            if not shim.is_file():
                raise FileNotFoundError("The npm-generated gemini.cmd is required for this check.")
            wrapper.write_text("& '" + str(shim).replace("'", "''") + "' @args\nexit $LASTEXITCODE\n", encoding="utf-8-sig")
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("GEMINI_", "GOOGLE_")) and key not in ("NODE_OPTIONS", "NODE_EXTRA_CA_CERTS")}
        env.update({"GEMINI_CLI_HOME": str(user), "GEMINI_CLI_SYSTEM_SETTINGS_PATH": str(root / "system.json"),
                    "GEMINI_CLI_SYSTEM_DEFAULTS_PATH": str(root / "defaults.json"),
                    "CI": "true", "NO_COLOR": "1", "PATH": str(node.parent) + os.pathsep + env["PATH"]})
        installed = user / f".gemini/extensions/{NAME}"

        def clean(text: str) -> str:
            for original, replacement in ((root, "<isolated>"), (cli, "<cli>"), (node.parent, "<runtime>")):
                text = text.replace(str(original), replacement).replace(original.as_posix(), replacement)
            return text

        def state() -> dict:
            manifest = installed / "gemini-extension.json"
            matching = manifest.exists() and all((installed / file.relative_to(source)).is_file()
                                                and (installed / file.relative_to(source)).read_bytes() == file.read_bytes()
                                                for file in source.rglob("*") if file.is_file())
            return {"installed": manifest.exists(), "version": json.loads(manifest.read_text(encoding="utf-8"))["version"] if manifest.exists() else None,
                    "installedSourceFilesMatch": matching if manifest.exists() else None}

        def run(label: str, arguments: list[str], expected_version: str | None) -> bool:
            # Only our inspected original extension may receive this update confirmation.
            input_text = "y\n" if label == "update" else ""
            input_file = root / "stdin.txt"
            input_file.write_text(input_text, encoding="utf-8")
            timed_out = False
            with input_file.open("rb") as stdin, (root / "stdout.txt").open("wb") as stdout, (root / "stderr.txt").open("wb") as stderr:
                command = ([powershell, "-NoProfile", "-NonInteractive", "-File", wrapper] if powershell
                           else [node, cli / "bundle/gemini.js"])
                process = subprocess.Popen([*command, "extensions", *arguments],
                                           cwd=workspace, env=env, stdin=stdin, stdout=stdout, stderr=stderr,
                                           creationflags=subprocess.CREATE_NO_WINDOW)
                try:
                    process.wait(timeout=45)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    # Kill only this experiment's child tree, including the CLI relaunch wrapper.
                    subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"],
                                   capture_output=True, check=False, timeout=10,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                    process.wait(timeout=10)
            actual = state()
            row = {"label": label, "command": clean("gemini extensions " + " ".join(arguments)),
                   "exitCode": process.returncode, "timedOut": timed_out,
                   "updateConfirmation": input_text.strip() if input_text else None,
                   "stdout": clean((root / "stdout.txt").read_text(encoding="utf-8", errors="replace")),
                   "stderr": clean((root / "stderr.txt").read_text(encoding="utf-8", errors="replace")),
                   "filesystemState": actual, "expectedVersion": expected_version,
                   "passed": not timed_out and process.returncode == 0 and actual["version"] == expected_version}
            if expected_version is not None:
                row["passed"] = row["passed"] and actual["installedSourceFilesMatch"]
            if label in ("list-disabled", "list-enabled"):
                enabled = "false" if label == "list-disabled" else "true"
                row["workspaceActivationVerified"] = f"Enabled (Workspace): {enabled}" in row["stdout"] + row["stderr"]
                row["passed"] = row["passed"] and row["workspaceActivationVerified"]
            report["steps"].append(row)
            print(json.dumps({"node": version, "step": label, "passed": row["passed"], "exitCode": row["exitCode"]}), flush=True)
            return row["passed"]

        sequence = [
            ("initial-list", ["list"], None),
            ("install", ["install", str(source), "--consent"], "1.0.0"),
            ("list-installed", ["list"], "1.0.0"),
            ("disable-workspace", ["disable", NAME, "--scope", "workspace"], "1.0.0"),
            ("list-disabled", ["list"], "1.0.0"),
            ("enable-workspace", ["enable", NAME, "--scope", "workspace"], "1.0.0"),
            ("list-enabled", ["list"], "1.0.0"),
            ("update", ["update", NAME], "1.1.0"),
            ("list-updated", ["list"], "1.1.0"),
            ("uninstall", ["uninstall", NAME], None),
            ("list-uninstalled", ["list"], None),
            ("rollback-install", ["install", str(source), "--consent"], "1.0.0"),
            ("list-rollback", ["list"], "1.0.0"),
            ("final-uninstall", ["uninstall", NAME], None),
        ]
        for label, arguments, expected_version in sequence:
            if label in ("update", "rollback-install"):
                source_version = "1.1.0" if label == "update" else "1.0.0"
                shutil.copytree(HERE / f"examples/73/doc-check-{source_version}", source, dirs_exist_ok=True)
            if not run(label, arguments, expected_version):
                report["status"] = "failed-stopped-before-next-command"
                break
        else:
            report["status"] = "native-lifecycle-passed"
    report["temporaryHomeRemoved"] = not root.exists()
    report["personalConfigurationModified"] = False
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", action="append", required=True, type=Path)
    parser.add_argument("--cli", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--powershell", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("Choose a fresh receipt; preserve previous observations.")
    report = {"checkedAt": datetime.now(timezone.utc).isoformat(),
              "method": "Unmodified CLI bundle in a Windows subprocess with redirected file stdio and isolated home; only the inspected original local update receives y. No terminal-emulator or cloud verification.",
              "runs": [verify(node.resolve(), args.cli.resolve(), args.powershell) for node in args.node]}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"output": str(args.output), "runs": [{"node": run["node"], "status": run["status"],
                      "steps": len(run["steps"])} for run in report["runs"]]}, ensure_ascii=False))
