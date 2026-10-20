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
- [ ] Independent agent re-fetches originals and audits the frozen source packet; fix every material discrepancy.
- [ ] Write source-bound full narration, two Shorts, visual plan, and production schemas; run content checks and two untouched blind reads.
- [ ] Produce and QA the episode and Shorts within the approved cost, then open the episode PR.

## How to verify

Read `docs/videos/story-everyday-airbnb-x14/source-matrix.md`, download its four SEC originals and compare response byte counts and SHA-256. Check each claim's period and denominator. Later run the story/video schema and lint gates and inspect generated media. `npm run check:tasks` validates this task file. No generated media exists in the source-packet phase.

## Notes

2026-10-20: Worktree `/workspace/travel_scanner_airbnb_x14`, branch `codex/brand-story-airbnb-x14` based on `origin/main` ec2c7676. Source packet lives at `docs/videos/story-everyday-airbnb-x14/`. Four worker-readable SEC HTML originals are all under 3 MB. The 2022 10-K is 3,213,119 bytes, so use it only for reviewer cross-checks; the worker-readable 2022 Q4 shareholder letter supports the core end claims. Do not use 2020 GAAP net loss as a proxy for the pandemic demand shock: it includes $2.8bn of IPO-triggered RSU expense and $868.5m full-year noncash warrant fair-value change. The shareholder letter separately gives $827m for **Q4** warrant revaluation; do not interchange quarter and full year. Do not equate gross nights, net Nights and Experiences Booked, gross booking value, company revenue, or net income. No paid calls, full script, upload, or PR in this source-packet phase.
