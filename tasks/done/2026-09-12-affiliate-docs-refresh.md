---
id: 2026-09-12-affiliate-docs-refresh
title: Refresh affiliate configuration docs and state the affiliates boundary
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:34Z
created_at: 2026-09-12T05:34:56Z
completed_at: 2026-09-12T12:08:19Z
branch: claude/affiliate-controls-and-guide-cta
depends_on:
  - 2026-09-12-affiliate-click-report
  - 2026-09-12-affiliate-readiness-matrix
scope:
  - docs/affiliate-configuration.md
  - architecture.md
---

# Refresh affiliate configuration docs and state the affiliates boundary

## Why

`docs/affiliate-configuration.md` still said the API sends `shorten: true`, named the old cache
key, counted five template variables and called the disclosure zh-TW-only; most line
references predated the September refactors. `architecture.md` had no affiliates paragraph.

## Definition of done

- [x] The stale claims and line references are corrected.
- [x] A placement and reporting section explains the surfaces, the switch and the report.
- [x] `architecture.md` states the affiliates boundary in one paragraph.
- [x] `docs/travel-services.md` and `docs/travel-guides.md` describe the placement contract and
      the article panel.

## Steps

- [x] Edit the four documents.

## How to verify

Read the sections against `affiliates/service.py`, `affiliates/router.py` and
`travel_services/schemas.py`.

## Notes

Remaining gaps are listed in the document's last section (stay-area CTAs, unmonetised
outbound links, API-14, no commission postback, code-only priority).
