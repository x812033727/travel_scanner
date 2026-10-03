#!/usr/bin/env python3
"""Validate the local Fountain draft and rebuild deterministic production handoff.

Standard library only. Timing fields are plans, never measured performance.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
NOTE = re.compile(r"\[\[(EPISODE|SCENE)\s+(\{.*?\})\]\]", re.S)
BEATS = {"cold_open", "setup", "turn_15", "turn_30", "climax_45", "ending"}
FLAGS = {"fire", "water", "stunt", "crowd", "vehicle", "period", "screen", "medical", "intimacy", "none"}


def proposed_block(episode, scene):
    """Initial location grouping, not a dated call sheet or supplier commitment."""
    if scene["date"].startswith("2011"):
        return "B07"
    if scene["date"].startswith("2013"):
        return "B08"
    location = scene["location"]
    if episode in {29, 30, 31} and location in {"L03", "L04", "L05", "L06", "L07", "L18", "L19", "L32"}:
        return "B09"
    if episode in {15, 22, 36, 38, 39, 40} and "crowd" in scene["flags"]:
        return "B10"
    for block, locations in {
        "B01": {"L03", "L04", "L39"},
        "B02": {"L06", "L07"},
        "B03": {"L10", "L11", "L16", "L28", "L31"},
        "B04": {"L08", "L09", "L17", "L18", "L30", "L34", "L40"},
        "B05": {"L01", "L13", "L14", "L19", "L20", "L21", "L35"},
    }.items():
        if location in locations:
            return block
    return "B06"


def csv_text(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def spoken(body):
    """Count dialogue following forced character cues; blank line ends a turn."""
    lines, speakers = [], []
    active = False
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("@"):
            speakers.append(line[1:])
            active = True
        elif not line:
            active = False
        elif active:
            # Some drafts put a language cue and speech on the same line.
            # Exclude only the leading parenthetical, not the spoken remainder.
            line = re.sub(r"^(?:（[^）]*）|\([^)]*\))\s*", "", line)
            lines.append(line)
    return len(HAN.findall("".join(lines))), speakers


def narration(body):
    """Read narration labels on either the character cue or leading direction."""
    result = []
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = block.strip().splitlines()
        if not lines or not lines[0].startswith("@"):
            continue
        labels = lines[0]
        speech = []
        leading = True
        for line in lines[1:]:
            if leading:
                match = re.match(r"^(?:（([^）]*)）|\(([^)]*)\))\s*(.*)$", line.strip())
                if match:
                    labels += " " + (match[1] or match[2] or "")
                    line = match[3]
            if line.strip():
                leading = False
                speech.append(line)
        if re.search(r"口白|旁白", labels):
            result.append("\n".join(speech))
    return result


def reading_html(episodes):
    output = ["""<!doctype html>
