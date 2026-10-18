---
id: 2026-10-11-exclude-rotating-source-widgets-from-news
title: Exclude rotating source widgets from news story fingerprints
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-11T09:18:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# Exclude rotating source widgets from news story fingerprints

## Why

Native final publication checks correctly hold candidates whose stored source
hash differs. Two guarded production read-only fetches now show changes outside
the reporting body: Meta Muse message-permission candidate
f72d9420-06d5-4e1f-b765-ff839f52022d changes only its Related News cards, while
Strategy Bitcoin-holdings candidate dc94c749-af79-46a2-8497-b1e18347a2a1 changes
only the appended market ticker/chart/projection figures. Both native body-v1
and content hashes change, so a plain "same story" assertion cannot publish them.
A source-specific, adequately covered story extraction should keep these widgets
outside the story fingerprint while still detecting edits to real article text.

## Definition of done

- [ ] Source-specific fixtures reproduce each current body-hash false change.
- [ ] The native parser and versioned fingerprint cover the complete reporting
      body while excluding only proven adjacent related-news or market widgets.
- [ ] Actual headline, attribution, dates, numbers and paragraph changes still
      invalidate evidence; short/ambiguous extraction conservatively falls back.
- [ ] Old hashes and stored excerpts receive a tested compatible transition;
      no arbitrary prefix matching, regex deletion or relaxed source guards.
- [ ] The unchanged fetch allowlist, public-IP pinning, Host/SNI/TLS, robots,
      response-size, rate and publication review gates are verified.

## Steps

- [ ] Read full old/current extracted stories and native parser configuration.
- [ ] Add realistic positive and negative source fixtures, including actual
      text changes, incomplete DOM, reordered widgets and old body versions.
- [ ] Independently review the extraction boundary and coverage thresholds.
- [ ] Document deployment/backfill behavior; any held candidate uses its own
      audited native refresh and ordinary checks, with existing assets/history.

## How to verify

Run focused native extraction/fingerprint tests, including a real story edit that
must fail source-current validation, followed by relevant news regressions.
A fixture pass is not production proof. After an approved deployment, perform
bounded native read-only fetches before a separately audited single-candidate
refresh; verify DB/audit/job/revision/public state without resetting caps.

## Notes

Created from actual 2026-10-11 native SafeNewsFetcher readbacks, not speculation.
Evidence root: <home>/.codex/news-review/20261010-6f71.
Meta current-source receipt b7520af198838600dbd941d2c60e0707f541306f54caae77a0597b38c79b3742
and exact diff f1b9944bf483b18d0b1c9558b48f84b3ff2c5a93e8f607237669dbeeee621e1e
prove the complete5861-character core before Related News is byte-identical;
two cards reorder and one related card date changes from September29 to October8.
Strategy native source receipt
6d07e9e87bd29703072c9d68e0786d0fc139cc3c414f217dec7e62cf8a02b319
returns200 with stored4867/current4766 characters; the only diff starts at its
Bitcoin ticker's USD price and continues through chart/projection widgets.
Root has not changed either native Evidence or any parser in this task.
The existing audited refresh route is an operational recovery, not a fix to
future dynamic-widget false holds. This unclaimed task needs fresh collision
checks before implementation; the shared API test scope has active owners.
