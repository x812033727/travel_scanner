---
id: 2026-11-10-integrate-news-reader-value
title: Integrate reviewed news reader value instructions after scope handoff
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-10T12:21:28Z
completed_at:
branch:
depends_on:
  - 2026-10-29-news-automation-drafts-notable-new-ai
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_ai.py
  - docs/news-automation.md
---

# Integrate reviewed news reader value instructions after scope handoff

## Why

Reader-facing news examples and an editorial standard are prepared in docs/news-editorial-upgrade-20261110. Existing writer/editor instructions can produce release-led headlines and repetitive structure; useful eligibility, cost and task context should appear earlier without weakening evidence or publication checks.

## Definition of done

- [ ] Resolve active ownership and PR #1857 overlap before claiming any writer paths.
- [ ] Integrate the reviewed reader-value instructions into writer/editor, preserving evidence, schema and publication gates.
- [ ] Validate relevant code paths and independently compare supported reader utility and hallucination boundaries; document model-run cost authorization if needed.

## Steps

- [ ] Read docs/news-editorial-upgrade-20261110/INTEGRATION.md and current owner changes.
- [ ] Implement a scoped candidate and tests after ownership handoff.
- [ ] Record review, CI and remaining deployment/settings/publication steps explicitly.

## How to verify

Run focused news AI tests, required API checks and independent editorial comparisons. Prompt-string tests alone are not evidence of better article quality. Use actual sources for availability/price facts and preserve distinct official, reported and untested claims.

## Notes

- Filed without claiming: active task 2026-10-29-news-automation-drafts-notable-new-ai and open PR #1857 include ai.py. Do not release another owner's ticket automatically.
- No code, paid model, production setting, deployment or publication was changed by the documentation work.
- Same-site official evidence expansion needs scanner ownership and a separate bounded design; it is outside this ticket's implementation scope. Existing cross-category duplicate task remains the home for retrieval-window improvements.
