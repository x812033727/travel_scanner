---
id: 2026-09-08-continue-evidence-backed-remaining-hotspot-candidate
title: Continue evidence-backed remaining hotspot candidate review
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-08T09:35:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/hotspot-review-next-batch.md
  - ops/hotspot_review_next_batch.py
  - ops/hotspot_review_next_batch.json
---

# Continue evidence-backed remaining hotspot candidate review

## Why

After the 2026-09-08 exact-browser batch, 1,769 hotspots remain pending. Eleven of twelve independently checked Taipei/Kaohsiung candidates were approved and verified in all five locale ranking endpoints; Sun Yat-sen Memorial Hall remains pending because the building is closed. The user requested candidate review using the built-in browser or existing Gemini API, not indiscriminate approval.

## Definition of done

- [x] Claim a bounded next batch from the current pending set and document exact identities, current official sources, coordinate provenance and decisions.
- [x] Only candidates passing source, map and durable-coordinate checks are approved; unresolved items retain explicit reasons.
- [x] Writes use a fresh backup, actual effective administrator, full-snapshot guards, normal services and replay-safe audit receipts.
- [x] Verify public visibility/exclusion and report actual counts, without claiming the whole backlog is completed after one batch.

## Steps

- [x] Read docs/hotspot-review-2026-09-08.md and the scoped one-off script before adapting a new dated manifest.
- [x] Verify live pending data and relevant deployed code; prior containers and request authorization can expire.
- [x] Research an explicit next batch, independently verify evidence, apply and verify outcomes.

## How to verify

Run read-only snapshots and a complete dry-run before any apply. Verify original actual administrator attribution, strict publication_gaps, normal and supplemental audit counts, same-manifest replay, and public BFF rankings/intro eligibility. Use the existing deployment locks and verify pg_restore -l on new private backups. Run Ruff, Python compilation and task checks for changed artifacts.

## Notes

The working official interactive finder is https://maps-docs-team.web.app/samples/places-placeid-finder/dist/ (linked from Google's official example). CUA AX textbox input followed by Down/Return exposes the selected actual Place ID. Do not derive a Place ID from CID/hex, persist Google coordinates/screenshots, or use paid Google matching merely because the admin UI offers it. Current official notices override old closure pages. Wikidata raw P625 can differ from old stored coordinates; verify actual JSON rank/precision/provenance and never relabel coordinates blindly. Existing one-off authorization expires; obtain valid current attribution through the existing admin workflow, never invent an actor. No quota increase, new discovery or remote Git/deployment authorization is implied by this follow-up task. Full tool tests in this isolated worktree have a missing @playwright/test dependency; focused task tests pass.

## 2026-09-12 batch

`docs/hotspot-review-next-batch.md` has the full write-up and
`ops/hotspot_review_next_batch.json` the row-level receipt. Pending went 987 -> 458.

The batch was not bounded to a dozen rows: all 987 were judged from a pre-built Wikidata +
Wikipedia evidence pack, every proposed rejection was put to two independent skeptics (90 of
132 overturned, 42 applied), and the map-identity gate was filled for 469 keeps through the
admin's own `map-candidates` endpoint, which bills Text Search Pro rather than the Place
Details tier that was already exhausted for September.

Writes went through the normal `POST /admin/hotspots/review` route from a logged-in admin
session in the browser, so attribution and audit receipts are the ordinary ones; no one-off
server script and no invented actor. Coordinates stayed `wikidata` on every row.

What this task still covers:

- 123 Korean rows cannot be approved without a `map.naver.com/p/entry/place/` URL. Blocked on
  `2026-09-06-naver-maps-key`, though note the gate wants the URL, not the API key.
- 233 rows judged `unsure` - mostly Hong Kong and Bangkok streets and municipal buildings with
  two-sentence articles. These need a person who knows the city.
- 49 rows whose Google candidate was a different place, and 14 whose Place ID already belongs
  to a published row (a duplicate signal worth chasing).
- 12 unresolvable AI-candidate names worth re-seeding by hand; they are listed in the doc.

Two findings were filed separately: `2026-09-12-denylist-tombstones-real-attractions` (three
of PR #403's seven deny types would tombstone real sights on 2026-09-15) and the observation
that `collect_hotspots` downgrades every `auto_approved` candidate to
`pending / map_identity_required`, which is why whitelisting a type never publishes anything
on its own.

A second session was draining the same queue at the same time; 61 of the rejections and 18 of
the approvals in the production window are theirs, not this batch's.

## 2026-09-12 second batch

Pending 458 -> 346; see the second half of `docs/hotspot-review-next-batch.md`.

Three things were settled that the next session should not re-litigate:

- **Korea is not model-solvable.** The gate takes only a `map.naver.com/p/entry/place/` URL,
  `map.naver.com` is policy-blocked in the browser, Wikidata has no NAVER Map place property,
  and only 1 of the 164 Korean rows' articles links NAVER at all (in the retired
  `siteview.nhn` form). It needs the key from `2026-09-06-naver-maps-key`, or a person.
- **A failed Google match is usually a bad query.** Re-query with the row's Wikidata
  local-language label plus its P131 administrative unit; that alone fixed 33 of 64.
- **`hotspot_map_identity_exists` has two cases.** Held by an approved row = the pending row is
  a duplicate. Held by a *rejected* row = a `candidate_import` tombstone is squatting a real
  attraction's identity; clear it with `action:'update', google_place_id: null` and approve the
  live row. Four sights were recovered that way.

