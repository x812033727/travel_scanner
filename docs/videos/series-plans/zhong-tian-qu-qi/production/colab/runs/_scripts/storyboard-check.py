"""Check storyboard scripts written to storyboard-shot-spec.md before they go to production.

Usage: python -I storyboard-check.py docs/videos/<slug>/script.md [more script.md ...]

Reads each script's six-column shot table
(| 鏡 | 景別、運鏡 | 畫面裡有誰 | 動作 | 台詞 | 秒數 |) and the `### ` scene sections, and reports:

- ERROR (exit 1): a scene without a **場頭** or without a line marked （結尾）; a question
  (？) with no 「→ 答在」 or 「懸念」 mark; scene seconds in the `（約 N 秒）` heading that differ
  from the sum of its shots by more than one second; a shot over 6 seconds not marked 長鏡;
  CRLF line endings.
- warning: a spoken line outside 10–24 characters (shouts marked 短喊 and the system are
  exempt); review these by hand — exceptions are allowed when the series notes say so.
- info: shot count, total seconds, and every affection panel 「名字 好感 +N → 總值」 so the
  ledger can be compared with the series notes.

Shot ids may carry a letter suffix (c08b) after a shot is split.
"""
import re
import sys

SHOT = re.compile(r"^\| c\d\d[a-z]? ")
PANEL = re.compile(r"(\S{2,3}) 好感 ([+-]\d+) → (-?\d+)")
STRIP = re.compile(r"[\s，。！？、…—「」：；．,.!?]")


def spoken_parts(cell):
    for part in cell.split("／"):
        m = re.match(r"\s*([^：（〔]+)(（[^）]*）)?：(.+)", part)
        if m:
            yield part, m.group(1).strip(), m.group(3)


def check(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    errors, warnings = [], []
    if b"\r\n" in raw:
        errors.append("CRLF line endings")
    shots = 0
    total = 0.0
    for scene in re.split(r"\n### ", text)[1:]:
        title = scene.split("\n", 1)[0]
        if "| 鏡 | 景別" not in scene:
            continue
        if "**場頭**" not in scene:
            errors.append(f"{title}: no 場頭")
        if "（結尾）" not in scene:
            errors.append(f"{title}: no line marked （結尾）")
        rows = [l for l in scene.split("\n") if SHOT.match(l) and l.count("|") == 7]
        scene_sum = 0.0
        for row in rows:
            cells = row.split("|")
            shot, line, sec = cells[1].strip(), cells[5], cells[6]
            m = re.search(r"([\d.]+) 秒", sec)
            seconds = float(m.group(1)) if m else 0.0
            if not m:
                warnings.append(f"{shot}: no seconds")
            if seconds > 6 and "長鏡" not in sec:
                errors.append(f"{shot}: {seconds} s but not marked 長鏡")
            scene_sum += seconds
            for part in line.split("／"):
                if "？" in part and "答在" not in part and "懸念" not in part:
                    errors.append(f"{shot}: question without 答在／懸念: {part.strip()[:30]}")
            for part, who, said in spoken_parts(line):
                if who == "系統" or "〔" in part or "短喊" in part:
                    continue
                body = re.sub(r"（[^）]*）", "", said)
                body = re.sub(r"←.*", "", body)
                n = len(STRIP.sub("", body))
                if n < 10 or n > 24:
                    warnings.append(f"{shot}: {who} line is {n} characters")
        shots += len(rows)
        total += scene_sum
        head = re.search(r"約 ([\d.]+) 秒", title)
        if head and rows and abs(float(head.group(1)) - scene_sum) > 1:
            errors.append(f"{title}: heading says {head.group(1)} s, shots add up to {scene_sum:g} s")
    panels = sorted(set(PANEL.findall(text)))
    return shots, total, panels, errors, warnings


def main(paths):
    sys.stdout.reconfigure(encoding="utf-8")
    failed = False
    for path in paths:
        shots, total, panels, errors, warnings = check(path)
        print(f"{path}: {shots} shots, {total:g} s")
        for p in panels:
            print(f"  panel {p[0]} {p[1]} → {p[2]}")
        for e in errors:
            print(f"  ERROR {e}")
        for w in warnings:
            print(f"  warning {w}")
        failed = failed or bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
