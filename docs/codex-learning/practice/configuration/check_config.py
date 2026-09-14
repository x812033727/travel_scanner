from pathlib import Path
import sys
import tomllib

if len(sys.argv) != 2:
    raise SystemExit("Usage: check_config.py SAMPLE.toml")
path = Path(sys.argv[1])
try:
    with path.open("rb") as stream:
        data = tomllib.load(stream)
except (OSError, tomllib.TOMLDecodeError) as exc:
    print(f"FAIL: {exc}")
    raise SystemExit(1)
if "web_search" not in data:
    print("FAIL: missing top-level web_search; inspect table placement")
    raise SystemExit(1)
value = data["web_search"]
if not isinstance(value, str) or value not in {"disabled", "cached", "indexed", "live"}:
    print("FAIL: unsupported web_search value for this exercise")
    raise SystemExit(1)
print(f"PASS: sample syntax and web_search={value}; Codex loading is not verified")
