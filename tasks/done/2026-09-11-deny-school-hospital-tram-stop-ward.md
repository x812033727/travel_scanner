---
id: 2026-09-11-deny-school-hospital-tram-stop-ward
title: Verify corrected hotspot deny types and protect historic attractions
status: done
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-11T16:53:58Z
completed_at: 2026-09-30T03:14:57Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/tests/test_hotspot_discovery.py
---

# Verify corrected hotspot deny types and protect historic attractions

The original seven-type policy below is historical. PR #561 superseded three of
those denials after pending-row review found real historic attractions. The
current acceptance criteria preserve that merged correction; this ticket must
not reinstate the blanket hospital, primary-school or military-base denial.

## Why

On 2026-09-12 production held 1,237 pending hotspots, 1,167 of them from the
2026-09-08 Wikimedia discovery pass. A random sample was mostly kindergartens,
primary schools, hospitals, tram stops, Vietnamese wards and office buildings:
their Wikidata types are not in `DENIED_TYPES`, so `classify_types` files them as
`unknown_type` and they land in the human queue. The weekly discovery pass rewrites
every pending row, so rows left pending never go away, and each pass can add more.
Rejected rows are tombstones and are never reopened, so denying a type is durable.

Separately, `discover_city` overwrote a denied candidate's status with
`pending / outside_city_radius` whenever it sat past the city radius, so a denied
type could still reach the queue.

## Definition of done

- [x] Four retained types are denied: Q56351315 Japanese high school,
      Q55521176 lower secondary school in Japan, Q2175765 tram stop and
      Q687188 ward of Vietnam.
- [x] Q9842 primary school, Q16917 hospital and Q245016 military base are not
      denied by type alone; they reach human review unless another classification
      applies, preserving the correction in PR #561.
- [x] Types that also describe an approved attraction still reach a human
      (Q5358913 elementary school in Japan, Q285783 intersection; streets unchanged).
- [x] Candidates outside the discovery radius are excluded; a denied candidate
      inside it stays rejected, matching the later bounded-radius implementation.
- [x] Merged as PR #403 (`7867d5dd`) and deployed 2026-09-12 in `6925e3d1`, which was
      verified to contain that commit.
- [x] Read the current deployed discovery result for the four retained types;
      inspect Q38278536, Q8669747, Q10911386 and Q2410409 for historical false
      rejection, recording any restoration needed separately before writing.

## Steps

- [x] Measure each candidate type against approved rows (stored `wikidata_types` for
      235 rows, live Wikidata P31 for the other 1,012 QIDs).
- [x] Extend `DENIED_TYPES` and fix the radius override.
- [x] Unit tests for both.
- [x] Merge and deploy.
- [x] Check a current discovery pass and the four historic-attraction rows;
      the original 2026-09-15 schedule is no longer a future checkpoint.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_hotspot_discovery.py
```

After verifying the deployed corrected policy, inspect the latest discovery
pass read-only, grouped by actual Wikidata type and review status. Aggregate
`denylisted_type` growth alone cannot distinguish intended rejection from lost
historic attractions. Also inspect Q38278536, Q8669747, Q10911386 and Q2410409
individually; source and map review are required before any restoration.

## Notes

Impact measured 2026-09-12 (pending / approved / rejected rows carrying the type, from
stored `wikidata_types`): Q9842 13/0/54, Q16917 9/0/33, Q2175765 8/0/5, Q687188 6/0/77,
Q56351315 5/0/17, Q245016 5/0/0, Q55521176 4/0/26. About 50 pending rows in total.

Rejected as denylist candidates because they would hit an approved attraction:
Q5358913 (袋町小学校平和資料館), Q285783 (Shibuya scramble crossing, 銀座四丁目),
Q27686 hotel, Q35054 post office, Q1021645 office building, Q655686 commercial
building, Q5327369 chōchō (each had at least one approved row). A type is denied if
*any* of a candidate's P31 values matches, so one approved hit is enough to exclude it.

The 173 Gemini reject recommendations from catalog-review run `d943205e` are a
separate, time-limited operational step: the next discovery pass rewrites those rows,
which changes their snapshot fingerprint and makes the assessments unappliable.

### 釋出認領（由站主授權，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

PR #403 於 2026-09-11 合併。原持有者 claude-opus-5（2026-09-11 認領）。剩下的兩項都是 2026-09-15 那一輪探索之後的查核，還沒有紀錄。

這張票和 `2026-09-12-denylist-tombstones-real-attractions`（P1）的 scope 完全相同，持有它就讓那張認領不到，所以改回 open。建議由接手 denylist-tombstones 的人一起做這裡的查核。

### 2026-09-29 local P1 reconciliation (codex-p1-product)

Claimed for the owner-authorized P1 review. The matching implementation PRs are
merged and no matching open PR or active same-feature implementation was found.
The former broad scopes have been narrowed to this local acceptance work. Forced
claims only bypass historical/shared scope metadata; no other agent application
changes are taken over. No production or cloud-account access is included.

Current-code evidence: `test_measured_non_attraction_types_are_rejected` checks
all four retained types; `test_types_that_also_describe_real_sights_reach_the_human_queue`
checks all three released types and mixed-type precedence. The radius test checks
outside-radius exclusion and inside-radius denial. These passed on 2026-09-29
together with community contracts: 52 passed, 8 PostgreSQL/S3 cases skipped.
No application changes or policy decision were needed. The outstanding live
status check remains open; this local pass cannot establish deployed row state.
### 2026-09-30 live check (claude-opus-5-5, read-only transaction on production)
Latest Wikimedia discovery pass: `last_seen_at` 2026-09-29 10:08 UTC (3,403 of
5,913 discovery rows seen in the last 8 days). Rows by stored `wikidata_types`,
status and reason (reasons bucketed: `denylisted_type`, a reviewer's text, or none):

| Type | Policy | Result on 2026-09-30 |
| --- | --- | --- |
| Q56351315 JP high school | denied | 40 `denylisted_type` (last seen 09-29), 22 reviewer-rejected |
| Q55521176 JP lower secondary | denied | 55 `denylisted_type` (09-29), 30 reviewer-rejected |
| Q2175765 tram stop | denied | 37 `denylisted_type` (09-29), 11 reviewer-rejected, 1 reviewer-approved (西4丁目) |
| Q687188 ward of Vietnam | denied | 55 `denylisted_type` (09-29), 81 rejected earlier |
| Q9842 primary school | review | 65 pending `unknown_type` (09-29), 1 approved, 66 reviewer-rejected |
| Q16917 hospital | review | 46 pending `unknown_type` (09-29), 2 approved, 40 reviewer-rejected |
| Q245016 military base | review | 3 pending `unknown_type` (09-29), 2 approved, 3 reviewer-rejected |

So the deployed policy is the corrected one: the four retained types are denied
on the latest pass, and the three released types reach the human queue rather
than being rejected by type.

The four historic rows are all `approved` and active: Q38278536 喜屋武城 (OKA,
military base), Q8669747 鎮平台 (HUI, military base; restored 2026-09-19 after the
09-12 type denial), Q10911386 原花園尋常小學校本館 (TNN, primary school) and
Q2410409 島醫院 (HIJ, hospital). No restoration is needed.

The approved tram stop keeps its decision: `run_discovery` (service.py) only
touches `last_seen_at` for curated or approved rows and never re-classifies them,
so a denied type cannot overwrite a reviewer's approval. No code change.
