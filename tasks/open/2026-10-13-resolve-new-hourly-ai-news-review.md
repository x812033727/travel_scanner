---
id: 2026-10-13-resolve-new-hourly-ai-news-review
title: Resolve new hourly AI news review and redraft holds from October 11 onward
status: review
priority: P1
area: ops
owner: codex-news-hourly-a8cd
claimed_at: 2026-10-13T03:32:56Z
created_at: 2026-10-13T03:32:51Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - docs/news-hourly-review-2026-10-13.md
---

# Resolve new hourly AI news review and redraft holds from October 11 onward

## Why

The hourly AI news pipeline is active, but new candidates can stop in review or
redraft for format, source, verification and locale reasons. On 2026-10-13 the
production admin showed 50 review holds, 25 redraft/failure entries and three
execution failures across all cohorts. The 2026-10-07 and 2026-10-10 cohorts
have separate owners and task files. This operation covers only candidates
created after the 2026-10-10 cohort capture; it will not replay those owners'
candidate IDs or paid jobs.

## Definition of done

- [x] Record an exact-ID baseline of new review and redraft candidates and the
      reason each is held.
- [x] Each candidate receives a persisted publication, rejection/duplicate
      decision, or a documented unresolved blocker with a follow-up task.
- [x] Published locales are checked on the public site, separately from queue
      acknowledgments and AI verdicts.

## Steps

- [x] Check board ownership and production settings; isolate new arrivals.
- [x] Correct eligible saved drafts in small batches, then request normal AI
      re-verification without bypassing the existing judge and publication gates.
- [x] Diagnose redrafts and failed runs; avoid ordinary retry or flagless backfill
      when either would duplicate paid work or bypass judge directions.
- [x] Reconcile the exact new cohort and save receipts in the scoped document.

## How to verify

Read candidate details and revisions in `/admin/news` and `/admin/guides`.
After each write, read the saved version, candidate status, assessments/runs,
and audit; verify all five public locale pages for any published item.

## Notes

- 2026-10-13 11:34 Taipei: `/admin/news` showed 50 review, 25 redraft
  (22 AI hand-backs), 3 failures and 592 published. Scan, automatic mode,
  all three auto-publish switches and Claude Opus 5.5 judge are on.
- New Evernorth candidate `392499e0-d820-4676-aba7-f01b06632527` has a
  saved five-locale article `541bb635-d186-4bb0-b45a-410f11f9d237`;
  zh-TW version 1 created 2026-10-13 02:16:57 Taipei is held by the
  `crypto_recommendation` hard check. Review of its original filing found a
  literal keyword false positive. The zh-TW draft was corrected and saved as
  version 2; normal re-verification subsequently passed and the AI judge
  published the five-locale article. See the scoped receipt document.
- New Bitmine candidate `02207914-e20f-4b3d-93b3-b041083de817` was rejected
  with an audited reason: its central story is ETH accumulation, a holding
  target, a projected timeline and staking returns. Rewording the hard-check
  keywords would not make that story eligible.
- New Clarity candidate `08ff40b0-30a1-4944-bc9c-bce7a0ff336d` had an
  AI hand-back for misattributing Derek Lowrey's statement to CoinDesk in
  zh-TW, en and ja. All three drafts were saved as version 2, then a single
  normal re-verification was queued. The AI final judge approved, the candidate
  was published, and all five public locale pages rendered.
- Huxe candidate `b5eb2cd8-f007-454f-b2ad-694e945f9cde` had a Guide
  created October 11 even though its source is dated October 10. Corrected
  planned-versus-completed wording in zh-TW and ja, then used the normal judge
  path. The first recheck found changed source content, so one latest-source
  recheck was queued with an audit reason. Verification and five locale reviews
  passed; the AI judge published it. All five public pages rendered, and the
  corrected zh-TW and ja text was read back.
- Meta Muse candidate `eed553a6-baaa-4e03-b5bc-449d10c54c97` was held
  at `news_locale_review_failed` (zh-CN) and misclassified CRYPTO. A different
  AI article about the same October 12 Muse Wonder / Full launch was already
  public from The Verge. The Decrypt candidate was rejected as a same-event
  duplicate with an audited explanation; the published article was unaffected.
  The cross-category dedupe miss is tracked in
  `2026-10-13-detect-duplicate-hourly-news-events-across`.
- Two October 10 source-dated redrafts cannot be assigned to the selected
  October 11+ cohort from the admin UI: their candidate creation times are not
  displayed, and the older cohort's exact-ID snapshot is unavailable. Both
  remain unchanged. See the scoped receipt document for their IDs.
- Final all-cohort admin snapshot: 46 review, 24 redraft (including three
  failures), 595 published and 935 rejected. These totals do not prove older
  backlog completion.
- `plink` production read was automatically blocked (`blocked by policy`,
  no more specific reason). The authenticated admin browser is available for
  readback and candidate-specific operations.
