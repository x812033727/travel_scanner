---
id: 2026-10-01-zh-cn-taiwan-vocabulary-in-the
title: zh-CN Taiwan vocabulary in the 11 packs other tasks held on 2026-10-02
status: done
priority: P2
area: docs
owner: claude-opus-5-5-zh-cn-vocab
claimed_at: 2026-10-02T19:26:27Z
created_at: 2026-10-01T21:09:49Z
completed_at: 2026-10-02T19:36:06Z
branch: claude/zh-cn-taiwan-vocabulary
depends_on: []
scope:
  - apps/api/app/guides/content/managed-hosting-comparison.json
---

# zh-CN Taiwan vocabulary in the 11 packs other tasks held on 2026-10-02

## Why

`2026-09-30-zh-cn-taiwan-vocabulary-in-the-2` fixed the zh-CN Taiwan vocabulary in every
pack no other task held. These 11 were held by active localization and news tasks on
2026-10-02, about 177 candidate words between them (paid-vs-organic-marketing 45 — mostly
搜寻 —, mailchimp-wordpress-newsletter 33 — mostly 外挂 —, brand-tone-vibe-marketing 23,
wordpress-chat-contact-buttons 22 帐号, marketing-plan-small-business 19,
email-newsletter-planning 18, marketing-mix-models 11, the AI news index 2, and one or two
each in wordpress-booking-system, kaohsiung-3-day-itinerary, managed-hosting-comparison).

## Definition of done

- [x] Claim once the holding tasks are finished (check `npm run tasks -- list`). Only the
      scoped pack, managed-hosting-comparison, was free; the other 10 moved to
      `2026-10-02-zh-cn-taiwan-vocabulary-in-the` (see Notes).
- [x] Same method as the parent: extract zh-CN reader strings (not code, URLs or machine
      fields), a mainland copy editor proposes minimal context edits (设定 stays for
      "set a goal/budget/limit", 预设 stays for "presuppose", quotes and proper nouns stay),
      apply with exact-once substring checks, other locales byte-identical.
- [ ] `pack_cli lint` 0 errors; re-import after merge with owner approval. Lint done (0
      errors); the re-import is not done: it needs the merge, a deploy and the owner's yes.

## Notes (2026-10-02, claude-opus-5-5-zh-cn-vocab)

- Scope stays one pack. On 2026-10-02 the other 10 are still held by tasks in `review` or
  `in-progress` whose content PRs are merged (#908, #899, #907, #857, #622, #672, #1041)
  but whose guarded production releases are pending.
  `docs/work-status-2026-09-29-article-release-plan.md` pins those releases to reviewed
  per-locale document hashes, so changing their zh-CN now would invalidate that evidence.
  They are filed as `2026-10-02-zh-cn-taiwan-vocabulary-in-the`, which depends on the
  holding tasks, with fresh counts per pack.
- managed-hosting-comparison: all 69 zh-CN strings read in context (not only the term-list
  hits). One edit: 可携性→可迁移性 (`/blocks/25/rows/4/1`, "数据与账号的可迁移性", matching the
  article's own 迁出／迁站). Kept: 设定 in "没有设定…固定时薪" (setting a rate, like a
  budget); 资料 meaning reference material (blocks 7 and 8); 续约, 首购, 加购, 计费期间,
  统计期间 and "依需求门槛" (the alt/description mirror the zh-CN SVG `<desc>`); 台湾用户 and
  新台币 are facts about the audience.
- Applied as an exact-once substring replacement. After parsing, zh-TW, en, ja, ko and the
  pack metadata are identical to before, and zh-CN differs only at that one pointer. The
  zh-CN hero and diagram SVG text has no Taiwan vocabulary, so no image changed.
- Checks: `pack_cli lint --kind life --slug managed-hosting-comparison` 0 errors (six
  existing warnings: no_summary ×5, en text_length); `pytest tests/test_guides_content_pack.py
  -q` 9 passed, 5 skipped. The repository has no zh-CN vocabulary checker; the scan used the
  parent's term list.
- Publish (owner approval, after a deploy that contains this PR):
  `guides-import --slug managed-hosting-comparison --locale zh-CN --dry-run`, then `--publish`.
