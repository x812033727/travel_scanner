---
id: 2026-09-30-add-openai-deployment-safety-hub-as
title: Add OpenAI Deployment Safety Hub as a first-party news source (openai.com article pages refuse the scanner)
status: open
priority: P1
area: api
owner:
claimed_at:
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

- [x] `sources.json` lists the Safety Hub index as an `html` evidence source, first-party, AI.
- [x] `max_entries_per_scan` is 1: the index lists newest first, so the first scan takes only
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
- Checked 2026-09-30 from outside the host: `parse_html_listing` on the index with this config
  returns the eight system cards newest first (`/gpt-6-1-sol` first) and none of the chrome;
  `read_article` on `/gpt-6-1-sol` keeps about 39,000 characters of the card. What is left is
  the host step (`sources_cli`, dry run then `--apply`) after this PR is deployed.
- The GPT-6.1 Sol card will be this source's first candidate. If the hand-written
  `ai-news-gpt-61-sol-20260929` is published first, Jev's duplicate check should catch it;
  if not, reject the candidate in `/admin/news`.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus-5-5-news-4-9 (since 2026-09-30T10:35:07Z) was stale and is released so it stops locking its scope. Landed: #1041. Still open: Load on host with sources_cli (dry run, then --apply) after deploy.
