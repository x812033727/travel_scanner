---
id: 2026-09-20-correct-nikko-pass-eligibility-for-accompanying
title: Correct NIKKO PASS eligibility for accompanying Japanese nationals
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:48:00Z
created_at: 2026-09-20T09:40:44Z
completed_at:
branch: claude/board-closures
depends_on: []
scope:
  - apps/api/app/guides/content/nikko-day-trip-from-tokyo.json
---

# Correct NIKKO PASS eligibility for accompanying Japanese nationals

## Why

The published `zh-TW` paragraph says `NIKKO PASS 只賣外國旅客`.
Tobu Railway's current official [All Area conditions](https://www.tobu.co.jp/en/ticket/nikko/all.html)
explicitly allow Japanese nationals accompanying foreign travelers to buy it too.
Its [FAQ](https://www.tobu.co.jp/en/faq/) says a passport must be presented
when buying the tourist pass. Four staged Batch 005 translations copied the
overly narrow eligibility statement and must wait for a version-pinned source correction.

## Definition of done

- [x] Correct only the eligibility paragraph in the published zh-TW source and preserve unrelated content and article visibility.
- [x] Pin the live revision, review the precise change, deploy and publish it with a guarded revision/backup/browser receipt.
- [ ] Refresh Batch 005's four Nikko translations against the corrected source before signing or publishing them.
  Moved to `2026-10-06-batch-005-nikko-kyoto-translations-refresh`.

## Steps

- [x] Identify official eligibility and passport conditions.
- [x] Reconcile the 2026-09-20 read-only live snapshot with the repository pack and prepare an exact source correction PR.
- [x] After green CI, merge, guarded deploy and publish the source revision.
- [ ] Refresh translation baseline. Moved to `2026-10-06-batch-005-nikko-kyoto-translations-refresh`.

## How to verify

Compare the deployed zh-TW page with Tobu's official conditions, verify the
published document hash and locale revision, and check signed-out desktop/mobile
pages. The four translated pages must remain unavailable until their new review.

## Notes

Official source checked 2026-09-20. The All Area page's Note says Japanese
nationals accompanying foreign travelers can purchase; the FAQ describes
non-Japanese citizens visiting Japan and accompanying Japanese customers, and
requires passport presentation. Do not infer citizenship from reading language.
The World Heritage Area page should be rechecked during the correction PR.
Read-only snapshot at 2026-09-20 09:12 UTC: article version 2, only zh-TW,
locale version/published version 6, document SHA-256
`5d81e30fa50ff59e2e4f18f774bf1ba1f5f1eff5a8c36f45f062e4a6a8ba6c61`,
pack SHA-256 `90ed494224cabb3dfba94f9b7d209f5716787ee7344dab96e7214e2e7a353497`.
The release must refresh this snapshot before any database write.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-article-localization (since 2026-09-20T09:40:50Z) was stale and is released so it stops locking its scope. Landed: #593. Still open: Correct eligibility paragraph in published zh-TW source (done in repo by #593, box not ticked); Pin live revision, deploy and publish with guarded revision/backup/browser receipt; Refresh Batch 005's four Nikko translations against corrected source; After merge: guarded deploy, publish source revision, refresh translation baseline.
- 2026-10-06 (claude-opus-5-5-board-closures). The publication was done on 2026-09-20; it is
  verified read-only here, and the translation refresh is split off:
  - **The change.** #593 (42adda043, merged 2026-09-20T10:51:54Z) changed one sentence in this
    pack and nothing else. 「NIKKO PASS 只賣外國旅客，」 became 「NIKKO PASS
    提供訪日的非日本國籍旅客購買，同行的日本國籍旅客也可購買。此券」. The rest of the paragraph
    (fares, validity, bus coverage) and every other block are byte-identical. The pack still
    has only zh-TW.
  - **Live.** The public API (editorial User-Agent) returns `status: published`,
    `published_locales: ['zh-TW']`, document `version: 8` and
    `modified_at: 2026-09-20T11:56:56Z`, which is after the merge and after the v6 snapshot
    above. Normalized through `GuideDocument`, its `document_hash` is
    `fe813e51…01e1e7`. That equals the pack at #593 and the pack on main today
    (cff4a6ac6), with zero field differences. Pack byte SHA-256 is `53b63aa9…a921`.
  - **Desktop and mobile.** In the built-in browser, signed out, at 1366×900 and 375×812, the
    page shows the corrected sentence, has no 「只賣外國旅客」, and on mobile has no horizontal
    overflow (scrollWidth 375). `verify_public.py --slug nikko-day-trip-from-tokyo --kind
    howto --locale zh-TW --sitemap` passed. en, ja, ko and zh-CN are still `unpublished`
    with `noindex`.
  - **Sources re-read 2026-10-06, all HTTP 200.** Tobu `all.html` and `city.html` (the
    World Heritage Area page this ticket asked to recheck) both say the pass is only
    available to foreign travellers, though Japanese nationals accompanying them can also
    buy it. The FAQ still requires the passport at purchase. The live sentence matches.
  - **Not verified.** The 2026-09-20 backup and receipt are not in the repository. What is
    verified is the outcome: live equals the corrected pack.
  - **Split.** DoD 3 and the "refresh translation baseline" half of the last step moved to
    `2026-10-06-batch-005-nikko-kyoto-translations-refresh`. The Batch 005 drafts sit in the
    Codex localization workspace outside the repository, and refreshing them needs a
    localization session and the owner's consent to publish. The baseline to bind to is
    `fe813e51…01e1e7`.
  - `pack_cli lint --slug nikko-day-trip-from-tokyo`: 0 errors, plus the existing
    `no_summary` warning.
