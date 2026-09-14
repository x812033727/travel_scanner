"""Compile the reviewed lesson manuscripts into the existing article-pack format.

Run with apps/api/.venv/Scripts/python.exe docs/gemini-series/build.py.
Artwork is original SVG, rendered by the existing content-pack renderer when --render is set.
The JSON catalogue is the only source of identity, order and navigation metadata.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "apps/api"))

from app.guides.content_pack import ArticlePack  # noqa: E402
from app.guides.pack_ingest import _body_length, render_svg  # noqa: E402
from PIL import Image  # noqa: E402
from artwork import artwork  # noqa: E402

CATALOGUE_PATH = ROOT / "apps/web/lib/guide-series.json"
CATALOGUE = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
ARTICLES = {entry["number"]: entry for entry in CATALOGUE["articles"]}
ARTICLES[0] = {"number": 0, "slug": CATALOGUE["hubSlug"], "title": "Gemini 完整教學：電腦、手機、CLI 與 Google AI 應用", "purpose": "找到適合自己的教學與學習路線", "group": "A", "related": [1, 29, 47]}
ORIGIN = "https://mokaair.com/zh-TW/life/"
CHECKED = "2026-09-14"


def prose(text: str) -> dict:
    inlines = []
    position = 0
    text = re.sub(r"(?<!`)`([^`]+)`(?!`)", r"\1", text)
    for match in re.finditer(r"\[\[(\d+)\|([^\]]+)\]\]", text):
        if match.start() > position:
            inlines.append({"type": "text", "text": text[position:match.start()]})
        article = ARTICLES[int(match[1])]
        inlines.append({"type": "link", "text": match[2], "url": ORIGIN + article["slug"]})
        position = match.end()
    if not inlines:
        return {"type": "paragraph", "text": text}
    if position < len(text):
        inlines.append({"type": "text", "text": text[position:]})
    return {"type": "rich_paragraph", "inlines": inlines}


def parse(source: str) -> list[dict]:
    lines = source.strip().splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line == "!command-reference":
            inventory = json.loads((HERE / "cli-command-inventory.json").read_text(encoding="utf-8"))
            links = json.loads((HERE / "command-links.json").read_text(encoding="utf-8"))
            if set(links) != {command["name"] for command in inventory["commands"]}:
                raise ValueError("every verified built-in command must have an editorial entry")
            for command in inventory["commands"]:
                purpose, lesson = links[command["name"]]
                name = "/" + command["name"]
                alias = "（別名：" + "、".join("/" + item for item in command["aliases"]) + "）" if command["aliases"] else ""
                subcommands = "；子指令：" + "、".join(item["name"] for item in command["subcommands"]) if command["subcommands"] else ""
                extra = f"延伸：[[{lesson}|{ARTICLES[lesson]['title'].split('：')[0]}]]。" if lesson != 31 else ""
                blocks.append(prose(f"{name}{alias}：{purpose}{subcommands}。{extra}"))
        elif line.startswith("!include-code "):
            relative = line.removeprefix("!include-code ").strip()
            example = (HERE / relative).resolve()
            if not example.is_relative_to(HERE / "examples"):
                raise ValueError("code include must stay inside examples")
            language = {".py": "python", ".mjs": "javascript", ".json": "json", ".txt": "text"}[example.suffix]
            blocks.append({"type": "code", "language": language, "label": example.name, "code": example.read_text(encoding="utf-8")})
        elif line.startswith("```"):
            info = line[3:].split(" ", 1)
            code = []
            i += 1
            while i < len(lines) and lines[i] != "```":
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError("unclosed code fence")
            blocks.append({"type": "code", "language": info[0] or "text", "label": info[1] if len(info) > 1 else (info[0] or "範例"), "code": "\n".join(code) + "\n"})
        elif line.startswith("## ") or line.startswith("### "):
            prefix, title = line.split(" ", 1)
            blocks.append({"type": "heading", "level": len(prefix), "text": title})
        elif line.startswith("- ") or re.match(r"\d+\. ", line):
            ordered = not line.startswith("- ")
            items = []
            pattern = r"^\d+\. " if ordered else r"^- "
            while i < len(lines) and re.match(pattern, lines[i]):
                items.append(re.sub(pattern, "", lines[i]))
                i += 1
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue
        elif line.startswith("> "):
            blocks.append({"type": "callout", "tone": "tip", "title": "操作提醒", "text": line[2:]})
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "```", "- ", "> ")) and not re.match(r"\d+\. ", lines[i]):
                paragraph.append(lines[i])
                i += 1
            blocks.append(prose("\n".join(paragraph)))
            continue
        i += 1
    return blocks


def build(number: int, render: bool) -> dict:
    article = ARTICLES[number]
    manuscript = HERE / "lessons" / f"{number:02}.md"
    blocks = parse(manuscript.read_text(encoding="utf-8"))
    first = next(b["text"] for b in blocks if b["type"] == "paragraph")
    source_rows = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))[str(number)]
    directory = ROOT / "apps/web/public/guides" / article["slug"]
    directory.mkdir(parents=True, exist_ok=True)
    art = artwork(article, blocks, directory)
    if render:
        for name in ["hero", "diagram-1"]:
            png = HERE / "renders" / article["slug"] / f"{name}.png"
            png.parent.mkdir(parents=True, exist_ok=True)
            render_svg(directory / f"{name}.svg", png)
            if name == "hero":
                with Image.open(png) as picture:
                    picture.convert("RGB").save(directory / "hero.jpg", quality=90)
    credit = {"author": "Mokaair", "license": "© Mokaair", "source_url": None}
    illustration = {"type": "image", "src": f'/guides/{article["slug"]}/diagram-1.svg', "alt": art["diagram_alt"], "width": 1600, "height": 900, "caption": art["diagram_caption"], "credit": credit}
    blocks.insert(next((i for i,b in enumerate(blocks) if b["type"] == "heading"), 1), illustration)
    if not any(b["type"] == "callout" for b in blocks):
        blocks.append({"type": "callout", "tone": "info", "title": "查證與範例", "text": f"本文於 {CHECKED} 對照官方文件整理。畫面操作依官方說明，非所有裝置均經實機測試；範例輸出是驗收目標，實際內容依資料而異。"})
    blocks.extend([{"type": "heading", "level": 2, "text": "完成後的檢核"}, {"type": "table", "header": ["檢查項目", "通過條件"], "rows": [["操作", "能依正文重做一次，說明每一步使用的輸入。"], ["結果", "能用原始資料或可重現測試核對輸出，而非只看語氣。"], ["延伸", "知道下一篇教學解決的問題，以及什麼時候需要它。"]], "caption": "完成實作後逐項確認。"}])
    related = article["related"]
    blocks.append(prose("接著可以閱讀 " + "、".join(f'[[{n}|{ARTICLES[n]["title"].split("：")[0]}]]' for n in related) + "，把本篇的操作接到下一個工作流程。"))
    blocks.append({"type": "link", "text": "返回 Gemini 教學總目錄", "url": ORIGIN + CATALOGUE["hubSlug"]})
    pack = {"slug": article["slug"], "kind": "life", "destination_id": None, "topics": ["ai", "tutorial"], "featured": False, "display_order": 100 + number, "locales": {"zh-TW": {"title": article["title"], "description": first[:350], "hero": {"src": f'/guides/{article["slug"]}/hero.jpg', "alt": art["hero_alt"], "width": 1600, "height": 900, "credit": credit}, "blocks": blocks, "sources": [{"title": row[0], "url": row[1], "checked_on": CHECKED} for row in source_rows]}}}
    validated = ArticlePack.model_validate(pack)
    article["minutes"] = max(1, (_body_length(validated.locales["zh-TW"]) + 399) // 400)
    destination = ROOT / "apps/api/app/guides/content" / f'{article["slug"]}.json'
    destination.write_text(json.dumps(validated.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"number": number, "slug": article["slug"], "characters": _body_length(validated.locales["zh-TW"]), "blocks": len(blocks)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs="*", type=int)
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    numbers = args.numbers or sorted(int(p.stem) for p in (HERE / "lessons").glob("*.md"))
    report = [build(number, args.render) for number in numbers]
    CATALOGUE_PATH.write_text(json.dumps(CATALOGUE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
