"""Check the exact published snippets without running install/login/network commands.

Runs the authored pure-function exercise before/after and the hook with local event
fixtures. General shell snippets are parsed, never executed. API SDK roundtrip tests
are separate and connect only to a local HTTP fixture.
"""
from __future__ import annotations

import ast
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build  # noqa: E402


def run(command: list[str], cwd: Path, data: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, input=data, encoding="utf-8", capture_output=True, timeout=30)


def main() -> None:
    report: dict = {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "boundary": "Syntax checks plus selected deterministic local executions; no Google login, remote API call, package install, or general shell snippet execution.",
        "syntax": [],
        "execution": [],
    }
    node = shutil.which("node")
    powershell = shutil.which("pwsh") or shutil.which("powershell")
    bash = Path(r"C:\Program Files\Git\bin\bash.exe")
    snippets: dict[int, list[dict]] = {}
    with tempfile.TemporaryDirectory(prefix="gemini-lesson-check-") as temporary:
        folder = Path(temporary)
        for manuscript in sorted((build.HERE / "lessons").glob("*.md")):
            number = int(manuscript.stem)
            snippets[number] = [b for b in build.parse(manuscript.read_text(encoding="utf-8")) if b["type"] == "code"]
            for index, block in enumerate(snippets[number]):
                language, code = block["language"], block["code"]
                status = "passed"
                if language == "json":
                    json.loads(code)
                elif language == "toml":
                    tomllib.loads(code)
                elif language == "python":
                    ast.parse(code)
                elif language == "javascript":
                    if not node:
                        raise RuntimeError("Node.js required for JavaScript syntax validation")
                    path = folder / f"lesson-{number}-{index}.mjs"
                    path.write_text(code, encoding="utf-8")
                    result = run([node, "--check", str(path)], folder)
                    if result.returncode:
                        raise RuntimeError(f"JavaScript {number}/{index}: {result.stderr}")
                elif language == "powershell":
                    if not powershell:
                        raise RuntimeError("PowerShell required for snippet parsing")
                    path = folder / "snippet.ps1"
                    path.write_text(code, encoding="utf-8-sig")
                    parser = folder / "parse.ps1"
                    parser.write_text("param([string]$SnippetPath)\n$parseTokens=$null\n$parseErrors=$null\n[System.Management.Automation.Language.Parser]::ParseFile($SnippetPath,[ref]$parseTokens,[ref]$parseErrors) | Out-Null\nif ($parseErrors.Count) { $parseErrors | ForEach-Object { $_.Message }; exit 1 }\n", encoding="utf-8-sig")
                    result = run([powershell, "-NoProfile", "-File", str(parser), str(path)], folder)
                    if result.returncode:
                        raise RuntimeError(f"PowerShell {number}/{index}: {result.stdout} {result.stderr}")
                elif language == "bash":
                    if not bash.is_file():
                        raise RuntimeError("Git Bash required for bash -n validation")
                    path = folder / "snippet.sh"
                    path.write_text(code, encoding="utf-8", newline="\n")
                    result = run([str(bash), "-n", str(path)], folder)
                    if result.returncode:
                        raise RuntimeError(f"Bash {number}/{index}: {result.stderr}")
                elif language in ("text", "markdown"):
                    status = "editorial-text-not-executable"
                else:
                    raise RuntimeError(f"Add a real syntax checker for {language}, lesson {number}")
                report["syntax"].append({"lesson": number, "block": index, "language": language, "label": block.get("label"), "status": status})

        if 34 in snippets:
            exercise = [b for b in snippets[34] if b["language"] == "javascript"]
            if len(exercise) != 3:
                raise RuntimeError("Coding exercise must contain initial implementation, tests and reference answer")
            (folder / "people.test.mjs").write_text(exercise[1]["code"], encoding="utf-8")
            (folder / "people.mjs").write_text(exercise[0]["code"], encoding="utf-8")
            before = run([node, "--test", "people.test.mjs"], folder)
            if before.returncode == 0:
                raise RuntimeError("Broken starter should fail the unchanged tests")
            (folder / "people.mjs").write_text(exercise[2]["code"], encoding="utf-8")
            after = run([node, "--test", "people.test.mjs"], folder)
            if after.returncode:
                raise RuntimeError(after.stdout + after.stderr)
            report["execution"].append({"lesson": 34, "check": "Identical three tests fail on starter and pass on reference solution", "beforeExit": before.returncode, "afterExit": after.returncode, "afterOutput": after.stdout})

        if 43 in snippets:
            hook = next(b for b in snippets[43] if b["language"] == "python")
            path = folder / "block-shell.py"
            path.write_text(hook["code"], encoding="utf-8")
            for name, expected in [("run_shell_command", "deny"), ("read_file", "allow")]:
                result = run([sys.executable, "-X", "utf8", str(path)], folder, json.dumps({"tool_name": name, "tool_input": {}}))
                if result.returncode or json.loads(result.stdout)["decision"] != expected:
                    raise RuntimeError(f"Hook did not return {expected}: {result.stderr}")
                report["execution"].append({"lesson": 43, "check": "Hook stdin/stdout protocol", "tool": name, "result": json.loads(result.stdout)})

        if 40 in snippets:
            command = tomllib.loads(next(b["code"] for b in snippets[40] if b["language"] == "toml"))
            if "{{args}}" not in command["prompt"] or not command["description"]:
                raise RuntimeError("Command template lost its argument or description")
            report["execution"].append({"lesson": 40, "check": "Parsed TOML preserves multiline prompt and literal {{args}}", "boundary": "Does not claim authenticated CLI invocation"})

    report["status"] = "passed"
    destination = build.HERE / "example-verification.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "snippets": len(report["syntax"]), "deterministicChecks": len(report["execution"]), "report": str(destination)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
