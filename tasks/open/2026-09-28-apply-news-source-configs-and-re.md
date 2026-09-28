---
id: 2026-09-28-apply-news-source-configs-and-re
title: Apply news source configs and re-check the three held articles
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-28T12:58:38Z
completed_at:
branch:
depends_on:
  - 2026-09-27-news-evidence-hashes-page-chrome-so
scope:
  - apps/api/app/news_automation/sources.json
---

# Apply news source configs and re-check the three held articles

## Why

`2026-09-27-news-evidence-hashes-page-chrome-so` added a story-only evidence hash
(`news_evidence.body_hash`, migration `0112_news_evidence_body_hash`) and new `config` for
three sources in `apps/api/app/news_automation/sources.json`: TechCrunch AI (story region
`entry-content`), The Verge AI (rails excluded) and CoinDesk (story region `document-body`,
price chips excluded). The code only helps once it is deployed and the configs are in the
production database; `sources.json` is not read at runtime, `sources_cli` loads it.

Evidence stored before the deploy has no body hash, so the publish revalidation still compares
`content_hash` for it, and the config change alters what those pages extract to. Waiting
candidates from these three sources stay held until an editor re-checks them once.

## Definition of done

- [x] Production `news_sources` rows for TechCrunch AI, The Verge AI and CoinDesk carry the
      configs from `sources.json`.
- [ ] `ai-news-openai-agent-image-leak-20260925`, `ai-news-sony-umg-suno-lawsuit-20260925` and
      `crypto-news-kalshi-sixth-circuit-ruling-20260925`, re-checked once, reach
      `news_ready_to_publish` or publish, or fail for a reason other than
      `source_content_changed`.

## Steps

- [x] Deploy the PR (skill `deploy`); check `alembic current` is `0112_news_evidence_body_hash`.
- [x] Write a JSON file holding only the three changed sources (same shape as `sources.json`),
      then dry-run and apply it in the api container:
      `python -m app.news_automation.sources_cli --file <that json>` and again with
      `--apply --actor-email <owner's admin email>` (skill `prod-host-ops`).
- [ ] Re-check each article once with `/admin/news` "重新查核", then confirm the new evidence
      rows have `body_hash` set (`body-v1:` prefix).
- [ ] Watch the next hourly scans: no `source_content_changed` holds for these three hosts.

## How to verify

`news_evidence.body_hash` is non-null on the refreshed rows; the three candidates' status and
`error_code` in `/admin/news`.

## Notes

- If a source's page layout changes, its body hash will read as None (too little story) and
  revalidation falls back to `content_hash`, i.e. the old behaviour, not a silent pass.
- 2026-09-28 15:00Z: `0d30e604` was deployed, and `alembic current` is
  `0112_news_evidence_body_hash`. `sources_cli --file` held only the three sources; the dry
  run showed three valid updates, and they were applied. Three evidence rows written in the
  next 15 minutes all had `body_hash` set. The re-check of the three held articles waits
  for the owner, because it costs model calls.
