"""Maintain 60 stable IDs independently of reading order. Planned rows create no packs."""
import json
from pathlib import Path
import re
from hashlib import sha256
from opencc import OpenCC

ROOT = Path(__file__).resolve().parents[2]
catalog_path = ROOT / "apps/web/lib/codex-learning/catalog.json"
catalog = {row["id"]: row for row in json.loads(catalog_path.read_text(encoding="utf-8"))}
planned = json.loads((ROOT / "docs/codex-learning/deep/planned.json").read_text(encoding="utf-8"))
plan = (ROOT / "docs/codex-learning/depth-plan.md").read_text(encoding="utf-8")
order = re.findall(r"^\| (\d+) \| ([A-J]) [^|]+ \| (\d+) \| [^|]+ \| `([^`]+)` \|", plan, re.M)
assert len(order) == 60
positions = {int(id_): (int(sequence), group, slug) for sequence, group, id_, slug in order}
cc = OpenCC("t2s")
for row in planned:
    locales = {locale: {"title": row["titles"][i], "description": row["outcomes"][i]} for i, locale in enumerate(["zh-TW", "en", "ja", "ko"])}
    locales["zh-CN"] = {key: cc.convert(value) for key, value in locales["zh-TW"].items()}
    old = catalog.get(row["id"], {})
    catalog[row["id"]] = {"id": row["id"], "slug": positions[row["id"]][2], "level": 0 if positions[row["id"]][1] < "D" else 1 if positions[row["id"]][1] < "G" else 2,
                          "platforms": row["platforms"], "goals": row["goals"], "minutes": 15, "aliases": row["aliases"],
                          "related": old.get("related", []), "locales": locales,
                          "ready": old.get("ready", False), "checkedOn": old.get("checkedOn")}
first_prerequisites = {"A": [], "B": [34], "C": [3], "D": [6], "E": [5], "F": [6], "G": [9, 10], "H": [18], "I": [18], "J": [19, 21]}
pilots = {3: (15, 25), 4: (12, 20), 10: (12, 20), 11: (12, 20), 23: (12, 25)}
authored_sources = json.loads((ROOT / "docs/codex-learning/deep/sources.json").read_text(encoding="utf-8"))
modules = {int(path.stem): json.loads(path.read_text(encoding="utf-8")) for path in (ROOT / "docs/codex-learning/deep/modules").glob("*.json")}
build_report = ROOT / "docs/codex-learning/deep/build-report.json"
compiled = {item["id"]: item for item in json.loads(build_report.read_text(encoding="utf-8"))["lessons"]} if build_report.exists() else {}
for id_, row in catalog.items():
    sequence, unit, slug = positions[id_]
    assert row["slug"] == slug, "A permanent URL must not be renumbered"
    row["order"] = sequence
    row["unit"] = unit
    row["batch"] = (sequence - 1) // 20 + 1
    preceding = next((int(other_id) for other_seq, _, other_id, _ in order if int(other_seq) == sequence - 1), None)
    following = next((int(other_id) for other_seq, _, other_id, _ in order if int(other_seq) == sequence + 1), None)
    row["prerequisites"] = first_prerequisites[unit] if (sequence - 1) % 6 == 0 else [preceding]
    if id_ in {35, 36, 37}:
        # These are alternative operating systems, not dependencies on one another.
        row["prerequisites"] = [5]
    if id_ in {38, 39}:
        row["prerequisites"] = [4]
    if id_ == 40:
        row["prerequisites"] = [3, 4]
    if id_ == 15:
        row["prerequisites"] = [2, 6]
    if id_ == 41:
        row["prerequisites"] = [40, 15]
    if not row["related"]:
        row["related"] = list(dict.fromkeys([value for value in [*row["prerequisites"], following, 12] if value and value != id_]))[:3]
    evidence = compiled.get(id_, {})
    full_draft = evidence.get("compiled", False) and evidence.get("fullFiveLocales", False)
    for locale in ["zh-TW", "en", "ja", "ko"]:
        path = ROOT / f'docs/codex-learning/deep/{locale}/{id_:02d}.md'
        full_draft = full_draft and path.exists() and sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == evidence.get("sourceHashes", {}).get(locale)
    pack_path = ROOT / f'apps/api/app/guides/content/{slug}.json'
    pack_exists = pack_path.exists()
    full_draft = full_draft and pack_exists and sha256(pack_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest() == evidence.get("packHash")
    if full_draft and pack_exists:
        row["ready"] = True
        row["checkedOn"] = max(source["checked_on"] for source in authored_sources[f'{id_:02d}'])
    row["depthStatus"] = "drafted" if row["ready"] else "planned"
    row["deepDraft"] = full_draft and pack_exists
    row["operationMinutes"] = modules.get(id_, {}).get("operationMinutes", pilots.get(id_, (None, None))[1])
    if id_ in modules:
        row["minutes"] = modules[id_].get("readingMinutes", 10)
    if id_ in pilots:
        row["minutes"] = pilots[id_][0]
catalog_path.write_text(json.dumps([catalog[id_] for id_ in sorted(catalog)], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

hub_path = ROOT / "apps/api/app/guides/content/codex-learning-hub.json"
hub = json.loads(hub_path.read_text(encoding="utf-8"))
intro = {
    "zh-TW": "從安裝、第一個任務到 MD 規則與進階整合，規劃 60 篇 Codex 教學、十個單元。依程度、平台、需求或指令搜尋下一篇；尚未公開的教學會標示狀態，方便安排學習路線。",
    "zh-CN": "从安装、第一个任务到 MD 规则与进阶集成，规划 60 篇 Codex 教程、十个单元。按程度、平台、需求或命令搜索下一篇；尚未公开的教程会标示状态，方便安排学习路线。",
    "en": "A planned 60-lesson, ten-unit Codex curriculum, from setup and your first task to MD instructions and advanced integrations. Find your next lesson by experience, platform, goal or command; unpublished entries show their status.",
    "ja": "導入と最初のタスクから MD の指示、高度な連携まで、60 レッスン・十単元を予定しています。習熟度、環境、目的、コマンドで次の記事を探せます。未公開の記事には状態を表示します。",
    "ko": "설치와 첫 작업부터 MD 지침과 고급 연동까지 60개 강의, 열 개 단원을 계획합니다. 수준, 환경, 목표, 명령으로 다음 글을 찾고 미게시 항목의 상태를 확인할 수 있습니다.",
}
for locale, document in hub["locales"].items():
    document["description"] = intro[locale]
    for block in document["blocks"]:
        if block["type"] == "paragraph" and (block["text"].startswith("32 /") or block["text"].startswith("60 /")):
            block["text"] = "60 / 10 / Windows · macOS · Linux · iOS · Android / CLI · IDE · Cloud"
        if block["type"] == "table":
            for i, label in enumerate(["01–20", "21–40", "41–60"]):
                block["rows"][i][0] = label
    if document["blocks"][0].get("type") == "paragraph":
        document["blocks"][0]["text"] = intro[locale]
    else:
        document["blocks"].insert(0, {"type": "paragraph", "text": intro[locale]})
hub_path.write_text(json.dumps(hub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f'60 catalog entries; {sum(row["ready"] for row in catalog.values())} draft packs / {sum(row["deepDraft"] for row in catalog.values())} deep drafts; no publication implied')
