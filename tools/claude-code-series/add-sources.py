"""Refresh a bounded set of additional primary references used by advanced lessons."""
import json
from research import ROOT, MANIFEST, fetch

additional = {
    50: ["https://code.claude.com/docs/en/desktop"],
    52: ["https://code.claude.com/docs/en/routines", "https://code.claude.com/docs/en/desktop-scheduled-tasks"],
    54: ["https://code.claude.com/docs/en/agent-sdk/quickstart", "https://code.claude.com/docs/en/agent-sdk/typescript"],
}
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
path = ROOT / "docs/claude-code-series/source-checks.json"
checks = {item["url"]: item for item in json.loads(path.read_text(encoding="utf-8"))}
for entry in manifest["entries"]:
    for url in additional.get(entry["number"], []):
        result = fetch(url)
        if result["status"] != 200 or not result["title"]:
            raise ValueError(result)
        checks[url] = result
        if url not in entry["sources"]:
            entry["sources"].append(url)
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
path.write_text(json.dumps(sorted(checks.values(), key=lambda item: item["url"]), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Verified {len(checks)} primary sources")
