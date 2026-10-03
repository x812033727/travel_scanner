---
id: 2026-10-03-ai-workflow-series-agent-plus-local
title: AI workflow series, agent-plus-local-model group: six zh-TW articles on pairing Claude Code and Codex with local models (GLM, Qwen, DeepSeek)
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1-agent-local
claimed_at: 2026-10-03T16:05:59Z
created_at: 2026-10-03T15:54:29Z
completed_at:
branch: claude/hybrid-model-tutorial-plan-e323dd
depends_on: []
scope:
  - docs/ai-workflow-series
  - apps/api/app/guides/content/ai-workflow-agent-local-two-routes.json
  - apps/api/app/guides/content/ai-workflow-agent-glm-qwen-deepseek.json
  - apps/api/app/guides/content/ai-workflow-agent-local-batch-script.json
  - apps/api/app/guides/content/ai-workflow-agent-local-mcp-tool.json
  - apps/api/app/guides/content/ai-workflow-agent-local-engine.json
  - apps/api/app/guides/content/ai-workflow-agent-local-checklist.json
  - apps/api/app/guides/content/ai-workflow-tutorials.json
  - apps/web/public/guides/ai-workflow-agent-local-two-routes
  - apps/web/public/guides/ai-workflow-agent-glm-qwen-deepseek
  - apps/web/public/guides/ai-workflow-agent-local-batch-script
  - apps/web/public/guides/ai-workflow-agent-local-mcp-tool
  - apps/web/public/guides/ai-workflow-agent-local-engine
  - apps/web/public/guides/ai-workflow-agent-local-checklist
  - apps/web/public/guides/ai-workflow-tutorials
  - apps/api/app/guides/series_data/ai-workflow.json
  - apps/api/tests/test_guide_series.py
---

# AI workflow series, agent-plus-local-model group: six zh-TW articles on pairing Claude Code and Codex with local models (GLM, Qwen, DeepSeek)

## Why

The owner asked (2026-10-03) for a hands-on tutorial on a hybrid workflow: Claude Code or Codex
paired with local AI, what to watch out for and how to do it well. The site already covers local
models (Ollama, LM Studio, hardware, cost) and the twelve-article `ai-workflow` series, but nothing
shows how an agent tool and a local model are wired together: `ai-workflow-local-and-cloud-mix`
is hand-written Python against two APIs, and `ai-workflow-coding-agents-division` is three cloud
CLIs. The owner's answers the same day: a small series is fine "but with more GLM, Qwen and
DeepSeek"; no hands-on testing, official commands only; this round stops at the ticket and the spec.

The spec is `docs/ai-workflow-series/agent-local/README.md`: six zh-TW articles as group E of the
existing series (display_order 412-417), the rules that differ from `BRIEF.md`, one assignment
per article, and the official facts read on 2026-10-03.

## Definition of done

- [ ] Six packs in zh-TW, each passing `docs/ai-workflow-series/check_article.py <slug> --assets`,
      with every command, flag and setting traced to an official page read on the writing day.
- [ ] Each article says once that the site did not run the steps; none reports a speed, a quality
      verdict or sample output as if measured.
- [ ] Every model tag or endpoint is labelled as weights on the reader's machine, an Ollama `:cloud`
      tag, or a vendor endpoint.
- [ ] One independent fact-check per article, reports in `docs/ai-workflow-series/factcheck/`.
- [ ] Series catalogue shows eighteen entries in groups A-E with the new `agent-local` path; the hub
      page text covers the new group without stating a count.
- [ ] `pack_cli lint --kind life` 0 errors, the series and content-pack tests green, `npm run check:tasks` green.
- [ ] Published only after the owner picks it from an options question; six URLs answer 200 and the
      hub lists them.

## Steps

- [x] Check nobody else is on the topic (branches, open PRs, tasks) and read what the site already has.
- [x] Read today's official pages for both wiring routes and for the GLM, Qwen and DeepSeek families.
- [x] Write the group spec with assignments and the fact table.
- [x] Owner reads the spec: six articles, vendor endpoints in (2026-10-04). Testing later was not
      asked for; the articles stay untested.
- [x] Relax the sources bound for the family article, extend `series.py` (`SLUGS`, `INTRO`).
- [ ] Writers x6 (the family article first), fact-checkers x6, second round where more than ten edits.
- [ ] Coordinator: read-through, hub update, `_DRAWINGS`, `build_catalogue.py --related` (group E,
      explicit `GROUP_OF`, `agent-local` path), relink and autolink, the series test.
- [ ] Lint, tests, PR; publish after the owner's explicit choice and verify the public pages.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 ./.venv/Scripts/python.exe ../../docs/ai-workflow-series/check_article.py <slug> --assets   # Linux: ./.venv/bin/python3
./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life
./.venv/Scripts/python.exe -m pytest tests/test_guide_series.py tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
npm run check:tasks
curl -s 'https://mokaair.com/api/travel/guides/series/ai-workflow?locale=zh-TW'   # after publishing: 18 entries
```

## Notes

- 2026-10-03 (claude-fable-5-1-agent-local): spec written and released for the owner to read.
- 2026-10-04: the owner answered "six articles, vendor endpoints in, start writing". Claimed again;
  the checker, `series.py`, the catalogue tables, the six hero drawings and the model whitelist were
  prepared before the writers started.
- `apps/api/tests/test_guide_series.py` is in scope although `2026-10-03-illustrated-slides-round-2-a-family`
  still lists all of `apps/api/tests`: that ticket sits in review after its PR #1172 merged and its branch
  was deleted, so nothing else is changing the file. `check:tasks` reports the overlap as a warning.
- The owner's "more GLM, Qwen, DeepSeek" was read as one extra article on the three families plus
  their tags in every hands-on article. The spec says how to fold it back to five if that was not meant.
- What the pages said on 2026-10-03 that shapes the series: on Ollama the current GLM and DeepSeek
  models (`glm-5.3`, `glm-5.3-flash`, `deepseek-v4.1-flash`, `deepseek-v4-pro`) exist only as
  `:cloud` tags; local tags are `glm-4.7-flash` (19GB up), `deepseek-r1` and the Qwen families.
  Anthropic's gateway page says it does not support routing Claude Code to non-Claude models.
  Ollama's context default is 4k below 24 GiB of VRAM while its Claude Code and Codex pages ask
  for 64k. The quotes and URLs are in the spec's fact table; re-read them on the writing day.
- Every agent prompt carries the network rule: User-Agent `Mokaair-editorial`, no personal data in any request.
