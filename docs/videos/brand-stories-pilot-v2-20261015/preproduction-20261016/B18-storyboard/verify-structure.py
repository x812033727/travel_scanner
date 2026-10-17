"""Offline structural verification; not an independent editorial or worker review."""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

base = Path(__file__).resolve().parent
repo = Path(sys.argv[1]).resolve()
load = lambda name: json.loads((base / name).read_text(encoding="utf-8"))
sha = lambda data: hashlib.sha256(data).hexdigest()
b = load("storyboard.json")
m = load("metrics.json")
source = repo / b["source_pins"][0]["file"]
full = source.read_text(encoding="utf-8")
matches = re.findall(r"^> (.+)\n\n\*\*製作註 ([A-Z]\d+[a-z]?)（不朗讀）\*\*：(.+)", full, re.M)
assert len(matches) == 24
original = {pid: text for text, pid, _ in matches}
assert len(original) == 24
assert [(p["id"], p["text"]) for p in b["paragraphs"]] == [(pid, text) for text, pid, _ in matches]
count = lambda text: sum(len(c.encode("utf-16-le")) // 2 for c in text if not c.isspace() and unicodedata.category(c)[0] not in "PSZ")
assert sum(count(t) for t in original.values()) == m["units"] == 2729
assert sha(source.read_bytes()) == b["original_fullscript_sha256"]
for pin in b["source_pins"]:
    assert pin["base"] == "repository_root"
    assert not Path(pin["file"]).is_absolute()
    assert sha((repo / pin["file"]).read_bytes()) == pin["sha256"]
rebuilt = {pid: "" for pid in original}
next_start = {pid: 0 for pid in original}
shot_by_id = {s["id"]: s for s in b["shots"]}
assert len(shot_by_id) == len(b["shots"]) == 103
for s in b["shots"]:
    for r in s["narration_refs"]:
        pid = r["paragraph_id"]
        assert r["start_utf16"] == next_start[pid]
        assert original[pid].encode("utf-16-le")[r["start_utf16"]*2:r["end_utf16"]*2].decode("utf-16-le") == r["text"]
        next_start[pid] = r["end_utf16"]
        rebuilt[pid] += r["text"]
assert rebuilt == original
assert b["adaptations"] == []
assert b["look"] == {"preset": "cute-mystery"}
assert b["image_model"] == "image-01"
assert b["subtitles"]["burn_in"] is False
illustrations = [s for s in b["shots"] if "prompt" in s]
cards = [s for s in b["shots"] if "card" in s]
assert len(illustrations) == 87 and len(cards) == 16
assert len({s["image_asset_key"] for s in illustrations}) == 82
assert len(b["hook_visual_reuse"]) == 3
for binding in b["hook_visual_reuse"]:
    a, c = (shot_by_id[binding[k]] for k in ["setup_shot", "recovery_shot"])
    assert a["prompt"] == c["prompt"]
    assert a["camera"] == c["camera"]
    assert a["image_asset_key"] == c["image_asset_key"] == binding["asset_key"]
assert [shot_by_id[r["recovery_shot"]]["narration_refs"][0]["paragraph_id"] for r in b["hook_visual_reuse"]] == ["I01", "E05", "T02"]
end = [shot_by_id[x] for x in b["end_visual_reuse"]["shot_ids"]]
assert len(end) == 3 and all(s["narration_refs"][0]["paragraph_id"] == "N03" for s in end)
assert len({s["prompt"] for s in end}) == len({s["image_asset_key"] for s in end}) == 1
assert len({s["camera"] for s in end}) == 3
assert [ch["key"] for ch in b["chapters"]] == ["hook", "origin", "idea", "engine", "turn", "now"]
assert [sid for ch in b["chapters"] for sid in ch["shot_ids"]] == list(shot_by_id)
assert sum(ch["units"] for ch in b["chapters"]) == 2729
assert b["bookends"][0]["duration_seconds"] == 5 and b["bookends"][1]["duration_seconds"] == 21
assert b["bookends"][0]["after_shot"] == "B18-S007"
assert b["bookends"][1]["after_shot"] == "B18-S103"
assert m["body_estimate_seconds"] == {"at_250_cpm": 654.96, "at_230_cpm": 711.91}
assert m["total_estimate_seconds"] == {"at_250_cpm": 680.96, "at_230_cpm": 737.91}
assert "ウロコ" in shot_by_id["B18-S032"]["post_source_overlay"]["scope"]
assert "コンベヤ附調理食台" in shot_by_id["B18-S049"]["card"]["scope"]
assert shot_by_id["B18-S068"]["card"]["source"] == "發明協會（S2）"
assert "實績" in shot_by_id["B18-S098"]["card"]["scope"] and "預估" in shot_by_id["B18-S098"]["card"]["scope"]
source_map = load("source-map.json")
assert all(cid in source_map["claims"] for s in b["shots"] for cid in s["source_cids"])
assert load("shot-reading-report.json")["summary"] == {"shots": 87, "traps": 0, "by_kind": {}}
for f in base.iterdir():
    if f.is_file() and f.suffix in [".md", ".json"]:
        raw = f.read_text(encoding="utf-8")
        assert not re.search(r"[A-Z]:[\\/]Users[\\/]|AppData[\\/]Local[\\/]Temp", raw, re.I), f.name
report = {
    "status": "LOCAL_STRUCTURAL_CHECKS_ONLY_NOT_EDITORIAL_REVIEW",
    "input": "storyboard.json",
    "storyboard_sha256": sha((base / "storyboard.json").read_bytes()),
    "fullscript_sha256": b["original_fullscript_sha256"],
    "original_paragraphs": 24,
    "reconstructed_units": 2729,
    "shots": 103,
    "illustrations": 87,
    "cards": 16,
    "unique_planned_images": 82,
    "hook_pairs_exact_prompt_camera_and_asset": 3,
    "end_same_image_placements": 3,
    "source_pins_match": True,
    "original_words_and_order_reconstructed": True,
    "all_source_cids_resolve": True,
    "portable_artifact_paths": True,
    "formal_chapter_runtime_media_owner_reviews": "pending",
}
(base / "structural-checks.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
