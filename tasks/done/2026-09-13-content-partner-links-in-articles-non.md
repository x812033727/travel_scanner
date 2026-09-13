---
id: 2026-09-13-content-partner-links-in-articles-non
title: Content partner links in articles: non-travel affiliate programs with disclosure, rel=sponsored and a click beacon
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-13T05:06:19Z
created_at: 2026-09-13T05:06:07Z
completed_at: 2026-09-13T09:37:17Z
branch: claude/claude-tutorial-affiliate-links-084ff0
depends_on: []
scope:
  - apps/api/app/affiliates/content_links.py
  - apps/api/app/affiliates/sub_id.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/tests/test_guide_partner_links.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_affiliate_sub_id.py
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/components/guides
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - docs/travel-guides.md
  - docs/affiliate-configuration.md
---

# Content partner links in articles: non-travel affiliate programs with disclosure, rel=sponsored and a click beacon

## Why

The owner is about to publish Claude (AI) tutorials in 生活分享 (`/life`) and wants to earn from
the tools those tutorials use — Hostinger for "deploy what Claude Code built", 博客來 for AI
books, later n8n, Make and course platforms. The affiliate plumbing only knows travel: eight
travel partners, five travel modules behind a DB CHECK, destination offers keyed to catalog
cities. The only way to get a non-travel partner URL onto an article today is a plain `link`
block, which publishes it undisclosed, without `rel="sponsored"`, and without a click record.
That is a 公平會薦證廣告 disclosure problem and a Google link-spam problem at the same time.

The travel clickout pattern cannot simply be reused. It is a same-origin POST that 303-redirects
with `Referrer-Policy: no-referrer`, and Hostinger's Affiliate Program Agreement (updated
2026-08-19) forbids "link cloaking or masking techniques … hiding that traffic source".
Content partners therefore get a direct, qualified link plus a separate click beacon.

## Definition of done

- [x] An editor can place a `partner_link` block (partner, https URL, label, optional note) in any
      article; only partners in the code registry and only their hosts are accepted, at most three
      per article, and Hostinger customer-referral links (`REFERRALCODE`) are refused with the reason.
- [x] The public article renders each resolved partner link as
      `<a target="_blank" rel="sponsored noopener" referrerPolicy="strict-origin-when-cross-origin">`
      straight to the partner URL, after a generic disclosure line, in all five locales.
- [x] A click sends a keepalive POST that writes one `affiliate_clicks` row
      (`sub_id` prefix `cnt_`, no identity) and never delays or blocks the navigation.
- [x] A partner removed from the registry makes its stored blocks draw nothing: public reads and
      the admin detail still return 200.
- [x] Plain `link` blocks, `sources` and image credits refuse affiliate URLs at write time with an
      error that points the editor at the partner-link block (the legal-page half is
      `2026-09-12-content-link-block-sponsored`).

## Steps

- [x] API: `affiliates/content_links.py` registry and URL checks, `cnt_` sub_id prefix,
      `PartnerLinkBlock`, write-time validation, public `partner_links`, admin partner list,
      click endpoint.
- [x] Web: block guard and segment split, server parsing, `partner-link.tsx`, article disclosure,
      admin editor, messages in five locales.
- [x] Tests (pytest and vitest) and docs (`docs/travel-guides.md`, `docs/affiliate-configuration.md`).

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guide_partner_links.py tests/test_guides.py tests/test_affiliate_sub_id.py tests/test_site_pages.py tests/test_error_localization.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
```

Manual: an article with a partner link shows the disclosure before it; the link opens the
partner URL in a new tab at once; the click POST carries `Origin` and returns 204; the admin
editor refuses a foreign host, a referral link and a fourth partner link.

## Notes

- Claimed with `--force`: `docs/affiliate-configuration.md` is still listed by
  `2026-09-12-trip-partner-offer-availability` (in-progress, claude-fable-5-1), whose PR #436
  merged as `e69039ef`; the three trip-partner tasks were never moved to done.
- No migration: `affiliate_clicks` has no CHECK and is append-only, so the article slug goes into
  `destination_summary` until `2026-09-12-attribute-affiliate-clicks-to-the-guide` adds
  `article_slug` (a note for that task is in its own Notes).
- The follow-up this plan meant to file — travel offer forms sending `Origin: null` because of
  `rel="noopener noreferrer"` — was found and fixed by another session in PR #447 while this
  branch was open, so no task was filed. Partner links are anchors, not forms, and their count
  request is a same-origin `fetch`, so that rule does not bite here either way.
- Defaults the owner approved with the plan and can still change: ordinary editorial links keep
  `noopener noreferrer` without `nofollow`; partner links are `sponsored noopener`; three per
  article; clicks are counted even under DNT/GPC because no identity is stored. The privacy
  policy should still mention partner-link click records; that belongs with
  `2026-09-06-legal-content-from-owner`.
- Programs shipped in the registry: `hostinger` (affiliate program links on `hostinger.com`;
  customer `REFERRALCODE` links refused) and `books_com_tw` (博客來 AP). Everything else waits
  for the owner to be accepted by a program and send one generated link, so the hosts are
  real rather than guessed. `2026-09-13-adsense-article-slot` has a note about keeping ad
  slots away from partner links.

## What shipped

- **API.** `app/affiliates/content_links.py` holds the registry and the two URL checks
  (`partner_link_problem` for the block, `affiliate_marker` for every ordinary URL).
  `PartnerLinkBlock` joins `GuideBlock`; `_validate_document` enforces the registry, the cap
  and the ordinary-URL rule on create, new translation, draft, publish and restore, and the
  content-pack importer inherits it. `public_article` resolves `partner_links` on every read;
  `POST /guides/{kind}/{slug}/partner-links/{key}/click` counts a click (rate-limited, 204, no
  identity, 404 for anything a reader could not have seen); `GET /admin/guides/partners`
  feeds the editor. `SUB_ID_RE` accepts `cnt_`.
- **Web.** `components/guides/partner-link.tsx` (direct sponsored link, badge, keepalive count);
  `article.tsx` draws partner islands from `splitGuideBlocks`' new `segment.partner` only when
  the API resolved them, with `guides.partnerDisclosure` above the first; `content-blocks.tsx`
  draws only `link` blocks as links; the admin editor has the block, the program list, the
  allowed-hosts hint and a placeholder preview. Ten message files carry the new keys.
- **Docs.** `docs/travel-guides.md` "Partner links" and pack rules; `docs/affiliate-configuration.md`
  §8 "非旅遊內容合作夥伴".

## Numbers

- API: ruff and mypy clean; the full suite 3600 passed, 240 skipped. The one failure,
  `test_warning_codes.py`, is the known Windows path-separator bug in that test's allowlist.
  `tests/test_guide_partner_links.py` covers the registry, the four write paths, the removed
  partner, the anonymous click row and every 404.
- Web: lint, typecheck, `check:i18n`, `check:tasks`, `test:tools` (28) clean; `test:web` 244 files,
  2634 tests passed.
- Real browser (headless Chromium through Playwright, `next dev` against a mock API serving one
  lifestyle article): the disclosure line precedes the link; the anchor is
  `rel="sponsored noopener"` with `referrerpolicy="strict-origin-when-cross-origin"`; clicking
  opened the partner URL in a new tab, and the partner received `Referer: <site origin>/`; the
  count POST carried `Origin`, passed the BFF and returned 204 with the key and locale intact.
  The script is worth keeping as a pattern: route the partner host with `context.route` to see
  the headers a partner would get, and listen on the page for the count request.
