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

---

# Second batch, same day: 458 -> 346

The first batch stopped at 458 because the type lever was exhausted and the first judgement
pass had left 233 rows "unsure". This batch attacked the three things that were actually
blocking those rows.

## Korea is unreachable, measured rather than assumed

164 of the 458 were Korean, and `has_exact_map_identity` accepts **only** a
`https://map.naver.com/p/entry/place/` URL for `KR` — a Google Place ID is never valid there.
Three independent routes were checked and all are closed:

- `map.naver.com` is blocked by policy in the browser pane, so the URL cannot be read by hand.
- Wikidata has no NAVER Map place identifier property at all (`Naver Encyclopedia`,
  `Naver movie`, `Naver VIBE`… exist; a map place ID does not).
- Of the 164 rows' Wikipedia articles, exactly **one** links `map.naver.com`, and in the
  retired `siteview.nhn?code=` form rather than the `p/entry/place/` form the gate requires.

So Korea needs the NAVER key (`2026-09-06-naver-maps-key`) or a person with a Korean browser.
No model pass can move it. That is a third of the remaining queue.

## Bad Google matches were bad queries, not a bad tool

64 rows had been judged keep but failed their Google lookup. Re-querying with the row's own
Wikidata **local-language label plus its P131 administrative unit** fixed 33 of them in one
pass:

| query that failed | query that worked |
|---|---|
| 善照寺 東京 (matched a same-name temple 11 km away) | 善照寺 杉並区 |
| 材木座海岸 鎌倉 (matched the neighbourhood) | 材木座海岸 材木座 → *Kamakura Zaimokuza Beach* |
| 清邁動物園 (matched the night zoo 8 km off) | สวนสัตว์เชียงใหม่ จังหวัดเชียงใหม่ |
| 打惱路玄天上帝廟 (1.9 km off) | ศาลเจ้าพ่อเสือ (เสาชิงช้า) |

## `hotspot_map_identity_exists` is a duplicate detector, and it has two cases

13 of those approvals were refused with a 409. Looking up who holds the Place ID splits them:

- **9 were held by an approved row** — the pending row genuinely duplicates a published
  attraction (朗豪坊 vs 朗豪坊購物商場, 原臺南公會堂 vs 吳園, Dinh III vs 保大宮). Rejected,
  naming the holder.
- **4 were held by a *rejected* row** — a `candidate_import` tombstone from 2026-09-07, with
  no rejection reason recorded, squatting the identity of a real attraction. Here the unique
  index was keeping a genuine sight out of the catalogue. Repaired by clearing the Place ID on
  the tombstone (`action:'update'`, `google_place_id: null`) and then approving the live row:
  警固公園, 臺中市孔廟, 國立工藝館, 海蔵寺 are now published.

## The intro was the problem, not the model

The 190 rows still undecided were re-judged with the **full** Wikipedia article instead of the
intro extract, plus Wikidata heritage/website/part-of/visitor statements. (`prop=extracts`
without `exintro` returns one page per request — `exlimit` does not apply to full text — so
these have to be fetched one at a time.)

| | first pass (intro) | second pass (full article) |
|---|---|---|
| keep | — | 93 |
| reject proposed | — | 80 |
| unsure | 190 | 37 |
| skeptic overturn rate | 68 % | ~25 % |

What the full article changed, concretely:

- **廣島市役所** — the intro says "city hall"; the body records the preserved basement of the
  old hall as a bomb-damage exhibition room, two A-bombed cherry trees, and a listing on
  Hiroshima's official tourism site.
- **仙台市立立町小學校** — an ordinary primary school, except for the 土井晚翠 school-song
  archive room opened inside it in 2003.
- **三井住友銀行橫濱支店** — a bank branch, in a 1931 Trowbridge & Livingstone building
  certified as a Yokohama historic structure in August 2025.
- **千田車廠** — a tram depot whose 1912 substation is a surviving A-bombed building, open to
  the public every 23 November with preserved A-bombed trams.

These are exactly the rows a two-sentence intro gets wrong in both directions.

## Result

