---
id: 2026-10-01-zh-cn-taiwan-vocabulary-in-the
title: zh-CN Taiwan vocabulary in the 11 packs other tasks held on 2026-10-02
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-01T21:09:49Z
completed_at:
branch:
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

- [ ] Claim once the holding tasks are finished (check `npm run tasks -- list`).
- [ ] Same method as the parent: extract zh-CN reader strings (not code, URLs or machine
      fields), a mainland copy editor proposes minimal context edits (设定 stays for
      "set a goal/budget/limit", 预设 stays for "presuppose", quotes and proper nouns stay),
      apply with exact-once substring checks, other locales byte-identical.
- [ ] `pack_cli lint` 0 errors; re-import after merge with owner approval.
