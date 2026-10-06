---
id: 2026-10-06-batch-005-nikko-kyoto-translations-refresh
title: Refresh Batch 005 Nikko and Kyoto translations against the corrected live zh-TW
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-06T01:30:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/nikko-day-trip-from-tokyo.json
  - apps/api/app/guides/content/kyoto-bus-subway-guide.json
  - apps/web/public/guides/nikko-day-trip-from-tokyo
  - apps/web/public/guides/kyoto-bus-subway-guide
---

# Refresh Batch 005 Nikko and Kyoto translations against the corrected live zh-TW

## Why

Article-localization Batch 005 staged en, ja, ko and zh-CN translations of
`nikko-day-trip-from-tokyo` and `kyoto-bus-subway-guide`, but the zh-TW they were made from
was wrong in places #593 has since corrected. The 2026-09-20 09:12 UTC snapshot was zh-TW v6,
document SHA-256 `5d81e30f…6c61` for Nikko and `ef895904…edda` for Kyoto.

- **Nikko:** the old source said 「NIKKO PASS 只賣外國旅客」, and the staged drafts copied it. Tobu
  sells the pass to foreign travellers and to Japanese nationals travelling with them, and asks
  for a passport at purchase.
- **Kyoto:** the old source told IC riders on flat-fare City Buses to tap at rear boarding and
  again at the front exit. It also put a one-day pass's first use at boarding. Its map caption
  and heading did not match the solid sightseeing-express line.

The corrected zh-TW is live as v8 for both, last modified 2026-09-20T11:56:56Z. The four target
locales of each slug are still `unpublished`. They must not go live with the old facts.

## Definition of done

- [ ] All four Nikko locales are made from the live zh-TW, and the normalized hash used is
      recorded here (`fe813e51…01e1e7` on 2026-10-06, equal to the repo pack). They say NIKKO
      PASS is sold to non-Japanese visitors and to Japanese nationals accompanying them, with a
      passport shown at purchase, and none infers citizenship from the reader's language.
- [ ] All four Kyoto locales, and their diagram text, are made from the live zh-TW, with its
      hash recorded. They say: board a flat-fare bus without tapping and tap once at the front
      exit; tap at both boarding and exit only on distance-fare (整理券) buses; on its first
      ride a one-day pass goes through the fare reader at the front exit, and on later rides
      the printed date is shown to the driver. Solid lines are rail or the sightseeing express
      (EX100/EX101), dashed lines are ordinary City Buses.
- [ ] A reviewer who is not the translator signs off on each locale, bound to the exact source
      and document hashes, as `.agents/skills/article-localization/SKILL.md` requires.
- [ ] Nothing is published before that review passes and the owner consents to the publish.

## Steps

- [ ] Find the staged Batch 005 drafts. They are route A work in the Codex localization
      workspace, outside this repository. Record where they are, or that they are gone and
      the four locales will be translated again by route B.
- [ ] Kyoto only: wait for `2026-10-06-publish-onsen-kyoto-bus-zh-tw`. Live zh-TW is
      `865362fe…9caa` and the repo pack is `da86dc07…513c`. They differ only in #1001's 6:00
      and #1028's 住宿稅, and that ticket publishes both. If you bind before it lands, record the
      hash you used and rebind after it does.
- [ ] Re-measure the live zh-TW hashes. Refresh or translate, review, and open the content PR.
      Publish only with the owner's consent, following the skill's chosen route.

## How to verify

Fetch `/api/travel/guides/howto/<slug>?locale=zh-TW` with the editorial User-Agent. Drop
`version`, `published_at` and `modified_at`, normalize with `GuideDocument`, and check that
`app.guides.service.document_hash` equals the source hash each review is bound to. In each
target locale, search for the old claims: pass sold only to foreigners, a boarding tap on
flat-fare buses, the one-day pass at boarding. All three must be absent. After publication,
run `verify_public.py --slug <slug> --kind howto --locale <loc> --sitemap` for each locale.

## Notes

- Split on 2026-10-06 (claude-opus-5-5-board-closures) from
  `2026-09-20-correct-nikko-pass-eligibility-for-accompanying` (DoD "Refresh Batch 005's four
  Nikko translations…") and `2026-09-20-correct-kyoto-flat-fare-bus-ic` (DoD "Rebase and
  review all four Kyoto translations and diagrams…"). Both source corrections are live and
  those tickets are closed.
- Official sources re-read on 2026-10-06, all HTTP 200 and still saying what the corrections
  rely on:
  - Tobu `https://www.tobu.co.jp/en/ticket/nikko/all.html` and `…/city.html`: only foreign
    travellers, though Japanese nationals accompanying them can also buy.
  - Tobu `https://www.tobu.co.jp/en/faq/`: the passport must be shown at purchase.
  - Kyoto City `https://www.city.kyoto.lg.jp/kotsu/page/0000324695.html`: 均一区間車 have no
    boarding reader and 整理券車 need a boarding tap. The 地下鉄・バス1日券 goes through the
    reader on first use, and later the date is shown to the driver.
  - The 2026-03-20 busnavi PDF.
- No record of Batch 005 is in the repository: nothing under `docs/article-localization/` and no
  ticket. Its staging is in the Codex workspace, which is why this cannot be finished from a
  repository checkout alone.