| | start of batch | now |
|---|---|---|
| pending | 458 | **302** |
| approved | 1,763 | 1,874 |
| rejected | 1,668 | 1,713 |

111 approvals and 45 rejections in this batch. Public rankings have since rebuilt and the
whole day's work is live: Tainan 59 → 93, Bangkok 35 → 91, Kanazawa 31 → 66, Hiroshima
46 → 72, Hue 20 → 50, Kamakura → 89.

### The rejection accounting nearly went wrong

80 rejections were proposed. The verifier agents for 9 of the 14 batches were killed by a
session limit part-way through the run, and the script's own tally counts a row with **no
ruling** the same as a row **no skeptic objected to** — so its first result reported 60
surviving rejections when only 15 had actually been checked. Re-running the verify phase
(`resumeFromRunId`, so the decide agents replayed from cache and only the dead verifiers ran
again) settled all 80: **36 survived, 44 were overturned**. Two of the 15 that had looked
clean before the re-run — 広島市立竹屋小学校 and 大阪ガス御堂筋東ビル — were refuted by the
second skeptic, so applying the early list would have tombstoned them wrongly.

The lesson is narrow and worth keeping: when a workflow's verification stage can fail
independently of its decision stage, count rulings per row rather than trusting the aggregate.

## Carried forward

- **164 Korean rows** — blocked as described above.
- **40 rows parked on purpose** — the AI-candidate rows given a verified `wikidata_item_id`
  in the first batch. They have no coordinates until the 2026-09-15 discovery pass adopts them
  by QID; nothing should touch them before then.
- **Rejections awaiting their second opinion.** 80 rejections were proposed; 15 had both
  skeptics agree and were applied, 22 were refuted, and the rest lost their verifier agents to
  a session limit mid-run. Unverified rejections were deliberately **not** applied — the
  workflow's own accounting treats "no ruling" the same as "no refutation", which is wrong when
  the ruling never ran, so they were separated by counting rulings per row rather than trusting
  the tally.
- 37 keeps whose Google candidate is still a different place. A last targeted round with
  hand-written queries recovered 8 more (眾恩祠, Học viện Âm nhạc Huế, Đèo Prenn, Upper Peirce
  Reservoir, 臺中市立棒球場, Chợ Âm Phủ, Đình Hoàng Mai, Wat Phra That Doi Kham); the rest are
  rivers, mountain passes and vanished city-gate sites with no distinct POI to point at.
- **The stored-coordinate defect is small, measured.** Every pending row with a QID was
  compared against its own live Wikidata P625: only **4** are more than 1 km out
  (旗山聖若瑟天主堂 32 km, 秋盆河 12 km, 宏總亞太財經廣場 3.8 km, 물장오리오름 1.3 km). A further
  115 have no P625 at all — almost all Korean, where the coordinate came from the Wikipedia
  geosearch instead. So bad coordinates are not what is holding the queue up.
- One trap worth naming: when re-querying by hand it is easy to type an approximate coordinate
  into the drift check, which silently invalidates it. 眾恩祠 looked 1.6 km out and was 0.003 km
  out once the row's real coordinate was used.

---

# Third batch: 302 -> 206, and the 40 parked rows un-parked

## The parked rows were a mistake, caught by checking the claim

The first batch gave 40 identity-less AI candidate rows a verified `wikidata_item_id` and left
them for the 2026-09-15 discovery pass to adopt by QID. That was stated twice as settled. It was
only two-thirds true.

`discover_city` asks MediaWiki `geosearch` with `gsradius = min(radius_km * 1000, 10_000)` and
`gslimit = min(limit, 100)`. Both are hard API caps, and geosearch returns results ordered by
distance — so discovery can only ever see the **100 nearest articles within 10 km** of a city
centre, whatever `radius_km` says. Measuring the 40 parked rows against that ring:

- 31 fall inside it.
- **9 do not, and could never have been re-discovered**: Kabuki-za (10.7 km), Tokyo
  International Forum (10.3 km), Asakusa Hanayashiki (13.8 km), Cape Maeda (12.8 km), Sōgen-ji
  (17.1 km), Tsuboya Pottery Museum (17.6 km), Klong Muang Beach (16.8 km), Ko Thap (17.4 km),
  Huyện Sỹ Church (24.7 km).

