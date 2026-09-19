"""Undo autolink's links on a few aliases that mislead in this series: the bare word AI,
參數 (which here means an API parameter, not a model weight), GenAI inside the
OpenTelemetry convention name, and 標記 (batch 2 uses it for a marker in a model id and for
ticking a field supported or not, never for a token). Article inlines with those texts become
text again; a rich paragraph left with only text turns back into a plain paragraph.

    prune_autolinks.py <content-dir> <slug>...
"""
import json, sys
from pathlib import Path

PRUNE = {"ai", "參數", "genai", "標記"}  # compared case-folded: autolink matches ASCII aliases case-insensitively


def prune_block(block):
    if block.get("type") != "rich_paragraph":
        return block, 0
    removed = 0
    inlines = []
    for node in block["inlines"]:
        if node.get("type") == "article" and node.get("text", "").casefold() in PRUNE:
            node = {"type": "text", "text": node["text"]}
            removed += 1
        if node.get("type") == "text" and inlines and inlines[-1].get("type") == "text":
            inlines[-1] = {"type": "text", "text": inlines[-1]["text"] + node["text"]}
        else:
            inlines.append(node)
    if all(n.get("type") == "text" for n in inlines):
        return {"type": "paragraph", "text": "".join(n["text"] for n in inlines)}, removed
    return {**block, "inlines": inlines}, removed


def main():
    root = Path(sys.argv[1])
    for slug in sys.argv[2:]:
        path = root / f"{slug}.json"
        pack = json.loads(path.read_text(encoding="utf-8"))
        total = 0
        for locale, doc in pack["locales"].items():
            blocks = []
            for block in doc["blocks"]:
                block, removed = prune_block(block)
                total += removed
                blocks.append(block)
            doc["blocks"] = blocks
        if total:
            path.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{slug}: pruned {total}")


if __name__ == "__main__":
    main()
