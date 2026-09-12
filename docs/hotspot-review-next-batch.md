# Hotspot review, 2026-09-12 batch: the whole pending queue

This batch took the pending hotspot queue from 987 rows to 458. It follows
[`hotspot-review-2026-09-08.md`](hotspot-review-2026-09-08.md), which reviewed twelve rows
by hand; this one judged all 987 and then filled the map-identity gate for everything the
judgement kept.

## What the queue actually was

Earlier passes had already removed the obvious noise, so "review the backlog" was the wrong
model of the problem. Measured against the full `P31` set of all 1,294 approved attractions
(the 1,056 without stored `wikidata_types` were read live from Wikidata):

| bucket | rows | meaning |
|---|---|---|
| whitelisted type | 151 | `classify_types` said `auto_approved`; `collect_hotspots` downgrades every one of those to `pending / map_identity_required`, so a clean candidate still waits for a Place ID |
| review-only type | 97 | temple, shrine, wat, urban park, art museum, Chinese temple |
| unknown type | 536 | 287 distinct `P31` values |
| no stored type | 186 | 60 of them AI candidates with no Wikidata identity at all |

The type lever was exhausted. Of the 287 unclassified types only 26 are carried by zero
approved attraction and appear on two or more pending rows — 68 rows in total — and reading
them one by one (sports venue, live house, arena, ryōtei, hawker centre, kiridōshi, gosho,
three-storied pagoda) showed none is safe to deny outright. **The queue was a Place ID
backlog, not a review backlog.**

## How the 987 were judged

An evidence pack was built first so no judgement depended on a live fetch: Wikidata label,
description and `P31` labels for every row (927 entities), plus the Wikipedia intro extract
(927 of 987 matched), plus the previous AI pass's note.

50 agents judged 20 rows each against an explicit policy — reject only for `not_a_place`,
`no_visitor_draw`, `too_broad`, `gone` or `duplicate`, and default to `unsure`, because a
rejection is a permanent tombstone. Calibration examples were drawn from rows the catalogue
has **already published**, so a category never decides on its own: 蘭桂坊 is a street,
濱海灣金沙 a hotel, 橫濱球場 a stadium, 廣島市立袋町小學校 a school, 定山渓郵便局 a post
office.

Every proposed rejection then went to two independent skeptics with different briefs — one
hunting for a reason a traveller *would* go, one checking the reject code against the
evidence — with instructions to refute when the evidence was too thin for a tombstone.

| | rows |
|---|---|
| judged | 987 |
| keep | 712 |
| unsure | 233 |
| rejection proposed | 132 |
| **overturned by a skeptic** | **90** |
| rejection applied | 42 |

The 68 % overturn rate is the finding, not a defect: the queue's remaining rows are mostly
real places, and two-thirds of the rejections a single pass proposed did not survive contact
with a second opinion.

## Filling the map-identity gate

`review_hotspot_candidates` refuses `action=approve` unless `map_match_status='verified'`,
and `_validate_hotspot_location` is pure local validation — writing a Place ID and approving
costs no Google call. Only *finding* the Place ID does.

Place Details Enterprise was already at 904 of its 1,000 free calls for September (the
automatic stop is at 900), so `match-hotspot-places` could not run at all. The admin's own
`POST /admin/hotspots/map-candidates` bills Text Search **Pro** instead
(`places_text_search_locate`, 2,921 of 5,000 used), returns one candidate for manual
confirmation and never writes Google coordinates into the catalogue. That was the route.

533 non-Korean keeps were queried, one call each. The returned name was then matched against
**every** Wikidata label and alias for the row's own QID, not just its stored name — Google
answers in the viewer's locale, so 亞皆老街 comes back as "Argyle Street" and きらめき通り as
"Kirameki-Dori", and a plain string comparison rejects both.

- 309 rows scored ≥ 0.75 against some alias and sat within 300 m: applied automatically.
- 223 rows failed that bar and were read one by one. 174 were the same place under a
  translation or a 異體字 variant (イオンモール沖縄ライカム / 永旺夢樂城沖繩來客夢,
  韓国人原爆犠牲者慰霊碑 / 韓國人原爆犧牲者慰靈碑); 49 were not, and stay pending.
- Rejected on distance alone: 善照寺 and 龍光寺 matched同名 temples 11 km away, 清邁動物園
  matched the night zoo 8 km off, 秋盆河 matched 45 km away.
- 14 approvals were refused with `hotspot_map_identity_exists`: that Place ID already belongs
  to a published attraction, which is itself a duplicate signal. Those rows stay pending.

Coordinates and `coordinate_source_type` stay `wikidata` on every approved row; Google
supplied only the identity.

## The 60 AI-candidate rows

`origin='gemini_candidate'` rows had no QID, no coordinates and no Wikipedia article, so they
could never pass the gate. Resolving each name against Wikidata and keeping only matches
inside the city's own discovery radius:

- 8 duplicated a row the catalogue already had → rejected.
- 40 got their verified `wikidata_item_id` written in. `collect_hotspots` keys on that column,
  so the next discovery pass adopts the row and fills its coordinates and types
  (西本願寺 Q1146038, 東本願寺 Q910281, Kabuki-za Q3082575, Tokyo International Forum
  Q1359892 …). Rejecting them would have been wrong: none is in the catalogue yet.
- 12 could not be resolved to any entity inside the radius → rejected. Rejecting a row with a
  null `wikidata_item_id` is safe: `discover_city` matches on that column, so a future pass
  can still add the real place under its own QID. They are worth re-seeding by hand:
  Thang Long Water Puppet Theatre, Phra Nang Cave Beach, Khao Ngon Nak, O Quan Chuong Gate,
  Turtle Lake (Hồ Con Rùa), Araha Park, Chatan Sunset Beach, JR Tower Observatory T38,
  Baan Chinpracha, Susan Hoi, Hat Noppharat Thara, Ton Duc Thang Museum.

## Result

| | before | after |
|---|---|---|
| pending | 987 | 458 |
| approved | 1,294 | 1,763 |
| rejected | 1,608 | 1,668 |

469 approvals and 60 rejections in this batch; a second session working the same queue
contributed another 18 approvals and 61 rejections in the same window, which is why the
production totals move further than this batch alone. `ops/hotspot_review_next_batch.json`
is the full row-level receipt read back out of production.

Rankings are snapshot-driven: `hotspot-collector` rebuilds every 21,600 s (6 h), so the new
rows reach `/api/travel/hotspots/rankings?destination_id=<city>` within that window without
anything being run by hand.

## What is left, and why

- **123 Korean rows.** `has_exact_map_identity` requires a `https://map.naver.com/p/entry/place/`
  URL for `KR`, never a Place ID. NAVER is not configured — see
  `tasks/open/2026-09-06-naver-maps-key.md`. Note the gate wants the *URL*, not the API key,
  so these are unblockable by hand as well as by key.
- **233 `unsure` rows**, mostly Hong Kong and Bangkok streets and市政 buildings where the
  Wikipedia article is two sentences long. They need a human who knows the city, not another
  model pass.
- **49 rows whose Google candidate was a different place**, and **14 whose Place ID is already
  taken** by a published row.
- Text Search Pro usage after this batch is roughly 3,700 of 5,000 for September.