So all 40 were un-parked instead: each row's own Wikidata P625 coordinate was written directly,
then matched and approved. 38 matched cleanly at once — Kabuki-za 0.043 km, 西本願寺 0.03 km,
Tokyo International Forum 0.044 km. 崇元寺 needed a second query (`崇元寺 沖縄市` returned the
street Sogenji-dori; `崇元寺石門 那覇市泊` returned the national-treasure gate at 0.003 km).
Huyện Sỹ Church is the one left: its Wikidata coordinate is ~30 km wrong and the Vietnamese
article carries none, so there is no durable source to write.

`2026-09-12-discovery-only-sees-100-articles-per-centre` tracks the underlying limit. It also
explains why the catalogue was missing Kabuki-za in the first place.

## The 61 rows two passes could not settle

These were sent to two independent adjudicators per batch, given the full article, the rejection
argument **and** the refutation that overturned it, and told explicitly what each verdict costs —
that "human" is not free, because it means a queue nobody clears. Only agreement decided.

| | |
|---|---|
| adjudicated | 61 |
| the two adjudicators agreed | 56 (92 %) |
| keep | 37 |
| reject | 18 |
| escalated to a human | 6 |

The recurring reason a rejection failed was named precisely by both adjudicators and is worth
keeping: **an argument from absence is not a visitor reason.** "The article is a two-sentence
stub, so something might be there" does not justify a keep; neither does pointing at a park or a
station *near* the street rather than on it. 京士柏道, 聖約翰里 and 運動場道 all fell that way.

What the adjudicators did keep, they kept on named evidence: 仙台市立東二番丁小學校 holds a
memorial Kannon for 23 children killed in the 1945 air raid with an inscription by 土井晩翠;
橫濱中央醫院 is a 1960 Yamada Mamoru building (the Tokyo Tower architect) in DOCOMOMO Japan's
208; 仙台中郵便局 and 仙台東二番丁郵便局 issue official 風景印 scenic postmarks, the same basis
on which 定山渓郵便局 is already published.

The six escalations are genuinely not model decisions. 大東亜聖戦大碑 is the clearest: both
adjudicators agreed on every fact — it is a real stone monument on the approach to 石川護國神社
with an annual festival — and both still refused, because whether a Traditional-Chinese travel
catalogue should list a monument that groups campaign to remove for glorifying the war is an
editorial judgement, not a factual one.

## Result

| | start of day | now |
|---|---|---|
| pending | 987 | **206** |
| approved | 1,294 | 1,952 |
| rejected | 1,608 | 1,731 |

**164 of the 206 are Korean** and blocked as described above. The non-Korean backlog is **42**:
the 6 human escalations, 3 rows whose Google candidate was wrong on this pass, and 33 keeps with
no distinct POI to point at — rivers (秋盆河, Sông Vàm Thuật), mountain passes (Đèo Tà Nung),
vanished city gates (臺灣府城小北門, 原臺灣府考棚遺構) and Tainan heritage buildings whose Place
ID belongs to the modern occupant of the site.

`ops/hotspot_review_next_batch.json` holds all 866 rows touched on 2026-09-12.

# Fourth batch, 2026-09-13: the non-Korean remainder, 41 -> 11

The third batch closed saying the 42 rows it left needed "a person or a different identity source",
because three shapes of Text Search query had failed on them. There was a different identity source,
unused: **Places Autocomplete**.

## Autocomplete is a different index path, and it was free

`POST /admin/hotspots/map-candidates` bills Text Search Pro and keeps only the **first** result.
The site's own `GET /api/travel/places/autocomplete` bills the **Essentials** tier — 10,000 free
requests a month, of which September had used 98 — returns up to **five** predictions, and with
`origin` set it reports `distanceMeters` for each one. It needs a logged-in user, not an admin.

September's Google budget at the start of this batch:

| SKU | used | free |
|---|---|---|
| Autocomplete Requests (essentials) | 98 | 10,000 |
| Text Search Pro | 3,713 | 5,000 |
| Place Details Enterprise | 904 | 1,000 (hard stop at 900) |