Still open:

- 164 Korean rows, 40 rows deliberately parked until the 2026-09-15 discovery pass adopts them
  by QID, ~30 rows whose Google candidate is a different place (several because the *stored*
  coordinate is wrong - 新營美術園區 is 76 km out, 旗山聖若瑟天主堂 32 km), and 37 rows the
  second pass still could not decide.
- **Rejections awaiting verification.** 80 were proposed by the second pass; 15 were applied
  after both skeptics cleared them, 22 were refuted, and the remainder lost their verifier
  agents to a session limit. They were deliberately left pending: the workflow tally counts
  "no ruling" as "not refuted", so verified and unverified rejections have to be separated by
  counting rulings per row. Re-run the verify phase before applying any of them.

## 2026-09-12 third batch — non-Korean backlog cleared to 42

Pending 302 -> 206. Full write-up in `docs/hotspot-review-next-batch.md`.

Two things the next session should know:

- **The 40 "parked" rows were un-parked, because the plan behind them was wrong.** They had been
  given a Wikidata QID and left for discovery to adopt, but `geosearch` caps the radius at 10 km
  and the result count at 100 per centre, so 9 of them - Kabuki-za and Tokyo International Forum
  among them - could never have been re-discovered. Each row's own P625 coordinate was written
  directly instead. See `2026-09-12-discovery-only-sees-100-articles-per-centre`.
- **"An argument from absence is not a visitor reason."** That single rule settled most of the
  61 rows two earlier passes had deadlocked on. A stub article's silence does not prove the
  street is empty, and a park *near* a road is not a reason to visit the road.

What is left, and why it is not a model's job:

- 164 Korean rows, blocked on the NAVER gate.
- 6 rows escalated on purpose by two agreeing adjudicators. 大東亜聖戦大碑 is the type case: the
  facts are agreed, and the question - whether a Traditional-Chinese travel catalogue should list
  a monument that campaigners want removed for glorifying the war - is editorial.
  新福宮 is also here, and note it was on an earlier session's deliberate do-not-reject list.
- 33 keeps with no distinct Google POI: rivers, mountain passes, vanished city gates, and Tainan
  heritage buildings whose Place ID belongs to the site's modern occupant. Three query shapes
  were tried (stored name + city; Wikidata local label + P131 ward; hand-written). Further model
  passes will not help; these need a person or a different identity source.
- Huyện Sỹ Church specifically: its Wikidata P625 is ~30 km wrong and the Vietnamese article has
  no coordinate, so there is no durable source to write. Fixing Wikidata upstream would fix it.

## 2026-09-13 fourth batch — non-Korean backlog 41 -> 11

Pending 205 -> 175. Write-up in `docs/hotspot-review-next-batch.md`; the row receipt file now holds
both batches under a `batches` array (nothing reads it, so the shape was changed rather than
overwritten).

The third batch's conclusion — "further model passes will not help; these need a person or a
different identity source" — was half right. The identity source existed and was unused:

- **Places Autocomplete, not Text Search.** `GET /api/travel/places/autocomplete` bills the
  Essentials SKU (10,000 free a month, 98 used), returns five predictions instead of
  `map-candidates`'s single one, and reports `distanceMeters` per prediction. It needs any
  logged-in user, not an admin. It found identities the three earlier Text Search query shapes
  had missed.
- **Confirm every approval with the other tool.** All 12 candidates were re-run through
  `map-candidates` and the place IDs compared. Three disagreed, and two of those disagreements were
  real errors: 原臺南高等工業學校校舍 is a duplicate of the published 成大博物館 row, and 遍照寺's
  1 m "perfect" match is the temple's columbarium while the temple is 3.2 km away. **A 1 m match
  proves nothing if the stored coordinate is wrong in the same direction as the candidate.**
- **Korea, re-measured.** NAVER's own search API answers an unauthenticated caller with an
  `ncaptcha` challenge. Not workable, and not something to work around. Still blocked on
  `2026-09-06-naver-maps-key`.

What is left, and it is genuinely small:

- 164 Korean rows (unchanged, deliberately).
- 9 non-Korean rows, each with its blocker written into `review_reason`. Of the four that were held
  up only by a wrong upstream coordinate, **two were cleared the same day with `admin_verified`**
  after the site owner declined to edit Wikidata: Huyện Sỹ Church (OSM way 907280822, which is
  itself tagged `wikidata=Q10800886` and disagrees with that item by 31 km; French Wikipedia
  corroborates within 78 m) and 新福宮 (OSM node 5110491036, re-homed `taichung` -> `taipei`).
  遍照寺 and Thác Mây Treo were left alone on purpose — ja-wiki carries the *same* coordinate as
  Wikidata for the first, and Wikidata has no P625 at all for the second, so neither has a sourceable
  replacement that is not Google's.
- Wikidata remains wrong for Q10800886 and Q10306724. Our rows no longer depend on it.
- 臺北天空塔 stays pending on the site owner's instruction until it opens, because `discover_city`
  skips rejected rows and a rejection would be permanent.

Rankings lag the writes: `refresh_rankings` takes every active public row but only runs inside
`hotspot-collector`, which rebuilds every 21,600 s, so approvals surface publicly within six hours.

Filed from this batch: `2026-09-12-search-text` — `review` rewrites `city_name` when it re-homes a
row but never rebuilds `search_text`, and `collect_hotspots` skips approved rows, so a moved row
stays searchable under its old city forever (three rows are in that state now).