<html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>潮退之後｜全季讀本</title>
<style>
body{max-width:860px;margin:3rem auto;padding:0 1.2rem;color:#222;background:#faf8f3;font:18px/1.9 serif}
nav{columns:2}a{color:#205768}h1,h2,h3{line-height:1.5}.episode{break-before:page;margin-top:5rem}
.scene{margin-top:3rem}.scene.ending{break-inside:avoid}.action{margin:1rem 0}.speaker{margin:1.5rem 0 0 23%;font-weight:bold}
.dialogue{margin:0 14% 0 18%;white-space:pre-wrap}.meta{font:13px/1.5 sans-serif;color:#555}
@media print{body{background:white;font-size:12pt;max-width:none;margin:0}.scene h3,.scene .meta,.speaker{break-after:avoid}nav{display:none}a{color:inherit;text-decoration:none}@page{size:A4;margin:20mm}}
</style><h1>潮退之後｜全季讀本</h1>
<p>真人劇製作對白稿 production-v1。供演員讀本與前製拆解；各集時長尚未實測。原稿與場景編號以 Fountain 為準。</p><nav>"""]
    for ep in episodes:
        number = ep["episode"]
        output.append(f'<div><a href="#ep-{number:02}">EP{number:02}｜{html.escape(ep["title"])}</a></div>')
    output.append("</nav>")
    for ep in episodes:
        output.append(f'<section class="episode" id="ep-{ep["episode"]:02}"><h2>EP{ep["episode"]:02}｜{html.escape(ep["title"])}</h2>')
        for scene in ep["scenes"]:
            scene_class = "scene ending" if scene["beat"] == "ending" else "scene"
            visible_heading = re.sub(r"\s*#([^#]+)#$", r"｜\1", scene["heading"].lstrip("."))
            output.append(f'<article class="{scene_class}" id="{scene["id"]}"><h3>{html.escape(visible_heading)}</h3>')
            output.append(f'<p class="meta">劇中 {scene["date"]}｜{scene["id"]}｜計畫 {scene["planned_seconds"]} 秒（未實測）</p>')
            for block in re.split(r"\n\s*\n", scene["body"].strip()):
                if not block.strip():
                    continue
                lines = block.strip().splitlines()
                if lines[0].startswith("@"):
                    output.append(f'<p class="speaker">{html.escape(lines[0][1:])}</p>')
                    output.append('<p class="dialogue">' + html.escape("\n".join(lines[1:])) + '</p>')
                else:
                    output.append('<p class="action">' + html.escape(block).replace("\n", "<br>") + '</p>')
            output.append("</article>")
        output.append("</section>")
    output.append("</html>\n")
    return "\n".join(output)


def prop_proofs(master):
    esc = html.escape
    rows = "".join(f'<tr><td>{i}</td><td>{esc(row["name"])}</td><td>{esc(row["note"])}</td></tr>' for i, row in enumerate(master["P05"]["visible_rows"], 1))
    memorial = "".join(f'<li>{esc(name)}</li>' for name in master["P06"]["names"])
    confirmed = "、".join(master["memorial"]["confirmed_dead"])
    return f'''<!doctype html><html lang="zh-Hant"><meta charset="utf-8">
<title>潮退之後｜文件道具校樣</title><style>
body{{max-width:760px;margin:2rem auto;font:20px/1.7 serif;color:#222;background:#faf8f3;padding:0 1rem}}
article{{background:white;padding:2rem;margin:3rem 0;border:1px solid #bbb;break-before:page}}
table{{border-collapse:collapse;width:100%}}td{{border-bottom:1px solid #aaa;padding:.5rem}}ol{{columns:2}}
.note{{font:14px/1.6 sans-serif;color:#666}}.sheet{{min-height:420px}}.line{{border-bottom:1px solid #aaa;height:3rem}}
@media print{{body{{background:white;font-size:16pt}}article{{border:0;padding:0;margin:0}}@page{{size:A4;margin:20mm}}}}
</style><h1>潮退之後｜文件道具校樣</h1><p>依 document-master.json 產生。供美術確認文字、順序及版本；材質、筆跡、折損與裝置版面依實際鏡位製作。</p>
<article><p class="note">P05-A｜虛構道具校樣；2026年偷拍舊紙本，劇中畫面下緣裁切，不露用途</p><div class="sheet"><p>100年</p><h2>9/12</h2><table>{rows}</table></div></article>
<article><p class="note">P06｜2011年錯登版本，不得替換成最終複核名冊</p><h2>第二漁港市場火災<br>聯合公祭名冊</h2><ol>{memorial}</ol><p class="note">第十一名宋以恆為錯誤登錄。阿嬤之子：陳正隆。</p></article>
<article><p class="note">P20／P21｜兩層日期校樣；景物圖、簽名及筆跡由美術依鏡位完成</p><h2>{esc(master["P20_P21"]["heading"])}</h2><p>主稿：{esc(master["P20_P21"]["base_date"])}（{esc(master["P20_P21"]["base_version"])}）</p><p>提案人：{esc(master["P20_P21"]["proposal_name"])}</p><div class="line">批註日期：{esc(master["P20_P21"]["annotation_date"])}</div><p>批註姓名：{esc("、".join(master["P20_P21"]["annotation_names"]))}</p><p class="note">{esc(master["P20_P21"]["interpretation"])}</p></article>
<article><p class="note">P23-A｜EP24較早照片版</p><h2>2019中秋</h2><div class="line"></div><div class="line"></div><p class="note">下一行留白。道具汙痕、兩個裝訂孔和摺痕與下一版完全相同。</p></article>
<article><p class="note">P23-B｜EP30扣押版；EP31只證明後補，不能判定寫入日</p><h2>2019中秋</h2><div class="line">以後不記</div><div class="line"></div></article>
<article><p class="note">P18｜骨灰檢驗結果文字校樣，非真實檢驗報告</p><h2>本次檢驗結果</h2><p>{esc(master["P18"]["result"])}</p><p class="note">不得新增「排除母子」「非宋以恆」或性別判定。</p></article>
<article><p class="note">EP40｜記憶公園文字校樣</p><h2>十一位罹難者</h2><p>{esc(confirmed)}</p><div class="line"></div><p class="note">另留一格；不把仍失蹤的宋以恆再次刻成死者。此稿只供字樣與數量核對。</p></article></html>\n'''


def build(partial=False):
    registry = json.loads((ROOT / "registry.json").read_text())
    calendar = {item["episode"]: item for item in json.loads((ROOT / "calendar.json").read_text())}
    errors, warnings, episodes = [], [], []
    master = json.loads((ROOT / "document-master.json").read_text())
    roster = [row["name"] for row in master["P05"]["visible_rows"]]
    memorial = master["P06"]["names"]
    if len(set(roster)) != 8 or roster[4] != "宋以恆" or len(set(memorial)) != 11 or memorial[10] != "宋以恆" or set(roster) & set(memorial) != {"宋以恆"}:
        errors.append("document-master: roster/public memorial count, order, or overlap changed")
    if len(set(master["memorial"]["confirmed_dead"])) != 11 or "宋以恆" in master["memorial"]["confirmed_dead"]:
        errors.append("document-master: final memorial must have eleven confirmed dead, excluding Yi-heng")
    cast_by_name = {info["name"]: ident for ident, info in registry["cast"].items()}
    cast_by_name["阿鐘"] = "C14"
    budget_doc = master["P20_P21"]
    if budget_doc["proposal_name"] != registry["cast"]["C13"]["name"] or budget_doc["annotation_names"] != [registry["cast"][ident]["name"] for ident in ("C09", "C11")]:
        errors.append("document-master: budget proposal/annotation names must match cast")
    files = sorted((ROOT / "scripts").glob("ep-*.fountain"))
    expected = {f"ep-{n:02}.fountain" for n in range(1, 41)}
    actual = {path.name for path in files}
    if not partial and actual != expected:
        errors.append(f"Expected exactly EP01–40; missing {sorted(expected-actual)}, unexpected {sorted(actual-expected)}")
    for path in files:
        raw = path.read_text(encoding="utf-8")
        notes = list(NOTE.finditer(raw))
        ep_notes = [note for note in notes if note[1] == "EPISODE"]
        if len(ep_notes) != 1:
            errors.append(f"{path.name}: expected one EPISODE note")
            continue
        try:
            ep = json.loads(ep_notes[0][2])
            n = ep["episode"]
            if n not in calendar or path.name != f"ep-{n:02}.fountain":
                raise ValueError("episode/file/calendar mismatch")
            if ep["title"] != calendar[n]["title"]:
                raise ValueError("episode title differs from calendar")
            if f'Title: 潮退之後 EP{n:02}｜{ep["title"]}' not in raw.splitlines():
                raise ValueError("Fountain title page differs from episode metadata")
            if ep.get("timing_status") != "unmeasured":
                raise ValueError("timing must be unmeasured until an actual table read")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f"{path.name}: {exc}")
            continue
        if re.search(r"\bTODO\b|\bTBD\b|以下省略|對白略|此處補入|\[待補\]", raw, re.I):
            errors.append(f"{path.name}: unresolved writing placeholder")
        if re.search(r"^[^\n@]+[。！？]@[^\n]+$", raw, re.M):
            errors.append(f"{path.name}: character cue attached to action; place @cue on its own line")
        scene_notes = [note for note in notes if note[1] == "SCENE"]
        scenes = []
        elapsed = 0
        narrated_lines = []
        for index, note in enumerate(scene_notes):
            prefix = raw[:note.start()].rstrip().splitlines()
            heading = prefix[-1] if prefix else ""
            end = scene_notes[index+1].start() if index+1 < len(scene_notes) else len(raw)
            body = raw[note.end():end]
            # The next heading precedes its metadata; keep it out of this body.
            if index+1 < len(scene_notes):
                body = re.sub(r"\n\.[^\n]*#[^\n]*#\s*$", "", body)
            try:
                scene = json.loads(note[2])
                ident = f"E{n:02}-S{index+1:02}"
                if scene["id"] != ident or not heading.startswith(".") or f"#{ident}#" not in heading:
                    raise ValueError(f"expected numbered heading and metadata {ident}")
                for key in ("date", "location", "time", "cast", "voice_only", "extras", "props", "flags", "beat", "planned_seconds"):
                    if key not in scene:
                        raise ValueError(f"missing {key}")
                for field, collection in (("cast", "cast"), ("props", "props")):
                    if len(scene[field]) != len(set(scene[field])):
                        raise ValueError(f"duplicate {field} IDs")
                    unknown = set(scene[field]) - set(registry[collection])
                    if unknown:
                        raise ValueError(f"unknown {field}: {sorted(unknown)}")
                if scene["location"] not in registry["locations"]:
                    raise ValueError("unknown location")
                if not set(scene["voice_only"]).issubset(scene["cast"]):
                    raise ValueError("voice_only must be a cast subset")
                if scene["time"] not in {"DAWN", "DAY", "DUSK", "NIGHT"}:
                    raise ValueError("invalid time")
                if scene["beat"] not in BEATS or not set(scene["flags"]).issubset(FLAGS):
                    raise ValueError("invalid beat/flags")
                day = scene["date"]
                historical = day == "2011-09-12" or day.startswith("2013-12")
                if not historical and not calendar[n]["start_date"] <= day <= calendar[n]["end_date"]:
                    raise ValueError(f"date {day} outside episode calendar")
                if not isinstance(scene["planned_seconds"], int) or scene["planned_seconds"] <= 0:
                    raise ValueError("planned_seconds must be a positive integer")
                chars, speakers = spoken(body)
                narrated_lines.extend(narration(body))
                for speaker in set(speakers):
                    name = re.split(r"[（(]", speaker)[0].strip()
                    ident_cast = cast_by_name.get(name)
                    if ident_cast and ident_cast not in scene["cast"]:
                        errors.append(f"{ident}: speaking role {name}/{ident_cast} missing from cast metadata")
                scene.update(heading=heading, body=body.strip(), dialogue_han=chars, speakers=speakers, planned_start_seconds=elapsed)
                elapsed += scene["planned_seconds"]
                if chars / scene["planned_seconds"] > 5.5:
                    warnings.append(f"{ident}: {chars} spoken Han / {scene['planned_seconds']} planned seconds; table read may overrun")
                scenes.append(scene)
            except (ValueError, KeyError, TypeError) as exc:
                errors.append(f"{path.name} scene {index+1}: {exc}")
        if narrated_lines and n not in {1, 10, 11, 20, 21, 30, 31, 40}:
            errors.append(f"{path.name}: narration is not allowed in this episode")
        if n == 40 and (len(narrated_lines) != 1 or re.sub(r"[\s。.!！…，,「」『』]", "", narrated_lines[0]) != "潮退了"):
            errors.append(f"{path.name}: EP40 must have exactly one narration, 潮退了")
        if not scenes:
            errors.append(f"{path.name}: no valid scenes")
            continue
        counts = Counter(scene["beat"] for scene in scenes)
        for beat in BEATS - {"setup"}:
            if counts[beat] != 1:
                errors.append(f"{path.name}: expected one {beat}, found {counts[beat]}")
        if scenes[0]["beat"] != "cold_open" or scenes[-1]["beat"] != "ending":
            errors.append(f"{path.name}: first/last scenes must be cold_open/ending")
        minimum_body = 3195 if n == 40 else 3165
        if not minimum_body <= elapsed <= 3585:
            errors.append(f"{path.name}: planned body {elapsed}s outside {minimum_body}–3585s")
        chars = sum(scene["dialogue_han"] for scene in scenes)
        if chars < 6000:
            warnings.append(f"EP{n:02}: {chars} spoken Han (<6000 reference); review dramatic action and table-read capacity")
        for scene in scenes:
            targets = {"turn_15":900, "turn_30":1800, "climax_45":2700}
            target = targets.get(scene["beat"])
            if target and not scene["planned_start_seconds"]-180 <= target <= scene["planned_start_seconds"]+scene["planned_seconds"]+180:
                warnings.append(f"{scene['id']}: {scene['beat']} outside ±3min of the target in planned timeline")
        ep.update(scenes=scenes, dialogue_han=chars, planned_body_seconds=elapsed, planned_program_seconds=elapsed+105+(0 if n == 40 else 30))
        episodes.append(ep)
    return registry, calendar, episodes, errors, warnings


def outputs(registry, calendar, episodes, warnings):
    files = {}
    rows, timing, cast_rows = [], [], []
    locations, props = defaultdict(list), defaultdict(list)
    speaking_parts = defaultdict(list)
    cast_by_name = {info["name"]: ident for ident, info in registry["cast"].items()}
    cast_by_name["阿鐘"] = "C14"
    index = ["# 潮退之後｜全季劇本索引", "", "由 `build_package.py` 從 Fountain 產生。所有時長均為計畫，尚未讀本實測；可發聲漢字不含動作、括註及 metadata，不等於片長。", "", "[可列印全季讀本](reading-copy.html)｜[逐場拆表](scenes.csv)｜[逐集時長](timing.csv)｜[角色故事日](cast-days.csv)｜[場地](locations.csv)｜[道具](props.csv)", "", "| 集 | 劇本 | 故事日期 | 場數 | 對白漢字 | 正文計畫 | 含頭尾預告 |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for ep in episodes:
        n = ep["episode"]
        dates = calendar[n]
        timing.append(dict(episode=n, title=ep["title"], scenes=len(ep["scenes"]), night_scenes=sum(s["time"] == "NIGHT" for s in ep["scenes"]), dialogue_han=ep["dialogue_han"], planned_body_seconds=ep["planned_body_seconds"], opening_seconds=45, closing_seconds=60, preview_seconds=(0 if n == 40 else 30), planned_program_seconds=ep["planned_program_seconds"], measured_program_seconds="", timing_status="unmeasured"))
        index.append(f'| {n:02} | [{ep["title"]}](../scripts/ep-{n:02}.fountain) | {dates["start_date"]}～{dates["end_date"]} | {len(ep["scenes"])} | {ep["dialogue_han"]} | {ep["planned_body_seconds"]/60:.2f} 分 | {ep["planned_program_seconds"]/60:.2f} 分 |')
        day_cast = defaultdict(lambda: {"on_camera":[], "voice_only":[]})
        for scene in ep["scenes"]:
            row = {key:scene[key] for key in ("id", "date", "time", "beat", "planned_seconds", "planned_start_seconds", "dialogue_han")}
            row.update(episode=n, proposed_block=proposed_block(n, scene), heading=scene["heading"], location_id=scene["location"], location=registry["locations"][scene["location"]]["name"], cast=";".join(scene["cast"]), cast_names=";".join(registry["cast"][c]["name"] for c in scene["cast"]), voice_only=";".join(scene["voice_only"]), extras=";".join(scene["extras"]), props=";".join(scene["props"]), flags=";".join(scene["flags"]))
            rows.append(row)
            locations[scene["location"]].append(scene)
            for speaker in {re.split(r"[（(]", cue)[0].strip() for cue in scene["speakers"]}:
                speaking_parts[speaker].append(scene["id"])
            for prop in scene["props"]:
                props[prop].append(scene)
            for cast in scene["cast"]:
                mode = "voice_only" if cast in scene["voice_only"] else "on_camera"
                day_cast[(scene["date"], cast)][mode].append(scene["id"])
        for (day, cast), appearances in sorted(day_cast.items()):
            cast_rows.append(dict(episode=n, story_date=day, cast_id=cast, name=registry["cast"][cast]["name"], on_camera_scenes=";".join(appearances["on_camera"]), voice_only_scenes=";".join(appearances["voice_only"]), note="故事日，非拍攝通告日"))
    files["episode-index.md"] = "\n".join(index)+"\n"
    files["scenes.csv"] = csv_text(["episode", "id", "proposed_block", "date", "heading", "location_id", "location", "time", "cast", "cast_names", "voice_only", "extras", "props", "flags", "beat", "planned_start_seconds", "planned_seconds", "dialogue_han"], rows)
    files["timing.csv"] = csv_text(["episode", "title", "scenes", "night_scenes", "dialogue_han", "planned_body_seconds", "opening_seconds", "closing_seconds", "preview_seconds", "planned_program_seconds", "measured_program_seconds", "timing_status"], timing)
    block_rows = []
    for number in range(1, 12):
        block = f"B{number:02}"
        assigned = [row for row in rows if row["proposed_block"] == block]
        block_rows.append(dict(block=block, scene_count=len(assigned), scenes=";".join(row["id"] for row in assigned), night_scenes=sum(row["time"] == "NIGHT" for row in assigned), note="依場地初分，副導按演員及實景重排；B11為補拍預留"))
    files["blocks.csv"] = csv_text(["block", "scene_count", "scenes", "night_scenes", "note"], block_rows)
    files["cast-days.csv"] = csv_text(["episode", "story_date", "cast_id", "name", "on_camera_scenes", "voice_only_scenes", "note"], cast_rows)
    cast_summary = []
    for ident, info in registry["cast"].items():
        appearances = [row for row in cast_rows if row["cast_id"] == ident]
        on_camera = sorted({row["episode"] for row in appearances if row["on_camera_scenes"]})
        voice_only = sorted({row["episode"] for row in appearances if row["voice_only_scenes"]})
        cast_summary.append(dict(cast_id=ident, name=info["name"], on_camera_episode_count=len(on_camera), on_camera_episodes=";".join(f"{n:02}" for n in on_camera), voice_episodes=";".join(f"{n:02}" for n in voice_only), note=info.get("note", "")))
    files["speaking-parts.csv"] = csv_text(["role", "registered_cast_id", "scene_count", "episodes", "scenes", "note"], [dict(role=name, registered_cast_id=cast_by_name.get(name, ""), scene_count=len(scenes), episodes=";".join(sorted({scene[1:3] for scene in scenes})), scenes=";".join(scenes), note="角色臺詞稱謂；未編號小角色須另報具詞演員，職務同名是否共用演員由副導確認") for name, scenes in sorted(speaking_parts.items())])
    files["cast-summary.csv"] = csv_text(["cast_id", "name", "on_camera_episode_count", "on_camera_episodes", "voice_episodes", "note"], cast_summary)
    files["table-read.csv"] = csv_text(["episode", "scene_id", "planned_seconds", "read_seconds", "staged_action_seconds", "measured_total_seconds", "reader_version", "notes"], [dict(episode=row["episode"], scene_id=row["id"], planned_seconds=row["planned_seconds"], read_seconds="", staged_action_seconds="", measured_total_seconds="", reader_version="", notes="") for row in rows])
    for collection, groups in (("locations", locations), ("props", props)):
        grouped = []
        for ident, info in registry[collection].items():
            scenes = groups[ident]
            grouped.append(dict(id=ident, name=info["name"], scene_count=len(scenes), scenes=";".join(s["id"] for s in scenes), episodes=";".join(sorted({s["id"][1:3] for s in scenes})), note=info.get("note", "")))
        files[f"{collection}.csv"] = csv_text(["id", "name", "scene_count", "scenes", "episodes", "note"], grouped)
    files["reading-copy.html"] = reading_html(episodes)
    files["prop-proofs.html"] = prop_proofs(json.loads((ROOT / "document-master.json").read_text()))
    summary = {"version":"production-v1", "timing_status":"unmeasured", "episodes":len(episodes), "scenes":len(rows), "dialogue_han":sum(ep["dialogue_han"] for ep in episodes), "validation_warnings":warnings}
    files["validation.json"] = json.dumps(summary, ensure_ascii=False, indent=2)+"\n"
    return files, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate all 40 and compare generated outputs without writing")
    parser.add_argument("--partial", action="store_true", help="diagnose drafts in progress; do not write or certify a full package")
    args = parser.parse_args()
    registry, calendar, episodes, errors, warnings = build(args.partial)
    files, summary = outputs(registry, calendar, episodes, warnings)
    if args.partial:
        print(json.dumps({**summary, "errors":errors}, ensure_ascii=False, indent=2))
        return bool(errors)
    if not errors:
        destination = ROOT / "breakdowns"
        if args.check:
            for name, contents in files.items():
                path = destination / name
                if not path.exists() or path.read_text() != contents:
                    errors.append(f"generated output out of date: {path.relative_to(ROOT)}")
        else:
            destination.mkdir(exist_ok=True)
            for name, contents in files.items():
                (destination / name).write_text(contents, encoding="utf-8")
    print(json.dumps({**summary, "errors":errors, "mode":"check" if args.check else "build"}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
