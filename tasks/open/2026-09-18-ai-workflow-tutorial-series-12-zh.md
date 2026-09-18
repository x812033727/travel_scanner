---
id: 2026-09-18-ai-workflow-tutorial-series-12-zh
title: AI workflow tutorial series: 12 zh-TW articles and a series hub on chaining different models
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-18T08:47:59Z
created_at: 2026-09-18T08:47:33Z
completed_at:
branch: claude/ai-workflow-series-workspace
depends_on: []
scope:
  - apps/api/tests/test_guide_series.py
---

# AI workflow tutorial series: 12 zh-TW articles and a series hub on chaining different models

## Why

The owner asked (2026-09-18) for tutorials about AI workflows, including the more technical
side of chaining different models. Plan mode settled on a 12-article zh-TW series with a
series hub, registered as the `ai-workflow` series under the `ai-coding` topic (hub
`display_order` 399, articles 400-411), deepening what the site already has (n8n/Zapier,
OpenRouter, agent frameworks, MCP lists) rather than repeating it. The workspace, brief,
checker, asset builder and model-id whitelist are in `docs/ai-workflow-series/`; the writing
itself waits for the weekly usage window to reset (it needs 12 writers and 12 fact-checkers).

## Definition of done

- [ ] 12 packs + the hub in zh-TW, each passing `docs/ai-workflow-series/check_article.py <slug> --assets`
      (code samples compile, model ids in `models-seen.json`, sources 3-8 official pages).
- [ ] One independent fact-check per article (second round only when >10 edits), reports in
      `docs/ai-workflow-series/factcheck/`.
- [ ] Series registered: `series_registry.json` + `series_data/ai-workflow.json` + `test_guide_series.py`
      (registry list and a catalogue test); the hub page lists the articles through `SeriesHub`.
- [ ] `pack_cli lint --kind life` 0 errors, `pytest tests/test_guide_series.py tests/test_guides_content_pack.py
      tests/test_guides_pack_ingest.py` green, `npm run check:tasks` green.
- [ ] Owner's explicit choice to publish; deploy first (registry into the API), then
      `guides-import --slug` hub + 12 in one run; `/zh-TW/life/ai-workflow-tutorials` shows the catalogue.

## Steps

- [x] Workspace: BRIEF, agents/ASSIGNMENTS (angles, must-link articles, source seeds, related), agents/FACTCHECK,
      series.py, check_article.py, build_assets.py, models-seen.json (22 ids read on 2026-09-18).
- [ ] Writers (sonnet) x13 from `agents/ASSIGNMENTS.md`.
- [ ] Fact-checkers (opus) x13.
- [ ] Coordinator read-through, `_DRAWINGS` x13, `build_assets.py`, `related`, relink/autolink.
- [ ] Registry, catalogue, tests; lint; PR.
- [ ] Publish after the owner's explicit choice; verify 13 URLs and the series endpoint.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 ./.venv/Scripts/python.exe ../../docs/ai-workflow-series/check_article.py <slug> --assets
./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life
./.venv/Scripts/python.exe -m pytest tests/test_guide_series.py tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
curl -s 'https://mokaair.com/api/v1/guides/series?locale=zh-TW' | grep -c ai-workflow   # after publishing
```

## Notes

- Overlaps `2026-09-14-life-finance-series-hub` (open, no owner) on `series_data/` and
  `test_guide_series.py`; the files are additive, not blocking.
- Every agent prompt carries the network rule: User-Agent `Mokaair-editorial`, no personal data in any request.
