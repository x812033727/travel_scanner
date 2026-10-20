---
id: 2026-10-20-brand-story-airbnb-x14
title: Brand story Airbnb X14
status: in-progress
priority: P1
area: docs
owner: codex-x14
claimed_at: 2026-10-20T20:08:28Z
created_at: 2026-10-20T20:08:25Z
completed_at:
branch: codex/brand-story-airbnb-x14
depends_on: []
scope:
  - docs/videos/story-everyday-airbnb-x14
  - tasks/open/2026-10-20-brand-story-airbnb-x14.md
---

# Brand story Airbnb X14

## Why

The owner wants another missing-brand film, one reviewable episode per PR, under the 奇聞檔案局 / brand-story rules. Airbnb is absent from the approved 100-title bank and X01–X13. Its 2020–2022 SEC filings support a concrete two-sided marketplace story: March–April cancellations exceeded new gross booked nights/experiences, Airbnb supported some hosts and cut costs, nearby and longer stays gained importance, then it reported its first full GAAP profitable year in 2022. The film must distinguish those observations from the unsupported claim that any single move caused the profit.

## Definition of done

- [ ] Source-verified main film with measured substantive body at least 8:00 (about 10 minutes target), a meaningful hook every 30–45 seconds, two independent 25–55-second Shorts, official 5-second / 21-second bookends, Traditional Chinese optional CC, and reviewable source, script, and visual evidence.
- [ ] Keep paid media and retries within the owner-authorized US$25 per episode cap; record real upload URLs only after upload.
- [ ] Submit a draft PR for this episode only after an independent source audit and two fresh blind reviews of the frozen script and Shorts.

## Steps

- [x] Confirm non-overlap with the 100-title bank and X01–X13; create isolated X14 branch/worktree.
- [x] Fetch and hash original SEC filings/exhibits; draft source matrix, six-chapter Treatment, and two standalone Short concepts.
- [x] Independent agent re-fetched originals and audited the source packet; corrected the period and host-retention HOLD items. V1–V3 full-script audits were HOLD; V4 independent full-script SEC audit passed at 831b75d6. V5 independent audit at 8acb3120 held on two visual mismatches; V6 needs a fresh audit bound to its own hashes.
- [x] Write source-bound full narration, two standalone Shorts, visual plan, and production schemas; revise after V1–V5 blind review HOLD/NO votes and run local content checks. Two fresh V6 blind reads remain pending.
- [ ] Produce and QA the episode and Shorts within the approved cost, then open the episode PR.

## How to verify

Read `docs/videos/story-everyday-airbnb-x14/source-matrix.md`, download its four SEC originals and compare response byte counts and SHA-256. Check each claim's period and denominator. Later run the story/video schema and lint gates and inspect generated media. `npm run check:tasks` validates this task file. No generated media exists in the source-packet phase.

## Notes

2026-10-20: Worktree `/workspace/travel_scanner_airbnb_x14`, branch `codex/brand-story-airbnb-x14` based on `origin/main` ec2c7676. Source packet lives at `docs/videos/story-everyday-airbnb-x14/`. Four worker-readable SEC HTML originals are all under 3 MB. The 2022 10-K is 3,213,119 bytes, so use it only for reviewer cross-checks; the worker-readable 2022 Q4 shareholder letter supports the core end claims. Do not use 2020 GAAP net loss as a proxy for the pandemic demand shock: it includes $2.8bn of IPO-triggered RSU expense and $868.5m full-year noncash warrant fair-value change. The shareholder letter separately gives $827m for **Q4** warrant revaluation; do not interchange quarter and full year. Do not equate gross nights, net Nights and Experiences Booked, gross booking value, company revenue, or net income. No paid calls, full script, upload, or PR in this source-packet phase.

