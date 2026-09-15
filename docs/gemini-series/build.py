"""Compile the reviewed lesson manuscripts into the existing article-pack format.

Run with apps/api/.venv/Scripts/python.exe docs/gemini-series/build.py.
Artwork is original SVG, rendered by the existing content-pack renderer when --render is set.
The JSON catalogue is the only source of identity, order and navigation metadata.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "apps/api"))

from app.guides.content_pack import ArticlePack
from app.guides.pack_ingest import _body_length, check_svg, render_svg
from artwork import artwork
from PIL import Image

CATALOGUE_PATH = ROOT / "apps/web/lib/guide-series.json"
CATALOGUE = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
ARTICLES = {entry["number"]: entry for entry in CATALOGUE["articles"]}
ARTICLES[0] = {"number": 0, "slug": CATALOGUE["hubSlug"], "title": "Gemini 完整教學：電腦、手機、CLI 與 Google AI 應用", "purpose": "找到適合自己的教學與學習路線", "group": "A", "related": [1, 29, 47]}
ORIGIN = "https://mokaair.com/zh-TW/life/"
CHECKED = "2026-09-14"


def prose(text: str, articles: dict | None = None) -> dict:
    articles = ARTICLES if articles is None else articles
    inlines = []
    position = 0
    text = re.sub(r"(?<!`)`([^`]+)`(?!`)", r"\1", text)
    for match in re.finditer(r"\[\[(\d+)(?:#(section-[1-9]\d*))?\|([^\]]+)\]\]", text):
        if match.start() > position:
            inlines.append({"type": "text", "text": text[position:match.start()]})
        article = articles[int(match[1])]
        suffix = "#" + match[2] if match[2] else ""
        inlines.append({"type": "link", "text": match[3], "url": ORIGIN + article["slug"] + suffix})
        position = match.end()
    if not inlines:
        return {"type": "paragraph", "text": text}
    if position < len(text):
        inlines.append({"type": "text", "text": text[position:]})
    return {"type": "rich_paragraph", "inlines": inlines}


def parse(source: str, *, articles: dict | None = None, base_dir: Path = HERE) -> list[dict]:
    articles = ARTICLES if articles is None else articles
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
                blocks.append(prose(f"{name}{alias}：{purpose}{subcommands}。{extra}", articles))
        elif line.startswith("!include-code "):
            relative = line.removeprefix("!include-code ").strip()
            example = (base_dir / relative).resolve()
            if not example.is_relative_to((base_dir / "examples").resolve()):
                raise ValueError("code include must stay inside examples")
            language = {".py": "python", ".mjs": "javascript", ".js": "javascript", ".json": "json", ".txt": "text", ".md": "markdown", ".toml": "toml", ".ps1": "powershell", ".sh": "bash", ".yaml": "yaml", ".yml": "yaml", ".html": "html", ".css": "css", ".jsonl": "text"}[example.suffix]
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
        elif line.startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|[\s:|\-]+\|", lines[i + 1]):
            def cells(row: str) -> list[str]:
                return [cell.strip() for cell in row.strip().strip("|").split("|")]
            header = cells(line)
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                row = cells(lines[i])
                if len(row) != len(header):
                    raise ValueError("table row must match the header width")
                rows.append(row)
                i += 1
            blocks.append({"type": "table", "header": header, "rows": rows})
            continue
        elif line.startswith(("## ", "### ")):
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
            while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "```", "- ", "> ", "!include-code ", "!command-reference", "|")) and not re.match(r"\d+\. ", lines[i]):
                paragraph.append(lines[i])
                i += 1
            blocks.append(prose("\n".join(paragraph), articles))
            continue
        i += 1
    return blocks


def build(number: int, render: bool, output_root: Path = ROOT) -> dict:
    article = ARTICLES[number]
    manuscript = HERE / "lessons" / f"{number:02}.md"
    blocks = parse(manuscript.read_text(encoding="utf-8"))
    first = next(b["text"] for b in blocks if b["type"] == "paragraph")
    source_rows = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))[str(number)]
    directory = output_root / "apps/web/public/guides" / article["slug"]
    directory.mkdir(parents=True, exist_ok=True)
    art = artwork(article, blocks, directory)
    if render:
        for name in ["hero", "diagram-1"]:
            png = output_root / "docs/gemini-series/renders" / article["slug"] / f"{name}.png"
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
    destination = output_root / "apps/api/app/guides/content" / f'{article["slug"]}.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(validated.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return {"number": number, "slug": article["slug"], "characters": _body_length(validated.locales["zh-TW"]), "blocks": len(blocks)}



def checked_child(parent: Path, name: str) -> Path:
    child = (parent / name).resolve()
    if not child.is_relative_to(parent.resolve()):
        raise ValueError(f"path escapes its authoring directory: {name}")
    return child


def advanced_context(track: str, numbers: list[int]) -> tuple[dict, list[dict]]:
    plan = json.loads((HERE / "advanced/curriculum.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "advanced/platform/catalogue-contract.json").read_text(encoding="utf-8"))
    members = [entry for entry in plan["articles"] if entry["track"] == track]
    if not members:
        raise ValueError(f"unknown track: {track}")
    selected = numbers or [entry["number"] for entry in members]
    if len(set(selected)) != len(selected) or not set(selected).issubset({entry["number"] for entry in members}):
        raise ValueError("numbers must be unique members of the selected track")
    expected = [(entry["number"], entry["slug"]) for entry in contract["articles"]]
    combined = [*(entry for entry in CATALOGUE["articles"] if entry["number"] <= 50), *plan["articles"]]
    if [(entry["number"], entry["slug"]) for entry in combined] != expected:
        raise ValueError("draft identities differ from the frozen catalogue contract")
    articles = {entry["number"]: entry for entry in combined}
    articles[0] = ARTICLES[0]
    return articles, [entry for entry in members if entry["number"] in selected]


def prepare_advanced(article: dict, track_dir: Path, articles: dict) -> tuple[dict, dict[str, str], Path, dict[str, bytes]]:
    number, slug = article["number"], article["slug"]
    lesson_dir = checked_child(track_dir, str(number))
    source = checked_child(lesson_dir, "lesson.md").read_text(encoding="utf-8")
    meta = json.loads(checked_child(lesson_dir, "meta.json").read_text(encoding="utf-8"))
    blocks = parse(source, articles=articles, base_dir=track_dir)
    first = next((block["text"] for block in blocks if block["type"] == "paragraph"), None)
    if not first:
        raise ValueError(f"{number}: begin with a plain introductory paragraph")
    faq_start = next((i for i, b in enumerate(blocks) if b["type"] == "heading" and b["level"] == 2 and "常見問題" in b["text"]), None)
    faq_end = next((i for i in range((faq_start or 0) + 1, len(blocks)) if blocks[i]["type"] == "heading" and blocks[i]["level"] == 2), len(blocks))
    if faq_start is None or sum(b["type"] == "heading" and b["level"] == 3 for b in blocks[faq_start:faq_end]) < 3:
        raise ValueError(f"{number}: provide at least three FAQ headings")
    required = {"code", "rich_paragraph", "table", "callout"}
    if not required.issubset({block["type"] for block in blocks}):
        raise ValueError(f"{number}: needs code, linked prose, a table and an authored callout")
    if sum(b["type"] == "heading" and b["level"] == 2 for b in blocks) < 3:
        raise ValueError(f"{number}: needs at least three sections")
    svg_files = {}
    for name in ["hero", "diagram-1"]:
        svg = checked_child(lesson_dir, name + ".svg").read_text(encoding="utf-8")
        problems = [p.message for p in check_svg(svg) if p.level == "error"]
        if re.search(r"\bon\w+\s*=|<!DOCTYPE|<!ENTITY", svg, re.IGNORECASE):
            problems.append("active SVG content is not allowed")
        if problems:
            raise ValueError(f"{number}/{name}: " + "; ".join(problems))
        svg_files[name] = svg
    credit = {"author": "Mokaair", "license": "© Mokaair", "source_url": None}
    image = {"type": "image", "src": f"/guides/{slug}/diagram-1.svg", "alt": meta["diagram_alt"],
             "width": 1600, "height": 900, "caption": meta["diagram_caption"], "credit": credit}
    blocks.insert(next(i for i, b in enumerate(blocks) if b["type"] == "heading"), image)
    blocks.append(prose("延伸閱讀：" + "、".join(f'[[{n}|{articles[n]["title"]}]]' for n in article["related"]) + "。", articles))
    downloads = {}
    for item in meta.get("downloads", []):
        filename = item["filename"]
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]*\.(zip|csv|json|md|txt)", filename) or filename in downloads:
            raise ValueError("download filenames must be unique, plain data/archive filenames")
        source_file = checked_child(track_dir, item["source"])
        if not source_file.is_relative_to((track_dir / "examples").resolve()):
            raise ValueError("downloads must stay inside the track examples directory")
        downloads[filename] = source_file.read_bytes()
        blocks.append({"type": "link", "text": item["text"], "url": f"https://mokaair.com/guides/{slug}/{filename}"})
    blocks.append({"type": "link", "text": "返回 Gemini 教學總目錄", "url": ORIGIN + CATALOGUE["hubSlug"]})
    pack = ArticlePack.model_validate({
        "slug": slug, "kind": "life", "topics": ["ai", "tutorial"], "display_order": 100 + number,
        "locales": {"zh-TW": {"title": article["title"], "description": meta.get("description", first[:350]),
            "hero": {"src": f"/guides/{slug}/hero.jpg", "alt": meta["hero_alt"], "width": 1600, "height": 900, "credit": credit},
            "blocks": blocks, "sources": meta["sources"]}},
    })
    length = _body_length(pack.locales["zh-TW"])
    if not 1800 <= length <= 3000:
        raise ValueError(f"{number}: {length} body characters; expected 1800–3000")
    return pack.model_dump(mode="json"), svg_files, lesson_dir, downloads


def build_advanced(track: str, numbers: list[int], content_root: Path, output_root: Path, render: bool) -> list[dict]:
    articles, selected = advanced_context(track, numbers)
    track_dir = checked_child(content_root, track)
    # Validate the whole selected batch before touching its destination.
    prepared = [(entry, *prepare_advanced(entry, track_dir, articles)) for entry in selected]
    with tempfile.TemporaryDirectory(prefix="gemini-authoring-") as temporary:
        staging = Path(temporary)
        report = []
        for entry, pack, svg_files, lesson_dir, downloads in prepared:
            slug = entry["slug"]
            assets = staging / "apps/web/public/guides" / slug
            assets.mkdir(parents=True)
            for name, svg in svg_files.items():
                (assets / (name + ".svg")).write_text(svg, encoding="utf-8", newline="\n")
            for name, data in downloads.items():
                (assets / name).write_bytes(data)
            if render:
                for name in svg_files:
                    png = staging / "docs/gemini-series/advanced/content" / track / "verification/renders" / slug / (name + ".png")
                    png.parent.mkdir(parents=True, exist_ok=True)
                    render_svg(assets / (name + ".svg"), png)
                    if name == "hero":
                        with Image.open(png) as picture:
                            picture.convert("RGB").save(assets / "hero.jpg", quality=90)
            else:
                hero = checked_child(lesson_dir, "hero.jpg")
                if not hero.is_file():
                    raise ValueError(f'{entry["number"]}: provide a reviewed hero.jpg or use --render')
                with Image.open(hero) as picture:
                    if picture.size != (1600, 900) or picture.format != "JPEG":
                        raise ValueError("hero.jpg must be a 1600×900 JPEG")
                shutil.copyfile(hero, assets / "hero.jpg")
            destination = staging / "apps/api/app/guides/content" / (slug + ".json")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(pack, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            length = _body_length(ArticlePack.model_validate(pack).locales["zh-TW"])
            report.append({"number": entry["number"], "slug": slug, "stage": 2, "track": track,
                           "characters": length, "minutes": max(1, (length + 399) // 400),
                           "labMinutes": entry["estimatedLabMinutes"], "status": "built-unpublished"})
        for file in staging.rglob("*"):
            if file.is_file():
                target = checked_child(output_root, str(file.relative_to(staging)))
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(file, target)
    # Reports are scoped to the author's track, so independent batches never overwrite each other.
    report_dir = output_root / "docs/gemini-series/advanced/content" / track / "verification"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "build.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("numbers", nargs="*", type=int)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--track", help="Build one planned track without changing the runtime catalogue")
    parser.add_argument("--content-root", type=Path, default=HERE / "advanced/content")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    args = parser.parse_args()
    output_root = args.output_root.resolve()
    if args.track:
        report = build_advanced(args.track, args.numbers, args.content_root.resolve(), output_root, args.render)
    else:
        numbers = args.numbers or sorted(int(p.stem) for p in (HERE / "lessons").glob("*.md"))
        report = [build(number, args.render, output_root) for number in numbers]
        destination = CATALOGUE_PATH if output_root == ROOT else output_root / "series.json"
        destination.write_text(json.dumps(CATALOGUE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
