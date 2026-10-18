---
id: 2026-10-11-show-final-judge-holds-on-news
title: Show final judge holds on news marked ready to publish
status: done
priority: P2
area: web
owner: claude-opus-5-5-news-judge-hold
claimed_at: 2026-10-17T03:30:34Z
created_at: 2026-10-11T04:30:42Z
completed_at: 2026-10-17T03:33:50Z
branch:
depends_on: []
scope:
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages/en.json
  - apps/web/lib/admin-news-messages/ja.json
  - apps/web/lib/admin-news-messages/ko.json
  - apps/web/lib/admin-news-messages/zh-CN.json
  - apps/web/lib/admin-news-messages/zh-TW.json
---

# Show final judge holds on news marked ready to publish

## Why

The news workspace classifies `manual_review/news_ready_to_publish` as ready
solely from `error_code`, even when the latest final AI judge requires an
editorial correction. In the October 11 recovery cohort, Flock candidate
`7bea807c-ffa3-44a2-b3be-92aee355e279` has this marker while its latest judge
verdict is `manual`: the article omitted the company's response to a disputed
misidentification allegation. Operators must read the actual review decision
before deciding to publish; the queue label should make that need visible.

## Definition of done

- [x] A candidate with a current final judge hold shows that hold and its
      corrective route instead of suggesting that AI review has passed.
- [x] Legitimate articles awaiting the owner's publish decision remain usable.
- [x] Manual publication retains the existing server publication checks and
      explicit owner decision; no rule silently overrides the stored judge.

## Steps

- [x] Inspect current summary/detail review fields and distinguish current,
      evidence-bound final decisions from old or replaced judge assessments.
- [x] Adjust the narrow workspace presentation using existing situations/copy
      where possible. If new summary fields or copy are required, amend scope
      through the task protocol before changing them.
- [x] Add one meaningful regression for ready-marker plus current judge hold,
      and verify ordinary ready-to-publish behavior.

## How to verify

Run the affected admin-news-workspace test and web typecheck. Verify an actual
stored `manual_review/news_ready_to_publish/judge_decision=manual` example
shows the reason and editing/reverification route. Read-only evidence does not
authorize a production publish action for the fixture or live candidate.

## Notes

Filed during original208 recovery; no implementation files changed or claimed.
Actual full readback: external operation workspace
`<home>/.codex/news-review/20261010-6f71/ready-flock-current-1121.capture/sql.json`,
SHA `56f4d0e82e201c8875245f3c3b96756ce5ea1e3984453ea2b2f8503ec3e3cbe3`,
captured2026-10-11T04:25:31Z. The latest stored judge has the current evidence
hash and explicitly requires the missing Flock response. All five locale reviews
pass, which does not override the final `manual` verdict. No active jobs or runs
were observed. A separate five-language content proposal has been independently
reviewed, but is not saved or published. This task concerns the workspace label.
- 2026-10-17 (claude-opus-5-5-news-judge-hold): claimed with `--force` over the stale
  `2026-10-11-news-fetcher-is-refused-by-cloudflare` claim (no live branch). The judge answers
  `news_ready_to_publish` as its "final" stage and records `details.hold` with that code, so the
  detail already listed the verdict and reasons; only the situation and its next-step text said
  every check had passed. A new situation `readyJudgeHold` (`news_ready_to_publish` with
  `judge_decision` "manual", which a rerun or re-check clears) explains the hold and the editor
  plus 重新查核 route; 五語發布 stays available as the owner's explicit decision with the server's
  existing checks. Scope amended for the five `lib/admin-news-messages` catalogs (one key each).
  Not verified against the stored Flock row: that readback lives on the owner's machine.
