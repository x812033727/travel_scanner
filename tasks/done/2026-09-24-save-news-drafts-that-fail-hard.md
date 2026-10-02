---
id: 2026-09-24-save-news-drafts-that-fail-hard
title: Save news drafts that fail hard checks as editable articles
status: done
priority: P3
area: api
owner: claude-opus-5-5-news-drafts
claimed_at: 2026-10-02T14:28:59Z
created_at: 2026-09-24T11:21:15Z
completed_at: 2026-10-02T15:08:53Z
branch: claude/news-save-failed-drafts
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# Save news drafts that fail hard checks as editable articles

## Why

`process_candidate` saves the five-locale guide article only after the hard checks pass
(`apps/api/app/news_automation/pipeline.py`, `_save_guide_bundle` after
`hard_policy_problems`). A draft that fails them (a missing FAQ block, a missing topic
link, a forbidden word in one locale) is kept only in `draft_bundle_json`: the admin page
shows it and its lint, but there is no article to open in the guide editor, so a small
formatting problem costs a whole new draft. Since 2026-09-24 these candidates go to the
需重寫 list with only 重新執行 and 退件.

## Definition of done

- [x] A hard-check failure saves the bundle as an unpublished guide article, so the
      candidate goes to manual review with the editor links, and 重新查核 re-runs the
      checks on the edited drafts.
- [x] Nothing about publication changes: publish still needs every check to pass.

## Steps

- [x] Save the bundle before returning the hard-check hold; `_needs_redraft` then keeps
      it in manual review because it has an article.
- [x] Pipeline test for both paths.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_news_review_actions.py -q
```

## Notes

- Found while making the review queue actionable
  (task 2026-09-24-make-the-news-review-queue-actionable). Measure first: on 2026-09-24
  hard-check failures were rare next to fact-check and locale-review stops.
- 2026-10-02 (claude-opus-5-5-news-drafts): claimed with `--force` over a stale overlap:
  2026-09-30-news-duplicate-check-treats-a-new (owner claude-opus-5-5-news-4-9, branch
  `claude/gifted-rubin-umw5s4`) also lists `apps/api/tests/test_news_pipeline.py`, but its
  PR #1041 is merged and no open PR uses that branch. The same stale branch holds
  `docs/news-automation.md` through several review tickets, so `check:tasks` may warn.
- What changed: `_second_stage` in `pipeline.py` now calls `_save_guide_bundle` before it
  looks at the hard-check result. A failure then holds the candidate with `_manual`
  (`manual_review`, `news_hard_checks_failed`); the detail names the failing locales and
  `lint_json` keeps each locale's problems. I called `_manual` directly rather than
  `_needs_redraft`: once the article is saved the candidate always has one, so
  `_needs_redraft` could only ever choose manual review here, and calling it would hide that.
- Publication is unchanged. Saving writes only drafts (`published_version` stays empty),
  Jev's last call is not asked, and the publish button and the pipeline both go through
  `service.publication_bundle`, which runs `hard_policy_problems` on the saved article
  again. Those two are the only callers of `publish_news_bundle`. A person can still
  publish the guide article from the guide editor, as with any other saved news article
  (final-edit and Jev holds).
- A slug collision or a missing topic now makes such a candidate `failed`, not
  `needs_redraft`, the same as a candidate that passed its checks. Both land in 需重寫.
- The backfill CLI still reopens old `needs_redraft` + `news_hard_checks_failed` rows. New
  ones are in 待審查 now, so it does not pick them up, and it should not.
- Tests (`tests/test_news_pipeline.py`): an automatic-mode article and an owner-confirmed one,
  each failing a hard check in ja only. Both are saved unpublished in manual review, and
  Jev's last call is not asked. In the automatic case the publish button refuses with
  `news_hard_checks_failed`. After an edit in the guide editor and 重新查核, the automatic
  one waits as `news_ready_to_publish` and then publishes, and the confirmed one publishes
  on its own. Both tests fail on the old pipeline: `needs_redraft`, and no article for
  the confirmed one.
- The web needs a change, filed as 2026-10-02-offer-re-verify-on-news-articles. A
  confirmed candidate in this state shows only 「重新翻譯並發布」 and 退件 (`translationHold`),
  with no 重新查核. The unconfirmed one's `fixArticle` text says the article was "edited",
  which is wrong here. `docs/news-automation.md` is in scope to describe the new hold (the
  doc said a hard-check failure waits for 「重新翻譯並發布」 only).
- Takes effect after an API deploy. Nothing needs a migration or a backfill.
