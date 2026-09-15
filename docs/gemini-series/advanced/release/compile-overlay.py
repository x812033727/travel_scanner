"""Compile three reviewed candidates without changing the production catalogue/packs."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
AUTHOR = ROOT / "docs/gemini-series"
sys.path.insert(0, str(AUTHOR))
from build import ArticlePack, _body_length, parse  # noqa: E402 -- shared author compiler lives outside a package


def compile_overlay() -> list[dict]:
    destination = HERE / "candidate"
    catalogue = json.loads((destination / "guide-series.json").read_text(encoding="utf-8"))
    articles = {item["number"]: item for item in catalogue["articles"]}
    articles[0] = {"slug": catalogue["hubSlug"]}
    source_records = json.loads((HERE / "source-checks.json").read_text(encoding="utf-8"))
    summaries = []
    for number in [0, 2, 49]:
        slug = articles[number]["slug"]
        pack = json.loads((ROOT / "apps/api/app/guides/content" / f"{slug}.json").read_text(encoding="utf-8"))
        document = pack["locales"]["zh-TW"]
        original = copy.deepcopy(document["blocks"])
        blocks = parse((HERE / "lessons" / f"{number:02}.md").read_text(encoding="utf-8"), articles=articles, base_dir=AUTHOR)
        image = next(b for b in original if b["type"] == "image")
        blocks.insert(next(i for i, b in enumerate(blocks) if b["type"] == "heading"), image)
        blocks.append({"type": "callout", "tone": "info", "title": "查證與範例", "text": source_records["lessons"][str(number)]["notice"]})
        tail = next(i for i, b in enumerate(original) if b["type"] == "heading" and b["text"] == "完成後的檢核")
        blocks.extend(original[tail:])
        def headings(entries):
            return [b["text"] for b in entries if b["type"] == "heading" and b["level"] == 2]
        if headings(blocks) != headings(original):
            raise ValueError(f"{number}: existing section anchors would change")
        document["description"] = next(b["text"] for b in blocks if b["type"] == "paragraph")[:350]
        document["blocks"] = blocks
        document["sources"] = source_records["lessons"][str(number)]["sources"]
        validated = ArticlePack.model_validate(pack)
        length = _body_length(validated.locales["zh-TW"])
        if number and not 1800 <= length <= 3000:
            raise ValueError(f"{number}: {length} body characters; expected 1800–3000")
        target = destination / "content" / f"{slug}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(validated.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        summaries.append({"number": number, "slug": slug, "characters": length, "preservedH2": headings(blocks)})
    return summaries


if __name__ == "__main__":
    print(json.dumps(compile_overlay(), ensure_ascii=False))
