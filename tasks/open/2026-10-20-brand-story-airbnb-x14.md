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
- [x] Independent agent re-fetched originals and audited the source packet; corrected the period and host-retention HOLD items. V1–V3 full-script audits were HOLD. V4 corrects hosting scope and two picture prompts; new full-script source audit is pending.
- [x] Write source-bound full narration, two standalone Shorts, visual plan, and production schemas; revise after V1–V3 blind review HOLD/NO votes and run local content checks. Two fresh V4 blind reads remain pending.
- [ ] Produce and QA the episode and Shorts within the approved cost, then open the episode PR.

## How to verify

Read `docs/videos/story-everyday-airbnb-x14/source-matrix.md`, download its four SEC originals and compare response byte counts and SHA-256. Check each claim's period and denominator. Later run the story/video schema and lint gates and inspect generated media. `npm run check:tasks` validates this task file. No generated media exists in the source-packet phase.

## Notes

2026-10-20: Worktree `/workspace/travel_scanner_airbnb_x14`, branch `codex/brand-story-airbnb-x14` based on `origin/main` ec2c7676. Source packet lives at `docs/videos/story-everyday-airbnb-x14/`. Four worker-readable SEC HTML originals are all under 3 MB. The 2022 10-K is 3,213,119 bytes, so use it only for reviewer cross-checks; the worker-readable 2022 Q4 shareholder letter supports the core end claims. Do not use 2020 GAAP net loss as a proxy for the pandemic demand shock: it includes $2.8bn of IPO-triggered RSU expense and $868.5m full-year noncash warrant fair-value change. The shareholder letter separately gives $827m for **Q4** warrant revaluation; do not interchange quarter and full year. Do not equate gross nights, net Nights and Experiences Booked, gross booking value, company revenue, or net income. No paid calls, full script, upload, or PR in this source-packet phase.

2026-10-20 later: Independent source-packet audit `reviews/source-audit-independent.md` at ae3cf24e was HOLD on per-month overclaim and listing-total-to-host-retention inference. Packet wording corrected in c3ecafe2. **Historical V1, superseded:** `video.json` SHA-256 `9eccafcb326cebca68d266114d744fbae3fa8c770aa20f081d6dd8e28e7ff8ce`, `shorts.json` SHA-256 `d678fd8db68586aeb2b64220004069d4c0e5ca023732841777ba33b7054edfaa`; the independent full-script source audit at a864fb82 was HOLD (host-support cutoff misapplied to guest refund and second-half 2020 demand framed too broadly), and blind A at fc84e3a7 voted NO on main and both Shorts (opening spoiled outcome, chronology doubled back, weak first Short frame and other story issues). These receipts remain as historical evidence, not V2 clearance.

2026-10-20 historical V2, superseded: Exact `video.json` SHA-256 `c41007ae00092640cfe996440fc7d655ea4a9564d851c13539a682b089abaf94`, `shorts.json` SHA-256 `006c146155f7f2f0e9707cc31ee4948ec8698dc1f52f9c2ee7754044862c0242`. Deterministic build: 135 spoken lines, 30 native number cards, 102 image-01 illustration candidates, 16 loops; hook 246 characters, substantive body 2,657 characters (paper estimate 8.86m at 300 cpm); Shorts 169 and 185 characters. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. Independent source audit `reviews/source-audit-v2-independent.md` at a199d63c was HOLD on active-listing denominator, inclusive stay thresholds and actual cohort movement; blind A `reviews/blind-a-v2-independent.md` at c98b9adb voted NO on spoiler, list-style eligibility, an unresolved question and Short 2. These receipts are historical only.

2026-10-20 historical V3, superseded: `video.json` SHA-256 `8c1b2fc9d699851e42d3cc7fe59d40ea0560ef393f3a8fe60eb462f9548bab0f`, `shorts.json` SHA-256 `545a0844636cbc769afb9254824a6a68bbaf0006ebcbbe37b58344ae5a04252c`. Deterministic build: 135 spoken lines, 30 native number cards, 102 image-01 illustration candidates, 16 loops; hook 241 characters, substantive body 2,677 characters (paper estimate 8.92m at 300 cpm); Shorts 169 and 189 characters. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. Independent SEC audit `reviews/script-source-audit-v3-independent.md` at ae60f33d HOLD: A2's hosting includes homes and experiences, the mixed 5.6m listing image used room keys, and the seven-night image excluded exactly seven. Blind A `reviews/blind-a-v3-independent.md` at 96beb7e4 HOLD 8/12 on opening spoiler, opening-to-chapter restart, 2021 repeat and 2022 number ladder; blind B `reviews/blind-b-v3-independent.md` at 12aabc4e HOLD 6/12 on spoiler, causal story, payoff, repetition and explanatory detours. All three receipts are historical, not V4 clearance.

2026-10-20 V4 frozen for new independent review: `video.json` SHA-256 `23f057225c826b5687559fb7a47ea58c5b00eeb342f460a9c8a5484de1b84a62`, `shorts.json` SHA-256 `545a0844636cbc769afb9254824a6a68bbaf0006ebcbbe37b58344ae5a04252c`. Deterministic build: 135 spoken lines, 27 native number cards, 105 image-01 illustration candidates, 19 loops; hook 228 characters, substantive body 2,696 characters (paper estimate 8.99m at 300 cpm; no audio timing yet); Shorts 169 and 189 characters. V4 removes future outcomes from the condensed opening, moves chapter two forward with the cancellation notice, follows the next-booking problem through company choices and observed demand, trims the 2022 spoken numeric ladder, and preserves source period/denominator/accounting/refund limits. It broadens A2's hosting to homes and experiences, pictures 5.6m as mixed listing tokens, and includes exactly seven nights in the ≥7-night illustration. Shorts narration is unchanged but its referenced main-film shots have changed and require new blind inspection. Video lint 0 errors/0 warnings; docs-video tests 236/236 and task check exit 0. New source audit and two fresh blind reads must bind **these** hashes; any JSON change invalidates them. No paid call, image, TTS, official animation workfile, MP4, upload or URL exists. Global picture-judge quota is reserved for older in-flight episodes, so do not start X14 bulk art until actual available quota and full-episode US$25 ledger are checked. Production quote and publishing handoff are in this folder.