Two rounds of autocomplete — the Wikidata local-language label first, then a rewritten query built
from what the full article actually said the place is called today — produced an exact-name identity
for 15 of the 41 rows: the 11 that were approved, the three that are now blocked only on a wrong
coordinate, and 下北沢オープンソースCafe, whose identity was never in doubt and which was rejected on
what the venue is. What the rewrite looked like matters more than the tool: 成功大學舊總圖書館
found nothing, `成大未來館` found it at 8 m; `Thái Hà Ấp` returned phone shops on Phố Thái Hà,
`Lăng Hoàng Cao Khải` (the estate's surviving tomb, named in the article body) returned it at 13 m;
`Đền Ngọc Sơn` returned temples in Ninh Bình, `Đền Ngọc Sơn Hoàn Kiếm` returned the right one at 12 m.

## Every approval was confirmed twice, and the second pass caught two errors

After autocomplete picked a candidate, the same row went through `map-candidates` (Text Search Pro,
12 calls) and the two place IDs were compared. Nine of twelve matched outright. The three that did
not were the interesting ones:

- **遍照寺 (沖縄市)** — autocomplete's hit sat 1 m from the stored coordinate, which looks like a
  perfect match. Text Search returned a *different* 遍照寺 3.2 km away. The 1 m hit is
  「遍照寺沖縄市桃原霊苑かなさ」, the temple's columbarium; the temple itself is at 久保田1-2-5.
  **The stored Wikidata coordinate points at the cemetery, not the temple** — so the row stays
  pending rather than being approved onto a graveyard.
- **原臺南高等工業學校校舍** — its 本館 is 成大博物館, and `ChIJA2xpnZJ2bjQRbOkCD2qgHqE` is already
  held by the approved row `wikidata-q14581491`. The pending row is a duplicate.
- **喜屋武城** — the two tools returned two Google POIs at the same address: the park built on the
  castle site and the pavilion at its top. The park was taken.

The lesson is narrow and reusable: **a 1 m match is not proof, because the coordinate can be wrong in
the same direction as the candidate.** Two independent lookups disagreeing is what exposed it.

## Three rows were filed under the wrong city, and Wikipedia was the reason twice

- **新營美術園區** was in 高雄 with 高雄 coordinates. Wikidata has no P625 and zh-wiki's `{{coord}}`
  is 22.6199,120.2817 — Kaohsiung — while the article's own first sentence says 臺南市新營區. The
  row was re-homed to `tainan` and given 23.30498,120.30618 from the Tainan city government's own
  tourism page (`official_tourism`, https://www.twtainan.net/zh-tw/attractions/detail/5609/).
- **Thác Mây Treo** was in 順化; the Vietnamese article says xã Bà Nà / phường Hải Vân, Đà Nẵng.
  Re-homed to `da-nang`. Still pending: Google's waterfall is 3.7 km from the stored point.
- **新福宮** is the same failure as 新營美術園區 and could not be fixed the same way: Wikidata *and*
  zh-wiki both carry 24.1352,120.6894 (Taichung) while the article says 臺北市中山區新生北路二段.
  Google confirms the Taipei address and gives a Place ID; there is no auditable source for the
  correct coordinate, so it stays pending with both facts written into the row.

## Result

| | before | after |
|---|---|---|
| pending | 205 | **173** |
| approved | 1,953 | 1,966 |
| rejected | 1,731 | 1,750 |

The 41 non-Korean rows became 13 approved, 19 rejected, 9 still pending. **164 Korean rows are
untouched by choice** — NAVER's search API answers a `ncaptcha` challenge to an unauthenticated
caller, which is not something to work around, so the gate still wants a key or a person.

Rankings are a snapshot: `refresh_rankings` selects every active public row, and `hotspot-collector`
rebuilds it every 21,600 s, so the eleven appear in `/hotspots/rankings` within six hours of the
writes rather than immediately. Verified by reading the code and by confirming that older approved
rows (國立成功大學博物館, and 47 rows in Hanoi) do answer the same query.

## What the 19 rejections rest on

None of them rest on a thin article. Fourteen rest on a fact about the place:

- **gone**: 大圓環 (roundabout removed in the 1990s, now 美麗島站), 臺南火車站前圓環 (rebuilt into a
  ㄇ-shaped road in March 2026), 臺灣府城小北門 (demolished 1926; the surviving 門額 is a museum
  object), วังวรวรรณ (expropriated for a road), 野澤屋 (closed as 橫濱松坂屋).
- **closed or not open**: 新建國戲院 (closed 2016), บ้านพระอาทิตย์ (a newspaper's offices),
  原住吉秀松宅邸 (private, ownership in litigation), 原臺南長老教中學校講堂暨校長宿舍 (inside an
  operating high school).
- **covered by a parent already published**: 吉羊康泰 in 臺中公園, 臺北于右任銅像 in 國父紀念館,
  朴寶劍樹 in 中央公園, 原臺南高等工業學校校舍 = 成大博物館, 臺北市市政大樓 (whose twin row
  `wikidata-q9105560` an earlier batch rejected).

Three are editorial and were put to the site owner rather than decided by a model: 大東亜聖戦大碑
and 信義計畫區 were rejected on their instruction; 臺北天空塔 was kept pending on their instruction,
because a rejection is a tombstone discovery skips and the tower is only under construction.

晏架街 and 下北沢オープンソースCafe are the two judgement calls: a Mok Cheong street whose article
lists only the buildings on it (the 京士柏道 precedent), and a coworking space whose Google entry is
exact but whose nature is a place to work.

## The 9 still pending, and what each one waits for

| row | blocked on |
|---|---|
| 遍照寺 (沖縄市) | stored coordinate is the temple's columbarium, 3.2 km from the temple |
| Thác Mây Treo | re-homed to Đà Nẵng; Google's waterfall is 3.7 km from the stored point |
| 昭南神社 | only a `Syonan Jinja Historic Marker` 1.48 km away |
| 鎮平台 | only `Đồn Mang Cá`, an active military compound, 522 m away |
| 枳殻坂, Đèo Tà Nung, Lăng Trường Thiệu, Lục bộ | no Google POI after four query shapes each |
| 臺北天空塔 | still under construction |

## Two more rows were cleared without touching Wikidata

Four rows were blocked only by a coordinate that is wrong upstream. The site owner declined to edit
Wikidata, so two of them — the two where a replacement could be sourced and cross-checked — were
cleared with `admin_verified` instead, the vocabulary's own term for a coordinate a human vouched
for, each pointing at an auditable public URL. They are the last two entries in the approved list
above, not in the pending table:

- **Huyện Sỹ Church** → 10.768614, 106.688957, from OpenStreetMap way 907280822. That way is
  **tagged `wikidata=Q10800886`**, the row's own QID, so OSM and Wikidata disagree by 31 km about
  the same object. French Wikipedia independently gives 10.76878, 106.68966 — 78 m away.
  Italian Wikipedia carries Wikidata's wrong value, which is how the error spread.
- **新福宮** → 25.0562546, 121.5261696, from OpenStreetMap node 5110491036
  (「台北新福宮，新生北路二段62巷，中山里，中山區」), re-homed from `taichung` to `taipei`.
  Google independently returns the same street number. Wikidata and zh-wiki are 113 km out.

The other two were left alone on purpose:

- **遍照寺 (沖縄市)** — ja-wiki carries the *same* coordinate as Wikidata, so this is not a
  transcription slip, and the temple was building a new 本堂 as of October 2023 which may well be
  at the 桃原 site. There is no source for a replacement that is not Google's.
- **Thác Mây Treo** — Wikidata has no P625 at all; the coordinate comes from vi-wiki, and nothing
  available says whether it or Google's pin is the right one.

Wikidata itself is therefore still wrong for Q10800886 and Q10306724. Anyone with an account can
fix them; our rows no longer depend on it.

**One wart this left behind**: `POST /admin/hotspots/review` rewrites `city_name` when it re-homes a
row but never rebuilds `search_text`, and `collect_hotspots` skips approved rows, so a moved row
stays searchable under its old city forever. Three rows are in that state right now. Filed as
`2026-09-12-search-text`.
