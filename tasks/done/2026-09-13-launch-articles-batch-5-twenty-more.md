---
id: 2026-09-13-launch-articles-batch-5-twenty-more
title: Launch articles batch 5: twenty more travel guides (Japan day trips, Korea, Thailand, Vietnam)
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-13T13:29:39Z
created_at: 2026-09-13T13:29:00Z
completed_at: 2026-09-14T01:33:29Z
branch: claude/travel-guide-articles-planning-50e722
depends_on: []
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
---

# Launch articles batch 5: twenty more travel guides (Japan day trips, Korea, Thailand, Vietnam)

## Why

Fifty zh-TW articles exist (PR #443, PR #446 live; PR #460 — batch 4 — open) plus the
Taiwan set in the other four locales (PR #454). The owner asked for twenty more in the same
way. This batch takes the day trips the city itineraries keep pointing at (Fuji and
Kawaguchiko, Nikko, Himeji, Otaru, Yufuin and Beppu, Takayama and Shirakawa-go, Nami
Island, Ayutthaya), the two "which pass / how to pay" questions still unanswered (Kansai
rail passes, Korean money and WOWPASS), a mainland-Japan car-rental guide (Okinawa has one),
deeper Seoul culture (five palaces and hanbok, Korean food and table rules), Bangkok's
in-city transit and Thailand's SIM guide, a first Chiang Mai itinerary, two dated notices
(Sapporo Snow Festival 2027, Korean ski season 2026–27), and opens Vietnam with the entry
notice Taiwanese readers actually need (e-visa) plus a Da Nang and Hoi An itinerary.

## Definition of done

- [x] Twenty packs under `apps/api/app/guides/content/`, zh-TW, each with a hero photo, a
      self-drawn SVG diagram, a table, a callout, sources with `checked_on`, and partner
      blocks per the rules in `docs/travel-guides.md`; the packaged-content test passes for
      every pack in the directory (130, counting the life series from PR #467).
- [x] Every photograph from Wikimedia Commons under CC0 / Public domain / CC BY / CC BY-SA,
      licence and author read from the Commons API; every number on a diagram appears in
      the article text and no label is below 15 px; every diagram looked at after rendering.
- [x] Facts checked on official pages on the day of writing; anything unverified written
      as 以官網為準.

## Steps

The twenty (slug · kind · destination · topics):

1. `fuji-kawaguchiko-day-trip` · howto · tokyo · itinerary, nature, viewpoint
2. `nikko-day-trip-from-tokyo` · howto · tokyo · itinerary, culture, nature
3. `kansai-rail-passes-guide` · howto · osaka-kyoto · transport, budget
4. `himeji-castle-day-trip` · howto · osaka-kyoto · itinerary, culture, transport
5. `otaru-day-trip-from-sapporo` · howto · sapporo · itinerary, food, culture
6. `sapporo-snow-festival-2027` · intel (2027-02-15) · sapporo · season, culture
7. `yufuin-beppu-2-day-from-fukuoka` · howto · fukuoka · itinerary, hotel, culture
8. `takayama-shirakawago-day-trip` · howto · nagoya · itinerary, culture, nature
9. `japan-car-rental-expressway-guide` · howto · none · transport, budget
10. `nami-island-petite-france-day-trip` · howto · seoul · itinerary, nature, family
11. `seoul-palaces-hanbok-guide` · howto · seoul · culture, itinerary
12. `korea-ski-resorts-2026-2027` · intel (2027-03-15) · none · season, nature
13. `korea-money-exchange-wowpass-guide` · howto · none · budget, packing
14. `korea-food-guide-must-eat` · howto · none · food, etiquette
15. `bangkok-bts-mrt-boat-guide` · howto · bangkok · transport, budget
16. `ayutthaya-day-trip-from-bangkok` · howto · bangkok · itinerary, culture, transport
17. `chiang-mai-3-day-itinerary` · howto · chiang-mai · itinerary, culture, nature
18. `thailand-esim-sim-wifi` · howto · none · connectivity, packing
19. `vietnam-entry-2026-evisa` · intel (2027-03-31) · none · entry
20. `da-nang-hoi-an-4-day-itinerary` · howto · da-nang · itinerary, beach, culture

- [x] Twenty single-article writing agents from one spec (`article_brief_v5.md`: pack,
      Commons manifest, the SVG diagram drawn by the agent, a self-check that also renders
      the diagram with headless Edge so the agent looks at its own layout).
- [x] `ingest_pack5.py --check <slug>` then `ingest_pack5.py <slug>` per article: pydantic
      validation, structure and link rules, diagram rules (numbers vs text, labels >= 15 px),
      copy the SVG, fetch and licence-check the photos, write sizes and credits, save.
- [x] Run the packaged-content test, commit, open the PR; publishing on the host follows
      the deploy (`guides-import --dry-run`, then `--publish`).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.cli guides-import --actor-email <admin> --dry-run
```

Then `/zh-TW/guides/howto/<slug>` (or `intel`) for each of the twenty renders its hero,
diagram, table and partner blocks; `/sitemap.xml` carries twenty more entries with `lastmod`.

## Notes

- Internal links point at batch-4 slugs too. PR #460 merged on 2026-09-13 and this branch was
  fast-forwarded onto main after it (and after PR #467, the life series, which shares both
  directories without sharing a slug). The Taiwan articles have no zh-TW version, so nothing
  here links to them.
- Kawaguchiko and Nikko are filed under `tokyo`, Himeji under `osaka-kyoto`, Otaru and the
  Snow Festival under `sapporo`, Yufuin and Beppu under `fukuoka`, Takayama under `nagoya`,
  Nami Island and the palaces under `seoul`, Ayutthaya under `bangkok`: the city the reader
  is staying in and the destination filter they will use. Chiang Mai and Da Nang are
  primary destinations with their own food directories. Offers for sapporo / fukuoka /
  nagoya / bangkok / chiang-mai / da-nang and every hotel / connectivity block render
  nothing until the back office approves an offer for that city.
- How it was produced (2026-09-13 evening to 09-14): one agent per article from one brief.
  The Fable session limit stopped all twenty at 22:06, with files half written. After the
  reset, `SendMessage` resumed each agent in place, its research still in context, with a
  note naming the files it had not saved. At 08:15 the Fable model limit stopped the last
  four for good (Takayama, Bangkok transit, Ayutthaya, Vietnam entry). Those went to Opus
  agents told to treat whatever was on disk as an unverified draft and to list every fact
  they changed. Takayama came back with 13 corrections: last-bus times, "the only Important
  Cultural Property", pass prices whose only source was a 2023 press release on a page that
  now 404s. Vietnam came back with 13: entry ports, onward travel from Phu Quoc, a PAI airport
  list that only a foreign embassy notice gave, the customs allowances. Ayutthaya carried
  the Fine Arts Department's old 50 / 220 baht fees; the April 2026 notice says 80 / 300.
  A draft that passes the mechanical check is not a checked article.
- Found in review and fixed here, beyond each agent's self-check:
  - `thailand-esim-sim-wifi` said operators must build biometric registration within 180
    days. The cited summary of the NBTC amendment of 2026-05-15 says 180 days of data retention
    and nothing about biometrics. Rewritten to what it does say: non-Thai SIM registration in
    person with a passport, three per operator, activation within 60 days.
  - `chiang-mai-3-day-itinerary` gave a songthaew fare cap from a 2017 news report as current;
    removed.
  - Diagrams. Nami Island put the 42-minute B-line total on one leg. Himeji's Shinkansen note
    overlapped the Shin-Osaka label. Otaru's bus curve ran through a station name. The
    mechanical check sees none of these.
  - Heroes. Nikko's Yomeimon original stayed at 281 KB at JPEG quality 44, so it was swapped
    for Lake Chuzenji (CC BY 2.0). Nami Island's autumn photo stayed at 314 KB and was
    re-encoded instead: a 1 px Gaussian blur at quality 46 gives 199 KB. The article column is
    about 728 CSS px, so on a 2× screen that blur is under half a pixel. Re-running
    `ingest_pack5.py nami-island-petite-france-day-trip` overwrites the file; run
    `nami_hero.py` after it.
  - Tables. On a 375 px phone the renderer squeezes every column into the viewport: 44–58 px
    per column, rows 281–329 px tall. The five-column tables in Nami, Himeji, the Seoul palaces
    and both Thailand SIM tables were folded to four. 39 other tables in the repository still
    have five or more columns; the renderer fix is `2026-09-14-guide-tables-squeezed-on-phones`.
  - Credits. The Commons `Artist` field came back as a URL, a `ja:User:` link, "U.S. Navy
    photo by …", or a photographer's licence note, on six photos. `fix_credits5.py` tidies
    them; re-run it after any re-ingest.
- Rendered check: a mock API that serves this directory as published articles, plus
  `next dev` on port 3111. Checked with full-page headless Edge screenshots on desktop and
  with the in-app browser's 375 px preset. The first request after a cold compile shows
  「暫時無法取得這篇文章」 because the page's API fetch times out after 3 s; reload once.
  `next dev` rewrites `apps/web/next-env.d.ts`; restore that file before committing.
- Facts worth remembering:
  - Nikko: NIKKO PASS is now 3,000 yen (world heritage area, 2 days) and 8,000 yen (all
    area, 4 days). The Akechidaira ropeway is closed from 2026-01-16 to 2027-08-31.
  - Himeji: non-residents pay 2,500 yen since 2026-03-01. Repairs scaffold part of the
    grounds from 2026-07 to 2027-07. The Shosha ropeway stops from 2027-02-05.
  - Driving in Japan: JAF's licence translation is 6,000 yen and online only. A Taiwanese
    motor vehicles office issues it for NT$100 on the spot. The Japan–Taiwan Exchange
    Association does not issue it. The legal speed on roads without a centre line fell to
    30 km/h on 2026-09-01.
  - Hokkaido winter 2027: Sapporo Snow Festival 02-04 to 02-11, Otaru Yuki Akari no Michi
    02-06 to 02-13, Asahikawa 02-06 to 02-11.
  - Seoul: the combined palace ticket is 6,000 won, valid six months, and excludes the Secret
    Garden. The Bukchon red zone is open to visitors 10:00–17:00.
  - Hoi An's old-town ticket system changed on 2026-01-26 (120,000 VND).
  - Ayutthaya: Fine Arts Department tickets are 80 baht per site and 300 for the
    seven-site pass (April 2026 notice). MRT Bang Sue exit 3 leads to Krung Thep Aphiwat;
    exit 2 leads to the old Bang Sue station.
  - Vietnam: e-visa 25 / 50 USD, three working days, up to 90 days. Visa-free entrants to Phu
    Quoc must leave from Phu Quoc. The PAI pre-arrival declaration has been piloted at Tan Son
    Nhat since 2026-04-15 and is voluntary. Cash above 5,000 USD or 15,000,000 VND and gold
    jewellery from 300 g must be declared. E-cigarettes and heated tobacco are banned since 2025.
- The Bangkok transit agent found `bangkok-4-day-itinerary` (batch 4) out of date, and it is
  corrected in this PR. The 20-baht flat fare was never for foreign visitors, and the cabinet
  revoked it on 2026-06-23 (PRD). The orange-flag express boat runs only on weekday peaks
  under the timetable in force since 2026-06-23; weekday daytime and weekends use the daytime
  yellow-flag boat or the blue-flag tourist boat. The blue line's first and last trains no
  longer match the BEM table, so the article now points there. BTS core fares (17–47 baht)
  and MRT blue-line fares (17–44 baht since 2026-07-03) replace "以官網為準". The diagram note
  and description changed with it; the host import will list that article as updated.
- Bangkok: foreign bank Visa, Mastercard and UnionPay contactless cards work on the MRT blue
  and purple lines, not on the BTS or the Gold Line. BTS extension fares have been 17–45 baht
  since 2025-11-01, 65 baht at most across both sections. Bangkok taxis start at 35 baht.
  The Gold Line fare (16 or 17 baht, depending on which official page) and the Rabbit card
  fee (the fee PDF returns 404) are left unstated.
- Expiring on 2026-09-30, filed as `2026-09-14-refresh-kansai-lite-and-expressway-passes`:
  the current KANSAI RAILWAY PASS LITE edition, the TEP application window and the KEP user
  agreement.
- Publishing on the host happens after deploy: `guides-import --dry-run`, then `--publish`
  with the admin e-mail, as for the earlier batches.
