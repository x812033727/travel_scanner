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

# The hub is an independently authored content pack. Updating lesson order or
# readiness must preserve its introductions, links and tables without rewriting it.
print(f'60 catalog entries; {sum(row["ready"] for row in catalog.values())} draft packs / {sum(row["deepDraft"] for row in catalog.values())} deep drafts; no publication implied')