2026-10-20 later: Independent source-packet audit `reviews/source-audit-independent.md` at ae3cf24e was HOLD on per-month overclaim and listing-total-to-host-retention inference. Packet wording corrected in c3ecafe2. **Historical V1, superseded:** `video.json` SHA-256 `9eccafcb326cebca68d266114d744fbae3fa8c770aa20f081d6dd8e28e7ff8ce`, `shorts.json` SHA-256 `d678fd8db68586aeb2b64220004069d4c0e5ca023732841777ba33b7054edfaa`; the independent full-script source audit at a864fb82 was HOLD (host-support cutoff misapplied to guest refund and second-half 2020 demand framed too broadly), and blind A at fc84e3a7 voted NO on main and both Shorts (opening spoiled outcome, chronology doubled back, weak first Short frame and other story issues). These receipts remain as historical evidence, not V2 clearance.

2026-10-20 historical V2, superseded: Exact `video.json` SHA-256 `c41007ae00092640cfe996440fc7d655ea4a9564d851c13539a682b089abaf94`, `shorts.json` SHA-256 `006c146155f7f2f0e9707cc31ee4948ec8698dc1f52f9c2ee7754044862c0242`. Deterministic build: 135 spoken lines, 30 native number cards, 102 image-01 illustration candidates, 16 loops; hook 246 characters, substantive body 2,657 characters (paper estimate 8.86m at 300 cpm); Shorts 169 and 185 characters. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. Independent source audit `reviews/source-audit-v2-independent.md` at a199d63c was HOLD on active-listing denominator, inclusive stay thresholds and actual cohort movement; blind A `reviews/blind-a-v2-independent.md` at c98b9adb voted NO on spoiler, list-style eligibility, an unresolved question and Short 2. These receipts are historical only.

2026-10-20 historical V3, superseded: `video.json` SHA-256 `8c1b2fc9d699851e42d3cc7fe59d40ea0560ef393f3a8fe60eb462f9548bab0f`, `shorts.json` SHA-256 `545a0844636cbc769afb9254824a6a68bbaf0006ebcbbe37b58344ae5a04252c`. Deterministic build: 135 spoken lines, 30 native number cards, 102 image-01 illustration candidates, 16 loops; hook 241 characters, substantive body 2,677 characters (paper estimate 8.92m at 300 cpm); Shorts 169 and 189 characters. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. Independent SEC audit `reviews/script-source-audit-v3-independent.md` at ae60f33d HOLD: A2's hosting includes homes and experiences, the mixed 5.6m listing image used room keys, and the seven-night image excluded exactly seven. Blind A `reviews/blind-a-v3-independent.md` at 96beb7e4 HOLD 8/12 on opening spoiler, opening-to-chapter restart, 2021 repeat and 2022 number ladder; blind B `reviews/blind-b-v3-independent.md` at 12aabc4e HOLD 6/12 on spoiler, causal story, payoff, repetition and explanatory detours. All three receipts are historical, not V4 clearance.

2026-10-20 V4 frozen for new independent review: `video.json` SHA-256 `23f057225c826b5687559fb7a47ea58c5b00eeb342f460a9c8a5484de1b84a62`, `shorts.json` SHA-256 `545a0844636cbc769afb9254824a6a68bbaf0006ebcbbe37b58344ae5a04252c`. Deterministic build: 135 spoken lines, 27 native number cards, 105 image-01 illustration candidates, 19 loops; hook 228 characters, substantive body 2,696 characters (paper estimate 8.99m at 300 cpm; no audio timing yet); Shorts 169 and 189 characters. V4 removes future outcomes from the condensed opening, moves chapter two forward with the cancellation notice, follows the next-booking problem through company choices and observed demand, trims the 2022 spoken numeric ladder, and preserves source period/denominator/accounting/refund limits. It broadens A2's hosting to homes and experiences, pictures 5.6m as mixed listing tokens, and includes exactly seven nights in the ≥7-night illustration. Shorts narration is unchanged but its referenced main-film shots have changed and require new blind inspection. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. New source audit and two fresh blind reads must bind **these** hashes; any JSON change invalidates them. No paid call, image, TTS, official animation workfile, MP4, upload or URL exists. Global picture-judge quota is reserved for older in-flight episodes, so do not start X14 bulk art until actual available quota and full-episode US$25 ledger are checked. Production quote and publishing handoff are in this folder.

