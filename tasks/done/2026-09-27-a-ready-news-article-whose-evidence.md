---
id: 2026-09-27-a-ready-news-article-whose-evidence
title: A ready news article whose evidence changed can neither publish nor be re-checked
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-27T11:51:22Z
created_at: 2026-09-27T11:51:15Z
completed_at: 2026-09-27T11:54:52Z
branch: claude/news-publish-parks-changed-evidence
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/tests/test_news_review_actions.py
---

# A ready news article whose evidence changed can neither publish nor be re-checked

## Why

On 2026-09-27 `ai-news-google-project-suncatcher-20260924` passed its re-verification and
stopped at `news_ready_to_publish`. Publishing it (`POST /admin/news/candidates/{id}/publish`,
the 五語發布 button) answered `409 news_evidence_changed`, because the Verge evidence page had
changed since the check. `publish_candidate` raised before committing anything, so the
candidate stayed at `news_ready_to_publish`. `refresh_candidate_evidence`, the re-check against
the current pages (ticket `2026-09-24-let-a-news-candidate-held-for`), only accepts
`news_evidence_changed`. The article could therefore neither publish nor be refreshed, and
news pages change often. The pipeline's own second stage already parks a candidate as
`news_evidence_changed` when this happens (`pipeline._second_stage`); the publish button did
not.

## Definition of done

- [x] A publish refused for changed evidence leaves the candidate at `manual_review` /
      `news_evidence_changed`, so `/admin/news` offers the re-check. No publish decision is
      recorded.
- [x] The re-check then runs on it (test).
- [ ] After the deploy, suncatcher is re-checked and published.

## Steps

- [x] `publish_candidate`: on `news_evidence_changed` from `publication_bundle`, store the hold
      and commit, then re-raise so the button still reports the 409.
- [x] Test in `test_news_review_actions.py`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_review_actions.py tests/test_news_pipeline.py tests/test_news_automation.py -q
```

## Notes

- The unticked item is the deploy and the follow-up on the one stuck article, which the
  session that wrote this ticket does after the merge.
- Pages whose extracted text changes on every visit (sidebars, "most read" lists) would keep
  failing the revalidation. If refreshed candidates keep coming back as
  `news_evidence_changed`, the extraction is the next thing to look at. See
  `2026-09-27-news-evidence-excerpts-stop-at-8`.
