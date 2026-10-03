"""Check and stage the summary blocks the ai-terms-batch workflow returned.

Usage (from the repo root):
  python3 docs/ai-terms-series/summaries.py check   RESULT.json...   # mechanical checks
  python3 docs/ai-terms-series/summaries.py batch   RESULT.json... > OUT.json

A RESULT.json is a workflow's return value: {"summaries": [{slug, summary, support, ...}]}
for the summaries mode, or {"results": [{slug, summary: [{slug, summary, ...}]}]} for the
articles mode. `batch` writes the `pack_cli summarize --from` format
({slug: {"zh-TW": {"summary": [...]}}}); `pack_cli` then refuses any figure the article
does not carry, which is the check that matters most and is not repeated here.

The checks below are the ones a script can make about the rules the workflow gave its
agents: sentence count and length, self-reference, verification narration, Mainland
wording, and that each quoted support line really occurs in the article.
"""

import json
import re
import sys
from pathlib import Path

CONTENT = Path("apps/api/app/guides/content")
STAGING = Path("docs/ai-terms-series/batch-03/staging")

SELF_REFERENCE = re.compile(r"本文|這篇|本篇")
NARRATION = re.compile(r"查證日|查證時|查證當天|查證過程|我們查不到")
MAINLAND = re.compile(r"信息|默認|優化|視頻|質量|用戶|軟件|網絡|數據(?!庫)|激活|(?<!演)算法|程序(?!性)")


def flatten(paths: list[str]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if "summaries" in data:
            rows.extend(data["summaries"])
        for result in data.get("results", []):
            rows.extend(result.get("summary") or [])
    return rows


def article_text(slug: str) -> str:
    """The page's words as a reader meets them: a rich paragraph's inlines joined, so a
    sentence with a link in it reads as one sentence; sources left out."""
    path = CONTENT / f"{slug}.json"
    if not path.is_file():
        path = STAGING / slug / "pack.json"
    document = json.loads(path.read_text(encoding="utf-8"))["locales"]["zh-TW"]
    parts = [document.get("title", ""), document.get("description", "")]
    for block in document.get("blocks", []):
        kind = block.get("type")
        if kind == "rich_paragraph":
            parts.append("".join(node.get("text", "") for node in block.get("inlines", [])))
        elif kind == "table":
            parts.extend(block.get("header", []))
            parts.extend(cell for row in block.get("rows", []) for cell in row)
            parts.append(block.get("caption", ""))
        elif kind == "list":
            parts.extend(block.get("items", []))
        elif kind == "faq":
            parts.extend(item.get(k, "") for item in block.get("items", []) for k in ("question", "answer"))
        else:
            parts.extend(str(block.get(k, "")) for k in ("text", "title", "caption", "alt", "description"))
    return "\n".join(parts)


def squash(text: str) -> str:
    return re.sub(r"[\s「」『』\"'“”‘’（）()，,。、；;：:！!？?…—-]", "", text)


def check(rows: list[dict]) -> int:
    problems = 0
    seen: set[str] = set()
    for row in rows:
        slug, items = row["slug"], row["summary"]
        if slug in seen:
            print(f"{slug}: duplicate entry")
            problems += 1
        seen.add(slug)
        text = article_text(slug)
        body = squash(text)
        total = sum(len(item) for item in items)
        if not 2 <= len(items) <= 4:
            print(f"{slug}: {len(items)} sentences")
            problems += 1
        if not 100 <= total <= 260:
            print(f"{slug}: {total} characters in all")
            problems += 1
        for item in items:
            for label, pattern in (("self-reference", SELF_REFERENCE), ("narration", NARRATION),
                                   ("Mainland wording", MAINLAND)):
                if found := pattern.search(item):
                    print(f"{slug}: {label} 「{found.group(0)}」 in 「{item}」")
                    problems += 1
            if len(item) > 120:
                print(f"{slug}: sentence of {len(item)} characters")
                problems += 1
            if not item.endswith("。"):
                print(f"{slug}: does not end with 。: 「{item}」")
                problems += 1
        for quote in row.get("support", []):
            # A quote may join body sentences with 「／」, 「｜」 or 「…」, and may label a
            # table cell or callout title it comes from; each quoted part must occur.
            for part in re.split(r"[／/｜|…→「」]+|\.\.\.|（callout）|callout|表格列?|標題", quote):
                part = re.sub(r"^(表格|callout|標題|小標)[^：:]*[：:]", "", part.strip())
                part = squash(part)
                if len(part) >= 8 and part not in body:
                    print(f"{slug}: support not found in the article: 「{part[:60]}」")
                    problems += 1
    print(f"{len(rows)} summaries, {problems} problems")
    return problems


def batch(rows: list[dict]) -> dict:
    return {row["slug"]: {"zh-TW": {"summary": row["summary"]}} for row in rows}


if __name__ == "__main__":
    command, files = sys.argv[1], sys.argv[2:]
    rows = flatten(files)
    if command == "check":
        sys.exit(1 if check(rows) else 0)
    if command == "batch":
        print(json.dumps(batch(rows), ensure_ascii=False, indent=2))
