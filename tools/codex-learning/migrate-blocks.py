"""Normalize local draft packs to the shared article contract. Never touch a database."""
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "apps/api"))
from app.guides.content_pack import ArticlePack  # noqa: E402

LABELS = {"zh-TW": "本步驟範例", "zh-CN": "本步骤示例", "en": "Example for this step",
          "ja": "この手順の例", "ko": "이 단계의 예제"}


def article(node):
    if node["type"] != "link":
        return node
    match = re.fullmatch(r"https://mokaair\.com/(?:zh-TW|zh-CN|en|ja|ko)/life/(codex-[a-z0-9-]+)", node["url"])
    return {"type": "article", "kind": "life", "slug": match[1], "text": node["text"]} if match else node


def main():
    pending = []
    for path in (ROOT / "apps/api/app/guides/content").glob("codex-*.json"):
        pack = json.loads(path.read_text(encoding="utf-8"))
        for locale, document in pack["locales"].items():
            blocks = []
            for block in document["blocks"]:
                if block["type"] == "rich_paragraph":
                    block = {"type": "rich_paragraph", "inlines": [article(n) for n in block.get("inlines", block.get("spans", []))]}
                elif block["type"] == "link":
                    target = article(block)
                    if target["type"] == "article":
                        block = {"type": "rich_paragraph", "inlines": [target]}
                elif block["type"] == "code":
                    block = {**block, "label": block.get("label", LABELS[locale])}
                blocks.append(block)
            document["blocks"] = blocks
        ArticlePack.model_validate(pack)
        pending.append((path, json.dumps(pack, ensure_ascii=False, indent=2) + "\n"))
    for path, encoded in pending:
        if path.read_text(encoding="utf-8") != encoded:
            path.write_text(encoded, encoding="utf-8")
    print(f"Validated {len(pending)} local packs against the shared block schema")


if __name__ == "__main__":
    main()
