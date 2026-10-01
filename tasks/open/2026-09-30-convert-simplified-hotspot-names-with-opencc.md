---
id: 2026-09-30-convert-simplified-hotspot-names-with-opencc
title: Convert simplified hotspot names with OpenCC instead of a model call
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-30T09:40:05Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/simplified_names.py
  - apps/api/tests/test_simplified_names.py
  - apps/api/app/cli.py
  - apps/api/pyproject.toml
  - apps/api/uv.lock
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

- [ ] `convert_names` converts with OpenCC `t2s` and keeps the `acceptable()` shape check.
- [ ] No model call, prompt or `SimplifiedBatch` remains; the CLI's `--provider` and
  `--max-output-tokens` are removed or ignored with a note.
- [ ] Tests cover converted, unchanged and rejected names without a fake provider.

## Steps

- [ ] Add `opencc-python-reimplemented` to `apps/api/pyproject.toml` and lock it; confirm the
  production image builds (it is pure Python).
- [ ] Rewrite `convert_names` and `tests/test_simplified_names.py`.
- [ ] Update the `cli.py` subcommand flags.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_simplified_names.py -q && uv run mypy app
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4 "LLM executor for a deterministic
plan"). Compare a sample of existing converted names against OpenCC before switching: a name the
model converted differently is either a model error or a variant OpenCC's phrase table handles.
