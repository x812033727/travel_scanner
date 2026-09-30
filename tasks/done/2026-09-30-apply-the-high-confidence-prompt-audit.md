---
id: 2026-09-30-apply-the-high-confidence-prompt-audit
title: Apply the high-confidence prompt audit findings
status: done
priority: P2
area: meta
owner: claude-opus-5-5
claimed_at: 2026-09-30T06:27:29Z
created_at: 2026-09-30T06:27:10Z
completed_at: 2026-09-30T06:36:31Z
branch: claude/prompt-audit-high
depends_on: []
scope:
  - apps/api/app/ai/structured_output.py
  - apps/api/tests/test_structured_output.py
  - apps/api/app/ai/catalog.py
  - .agents/skills/prod-host-ops/references/ai-settings.md
  - .agents/skills/prod-host-ops/references/news-ops.md
  - .agents/skills/dev-and-ci/references/checks.md
  - .agents/skills/task-board/references/merge.md
  - .agents/skills/backend-conventions/SKILL.md
  - .claude/skills/backend-conventions/SKILL.md
  - .agents/skills/web-i18n-e2e/references/e2e-local.md
  - .agents/skills/content-pipeline/references/travel-batch.md
  - .agents/skills/catalog-import/SKILL.md
  - .claude/skills/catalog-import/SKILL.md
  - .agents/skills/catalog-import/references/commands.md
  - .agents/skills/article-localization/SKILL.md
  - .claude/skills/article-localization/SKILL.md
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
---

# Apply the high-confidence prompt audit findings

## Why

A `/claude-api prompt-audit` run on 2026-09-30 (target Claude Opus 5.5 for skills and
instruction files, the pinned model for each Anthropic call site) found twelve
high-confidence findings: one missing refusal branch in the Anthropic response reader, a
model catalog that disagreed with itself and missed the current Sonnet, and ten skill
passages that the repository itself contradicts (deleted settings, closed tickets, a
"hard limit" that is only a warning, a stale "latest" migration, an incomplete CI spec
list, a subcommand table missing three commands, and two passages that disagree with a
newer file). Current models follow instructions literally, so a stale fact in a skill is
acted on, not skimmed.

## Definition of done

- [x] `anthropic_output_text` raises on `stop_reason: "refusal"` before reading any text,
  naming the category, and a test covers a refusal that carries partial text.
- [x] The catalog lists `claude-sonnet-5-5`, uses the `claude-haiku-4-5` alias, and no longer
  calls two models the most expensive.
- [x] The ten skill passages state the current fact; every edited SKILL.md is mirrored to
  `.claude/skills/`.

## Steps

- [x] H1 refusal branch + test (`structured_output.py`, `test_structured_output.py`).
- [x] H2 catalog entries (`catalog.py`).
- [x] H3 `ai-settings.md`: the usage-limit field is gone; the limit is fixed at 100%.
- [x] H4 `news-ops.md`: `docs/news-automation.md` already documents `--profile news`.
- [x] H5 `checks.md`: the midnight-flake ticket is done; state the fix instead.
- [x] H6 `merge.md`: the flake table pointed at a done ticket and said "rerun"; point to
  `dev-and-ci/references/ci-triage.md`, which holds every row.
- [x] H7 `backend-conventions/SKILL.md`: copy the highest-numbered migration, not 0093.
- [x] H8 `e2e-local.md`: add the three specs `ci.yml` runs.
- [x] H9 `travel-batch.md`: the repo text range is a warning, not a CI gate.
- [x] H10 `catalog-import`: 33 subcommands; add `refresh-holidays`, `video-media-prune`,
  `video-story-import` to `commands.md`.
- [x] H11 `article-localization/SKILL.md`: only SKILL.md is mirrored.
- [x] H12 `youtube-video/SKILL.md`: per-video languages have shipped.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_structured_output.py tests/test_ai_catalog.py -q
npm run test:tools && npm run check:tasks
```

## Notes

- A stored `claude-haiku-4-5-20251001` keeps working: the id still matches
  `MODEL_ID_PATTERN`, the API accepts it, and the admin select shows an id missing from the
  catalog as a custom model.
- The default Anthropic model (`anthropic_model = "claude-sonnet-5"`) is unchanged; moving
  it to Sonnet 5.5 is the owner's call.
- The audit's medium-confidence findings (video translation stages inheriting the zh-TW
  interface rule, trip-parser effort and max_tokens, schema prose sent to schema-enforcing
  providers, cache-hostile locale ordering, numeric report caps, dated wording) were not
  applied here.
