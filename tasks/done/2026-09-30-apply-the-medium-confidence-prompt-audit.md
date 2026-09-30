---
id: 2026-09-30-apply-the-medium-confidence-prompt-audit
title: Apply the medium-confidence prompt audit findings
status: done
priority: P2
area: meta
owner: claude-opus-5-5
claimed_at: 2026-09-30T09:29:31Z
created_at: 2026-09-30T09:28:28Z
completed_at: 2026-09-30T09:42:00Z
branch: claude/prompt-audit-medium
depends_on: []
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/story.mjs
  - apps/api/app/ai/trip_parser.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/video_media/judge.py
  - apps/api/tests/test_ai_trip_parser_llm.py
  - apps/api/tests/test_hotspot_ai_search.py
  - apps/api/tests/test_ai_itinerary.py
  - apps/api/tests/test_video_media_judge.py
  - .agents/skills/content-pipeline/references
  - .agents/skills/youtube-video/references/prompts
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/drama.md
  - .agents/skills/task-board/SKILL.md
  - .claude/skills/task-board/SKILL.md
  - .agents/skills/task-board/references/merge.md
  - .agents/skills/article-localization/references
  - .agents/skills/catalog-import/references/merchants.md
  - .agents/skills/deploy/references/pitfalls.md
  - tasks/README.md
---

# Apply the medium-confidence prompt audit findings

## Why

The 2026-09-30 `/claude-api prompt-audit` (skills and instruction files audited against Claude
Opus 5.5; each Anthropic call site against its pinned model; OpenAI, MiniMax, Gemini and Jev
call sites only for model-agnostic patterns) found nineteen medium-confidence findings. They
fall into four groups:

- prompt text the target models now follow too literally: a zh-TW-only rule inherited by
  translation stages, numeric report caps, a prohibition list restating a positive rule;
- request shapes sized for older behaviour: a 4,000-token trip-parser cap with no effort while
  current Claude models think by default, and 8,000-token story caps on an always-thinking
  listener;
- work the code already does, repeated in prose: schema and JSON-shape prose sent to providers
  whose strict schema output already enforces it, a source list the pipeline has locked, rubric
  keys a response schema can require;
- skill passages written as history rather than as the current rule.

The high-confidence set is #1031. This ticket is the medium set. PR #1032, a parallel audit by
another session, already covers three medium items (content-pipeline SKILL.md routing,
catchtable dates, the dated listener-rewrite example), so they are left to it.

## Definition of done

- [x] Translation and caption-review stages no longer receive "use the zh-TW interface names".
- [x] The Anthropic trip parser sends `effort: low` (not for Haiku 4.5, which rejects it) and no
  longer repeats the schema that `output_config.format` carries.
- [x] OpenAI (strict) and Anthropic guide search, and every planner but MiniMax, no longer get
  the schema or JSON shape in their prompt; MiniMax still does.
- [x] The news locale calls put the locale after the content every locale shares, and the
  locale review no longer asks the model to check the pipeline-locked source list.
- [x] The media judge's response schema requires every rubric key; the JSON prose is gone.
- [x] The story listener and fix stages get 16,000 output tokens.
- [x] Report caps, the prohibition list, the merge-row exception, the chromium note, the pinned
  owner name, the news-batch routing, dated wording and the `--reason` flag are fixed in the
  skills and `tasks/README.md`.

## Steps

- [x] M1 `prompts.mjs` COMMON: the interface-name rule applies to zh-TW text.
- [x] M2 + M3 `trip_parser.py`: effort, schema left to `output_config.format`.
- [x] M3 `ai_search.py`: `_with_schema` for MiniMax only (Responses), never for Anthropic.
- [x] M4 `itinerary.py`: `MINIMAX_SHAPE` appended for MiniMax only.
- [x] M6 + M7 `news_automation/ai.py`: key order; locale-review wording.
- [x] M8 `video_media/judge.py`: per-request schema with `required` rubric keys.
- [x] M11 `story.mjs`: 16,000-token listener and fix stages.
- [x] M12 report caps in ten prompt templates.
- [x] M13 `verifier-travel.md` step 4.
- [x] M14 `task-board/SKILL.md` (both copies) row 6.
- [x] M15 `merge.md` chromium note.
- [x] M16 `tasks/README.md` owner name.
- [x] M17 `news-batch.md` routing (the SKILL.md half is in #1032).
- [x] M18 dated wording: publish-runbook, content-pipeline pitfalls, article-localization pitfalls,
  merchants, deploy pitfalls, script-writing, drama, caption-translate.
- [x] M19 `pipeline.md` `migrate-prepared --reason`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app
cd apps/api && uv run pytest tests/test_ai_itinerary.py tests/test_hotspot_ai_search.py tests/test_ai_trip_parser_llm.py tests/test_video_media_judge.py tests/test_news_pipeline.py -q
node --test tools/video/automation/*.test.mjs && node --test tools/skills.test.mjs
```

After deploying, watch the guide-search and news repair-retry rate (`repair_instruction` second
attempts) for a day: if OpenAI or Anthropic validation failures rise without the schema in the
prompt, restore `_with_schema` for that provider.

## Notes

- Claimed with `--force`: `2026-09-28-sothatswhy-shorts-from-episode` (prompts.mjs) and
  `2026-09-27-news-evidence-excerpts-stop-at-8` (news_automation/ai.py) held overlapping scope,
  but both claims were more than 24 hours old, their branches are gone from origin, and their
  PRs are merged (#904, #950 and #962 for the first, #966 for the second).
- Not done here and filed instead: OpenCC for simplified names (M5,
  `2026-09-30-convert-simplified-hotspot-names-with-opencc`), compilation thumbnails (M9, waits
  on #1030, which rewrites the same prompt block;
  `2026-09-30-let-the-compilation-planner-judge-thumbnails`), pause beats in code (M10,
  `2026-09-30-set-register-pause-beats-in-code`), and the two dated lines in `automated.md`,
  whose scope an active ticket holds (`2026-09-30-drop-the-dated-wording-left-in`).
