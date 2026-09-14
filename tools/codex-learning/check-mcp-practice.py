"""Check CLI configuration in a temporary home and the public Docs MCP directly.

No model requests, user authentication, private files, or global settings writes.
"""
import argparse
import json
import os
import subprocess
import tempfile
import urllib.request
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
URL = "https://developers.openai.com/mcp"
SOURCE = "https://learn.chatgpt.com/docs/agent-configuration/agents-md"
parser = argparse.ArgumentParser()
parser.add_argument("--codex", required=True)
args = parser.parse_args()
checks = []
actual_config = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
before = actual_config.read_bytes() if actual_config.exists() else None

with tempfile.TemporaryDirectory(prefix="codex-mcp-practice-") as folder:
    isolated = Path(folder).resolve()
    assert isolated.parent == Path(tempfile.gettempdir()).resolve()
    assert isolated.name.startswith("codex-mcp-practice-")
    env = {**os.environ, "CODEX_HOME": str(isolated)}
    config = isolated / "config.toml"
    baseline = '[mcp_servers.preserved]\nurl = "https://example.invalid/mcp"\nenabled = false\n'
    config.write_text(baseline, encoding="utf-8")

    def cli(*commands, expected=0):
        result = subprocess.run([args.codex, *commands], cwd=isolated, env=env, capture_output=True, encoding="utf-8", timeout=45, check=False)
        assert result.returncode == expected, result.stderr
        return result.stdout

    version = cli("--version").strip()
    cli("mcp", "add", "codexLearningDocs", "--url", URL)
    inspected = json.loads(cli("mcp", "get", "codexLearningDocs", "--json"))
    assert inspected["name"] == "codexLearningDocs" and inspected["transport"]["url"] == URL
    parsed = tomllib.loads(config.read_text(encoding="utf-8"))
    assert parsed["mcp_servers"]["preserved"] == tomllib.loads(baseline)["mcp_servers"]["preserved"]
    checks.append("CLI add/get saved the exact HTTP URL and preserved an unrelated disabled server")
    source = config.read_text(encoding="utf-8")
    config.write_text(source.replace("[mcp_servers.codexLearningDocs]", "[mcp_servers.codexLearningDocs]\nenabled = false"), encoding="utf-8")
    assert json.loads(cli("mcp", "get", "codexLearningDocs", "--json"))["enabled"] is False
    checks.append("CLI get reflects disabled state; this is configuration evidence, not a model tool-catalog test")
    config.write_text(source, encoding="utf-8")
    cli("mcp", "remove", "codexLearningDocs")
    assert tomllib.loads(config.read_text(encoding="utf-8")) == tomllib.loads(baseline)
    cli("mcp", "get", "codexLearningDocs", expected=1)
    checks.append("CLI remove removed only the practice entry; a subsequent get failed as expected")

assert (actual_config.read_bytes() if actual_config.exists() else None) == before
checks.append("The real user configuration remained byte-for-byte unchanged")

sequence = 0
def rpc(method, params):
    global sequence
    sequence += 1
    payload = {"jsonrpc": "2.0", "id": sequence, "method": method, "params": params}
    request = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": "2025-03-26"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read().decode()
        message = json.loads(raw) if response.headers.get_content_type() == "application/json" else json.loads(next(line[6:] for line in raw.splitlines() if line.startswith("data: ")))
    assert message["id"] == sequence and "error" not in message
    return message["result"]

initialized = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "codex-learning-check", "version": "1.0"}})
assert initialized["serverInfo"]["name"] == "openai-docs-mcp"
tools = rpc("tools/list", {})["tools"]
assert "fetch_openai_doc" in [tool["name"] for tool in tools]
checks.append("Public Docs MCP initialized and advertised a document retrieval tool without credentials")
result = rpc("tools/call", {"name": "fetch_openai_doc", "arguments": {"url": SOURCE}})
assert not result.get("isError")
body = "\n".join(block.get("text", "") for block in result["content"])
assert "AGENTS.md" in body and "global" in body and "project" in body
checks.append("Direct MCP retrieval returned the official AGENTS.md page, containing global and project guidance")
report = {"checkedAt": datetime.now(timezone.utc).isoformat(), "status": "passed", "cliVersion": version, "environment": "Windows; isolated child-process CODEX_HOME; direct public HTTP MCP", "checks": checks, "source": SOURCE, "sourceHash": sha256(body.encode()).hexdigest(), "toolCountObserved": len(tools), "notTested": ["Codex model invocation or tool selection", "desktop or IDE settings UI", "macOS and Linux execution", "OAuth", "physical phones"], "authorHashes": {key: sha256((ROOT / f"docs/codex-learning/deep/modules/{key}.json").read_bytes()).hexdigest() for key in ["25", "52"] if (ROOT / f"docs/codex-learning/deep/modules/{key}.json").exists()}}
(ROOT / "docs/codex-learning/evidence/mcp-practice.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"{len(checks)} MCP practice checks passed; no model or account connection invoked")
