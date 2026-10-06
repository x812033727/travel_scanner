---
id: 2026-09-20-correct-hakone-and-noboribetsu-bathing-tax
title: Correct Hakone and Noboribetsu bathing tax age wording
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:46:31Z
created_at: 2026-09-20T08:37:30Z
completed_at:
branch: claude/board-closures
depends_on: []
scope:
  - apps/api/app/guides/content/japan-onsen-ryokan-guide.json
---

# Correct Hakone and Noboribetsu bathing tax age wording

## Why

The published Traditional Chinese onsen guide says both Hakone and Noboribetsu
exempt children aged 12 and under. Noboribetsu exempts children **under** 12;
Hakone's rule also names elementary-school pupils and children until the first
March 31 on or after the day they legally attain age 12. In Japanese law that
attainment day is not necessarily the birthday, and March 31 itself is included.

## Definition of done

- [x] The source paragraph and tax table state each municipality's rule without
  excluding the attainment day or extending the school-year boundary.
- [x] The exact source pack passes schema validation, CI, and guarded publication
  of only the existing zh-TW locale.

## Steps

- [x] Compare the two municipal tax pages and the education ministry's age-law
  explanation; independently review the March 31 boundary.
- [x] Correct the existing pack without changing prices, URLs or other prose.
- [x] Merge reviewed CI, deploy, perform version-pinned dry run and publication.
- [x] Verify desktop/mobile live page and preserved non-public locales.

## How to verify

Validate the pack with `ArticlePack.model_validate_json`, verify its normalized
`document_hash` and byte SHA-256, run `npm run check:tasks`, and require exact-head
PR CI. Production must match the old published version/hash before the guarded
draft and publish calls, then match the corrected published hash afterward.

## Notes

- Hakone: https://www.town.hakone.kanagawa.jp/www/contents/1100000000874/index.html
- Noboribetsu: https://www.city.noboribetsu.lg.jp/docs/2013031100289/
- Legal age: https://www.mext.go.jp/a_menu/shotou/shugaku/detail/1422233.htm
- Exact revised pack hash `febd82c4b31ef49e7a625efc4174e4174e6c5f8c4716bdd4e85997a2e6f985aa`;
  normalized zh-TW document hash `66c6ecf6f37010ea0f5cc514e541950c3543183f17496ddfe3c57fd837102a8d`.
- The correction changes the source used by Batch 003. Its onsen translations
  must be regenerated from a fresh published baseline and reviewed again.

- 2026-09-30 (claude-opus-5-5, owner-approved `--force` on
  `2026-09-20-lodging-tax-wording-site-wide`): in this ticket's packs the zh-TW
  title, description and body now say 住宿稅 where they said 宿泊稅 or 宿泊税.
  No number changed; Japanese official page names in `sources` are unchanged.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-article-localization (since 2026-09-20T08:37:35Z) was stale and is released so it stops locking its scope. Landed: #588 #1028. Still open: Pack passes CI and guarded zh-TW publication; Deploy, version-pinned dry run and publication; Verify desktop/mobile live page and preserved non-public locales.
- 2026-10-06 (claude-opus-5-5-board-closures). The publication was done on 2026-09-20; it is
  verified read-only here:
  - **Repo.** #588 merged at 2026-09-20T09:05:00Z. The pack at that commit (8264c01a7) has
    byte SHA-256 `febd82c4…f985aa` and normalized zh-TW hash `66c6ecf6…2a8d`, the exact two
    hashes recorded above. It validates as an `ArticlePack`.
  - **Live.** The public API (`/api/travel/guides/howto/japan-onsen-ryokan-guide?locale=zh-TW`,
    editorial User-Agent) returns `status: published`, `published_locales: ['zh-TW']`, document
    `version: 8` and `modified_at: 2026-09-20T09:33:35Z`, 28 minutes after the merge. With
    `version`, `published_at` and `modified_at` dropped and the document normalized through
    `GuideDocument`, `document_hash` is `66c6ecf6…2a8d`. That is the corrected document,
    published to zh-TW only.
  - **Text on the live page.** It contains 「登別市未滿 12 歲免收」, 「箱根町未滿 12 歲免收」 and
    「首個 3 月 31 日止（含當日）」. The official pages, re-read today with HTTP 200, still say
    the same thing. Hakone: 「年齢12歳未満の方（小学生以下または12歳に達する日以後の最初の3月31日までの間にある方）」.
    Noboribetsu: 「年齢１２歳未満の者」. MEXT's age-reckoning page still explains that the age
    is reached at the end of the day before the birthday.
  - **Desktop and mobile.** In the built-in browser, signed out, at 1366×900 and 375×812
    (mobile preset), the page rendered the right h1 and the corrected sentences. On mobile
    there is no horizontal overflow (scrollWidth 375), and the tax table shows the corrected
    入湯稅 row. `verify_public.py --slug japan-onsen-ryokan-guide --kind howto --locale zh-TW
    --sitemap` passed: 200, h1, canonical, no noindex, images 200, listed in the sitemap.
  - **Non-public locales preserved.** For en, ja, ko and zh-CN the API returns
    `"status":"unpublished"`, and `/<loc>/guides/howto/japan-onsen-ryokan-guide` carries
    `noindex`.
  - **Not verified.** The 2026-09-20 dry-run and backup receipts are not in the repository.
    What is verified is the result: live equals the corrected pack.
  - **The repo is now ahead of live.** #1028 changed seven 宿泊稅 to 住宿稅 across six fields:
    `description`, `blocks[0].text`, `blocks[2].text`, `blocks[3].caption`,
    `blocks[3].rows[3][0]` and `blocks[24].items[1]`. Nothing else differs, so the repo pack's
    hash is `cd4ad6ca…85f1`. That wording is not live; the mobile table still shows
    「宿泊稅（東京都）」. Publishing it is filed as `2026-10-06-publish-onsen-kyoto-bus-zh-tw`
    (host only, owner consent).
  - **Batch 003.** The four onsen target locales stay with
    `2026-09-20-five-language-article-batch-003`. They should translate from whatever zh-TW
    is live when they start.
  - `pack_cli lint --slug japan-onsen-ryokan-guide`: 0 errors, plus the existing
    `no_summary` warning.
