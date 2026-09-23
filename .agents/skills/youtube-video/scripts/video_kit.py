#!/usr/bin/env python3
"""Tools for one YouTube video's working directory: script skeleton, checks, teleprompter,
shot list, upload metadata and slide rendering.

The script format is described in .agents/skills/youtube-video/references/script-format.md.
Standard library only, so any Python 3.10+ runs it without the repository's virtualenv.
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CONTENT = ROOT / "apps" / "api" / "app" / "guides" / "content"
SITE = "https://mokaair.com"

CUE_TYPES = ("字卡", "截圖", "錄影", "鏡頭", "B-roll", "音效")
CUE = re.compile(r"^\[(" + "|".join(re.escape(t) for t in CUE_TYPES) + r")\]\s*(.*)$")
SOURCES_HEADING = "來源"
DEFAULT_CPM = 250
HOOK_LIMIT = 30
CHAPTER_MIN = 10
SENTENCE_LIMIT = 40
STILL_LIMIT = 30
# Article phrasing that does not survive being read aloud.
WRITTEN_ONLY = (
    "本文",
    "這篇文章",
    "如上表",
    "如下表",
    "上表",
    "下表",
    "綜上所述",
    "值得注意的是",
    "筆者",
    "如圖所示",
)
TIMED_FORMATS = ("roundup", "tutorial")


# --- parsing ------------------------------------------------------------------------------


@dataclass
class Line:
    kind: str  # "say" or a cue type
    text: str


@dataclass
class Chapter:
    title: str
    lines: list[Line] = field(default_factory=list)

    def narration(self) -> list[str]:
        return [line.text for line in self.lines if line.kind == "say"]


@dataclass
class Script:
    meta: dict[str, str]
    chapters: list[Chapter]
    sources: list[str]


def parse(path: Path) -> Script:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    meta: dict[str, str] = {}
    front = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.S)
    if front:
        for raw in front.group(1).splitlines():
            if ":" in raw:
                key, value = raw.split(":", 1)
                meta[key.strip()] = value.strip()
        text = text[front.end() :]
    chapters: list[Chapter] = []
    sources: list[str] = []
    in_sources = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            title = line[3:].strip()
            in_sources = title == SOURCES_HEADING
            if not in_sources:
                chapters.append(Chapter(title))
            continue
        if line.startswith("#"):
            continue
        if in_sources:
            sources.append(re.sub(r"^[-*]\s*", "", line))
            continue
        if not chapters:
            chapters.append(Chapter("開場"))
        cue = CUE.match(line)
        if cue:
            chapters[-1].lines.append(Line(cue.group(1), cue.group(2)))
        else:
            chapters[-1].lines.append(Line("say", re.sub(r"^[-*>]\s*", "", line)))
    return Script(meta, chapters, sources)


def spoken_units(text: str) -> int:
    """Characters as they are spoken: a CJK character is one, a Latin word or a run of digits
    two, punctuation nothing."""
    units = 0
    for token in re.findall(r"[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[぀-ヿ㐀-鿿가-힯]", text):
        units += 1 if re.match(r"[぀-ヿ㐀-鿿가-힯]", token) else 2
    return units


def seconds(text: str, cpm: int) -> float:
    return spoken_units(text) * 60.0 / cpm


def clock(total: float) -> str:
    total = int(round(total))
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def estimated_starts(script: Script, cpm: int) -> list[float]:
    starts, elapsed = [], 0.0
    for chapter in script.chapters:
        starts.append(elapsed)
        elapsed += sum(seconds(t, cpm) for t in chapter.narration())
    return starts


# --- from-article ---------------------------------------------------------------------------


def block_text(block: dict) -> str:
    if block.get("type") == "rich_paragraph":
        return "".join(inline.get("text", "") for inline in block.get("inlines", []))
    return block.get("text", "")


def comment(text: str) -> str:
    return "<!-- " + text.replace("--", "—").replace("\n", " ") + " -->"


def cmd_from_article(args: argparse.Namespace) -> int:
    pack_path = CONTENT / f"{args.slug}.json"
    if not pack_path.is_file():
        print(f"FAIL no content pack at {pack_path.relative_to(ROOT)}", file=sys.stderr)
        return 1
    pack = json.loads(pack_path.read_text(encoding="utf-8"))
    locale = pack["locales"].get(args.locale)
    if not locale:
        print(
            f"FAIL {args.slug} has no {args.locale}; it has {', '.join(pack['locales'])}",
            file=sys.stderr,
        )
        return 1
    out = [
        "---",
        f"title: {locale['title']}",
        f"format: {args.format}",
        "recorded_on: ",
        f"article: {args.slug}",
        f"locale: {args.locale}",
        f"summary: {locale.get('description', '')}",
        "---",
        "",
        comment(
            "骨架由 video_kit.py from-article 產生。註解是文章素材，不會被唸出來；"
            "照 formats.md 重排章節、把素材改寫成口播，刪掉用不到的註解。"
        ),
        "",
        "## 開場",
        comment("≤ 30 秒：觀眾的問題、一個反直覺的說法、這支會給什麼"),
        "[鏡頭] 正面",
        "",
    ]
    for block in locale.get("blocks", []):
        kind = block.get("type")
        if kind == "heading":
            if block.get("level", 2) <= 2:
                out += ["", f"## {block['text']}"]
            else:
                out.append(comment(f"小節：{block['text']}"))
        elif kind in ("paragraph", "rich_paragraph"):
            out.append(comment(f"素材：{block_text(block)}"))
        elif kind == "summary":
            out.append(comment("重點：" + "／".join(block.get("items", []))))
        elif kind == "list":
            out.append(comment("清單：" + "／".join(block.get("items", []))))
        elif kind == "callout":
            out.append(comment(f"提醒（{block.get('title', '')}）：{block.get('text', '')}"))
        elif kind == "table":
            header = "｜".join(block.get("header", []))
            out.append(f"[字卡] 表格（最多三列）：{header}")
            for row in block.get("rows", []):
                out.append(comment("列：" + "｜".join(row)))
        elif kind == "code":
            out.append(f"[錄影] 示範：{block.get('label') or block.get('language', '程式碼')}")
            out.append(comment("畫面上要出現的內容：" + block.get("code", "")[:400]))
        elif kind == "image":
            out.append(f"[截圖] 文章圖解 {block.get('src', '')}：{block.get('alt', '')}")
        elif kind == "faq":
            for item in block.get("items", []):
                out.append(
                    comment(f"常見問題：{item.get('question', '')} → {item.get('answer', '')}")
                )
        elif kind == "link":
            out.append(comment(f"連結（放說明欄）：{block.get('text', '')} {block.get('url', '')}"))
    out += [
        "",
        "## 結論",
        comment("回到開場的問題，一句話答案＋一個下一步"),
        "",
        f"## {SOURCES_HEADING}",
    ]
    for source in locale.get("sources", []):
        out.append(
            f"- {source.get('title', '')} {source.get('url', '')}"
            f"（文章查核 {source.get('checked_on', '?')}，錄影前重新確認）"
        )
    target = Path(args.out)
    if target.exists() and not args.force:
        print(f"FAIL {target} exists; pass --force to overwrite", file=sys.stderr)
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {target}")
    return 0


# --- check ----------------------------------------------------------------------------------


def cmd_check(args: argparse.Namespace) -> int:
    script = parse(Path(args.script))
    fails: list[str] = []
    warns: list[str] = []
    if not script.meta.get("title"):
        fails.append("frontmatter has no title")
    if script.meta.get("format") in TIMED_FORMATS and not script.meta.get("recorded_on"):
        warns.append(f"format {script.meta['format']} goes stale: fill recorded_on")
    if len(script.chapters) < 3:
        fails.append(f"{len(script.chapters)} chapters; YouTube needs at least 3 for a chapter bar")
    if not script.sources:
        fails.append(f"no ## {SOURCES_HEADING} section, or it is empty")
    for phrase in WRITTEN_ONLY:
        if phrase in script.meta.get("summary", ""):
            warns.append(f"summary: written-only phrase 「{phrase}」; it opens the description")

    total = 0.0
    print(f"{'#':>2}  {'start':>5}  {'length':>6}  {'cues':>4}  chapter")
    for index, chapter in enumerate(script.chapters):
        length = sum(seconds(t, args.cpm) for t in chapter.narration())
        cues = sum(1 for line in chapter.lines if line.kind != "say")
        print(f"{index + 1:>2}  {clock(total):>5}  {length:>5.0f}s  {cues:>4}  {chapter.title}")
        where = f"chapter {index + 1} 「{chapter.title}」"
        if not chapter.narration():
            fails.append(f"{where} has no narration")
        elif length < CHAPTER_MIN:
            fails.append(
                f"{where} is about {length:.0f}s; YouTube chapters must be at least {CHAPTER_MIN}s"
            )
        if index == 0 and length > HOOK_LIMIT:
            fails.append(f"the opening is about {length:.0f}s; keep it to {HOOK_LIMIT}s")
        still = 0.0
        for line in chapter.lines:
            if line.kind != "say":
                still = 0.0
                continue
            still += seconds(line.text, args.cpm)
            if still > STILL_LIMIT:
                warns.append(
                    f"{where}: {still:.0f}s of narration with no visual cue, "
                    f"before 「{line.text[:20]}」"
                )
                still = float("-inf")
            for sentence in re.split(r"(?<=[。！？!?])", line.text):
                if spoken_units(sentence) > SENTENCE_LIMIT:
                    warns.append(f"{where}: long sentence 「{sentence[:24]}…」")
            for phrase in WRITTEN_ONLY:
                if phrase in line.text:
                    warns.append(
                        f"{where}: written-only phrase 「{phrase}」 in 「{line.text[:24]}」"
                    )
        total += length
    print(f"\ntotal about {clock(total)} at {args.cpm} characters per minute")
    for warn in warns:
        print(f"WARN {warn}")
    for fail in fails:
        print(f"FAIL {fail}")
    print(f"\n{len(fails)} FAIL, {len(warns)} WARN")
    return 1 if fails else 0


# --- teleprompter and shots -----------------------------------------------------------------


def write_or_print(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
        print(f"wrote {out}")
    else:
        sys.stdout.write(text)


def cmd_teleprompter(args: argparse.Namespace) -> int:
    script = parse(Path(args.script))
    blocks = ["\n".join(chapter.narration()) for chapter in script.chapters if chapter.narration()]
    write_or_print("\n\n".join(blocks) + "\n", args.out)
    return 0


def cmd_shots(args: argparse.Namespace) -> int:
    script = parse(Path(args.script))
    rows = [["no", "chapter", "est_start", "type", "content"]]
    elapsed, number = 0.0, 0
    for chapter in script.chapters:
        for line in chapter.lines:
            if line.kind == "say":
                elapsed += seconds(line.text, args.cpm)
                continue
            number += 1
            rows.append([f"{number:02d}", chapter.title, clock(elapsed), line.kind, line.text])
    if args.out:
        with open(args.out, "w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle).writerows(rows)
        print(f"wrote {args.out} ({number} shots)")
    else:
        csv.writer(sys.stdout).writerows(rows)
    return 0


# --- metadata -------------------------------------------------------------------------------


def parse_clock(value: str) -> int:
    parts = [int(p) for p in value.split(":")]
    total = 0
    for part in parts:
        total = total * 60 + part
    return total


def read_chapters(path: Path) -> tuple[list[tuple[int, str]], list[str]]:
    chapters, errors = [], []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        match = re.match(r"^((?:\d+:)?\d{1,2}:\d{2})\s+(.+)$", raw)
        if not match:
            errors.append(f"{path.name}:{number} is not 「分:秒 章節名」: {raw}")
            continue
        chapters.append((parse_clock(match.group(1)), match.group(2).strip()))
    if chapters and chapters[0][0] != 0:
        errors.append("the first chapter must start at 00:00")
    if len(chapters) < 3:
        errors.append(f"{len(chapters)} chapters; YouTube needs at least 3")
    for (start, title), (after, _) in zip(chapters, chapters[1:], strict=False):
        if after - start < CHAPTER_MIN:
            errors.append(
                f"「{title}」 lasts {after - start}s; chapters must be at least {CHAPTER_MIN}s"
            )
        if after <= start:
            errors.append(f"timestamps must increase: 「{title}」")
    return chapters, errors


def article_url(slug: str, locale: str, campaign: str) -> tuple[str | None, str | None]:
    pack_path = CONTENT / f"{slug}.json"
    if not pack_path.is_file():
        return None, f"article {slug} has no content pack in this checkout; add the link by hand"
    kind = json.loads(pack_path.read_text(encoding="utf-8")).get("kind")
    path = f"/life/{slug}" if kind == "life" else f"/guides/{kind}/{slug}"
    query = f"?utm_source=youtube&utm_medium=video&utm_campaign={campaign}"
    return f"{SITE}/{locale}{path}{query}", None


def cmd_metadata(args: argparse.Namespace) -> int:
    script = parse(Path(args.script))
    meta = script.meta
    errors: list[str] = []
    notes: list[str] = []
    if args.chapters:
        chapters, errors = read_chapters(Path(args.chapters))
        if len(chapters) != len(script.chapters):
            notes.append(
                f"chapters.txt has {len(chapters)} chapters, the script {len(script.chapters)}"
            )
        estimated = False
    else:
        starts = estimated_starts(script, args.cpm)
        chapters = [(round(s), c.title) for s, c in zip(starts, script.chapters, strict=True)]
        estimated = True

    title = meta.get("title", "")
    if len(title) > 100:
        errors.append(f"title is {len(title)} characters; YouTube allows 100")
    lines = [meta.get("summary", "（前兩行：這支回答什麼、給誰看）"), ""]
    if meta.get("recorded_on"):
        lines += [f"錄製日期：{meta['recorded_on']}（內容以錄製當時為準）", ""]
    lines.append("章節")
    lines += [f"{clock(start)} {name}" for start, name in chapters]
    slug = meta.get("article")
    if slug:
        url, problem = article_url(slug, meta.get("locale", "zh-TW"), args.campaign or slug)
        if problem:
            notes.append(problem)
        if url:
            lines += ["", "完整文字版與整理表格", url]
    if script.sources:
        lines += ["", "資料來源"] + [f"・{source}" for source in script.sources]
    lines += ["", "（揭露：有業配、聯盟連結或贊助時寫在這裡）", "", "#hashtag1 #hashtag2"]
    description = "\n".join(lines)
    if len(description) > 5000:
        errors.append(f"description is {len(description)} characters; YouTube allows 5,000")
    if re.search(r"[<>]", description):
        errors.append("the description contains < or >, which YouTube rejects")

    out = [f"# 上架包：{title}", ""]
    if estimated:
        out += [
            "> **章節是估計時間，剪完要換。** 把實際時間寫進 chapters.txt，"
            "再跑 `metadata --chapters chapters.txt`。",
            "",
        ]
    out += [
        "## 標題候選",
        "",
        f"1. {title}",
        "2. （候選二）",
        "3. （候選三）",
        "",
        "## 說明欄",
        "",
        "```text",
        description,
        "```",
        "",
        "## 字幕",
        "",
        "YouTube Studio → 字幕 → 中文（台灣）→ 自動同步，"
        "貼上 teleprompter.txt（先照實際口播修正）。",
        "",
        "## 需要站主決定",
        "",
        "- [ ] 是否含付費宣傳",
        "- [ ] 變造或合成內容揭露（AI 產生的逼真人聲、人像、場景）",
        "- [ ] 是否為兒童專屬（這類影片通常為「否」）",
        "- [ ] 公開狀態與排程時間",
        "",
    ]
    text = "\n".join(out)
    write_or_print(text, args.out)
    for note in notes:
        print(f"WARN {note}", file=sys.stderr)
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    return 1 if errors else 0


# --- render ---------------------------------------------------------------------------------


def find_chromium(explicit: str | None) -> str | None:
    if explicit:
        return explicit
    if os.environ.get("CHROMIUM_BIN"):
        return os.environ["CHROMIUM_BIN"]
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if base:
        for pattern in (
            "chromium_headless_shell-*/chrome-linux/headless_shell",
            "chromium-*/chrome-linux/chrome",
        ):
            matches = sorted(glob.glob(os.path.join(base, pattern)))
            if matches:
                return matches[-1]
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def cmd_render(args: argparse.Namespace) -> int:
    folder = Path(args.folder)
    pages = sorted(folder.glob("*.html"))
    if not pages:
        print(f"FAIL no .html in {folder}", file=sys.stderr)
        return 1
    chromium = find_chromium(args.chromium)
    if not chromium:
        print("FAIL no Chromium: pass --chromium or set CHROMIUM_BIN", file=sys.stderr)
        return 1
    failed = 0
    for page in pages:
        width, height = (1280, 720) if page.name.startswith("thumbnail") else (1920, 1080)
        png = page.with_suffix(".png")
        command = [
            chromium,
            "--headless",
            "--no-sandbox",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            f"--screenshot={png.resolve()}",
            page.resolve().as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)  # noqa: S603
        if result.returncode != 0 or not png.is_file():
            failed += 1
            print(f"FAIL {page.name}: {result.stderr.strip()[-300:]}")
        else:
            print(f"ok   {png.name} {width}x{height}")
    return 1 if failed else 0


# --- entry ----------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="video_kit.py", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("from-article", help="script skeleton from a Mokaair content pack")
    p.add_argument("slug")
    p.add_argument("--out", required=True)
    p.add_argument("--locale", default="zh-TW")
    p.add_argument("--format", default="explainer", choices=("explainer", "roundup", "tutorial"))
    p.add_argument("--force", action="store_true")
    p.set_defaults(run=cmd_from_article)

    for name, run, helptext in (
        ("check", cmd_check, "estimate timing and flag problems"),
        ("teleprompter", cmd_teleprompter, "narration only, one sentence per line"),
        ("shots", cmd_shots, "shot list CSV"),
        ("metadata", cmd_metadata, "upload package: title, description, chapters"),
    ):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("script")
        p.add_argument("--cpm", type=int, default=DEFAULT_CPM, help="spoken characters per minute")
        if name != "check":
            p.add_argument("--out")
        if name == "metadata":
            p.add_argument(
                "--chapters",
                help="real chapter times after the edit, one 「分:秒 章節名」 per line",
            )
            p.add_argument("--campaign", help="utm_campaign; defaults to the article slug")
        p.set_defaults(run=run)

    p = sub.add_parser("render", help="render slides/*.html to PNG")
    p.add_argument("folder")
    p.add_argument("--chromium")
    p.set_defaults(run=cmd_render)

    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    sys.exit(main())
