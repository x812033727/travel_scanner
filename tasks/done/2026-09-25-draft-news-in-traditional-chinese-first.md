---
id: 2026-09-25-draft-news-in-traditional-chinese-first
title: Draft news in Traditional Chinese first and translate only after the owner confirms publication
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T07:03:11Z
created_at: 2026-09-25T07:03:01Z
completed_at: 2026-09-25T07:22:54Z
branch: claude/news-zh-draft-first
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_review_actions.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_admin.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
  - docs/news-automation.md
---

# Draft news in Traditional Chinese first and translate only after the owner confirms publication

## Why

On 2026-09-25 the site owner reviewed the 待審查 list and found that nothing in it could be
published. Every candidate came from an official feed (Apple, NVIDIA, Google, Anthropic,
Hugging Face, the Ethereum Foundation), but the evidence gate required pages from two
different websites, so each one stopped before a draft, and 140 more had been rejected as
缺證據 the day before. The owner decided:

1. Every hourly scan result that Jev does not judge a duplicate goes to the writer. One
   page from an enabled source (official or trusted) is enough.
2. The writer drafts in Traditional Chinese only; the fact-checker checks it against the
   source; the owner reads the draft in 待審查.
3. Only after the owner confirms publication are the other four languages translated,
   reviewed and checked, and then the article publishes by itself.

Defaults kept (confirmed with the plan): the writer still excludes marketing, event
recaps, rumours and hiring; automatic publication still needs two websites.

## Definition of done

- [x] A candidate with one evidence website is drafted, fact-checked, assessed by Jev on
      zh-TW only, and waits as `news_zh_draft_ready` without any translation.
- [x] `POST /admin/news/candidates/{id}/approve` records the owner's publish decision and
      queues stage two, which translates, reviews, checks, saves and publishes.
- [x] A confirmed candidate that stops in stage two keeps the confirmation and can be
      resumed; retry forgets it.
- [x] `/admin/news` shows the zh-TW draft with 「確認發布，翻譯其他語言」, 「重新執行」 and
      退件, and 「重新翻譯並發布」 for a stalled confirmed one.

## Steps

- [x] policy: `evidence_present`; hard checks need one source website.
- [x] ai: writer and verifier instructions allow one attributed source; Jev per locale list.
- [x] pipeline: stage one / stage two split, slug kept on the draft run, reverify tail.
- [x] service: shared `publication_bundle` / `publish_news_bundle`, `approve_candidate`,
      retry clears the decision; router and i18n.
- [x] web: three situations, approve and retranslate buttons, copy in five locales.
- [x] docs and tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_news_review_actions.py tests/test_news_automation.py tests/test_news_admin.py -q
npm run test:web -- admin-news-workspace
```

After deploying: in 待審查, press 「不是重複，繼續寫」 on one of the official stories; a few
minutes later it shows as 「繁中草稿待確認」 with a zh-TW preview only. Confirm it, and a
few minutes later all five locales are published.

## Notes

- Jev use drops to two calls per candidate (duplicate + zh-TW), but many more candidates
  reach the writer now; `JEV_DAILY_CALL_BUDGET` (200) may run out on busy days, in which
  case the duplicate check answers "uncertain". Watch it; raising it is the owner's call.
- The writer's slug is stored on the `draft` pipeline run's metadata so stage two can
  create the article without a new column.
- Candidates from before this change that already hold five-locale drafts
  (`news_jev_manual`, `shadow_review`) keep the publish button, which now accepts one
  source website too.
- Not done here: letting the owner edit the zh-TW draft before confirming (there is no
  article yet, so the guide editor cannot open it).
