---
id: 2026-09-28-let-trusted-newsrooms-publish-alone-and
title: Let trusted newsrooms publish alone and rerun stories rejected for empty excerpts
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-28T05:17:16Z
created_at: 2026-09-28T05:17:00Z
completed_at:
branch: claude/ai-hourly-news-efficiency-b1c0d2
depends_on:
  - 2026-09-28-news-extractor-keeps-tag-lists-and
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_backfill_cli.py
---

# Let trusted newsrooms publish alone and rerun stories rejected for empty excerpts

## Why

On 2026-09-28 the owner said the hourly news publishes too little, and approved three
follow-ups to the extractor fix (`2026-09-28-news-extractor-keeps-tag-lists-and`):

1. Re-queue the 38 uncertain-duplicate holds that only exist because Jev's budget was spent.
   `backfill_cli --jev-quota-holds` already does this. It needs no code.
2. Let a story whose only evidence is one major newsroom (TechCrunch, The Verge or CoinDesk)
   publish automatically when Jev says act. Until now only two websites or a first-party page
   could. 18 verified zh-TW drafts were waiting for the owner, and Jev had said act on 8 of
   them.
3. Rerun the stories the writer rejected as not newsworthy only because the excerpt held a tag
   list, navigation or CSS.

## Definition of done

- [x] A source whose `config_json` has `auto_publish_alone: true` counts as enough evidence for
      automatic publication (`policy.trusted_alone_sites`, `auto_evidence_ok`). The final
      editor and Jev's last call still guard it.
- [x] `backfill_cli --refetch-source NAME` refetches the evidence of that source's
      `news_not_eligible` rejections that no person made, then reopens and queues each
      readable one. An unreadable page stays rejected and is reported.
- [ ] Production: the flag is set on the three newsrooms, and the three backfills are run.

## Steps

- [x] Policy and pipeline.
- [x] Backfill option.
- [x] Tests.
- [x] `sources.json`: `auto_publish_alone` on TechCrunch AI, The Verge AI and CoinDesk (the
      owner confirmed it again after the auto-mode classifier blocked the first edit).
- [ ] After deploy: `sources_cli --apply` pushes the flag to production.
- [ ] After deploy, on the host:
      `backfill_cli --since 2026-09-01 --jev-quota-holds --apply` and
      `backfill_cli --since 2026-09-15 --refetch-source ... --apply` for Cloudflare blog,
      Chainalysis blog, SEC press releases, Meta Newsroom, Ethereum Foundation blog and Google
      DeepMind blog.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_backfill_cli.py tests/test_news_automation.py tests/test_news_pipeline.py -q
```

## Notes

- Nothing changes until a source carries the flag. The rule is config, not code, so the owner
  can add or remove a newsroom through `sources.json` and `sources_cli --apply`.
- The flag does not reach drafts already waiting as `news_zh_draft_ready`. Those were
  assessed before it existed, so they still need the owner's button, or a separate decision.
