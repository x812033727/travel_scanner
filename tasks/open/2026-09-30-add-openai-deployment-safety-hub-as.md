---
id: 2026-09-30-add-openai-deployment-safety-hub-as
title: Add OpenAI Deployment Safety Hub as a first-party news source (openai.com article pages refuse the scanner)
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T10:35:07Z
created_at: 2026-09-30T10:34:33Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
---

# Add OpenAI Deployment Safety Hub as a first-party news source (openai.com article pages refuse the scanner)

## Why

Every OpenAI model launch ships with a system card on `deploymentsafety.openai.com`, which
the scanner can read (robots allows all; the GPT-6.1 Sol page extracts to about 39,000
characters and states the launch, the date and the Preparedness ratings), while the
`openai.com/index/*` announcement pages refuse it with 403. Found 2026-09-30 while writing batch 4.9 by hand (`tasks/open/2026-09-30-news-batch-4-9-gpt-6.md`).

## Definition of done

- [ ] `sources.json` lists the Safety Hub index as an `html` evidence source, first-party, AI.
- [ ] `max_entries_per_scan` is 1: the index lists newest first, so the first scan takes only
      the newest system card and older ones are never drafted as news.
- [ ] Loaded on the host with `sources_cli` (dry run, then `--apply`), after the deploy.

## How to verify

Host: `python -m app.news_automation.sources_cli` validates it; `/admin/news` shows the
source `succeeded` after its first scan.

## Notes

- `minimum_title_length` 25 drops the page chrome ("Skip to content", "Deployment Safety
  Hub", "Learn more"); every system-card link text starts with its date and is longer.
- If two system cards appear within one hour, the second is picked up only once it is the
  newest; raise the cap only with a baseline so old cards are not drafted.
