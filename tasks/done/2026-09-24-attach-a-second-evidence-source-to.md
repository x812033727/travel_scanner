---
id: 2026-09-24-attach-a-second-evidence-source-to
title: Attach a second evidence source to first-party news candidates
status: done
priority: P2
area: api
owner: claude-opus-5-5-news-admin-followups
claimed_at: 2026-10-06T01:15:06Z
created_at: 2026-09-24T00:27:44Z
completed_at: 2026-10-06T01:21:34Z
branch: claude/news-admin-followups
depends_on: []
scope:
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# Attach a second evidence source to first-party news candidates

## Why

The news pipeline publishes nothing on fewer than two `evidence` pages, one of them
first-party (`news_evidence_insufficient` → manual review). The scanner finds the second
page only by following links inside the article it just read. That works when a press
article links to the official announcement. It almost never works the other way: an
official blog post from a first-party feed rarely links to independent coverage, so
every candidate discovered from a first-party feed arrives with one evidence page and
stops in manual review. Retrying does not help, because evidence is never refetched or
extended after the scan.

## Definition of done

- [ ] When a later scan reads an evidence page (from any enabled evidence source) that
      links to, or is the same event as, an open candidate's first-party page, that page
      is attached to the candidate as evidence and the candidate is re-queued.
- [x] Attaching is idempotent, respects the existing host allow-list and SSRF rules, and
      never attaches `lead_only` pages as evidence.

## Steps

- [x] Decide the matching rule (exact outbound link to the candidate's canonical URL is
      the safe first step; semantic matching through Jev is a second step).
- [x] Attach, update `evidence_hash`, re-queue candidates waiting on
      `news_evidence_insufficient`, with scanner tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- Found while hardening the news automation (task
  2026-09-24-harden-hourly-news-automation-before-first). Measure it in the shadow period
  first: the share of candidates ending in `news_evidence_insufficient` tells how urgent
  this is.
- 2026-09-30 (claude-opus-5-5-news-4-9): done for the case that now matters most. Since the
  owner decision of 2026-09-25 one evidence page is enough to draft and a first-party page
  is enough to publish, so a first-party candidate no longer waits on a second site. What
  waits is a story with *no* usable evidence: a refused page kept as a feed-summary lead
  (`news_page_refused`, same day) or a candidate with only lead-only pages. `scan_source`
  now attaches a readable page from an `evidence` source that links to such a candidate
  (exact link, ignoring query, fragment and trailing slash), requeues the candidate and
  closes the report as `duplicate` / `news_attached_as_evidence`, with
  `test_a_report_linking_to_a_waiting_story_becomes_its_evidence`.
- Not done: attaching a second site to a candidate that already drafts (only useful for
  automatic publication without a first-party page), and matching by event rather than
  by link (Jev). Left open for that; release it if nobody wants them.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus-5-5-news-4-9 (since 2026-09-30T11:25:43Z) was stale and is released so it stops locking its scope. Landed: #1041. Still open: Attach a later evidence page that links to, or covers the same event as, an open first-party candidate, then r; Idempotent attach that follows the allow-list and SSRF rules and never attaches lead_only pages; Attach, update evidence_hash and requeue, with scanner tests.
- 2026-10-06 (claude-opus-5-5-news-admin-followups): closed. What #1041 built is now pinned
  by tests, and what is left moved to `2026-10-06-match-news-evidence-by-event`.
  - Second box: `test_a_report_linking_to_a_waiting_story_becomes_its_evidence` now also scans
    the press feed a second time (nothing attached again, no new candidate, nothing queued: the
    report is already seen), scans a fourth source whose report links to the story after it
    left `needs_evidence` (not attached; it files its own candidate and the story is not queued
    again), and records every request: each article and linked page is fetched with the enabled
    sources' hosts as `allowed_hosts`, and a link to a site that is no source is never
    requested. The SSRF checks are the fetcher's own (`SafeNewsFetcher`, covered by
    `test_ssrf_url_validation_and_policy_state_machine_fail_closed` and the safe-fetcher
    tests); the attach adds no fetch of its own. The `lead_only` gate was already tested
    (the gossip source) and is `detail_source.role == "evidence"` in `scan_source`.
  - Second step: the attach and re-queue are in `scan_source` (#1041); `evidence_hash` is
    recomputed from all of the story's pages when the re-queued job runs (`pipeline.py`, before
    `evidence_present`), so the scanner does not set it. "Waiting on
    `news_evidence_insufficient`" is any candidate in `needs_evidence`, which covers that code
    and `news_page_refused`.
  - First box, left unticked: its link half is done for stories in `needs_evidence`; its
    first-party half is superseded. Since the owner's decisions of 2026-09-25 (one evidence
    page drafts, a first-party page publishes on its own: `evidence_present` and
    `auto_evidence_ok` in `policy.py`) and 2026-09-28 (so does a trusted newsroom's page), a
    first-party candidate no longer waits for a second site. Matching by event (Jev, a paid
    call per page, and not trusted to act on CJK while `jev_cjk_autopilot_enabled` is false)
    and attaching to stories already drafting (a paid re-verification each) both need the
    owner, so they are in `2026-10-06-match-news-evidence-by-event`.
  - Scope narrowed to the two files this change touches; `scanner.py` and
    `admin-news-messages` were the scope of the #1041 part.
