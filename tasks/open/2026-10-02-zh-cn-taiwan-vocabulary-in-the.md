---
id: 2026-10-02-zh-cn-taiwan-vocabulary-in-the
title: zh-CN Taiwan vocabulary in the 10 packs still held by localization and news releases
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-02T19:34:19Z
completed_at:
branch:
depends_on:
  - 2026-09-28-batch036-marketing-pair-a
  - 2026-09-28-localize-newsletter-pair-a-in-five
  - 2026-09-28-localize-marketing-mix-and-brand-tone
  - 2026-09-27-integrate-batch029-wordpress-contact-guides
  - 2026-09-21-taiwan-zh-tw-third-sub-batch
  - 2026-09-16-news-batch-4-4-the-8
  - 2026-09-30-news-batch-4-9-gpt-6
  - 2026-09-30-news-batch-4-10-claude-sonnet
scope:
  - apps/api/app/guides/content/paid-vs-organic-marketing.json
  - apps/api/app/guides/content/mailchimp-wordpress-newsletter.json
  - apps/api/app/guides/content/brand-tone-vibe-marketing.json
  - apps/api/app/guides/content/wordpress-chat-contact-buttons.json
  - apps/api/app/guides/content/marketing-plan-small-business.json
  - apps/api/app/guides/content/email-newsletter-planning.json
  - apps/api/app/guides/content/marketing-mix-models.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/wordpress-booking-system.json
  - apps/api/app/guides/content/kaohsiung-3-day-itinerary.json
---

# zh-CN Taiwan vocabulary in the 10 packs still held by localization and news releases

## Why

`2026-10-01-zh-cn-taiwan-vocabulary-in-the` was filed for 11 packs whose zh-CN still uses
Taiwan vocabulary (搜寻, 外挂, 帐号, 资讯, 联络 …) but that other tasks held. On 2026-10-02 it
could only fix the one free pack, managed-hosting-comparison. These 10 are still held by
localization and news tasks whose content PRs are merged but whose guarded production
release is pending. `docs/work-status-2026-09-29-article-release-plan.md` pins those
releases to reviewed per-locale document hashes, so editing their zh-CN now would invalidate
the review evidence the release depends on. Hence the `depends_on` list.

Candidates on 2026-10-02 (the parent's term list, reader strings only; 设定 counted even
where it stays): paid-vs-organic-marketing 42 (搜寻 29), mailchimp-wordpress-newsletter 33
(外挂 14), email-newsletter-planning 23, wordpress-chat-contact-buttons 22 (帐号),
brand-tone-vibe-marketing 21 (资讯 17), marketing-plan-small-business 15,
marketing-mix-models 9, wordpress-booking-system 3, the AI news index 2 (使用者),
kaohsiung-3-day-itinerary 2.

## Definition of done

- [ ] Every zh-CN reader string in the 10 packs uses mainland vocabulary; zh-TW, en, ja,
      ko, pack metadata, code, URLs and quotes are byte-identical.
- [ ] `pack_cli lint` 0 errors; the changed packs re-imported after merge with owner approval.

## Steps

- [ ] Claim only after the holding tasks are done (each one's release is published and its
      ticket moved to `tasks/done/`); a merged content PR alone is not enough.
- [ ] Same method as `2026-09-30-zh-cn-taiwan-vocabulary-in-the-2`: extract zh-CN reader
      strings (not code, URLs or machine fields), a mainland copy editor proposes minimal
      context edits (设定 stays for "set a goal/budget/limit", 预设 stays for "presuppose",
      资料 stays for "materials", quotes and proper nouns stay), apply with exact-once
      substring checks, compare the other locales after parsing.
- [ ] If a changed string mirrors a zh-CN image's `<desc>` or label, add that SVG under
      `apps/web/public/guides/<slug>/` to the scope with the reason, or leave the string.

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life --slug <slug>   # each changed pack
uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

- Filed 2026-10-02 by `claude-opus-5-5-zh-cn-vocab` from `2026-10-01-zh-cn-taiwan-vocabulary-in-the`.
- Holders on 2026-10-02 and their merged content PRs: batch036 pair A (#908), newsletter
  pair A (#899), batch036 pair B (#907), batch029 contact (#857), taiwan zh-TW batch 003
  (#622), news 4.4 (#672), news 4.9/4.10 (#1041). The AI index is also in the open
  `2026-09-26-refresh-stale-parts-of-the-three`.
