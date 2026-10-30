#!/usr/bin/env python3
"""Run inside the image on CI (no GPU, no models): is every workflow node there, with its inputs?

Expects ComfyUI on COMFY_URL. A workflow naming a node the pinned commits do not have, or leaving
out a required input, fails here instead of on a pod billed by the hour.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

COMFY = os.environ.get("COMFY_URL", "http://127.0.0.1:8189")
WORKFLOWS = Path(__file__).resolve().parent / "workflows"


def main() -> int:
    with urllib.request.urlopen(f"{COMFY}/object_info", timeout=120) as response:
        info = json.load(response)
    problems = []
    paths = sorted(WORKFLOWS.glob("*.json"))
    for path in paths:
        for node_id, node in json.loads(path.read_text(encoding="utf-8")).items():
            spec = info.get(node["class_type"])
            if spec is None:
                problems.append(f"{path.name} node {node_id}: {node['class_type']} is not installed")
                continue
            required = spec["input"].get("required", {})
            known = set(required) | set(spec["input"].get("optional", {}))
            for name, item in required.items():
                has_default = isinstance(item, list) and len(item) > 1 and isinstance(item[1], dict) and "default" in item[1]
                if name not in node["inputs"] and not has_default:
                    problems.append(f"{path.name} node {node_id}: {node['class_type']} needs {name}")
            # VHS_VideoCombine takes extra widgets per output format, which object_info lists apart.
            if node["class_type"] != "VHS_VideoCombine":
                for name in set(node["inputs"]) - known:
                    problems.append(f"{path.name} node {node_id}: {node['class_type']} has no input {name}")
    for line in problems:
        print(f"[smoke] {line}", file=sys.stderr)
    print(f"[smoke] {len(problems)} problem(s) in {len(paths)} workflows")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
