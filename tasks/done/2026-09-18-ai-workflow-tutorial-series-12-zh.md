---
id: 2026-09-18-ai-workflow-tutorial-series-12-zh
title: AI workflow tutorial series: 12 zh-TW articles and a series hub on chaining different models
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-18T08:47:59Z
created_at: 2026-09-18T08:47:33Z
completed_at: 2026-09-19T03:39:12Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - docs/ai-workflow-series
  - apps/api/app/guides/content/ai-workflow-tutorials.json
  - apps/api/app/guides/content/ai-workflow-basics.json
  - apps/api/app/guides/content/ai-workflow-split-tasks-across-models.json
  - apps/api/app/guides/content/ai-workflow-cost-quality-latency.json
  - apps/api/app/guides/content/ai-workflow-unified-api-layer.json
  - apps/api/app/guides/content/ai-workflow-model-routing-cascade.json
  - apps/api/app/guides/content/ai-workflow-structured-handoff.json
  - apps/api/app/guides/content/ai-workflow-cross-review-judge.json
  - apps/api/app/guides/content/ai-workflow-coding-agents-division.json
  - apps/api/app/guides/content/ai-workflow-mcp-shared-tools.json
  - apps/api/app/guides/content/ai-workflow-local-and-cloud-mix.json
  - apps/api/app/guides/content/ai-workflow-tracing-evals.json
  - apps/api/app/guides/content/ai-workflow-failures-and-guardrails.json
  - apps/web/public/guides/ai-workflow-tutorials
  - apps/web/public/guides/ai-workflow-basics
  - apps/web/public/guides/ai-workflow-split-tasks-across-models
  - apps/web/public/guides/ai-workflow-cost-quality-latency
  - apps/web/public/guides/ai-workflow-unified-api-layer
  - apps/web/public/guides/ai-workflow-model-routing-cascade
  - apps/web/public/guides/ai-workflow-structured-handoff
  - apps/web/public/guides/ai-workflow-cross-review-judge
  - apps/web/public/guides/ai-workflow-coding-agents-division
  - apps/web/public/guides/ai-workflow-mcp-shared-tools
  - apps/web/public/guides/ai-workflow-local-and-cloud-mix
  - apps/web/public/guides/ai-workflow-tracing-evals
  - apps/web/public/guides/ai-workflow-failures-and-guardrails
  - apps/api/app/guides/series_registry.json
  - apps/api/app/guides/series_data/ai-workflow.json
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

- [x] 12 packs + the hub in zh-TW, each passing `docs/ai-workflow-series/check_article.py <slug> --assets`
      (code samples compile, model ids in `models-seen.json`, sources 3-8 official pages).
- [x] One independent fact-check per article (second round only when >10 edits), reports in
      `docs/ai-workflow-series/factcheck/` (13 reports; 10 carry a second round).
- [x] Series registered: `series_registry.json` + `series_data/ai-workflow.json` + `test_guide_series.py`
      (registry list and a catalogue test); the hub page lists the articles through `SeriesHub`.
- [x] `pack_cli lint --kind life` 0 errors, `pytest tests/test_guide_series.py tests/test_guides_content_pack.py
      tests/test_guides_pack_ingest.py` green, `npm run check:tasks` green.
- [x] Owner's explicit choice to publish; deploy first (registry into the API), then
      `guides-import --slug` hub + 12 in one run; `/zh-TW/life/ai-workflow-tutorials` shows the catalogue.

## Steps

- [x] Workspace: BRIEF, agents/ASSIGNMENTS (angles, must-link articles, source seeds, related), agents/FACTCHECK,
      series.py, check_article.py, build_assets.py, models-seen.json (22 ids read on 2026-09-18).
- [x] Writers (sonnet) x13 from `agents/ASSIGNMENTS.md` (12 in parallel; the hub after the twelve titles were final).
- [x] Fact-checkers (opus) x13, plus a second round on 1, 3, 4, 5, 6, 8, 9, 10, 11, 12 (all `ok`).
- [x] Coordinator read-through, `_DRAWINGS` x13, `build_assets.py`, `related`, relink/autolink (autolink pruned by `prune_autolinks.py`).
- [x] Registry, catalogue (`build_catalogue.py`), tests; lint; PR from `claude/travel-scanner-pr-552-rpq36m`.
- [x] Publish after the owner's explicit choice; verify 13 URLs and the series endpoint.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 ./.venv/Scripts/python.exe ../../docs/ai-workflow-series/check_article.py <slug> --assets   # Linux: ./.venv/bin/python3
./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life
./.venv/Scripts/python.exe -m pytest tests/test_guide_series.py tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
curl -s 'https://mokaair.com/api/travel/guides/series?locale=zh-TW' | grep -c ai-workflow   # after publishing
curl -s 'https://mokaair.com/api/travel/guides/series/ai-workflow?locale=zh-TW'              # 12 entries
```

## Notes

- Done 2026-09-19: PR #553 squash-merged as a69763b5, deploy_20260919_032927 (no migration, health 3/3).
  At the owner's choice ("發布 13 篇") one run of `guides-import --locale zh-TW --slug` x13 `--publish`,
  after a second dry-run matched the one shown to the owner byte for byte: created 13 / published 13 /
  taxonomy_updated 12 / failed null, and a replay dry-run reports all 13 `unchanged`. Public checks:
  13 URLs 200 with their real titles and no robots meta, 13 `hero.jpg` 200, 13 entries in
  `sitemaps/sitemap/life-zh-TW.xml`, the hub page links the 12 articles, and the series list shows
  `ai-workflow` (source `api-series`, topic `ai-coding`, entries 12, hub `ai-workflow-tutorials`).
  Deploy, import and checks run by claude-opus-5.
- The public API lives behind the web BFF at `/api/travel/...`. The `https://mokaair.com/api/v1/guides/series`
  this file and the README first gave answers 404, so both now use the BFF path.
- Every article page embeds 「這篇文章目前看不到」 as the `unavailableTitle` string, published or not;
  grep for it proves nothing, so check the `<title>` and the robots meta instead.

- 2026-09-19: everything but publication is done on `claude/travel-scanner-pr-552-rpq36m`. The full handover
  (what shipped, check results, the environment differences, the nine model ids added, the per-article
  items left for the owner) is the last section of `docs/ai-workflow-series/README.md`.
- Two portability bugs in the workspace were fixed on the way: `build_assets.py` wrote under
  `public/guides/guides/`, and the flow diagram's step numerals tripped `diagram_number_not_in_text`.
- One existing test needed a change: `test_unavailable_targets_leave_no_public_navigation_or_inline_link`
  took `catalogues()[0]` as the Claude Code catalogue; it now selects it by slug.
- Filed `2026-09-19-ollama-getting-started-tool-choice-recheck` for a discrepancy a checker found in an
  older article.
- Overlaps `2026-09-14-life-finance-series-hub` (open, no owner) on `series_data/` and
  `test_guide_series.py`; the files are additive, not blocking.
- Every agent prompt carries the network rule: User-Agent `Mokaair-editorial`, no personal data in any request.
