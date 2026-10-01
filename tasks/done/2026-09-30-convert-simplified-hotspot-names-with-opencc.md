---
id: 2026-09-30-convert-simplified-hotspot-names-with-opencc
title: Convert simplified hotspot names with OpenCC instead of a model call
status: done
priority: P3
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-01T03:18:50Z
created_at: 2026-09-30T09:40:05Z
completed_at: 2026-10-01T03:30:29Z
branch: claude/opencc-simplified-names
depends_on: []
scope:
  - apps/api/app/hotspots/simplified_names.py
  - apps/api/tests/test_simplified_names.py
  - apps/api/app/cli.py
  - apps/api/pyproject.toml
  - apps/api/uv.lock
  - .agents/skills/catalog-import/SKILL.md
  - .agents/skills/catalog-import/references/commands.md
  - .agents/skills/catalog-import/references/other-data.md
  - .claude/skills/catalog-import/SKILL.md
---

# Convert simplified hotspot names with OpenCC instead of a model call

## Why

`apps/api/app/hotspots/simplified_names.py` asks a model to convert Traditional Chinese place
names to Simplified "character by character". Its own docstring says the shape check cannot tell
a conversion from a rename without "the very conversion table this check does without". A
character conversion is deterministic: the input fully determines the output, so a model call
adds cost and a chance of renames (the prompt already has to forbid 鄭王廟 → 黎明寺).
`tools/codex-learning/build.py` already uses OpenCC `t2s` for the same job.

## Definition of done

- [x] `convert_names` converts with OpenCC `t2s` and keeps the `acceptable()` shape check.
- [x] No model call, prompt or `SimplifiedBatch` remains; the CLI's `--provider` and
  `--max-output-tokens` are removed or ignored with a note.
- [x] Tests cover converted, unchanged and rejected names without a fake provider.

## Steps

- [x] Add `opencc-python-reimplemented` to `apps/api/pyproject.toml` and lock it; confirm the
  production image builds (it is pure Python).
- [x] Rewrite `convert_names` and `tests/test_simplified_names.py`.
- [x] Update the `cli.py` subcommand flags.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_simplified_names.py -q && uv run mypy app
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4 "LLM executor for a deterministic
plan"). Compare a sample of existing converted names against OpenCC before switching: a name the
model converted differently is either a model error or a variant OpenCC's phrase table handles.

2026-10-01 (claude-opus-5-5): claimed with `--force`; the only overlap was
`2026-09-14-redis-py-8-migration` on `apps/api/pyproject.toml` and `uv.lock`, in review and
claimed 2026-09-19 (stale). Scope widened to the catalog-import skill files that documented
`--provider`/`--max-output-tokens` and the "host only, AI key" workflow.

Comparison before switching (OpenCC `t2s`, opencc-python-reimplemented 0.1.7) over all 928
distinct Traditional names: the 563 rows of the five bootstrap files (374 with a stored zh-CN
label) plus the 392 area names (280 in `SIMPLIFIED_AREA_NAMES`). 922 agree with what the model
stored (or with "unchanged"); 鄭王廟 → 郑王庙. Six differ, and in all six the model was better:

| Traditional (as seeded) | model stored | OpenCC t2s |
| --- | --- | --- |
| 楽水園 | 乐水园 | 楽水园 |
| 桜井二見ヶ浦 | 樱井二见ヶ浦 | 桜井二见ヶ浦 |
| 円頓寺商店街 | 圆顿寺商店街 | 円顿寺商店街 |
| 有楽苑 | 有乐苑 | 有楽苑 (unchanged, so the label would be dropped) |
| 天神／薬院 (area) | 天神／药院 | 天神／薬院 |
| 二鯤鯓砲臺 | 二鲲鯓炮台 | 二鲲鯓砲台 (砲 is a valid variant) |

Five are Japanese shinjitai (楽 桜 円 薬) in the *Traditional* seed name itself; OpenCC has no
mapping for Japanese forms (this package ships no `jp2t` config, and `tw2s` gives the same
result), so they pass through and the zh-CN label mixes Japanese characters into Simplified.
The owner chose a pre-map over changing seed data: `SHINJITAI_TO_TRADITIONAL` in
`simplified_names.py` maps 24 Japanese forms to Traditional before `t2s` (楽 桜 円 薬 沢 関 駅
広 県 竜 恵 栄 売 両 乗 鉄 塩 蔵 稲 歩 渓 滝 豊 戸). Each was checked: plain `t2s` leaves it
untouched and `t2s` of the Traditional form gives the standard Simplified character. Left out:
国 将 横 (`t2s` already handles them) and 浜, which is also a Chinese character (沙家浜). No
kana are mapped.

Re-run with the pre-map: 927 of 928 match the stored model output. The pre-map changed only
the five Japanese-form names, all now equal to the model's result. The one remaining
difference is 二鯤鯓砲臺 → 二鲲鯓砲台 (model: 炮台); 砲 is a valid variant, accepted. A dry run
of `fill-simplified-names` needs no database or key now.

Production image not built locally: the package is a pure-Python wheel installed from
`uv.lock` like every other dependency.