2026-10-20 V4 review result, historical: independent SEC audit `reviews/script-source-audit-v4-independent.md` passed at 831b75d6 for the V4 frozen JSON. Fresh blind A `reviews/blind-a-v4-independent.md` at f4f63a58 and blind B `reviews/blind-b-v4-independent.md` at 9a6a07be each voted HOLD (8/12), citing spoken outline/recap, weak named callbacks, the 2022 figure ladder, and missing Short portrait specifics. These receipts are **not** V5 clearance.

2026-10-20 V5 frozen for new independent review: `video.json` SHA-256 `e38a12eef5f51da9eb13b8a1cab3bb7b7fdc867889e7580ae1c11cd1b961c199`; `shorts.json` SHA-256 `b581e9f717769bace170833d8ef48c36b7b499fcf306baaa40542dffbf31ac2e`. Deterministic build: 119 spoken lines, 26 native number cards, 90 image-01 illustration candidates, 19 loops; 158-character condensed opening and 2,429-character substantive body (paper estimate 8.10 minutes at 300 characters/minute). The timeline estimator gives 11:31 before official bumpers and approximately 11:57 including 5-second opening and 21-second ending placeholders, not measured audio. Shorts are 169 and 192 characters. V5 plants distinct future moments without their outcomes, names their callbacks, replaces spoken roadmaps with events, removes repeated support/ratio recaps and cuts the 2022 metric ladder. Short 2 voices its 2021 Q4 date. The visual plan specifies all 16 portrait beats, including two native 9:16 remakes of statistical cards, with crop/safe-area/CC constraints but no render claim. V5 keeps the V4 SEC denominator, date, refund and accounting guardrails. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. New independent SEC audit and two fresh blind reads must bind **these** hashes; any JSON change invalidates them. No paid call, image, TTS, official animation workfile, MP4, upload, URL, or PR exists; task remains open.

2026-10-20 V5 independent reviews, historical: SEC source/image audit `reviews/script-source-audit-v5-independent.md` at 8acb3120 HOLD because the cross-border traveler narration used a long-stay analyst prompt and Short 1's noncash warrant line used booking-bowl art. Blind A `reviews/blind-a-v5-independent.md` at 635c2c74 voted FAIL 5/12 on the generic opening, spoken question outline, body restart, unpaid governing question, repeated result, and finance detours; blind B `reviews/blind-b-v5-independent.md` at 513334cf voted HOLD 11/12 chiefly on the same unpaid question. These bind only V5 and cannot clear V6.

2026-10-20 V6 frozen for new independent review: `video.json` SHA-256 `0eff8316af17596f5d411941569632b99fbee96c5cda3dce32bc2a3cd788bed9`; `shorts.json` SHA-256 `b9bf67b88b1a16211ac76ffbebace8fdd39b8794582722956b9eb270f3c2395f`. Deterministic build: 119 spoken lines, 26 native number cards, 90 image-01 illustration candidates, 19 loops; 196-character condensed opening and 2,501-character substantive body (paper estimate 8.34 minutes at 300 characters/minute, pending audio). Opening's March 20 cancellation is explicitly representative and fictional, followed by dated loan, staff and search actions whose specifics pay off later. Chapter two begins with that cancellation's consequence; the ending answers how another transaction could reconnect traveler and host without crediting any one step for profit. Cross-border art now depicts a traveler crossing an unlettered border, and Short 1's warrant beat uses the annual ledger with its separate valuation column. Short 2's 2019 comparison is a native portrait 2019 Q4 card. All 16 Short beats carry planned, unrendered 1080×1920 safe-area and crop/rebuild instructions in `shorts.json`. New SEC source/image audit and **two fresh blind reads** must bind these V6 hashes; prior passes do not transfer. No paid call, image, TTS, official animation workfile, MP4, upload, URL, or PR exists; task remains open.

V6 local checks on those exact JSON bytes: video lint 0 errors／0 warnings; both Shorts validate with all 16 per-beat portrait plans present; `npm run test:docs-videos` 236／236; `npm run check:tasks` exit 0 with unrelated stale-claim warnings; `git diff --check` exit 0. These structural checks are not a substitute for independent source/image or blind review.
