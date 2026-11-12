#!/usr/bin/env python3
"""Till the Verdict Do Us Part 第一季台詞表。

讀 docs/videos/till-the-verdict-eNNN/script.md 每一張分鏡表
（| 鏡 | 景別、運鏡 | 畫面裡有誰 | 動作 | 台詞 | 秒數 |），
每一句說出口的台詞寫成 lines-s1.csv 的一列，並印出每集的數字與給編劇的警告。

只用標準函式庫，唯讀劇本：

    python3 -I docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/production/lines/extract.py

選項：--root 指定 repo 根目錄（預設從本檔往上找），--out 指定 CSV 路徑
（預設本檔旁的 lines-s1.csv），--quiet 只印數字不印警告。
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPISODE_DIR = re.compile(r"^till-the-verdict-e(\d{3})$")

FIELDS = [
    "episode",
    "shot",
    "speaker",
    "voice",
    "kind",
    "english",
    "words",
    "tone",
    "answer_to",
    "because_of",
    "shot_seconds",
]

# 警告門檻（站主的規則）
MAX_WORDS = 14  # 超過 14 個字太長
MIN_MODEL_WORDS = 6  # 模型原聲 ≤6 個字太短
WORDS_PER_SECOND = 2.5
SECONDS_PAD = 0.5

NAME = r"[A-Za-z㐀-鿿][A-Za-z0-9㐀-鿿.'’ ·-]*?"
# 「Nora（原聲，低聲）：」；前面要是格子開頭、空白、右括號、句號或分號，才算新的一句
HEAD_WITH_MARKS = re.compile(
    rf"(?:(?<=^)|(?<=[\s）)」。；;>]))(?P<speaker>{NAME})（(?P<marks>[^（）]*)）[：:]"
)
# 格子開頭沒有括號的「Nora：」
HEAD_PLAIN = re.compile(rf"^(?P<speaker>{NAME})：")
LINE_BREAK = re.compile(r"<br\s*/?>|\\n", re.IGNORECASE)
PAREN = re.compile(r"（([^（）]*)）")
SHOT_ID = re.compile(r"c\d+[a-z]?")
ANSWER = re.compile(r"→\s*答在\s*([^）←→]*)")
BECAUSE = re.compile(r"←\s*因為\s*((?:c\d+[a-z]?(?:\s*[、,，/和與及]\s*)?)+)")
SECONDS = re.compile(r"([\d.]+)\s*(?:[–—~～-]\s*([\d.]+))?\s*秒")
WORD = re.compile(r"[A-Za-z0-9]")
MOUTH_TALKING = "嘴在說話"

VOICE_TOKENS = {"原聲", "模型原聲"}
OFFSCREEN_TOKENS = {"畫外", "畫外音"}
INNER_TOKENS = {"心裡話", "內心", "心聲"}
PHONE_RE = re.compile(r"^電話$|電話(?:裡|那頭|濾波|錄音)|語音|留言")
TV_RE = re.compile(r"電視|廣告")
SHOUT_RE = re.compile(r"(?<!不是)短喊")


def find_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "docs" / "videos").is_dir() and (parent / ".git").exists():
            return parent
    for parent in [start, *start.parents]:
        if (parent / "docs" / "videos").is_dir():
            return parent
    sys.exit("找不到 repo 根目錄（含 docs/videos 的資料夾），請用 --root 指定")


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", body)]


def clean_shot(cell: str) -> str:
    m = SHOT_ID.search(cell.replace("*", ""))
    return m.group(0) if m else cell.replace("*", "").strip()


def parse_seconds(cell: str) -> float | None:
    m = SECONDS.search(cell)
    if not m:
        return None
    # 範圍（約 2–3 秒）取上限：只有連上限都不夠才警告
    value = m.group(2) or m.group(1)
    try:
        return float(value)
    except ValueError:
        return None


def tokens(marks: str) -> list[str]:
    return [t.strip() for t in re.split(r"[，；,;]", marks) if t.strip()]


def is_voice_paren(content: str) -> bool:
    return any(t in VOICE_TOKENS or t.startswith("Gemini") for t in tokens(content))


def fmt_seconds(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:g}"


def word_count(english: str) -> int:
    return sum(1 for w in english.split() if WORD.search(w))


def split_lines(cell: str) -> tuple[list[tuple[str, str, str]], list[str]]:
    """把一格台詞拆成 [(speaker, marks, 這句剩下的文字)]，回傳 (句子, 拆不出來的片段)。"""
    out: list[tuple[str, str, str]] = []
    leftovers: list[str] = []
    for piece in LINE_BREAK.split(cell):
        piece = piece.strip()
        if not piece or piece.startswith(("—", "-", "–")):
            continue
        heads = list(HEAD_WITH_MARKS.finditer(piece))
        if not heads or heads[0].start() != 0:
            plain = HEAD_PLAIN.match(piece)
            if plain and (not heads or plain.end() <= heads[0].start()):
                end = heads[0].start() if heads else len(piece)
                out.append((plain.group("speaker").strip(), "", piece[plain.end() : end]))
            elif heads:
                leftovers.append(piece[: heads[0].start()])
            else:
                leftovers.append(piece)
        for i, head in enumerate(heads):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(piece)
            out.append((head.group("speaker").strip(), head.group("marks"), piece[head.end() : end]))
    return out, leftovers


def parse_line(speaker: str, marks: str, text: str) -> dict[str, object]:
    cut = len(text)
    for ch in ("（", "←", "→"):
        pos = text.find(ch)
        if pos != -1:
            cut = min(cut, pos)
    english = text[:cut].strip()
    rest = text[cut:]

    voice_parens = [p for p in PAREN.findall(rest) if is_voice_paren(p)]
    mark_tokens = tokens(marks) + [t for p in voice_parens for t in tokens(p)]

    has_gemini = any(t.startswith("Gemini") for t in mark_tokens)
    has_model = any(t in VOICE_TOKENS for t in mark_tokens)
    voice = "gemini" if has_gemini else "model" if has_model else ""

    joined = "，".join(mark_tokens)
    if any(t in INNER_TOKENS for t in mark_tokens):
        kind = "inner"
    elif TV_RE.search(joined):
        kind = "tv"
    elif any(PHONE_RE.search(t) for t in mark_tokens):
        kind = "phone"
    elif SHOUT_RE.search(joined):
        kind = "shout"
    elif any(t in OFFSCREEN_TOKENS for t in mark_tokens):
        kind = "off-screen"
    else:
        kind = "on-screen"

    def is_tag(t: str) -> bool:
        return (
            t in VOICE_TOKENS
            or t.startswith("Gemini")
            or t in OFFSCREEN_TOKENS
            or t in INNER_TOKENS
            or t == "短喊"
            or bool(PHONE_RE.search(t))
            or t in {"電視", "廣告旁白"}
        )

    tone = "，".join(t for t in tokens(marks) if not is_tag(t))

    scan = marks + " " + rest
    answers: list[str] = []
    for m in ANSWER.finditer(scan):
        ids = SHOT_ID.findall(m.group(1).split("：")[0])
        answers.extend(ids or [m.group(1).split("：")[0].strip()])
    becauses: list[str] = []
    for m in BECAUSE.finditer(scan):
        becauses.extend(SHOT_ID.findall(m.group(1)))

    return {
        "speaker": speaker,
        "voice": voice,
        "kind": kind,
        "english": english,
        "words": word_count(english),
        "tone": tone,
        "answer_to": ";".join(dict.fromkeys(answers)),
        "because_of": ";".join(dict.fromkeys(becauses)),
        "ambiguous_voice": has_gemini and has_model,
    }


def read_episode(path: Path, episode: str, warn) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    header: list[str] | None = None
    scene = ""
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if raw.startswith("#"):
            scene = raw.lstrip("#").strip()
            header = None
            continue
        if not raw.startswith("|"):
            header = None
            continue
        cells = split_row(raw)
        if header is None:
            if cells and cells[0] == "鏡" and "台詞" in cells:
                header = cells
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        if len(cells) != len(header):
            warn("table", episode, f"第 {lineno} 行", f"欄數 {len(cells)}，表頭是 {len(header)}，照位置讀")
        col = {name: i for i, name in enumerate(header)}

        def get(name: str) -> str:
            i = col.get(name)
            return cells[i] if i is not None and i < len(cells) else ""

        shot = clean_shot(get("鏡"))
        action = get("動作")
        seconds = parse_seconds(get("秒數"))
        if seconds is None:
            warn("table", episode, shot, f"秒數讀不出來：{get('秒數')!r}")
        lines, leftovers = split_lines(get("台詞"))
        for bit in leftovers:
            if re.search(r"[A-Za-z]{2,}", bit):
                warn("table", episode, shot, f"台詞格有一段認不出說話的人，沒寫進表：{bit[:60]}")
        for speaker, marks, text in lines:
            row = parse_line(speaker, marks, text)
            if not row["english"]:
                warn("table", episode, shot, f"{speaker} 這句讀不到英文")
                continue
            if not row["voice"]:
                warn("table", episode, shot, f"{speaker} 沒標原聲或 Gemini，先當成 model")
                row["voice"] = "model"
            if row.pop("ambiguous_voice"):
                warn("table", episode, shot, f"{speaker} 同一句同時標了原聲與 Gemini，當成 gemini")
            row.update(
                episode=episode,
                shot=shot,
                shot_seconds=fmt_seconds(seconds),
                _scene=scene,
                _action=action,
                _seconds=seconds,
            )
            rows.append(row)
    return rows


def check(rows: list[dict[str, object]], warn) -> None:
    by_shot: dict[tuple[str, str], list[dict[str, object]]] = collections.OrderedDict()
    by_scene: dict[tuple[str, str, str], dict[str, list[str]]] = collections.OrderedDict()
    for row in rows:
        ep, shot = str(row["episode"]), str(row["shot"])
        words = int(row["words"])  # type: ignore[arg-type]
        if words > MAX_WORDS:
            warn("long", ep, shot, f"{row['speaker']} {words} 字（上限 {MAX_WORDS}）：{row['english']}")
        if row["voice"] == "model" and words <= MIN_MODEL_WORDS:
            warn("short", ep, shot, f"{row['speaker']} {words} 字：{row['english']}")
        if row["voice"] == "gemini" and MOUTH_TALKING in str(row["_action"]):
            warn("mouth", ep, shot, f"{row['speaker']} 是 Gemini（{row['kind']}），動作卻寫「{MOUTH_TALKING}」")
        by_shot.setdefault((ep, shot), []).append(row)
        key = (ep, str(row["_scene"]), str(row["speaker"]))
        by_scene.setdefault(key, {}).setdefault(str(row["voice"]), []).append(shot)

    for (ep, scene, speaker), voices in by_scene.items():
        if "model" in voices and "gemini" in voices:
            warn(
                "mixed",
                ep,
                ",".join(sorted(set(voices["model"] + voices["gemini"]))),
                f"{speaker} 在「{scene}」同時有原聲（{','.join(voices['model'])}）"
                f"與 Gemini（{','.join(voices['gemini'])}）",
            )

    for (ep, shot), shot_rows in by_shot.items():
        seconds = shot_rows[0]["_seconds"]
        if seconds is None:
            continue
        words = sum(int(r["words"]) for r in shot_rows)  # type: ignore[arg-type]
        need = words / WORDS_PER_SECOND + SECONDS_PAD
        if float(seconds) < need - 1e-9:  # type: ignore[arg-type]
            warn("tight", ep, shot, f"{words} 字要 {need:.1f} 秒，鏡長只有 {fmt_seconds(seconds)} 秒")  # type: ignore[arg-type]


WARN_TITLES = collections.OrderedDict(
    [
        ("long", f"台詞超過 {MAX_WORDS} 個字"),
        ("short", f"模型原聲只有 {MIN_MODEL_WORDS} 個字以內"),
        ("mouth", "Gemini 台詞的鏡，動作寫「嘴在說話」"),
        ("mixed", "同一場同一個角色既有原聲又有 Gemini"),
        ("tight", f"鏡長短於 字數/{WORDS_PER_SECOND:g} + {SECONDS_PAD:g} 秒"),
        ("table", "表格讀取問題"),
    ]
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, help="repo 根目錄")
    parser.add_argument("--out", type=Path, default=HERE / "lines-s1.csv", help="CSV 輸出路徑")
    parser.add_argument("--quiet", action="store_true", help="不印警告明細")
    args = parser.parse_args()

    root = args.root.resolve() if args.root else find_root(HERE)
    videos = root / "docs" / "videos"
    scripts = []
    for d in sorted(videos.iterdir()):
        m = EPISODE_DIR.match(d.name)
        if m and (d / "script.md").is_file():
            scripts.append((f"e{m.group(1)}", d / "script.md"))
    if not scripts:
        sys.exit(f"{videos} 底下沒有 till-the-verdict-eNNN/script.md")

    warnings: dict[str, list[tuple[str, str, str]]] = collections.defaultdict(list)

    def warn(kind: str, episode: str, shot: str, message: str) -> None:
        warnings[kind].append((episode, shot, message))

    rows: list[dict[str, object]] = []
    shots_per_ep: dict[str, int] = {}
    for episode, path in scripts:
        ep_rows = read_episode(path, episode, warn)
        rows.extend(ep_rows)
        text = path.read_text(encoding="utf-8")
        shots_per_ep[episode] = len(re.findall(r"^\|\s*\**c\d+", text, flags=re.MULTILINE))
    check(rows, warn)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"讀了 {len(scripts)} 集，寫出 {len(rows)} 句 → {args.out}")
    print()
    print("集    鏡數  台詞  原聲  Gemini  字數  警告")
    warn_per_ep = collections.Counter(ep for items in warnings.values() for ep, _, _ in items)
    for episode, _ in scripts:
        ep_rows = [r for r in rows if r["episode"] == episode]
        model = sum(1 for r in ep_rows if r["voice"] == "model")
        gemini = sum(1 for r in ep_rows if r["voice"] == "gemini")
        words = sum(int(r["words"]) for r in ep_rows)  # type: ignore[arg-type]
        print(
            f"{episode}  {shots_per_ep[episode]:>4}  {len(ep_rows):>4}  {model:>4}  {gemini:>6}"
            f"  {words:>4}  {warn_per_ep.get(episode, 0):>4}"
        )

    voices = collections.Counter(str(r["voice"]) for r in rows)
    kinds = collections.Counter(str(r["kind"]) for r in rows)
    speakers = collections.Counter(str(r["speaker"]) for r in rows)
    print()
    print("聲音：" + "，".join(f"{k} {v}" for k, v in voices.most_common()))
    print("種類：" + "，".join(f"{k} {v}" for k, v in kinds.most_common()))
    print("說最多的人：" + "，".join(f"{k} {v}" for k, v in speakers.most_common(8)))

    print()
    print("警告：" + "，".join(f"{WARN_TITLES[k]} {len(warnings[k])}" for k in WARN_TITLES if warnings[k]) or "警告：無")
    if not args.quiet:
        for kind, title in WARN_TITLES.items():
            items = warnings.get(kind)
            if not items:
                continue
            print()
            print(f"## {title}（{len(items)}）")
            for episode, shot, message in items:
                print(f"  {episode} {shot}  {message}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
