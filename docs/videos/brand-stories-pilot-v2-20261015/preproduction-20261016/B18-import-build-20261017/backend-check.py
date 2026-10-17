"""Diagnose the isolated two-row candidate without writing an import file.

This mirrors build.mjs's review-only fields and caveat concatenation. It is a
diagnostic for a blocked build, not a replacement for the exact compiler.
Run from the repository root with PYTHONPATH=apps/api.
"""

from __future__ import annotations

import json
from pathlib import Path

from app.video_automation.stories import check_story_file


HERE = Path(__file__).resolve().parent / "sandbox/docs/videos/brand-stories-pilot-v2-20261015"
ACTIVE = Path(__file__).resolve().parents[2]


def read(relative: str) -> dict:
    return json.loads((HERE / relative).read_text(encoding="utf-8"))


series = read("series.json")
rows: list[dict] = []
for episode_id in ("A01", "B18"):
    row = read(f"episodes/{episode_id}.json")
    review = read(f"episodes/reviews/{episode_id}.json")
    reviewer_only = set(review.get("reviewer_only") or [])
    row["must_verify"] = [
        {**{key: value for key, value in claim.items() if key != "reviewer_only"},
         **({"reviewer_only": True} if index in reviewer_only else {})}
        for index, claim in enumerate(row["must_verify"])
    ]
    caveats = [row.get("caveats", "").strip(), review.get("notes", "").strip()]
    row["caveats"] = "\n\n".join(dict.fromkeys(part for part in caveats if part))
    rows.append(row)

document = {"schema_version": 1, "series": series, "stories": rows}
check = check_story_file(document, series["slug"])
active_document = json.loads((ACTIVE / "stories.json").read_text(encoding="utf-8"))
active_rows = {row["id"]: row for row in active_document["stories"]}
changed_b18_keys = sorted(
    key
    for key in set(rows[1]) | set(active_rows["B18"])
    if rows[1].get(key) != active_rows["B18"].get(key)
)
print(
    json.dumps(
        {
            "kind": "in-memory-diagnostic-not-compiled-import-file",
            "story_ids": [row["id"] for row in rows],
            "caveat_lengths": {row["id"]: len(row["caveats"]) for row in rows},
            "series_equal_to_active_compiled": series == active_document["series"],
            "A01_equal_to_active_compiled": rows[0] == active_rows["A01"],
            "B18_changed_compiled_keys": changed_b18_keys,
            "problems": check.problems,
            "refused": check.refused,
            "ignored": check.ignored,
        },
        ensure_ascii=False,
        indent=2,
    )
)
