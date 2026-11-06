#!/usr/bin/env python3
"""把《恁祖媽今年18》一集的 script.md 解析成結構化的場與鏡（標準函式庫，python3 -I 跑）。

  parse_script.py docs/videos/tai-nainai-e001/script.md [--json]

輸出（--json）：{"episode": 1, "scenes": [{"n", "title", "header": {欄位: 文字}, "sets": [cast.json 的場景 id], "lamp": [...],
"shots": [{"id", "camera", "who", "action", "dialogue": [...], "seconds", "row", "row_sha256"}]}]}。
台詞拆成 {"speaker_label", "speaker", "notes", "text", "inner", "offscreen", "refs"}：speaker 是 cast.json 的
角色或路人 id（對不到時為 null，交給 compile.py 報錯）。row_sha256 是那一列六欄原文的雜湊，shots-en.json 用它綁定。
不加 --json 時印每場的鏡數、秒數與對不到的說話人。
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAST = HERE.parent / "cast.json"

SHOT_ID = re.compile(r"c\d+[a-z]?")
SCENE = re.compile(r"^### 第(.+?)[場段]：(.+?)(?:（約 ([\d.]+) 秒）)?\s*$")
HEADER_ITEM = re.compile(r"^- \*\*(.+?)\*\*：(.*)$")
SET_REF = re.compile(r"`(?:set-)?([a-z0-9-]+?)(?:-t\d+)?`")
LAMP = re.compile(r"燈\s*(\d+)")
SECONDS = re.compile(r"([\d.]+)\s*秒")
# 「林美鳳（拖長尾音）：……」；說話人是行首到第一個全形括號或冒號
LINE = re.compile(r"^(?P<who>[^（：—]{1,12}?)(?:（(?P<notes>[^）]*)）)?：(?P<text>.+)$")
REF_MARK = re.compile(r"（(?:→ 答在|← 因為)[^）]*）|← 因為 [c\d、，, ]+|（結尾）|（懸念[^）]*）")

ALIASES = {
    "月棠": "yuetang-18", "沈月棠": "yuetang-18", "玉琴": "yuqin", "沈玉琴": "yuqin", "建邦": "jianbang", "沈建邦": "jianbang",
    "知遠": "zhiyuan", "沈知遠": "zhiyuan", "小滿": "xiaoman", "沈小滿": "xiaoman", "福伯": "fubo", "建業": "jianye", "沈建業": "jianye",
    "林美鳳": "meifeng", "美鳳": "meifeng", "知行": "zhixing", "沈知行": "zhixing", "周懷安": "zhouhuaian", "顧承霖": "guchenglin",
    "江慕白": "jiangmubai", "蘇曉": "suxiao", "老陳": "laochen", "何曉陽": "hexiaoyang", "曉陽": "hexiaoyang", "林導": "lindao",
    "作甫": "zuofu", "沈作甫": "zuofu", "阿凱": "akai", "錢老闆": "qianlaoban", "吳校長": "wuxiaozhang", "陳老師": "chenlaoshi",
    "何啟盛": "heqisheng", "鄭醫師": "zhengyishi", "林主任": "linzhuren", "高經理": "gaojingli", "鄧會長": "denglao",
    "春桃阿婆": "chuntao", "春桃": "chuntao",
}


SET_IDS = {s["id"] for s in json.loads(CAST.read_text(encoding="utf-8"))["sets"]}


def load_cast() -> tuple[dict, dict]:
    cast = json.loads(CAST.read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in cast["characters"]}
    extras = {e["name"]: e["id"] for e in cast["extras"]}
    return chars, extras


def speaker_id(label: str, notes: str, chars: dict, extras: dict) -> str | None:
    label = label.strip()
    if label in ("月棠", "沈月棠") and re.search(r"96|九十六", notes):
        return "yuetang-96"
    if label in ALIASES:
        return ALIASES[label]
    for name, eid in extras.items():
        if label == name or label in name.split("、") or name.startswith(label) or name.endswith(label):
            return eid
    if label == "電話那頭":
        for alias, cid in ALIASES.items():
            if alias in notes:
                return cid
    return None


def parse_dialogue(cell: str, chars: dict, extras: dict) -> list[dict]:
    cell = REF_MARK.sub("", cell.strip()).strip()
    if cell in ("—", "-", "") or cell.startswith("（無台詞") or cell.startswith("—"):
        return []
    out = []
    for part in re.split(r"<br\s*/?>", cell):
        part = part.strip()
        m = LINE.match(part)
        if not m:
            out.append({"speaker_label": None, "speaker": None, "notes": "", "text": part, "inner": False, "offscreen": False, "refs": [], "raw": part})
            continue
        notes = m.group("notes") or ""
        text = m.group("text").strip()
        refs = [r.strip("（）") for r in REF_MARK.findall(text)]
        text = REF_MARK.sub("", text).strip()
        look = re.search(r"`([a-z0-9-]+)`", notes)
        labels = [x for x in re.split(r"[、與和]", m.group("who").strip()) if x]
        ids = [speaker_id(x, notes, chars, extras) for x in labels]
        out.append({
            "speaker_label": m.group("who").strip(),
            "speaker": ids[0] if all(ids) else None,
            "together": ids[1:] if len(ids) > 1 and all(ids) else [],
            "notes": notes,
            "look": look.group(1) if look else None,
            "text": text,
            "inner": "心裡話" in notes,
            "offscreen": "畫外" in notes or "電話" in notes,
            "refs": refs,
            "raw": part,
        })
    return out


def parse(path: Path) -> dict:
    chars, extras = load_cast()
    ep = int(re.search(r"e(\d{3})", str(path)).group(1))
    scenes: list[dict] = []
    cur = None
    in_header = False
    in_table = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        m = SCENE.match(raw)
        if m:
            cur = {"n": m.group(1), "title": m.group(2), "seconds_note": float(m.group(3)) if m.group(3) else None,
                   "header": {}, "sets": [], "lamp": [], "shots": []}
            scenes.append(cur)
            in_header = in_table = False
            continue
        if cur is None:
            continue
        if raw.startswith("## "):
            cur = None
            continue
        if raw.startswith("**場頭**"):
            in_header = True
            continue
        h = HEADER_ITEM.match(raw)
        if in_header and h:
            cur["header"][h.group(1)] = h.group(2)
            last_key = h.group(1)
            continue
        if in_header and raw.startswith("  ") and cur["header"]:
            key = list(cur["header"])[-1]
            cur["header"][key] += raw.strip()
            continue
        if raw.startswith("| 鏡 | 景別"):
            in_header, in_table = False, True
            continue
        if in_table and raw.startswith("| ---"):
            continue
        if in_table and raw.startswith("|"):
            cells = [c.strip() for c in raw.strip().strip("|").split(" | ")]
            if len(cells) != 6 or not SHOT_ID.fullmatch(cells[0]):
                raise ValueError(f"{path}: cannot read the row {raw[:80]!r}")
            sec = SECONDS.search(cells[5])
            cur["shots"].append({
                "id": cells[0], "camera": cells[1], "who": cells[2], "action": cells[3],
                "dialogue": parse_dialogue(cells[4], chars, extras),
                "seconds": float(sec.group(1)) if sec else None,
                "long": "長鏡" in cells[5] or "長鏡" in cells[1],
                "row": raw.strip(),
                "row_sha256": hashlib.sha256(raw.strip().encode("utf-8")).hexdigest(),
            })
            continue
        if in_table and not raw.startswith("|"):
            in_table = False
    prev_sets: list[str] = []
    for sc in scenes:
        place = " ".join(v for k, v in sc["header"].items() if k.startswith("地點"))
        when = " ".join(v for k, v in sc["header"].items() if k.startswith("時間"))
        sc["sets"] = [x for x in dict.fromkeys(SET_REF.findall(place)) if x in SET_IDS]
        sc["lamp"] = [int(n) for n in LAMP.findall(when)]
        if not sc["sets"] and "同一間" in place:
            sc["sets"] = prev_sets  # 「同一間正廳（格局同第一段）」
        prev_sets = sc["sets"]
    return {"episode": ep, "source": str(path), "scenes": scenes}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    doc = parse(Path(argv[0]))
    if "--json" in argv:
        print(json.dumps(doc, ensure_ascii=False, indent=1))
        return 0
    bad = 0
    for sc in doc["scenes"]:
        secs = sum(s["seconds"] or 0 for s in sc["shots"])
        print(f"第{sc['n']}場 {sc['title']}：{len(sc['shots'])} 鏡、{secs:g} 秒、場景 {sc['sets']}、燈 {sc['lamp']}")
        for s in sc["shots"]:
            for d in s["dialogue"]:
                if not d["speaker"]:
                    bad += 1
                    print(f"  {s['id']}: 說話人對不到 cast.json：{d['speaker_label']!r}（{d['raw'][:40]}）")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
