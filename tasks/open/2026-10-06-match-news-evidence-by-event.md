---
id: 2026-10-06-match-news-evidence-by-event
title: Match news evidence by event and attach it to drafting candidates
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-06T01:19:01Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
  - docs/news-automation.md
---

# Match news evidence by event and attach it to drafting candidates

## Why

The news scanner attaches a page to a story only in one case (landed in #1041,
`_waiting_for` in `apps/api/app/news_automation/scanner.py`): the story is in
`needs_evidence` and the page, from an enabled `evidence` source, links to the story's own
URL (compared without query, fragment or trailing slash). Two cases from the original ticket
`2026-09-24-attach-a-second-evidence-source-to` are not covered:

1. **Same event, no link.** A press report about the same announcement that does not link to
   it (or links to a different URL of the company) files its own candidate instead of
   corroborating the story. Matching "same event" needs a model call per page, through Jev or
   the news models, and Jev is not trusted to act on CJK text (`jev_cjk_autopilot_enabled`
   ships false in `apps/api/app/config.py`).
2. **A story already drafting.** Once a story has left `needs_evidence`, a later report linking
   to it files its own candidate (pinned by
   `test_a_report_linking_to_a_waiting_story_becomes_its_evidence`). For the new page to count,
   the story's checks must run again on the changed evidence (a new `evidence_hash`, computed
   in `pipeline.py` when the job runs), which for a drafted or reviewed story is a paid
   re-verification.

Since the owner's decisions of 2026-09-25 (one evidence page is enough to draft; a first-party
page publishes on its own, `evidence_present` and `auto_evidence_ok` in
`apps/api/app/news_automation/policy.py`) and 2026-09-28 (a page from a trusted newsroom
publishes on its own), a second site only matters for a story whose single page is neither
first-party nor trusted. Both cases cost money per page or per story, so whether they are worth
it is the owner's call.

## Definition of done

- [ ] The owner has decided whether either case is wanted, recorded in Notes with its date
      (the measurement below helps).
- [ ] If event matching is wanted: a page from an enabled `evidence` source that covers the same
      event as an open candidate, without linking to it, is attached to that candidate instead
      of filing its own, with the model call bounded per scan and a CJK page never attached on
      the model's word alone while `jev_cjk_autopilot_enabled` is false.
- [ ] If attaching to drafting stories is wanted: a later page linking to a story in a chosen
      set of statuses is attached, and the re-verification it triggers is counted against the
      news budget.
- [ ] If neither is wanted: this ticket is closed with that decision in Notes.

## Steps

- [ ] Measure on the production database (read-only, with the owner's consent) how many
      candidates of the last 30 days are `duplicate` stories that a link or event match would
      have joined, and how many stories ended single-source without a first-party or trusted
      page.
- [ ] Ask the owner, with those numbers and the per-page cost of a model match.
- [ ] Build what was chosen in `scanner.py`, with scanner tests next to
      `test_a_report_linking_to_a_waiting_story_becomes_its_evidence`.
- [ ] Update the attach paragraph in `docs/news-automation.md`.

## How to verify

```bash
cd apps/api && PYTHONUTF8=1 uv run pytest tests/test_news_automation.py -q -k "waiting_story or attach"
```

## Notes

- Split from 2026-09-24-attach-a-second-evidence-source-to (claude-opus-5-5-news-admin-followups,
  2026-10-06). That ticket closed with the exact-link attach (#1041) plus regression tests for
  its idempotency, the lead-only gate and the host allow-list; its first-party half is
  superseded by the 2026-09-25 and 2026-09-28 owner decisions.
- The measurement step reads the production database, so it needs the owner's consent and a
  read-only query run by whoever holds host access; it is not a reason to skip the decision.
