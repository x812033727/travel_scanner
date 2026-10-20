---
id: 2026-10-20-brand-story-spotify-x13
title: Brand story Spotify X13
status: in-progress
priority: P1
area: docs
owner: codex-x13
claimed_at: 2026-10-20T20:01:33Z
created_at: 2026-10-20T20:01:30Z
completed_at:
branch: codex/brand-story-spotify-x13
depends_on: []
scope:
  - docs/videos/story-everyday-spotify-x13
  - tasks/open/2026-10-20-brand-story-spotify-x13.md
---

# Brand story Spotify X13

## Why

The owner asks to continue making missing-brand films, with a new PR then the next topic, under the existing 奇聞檔案局 / brand-story rules. Spotify is absent from X01–X12 and the 100-topic plan. Its original SEC filings document a concrete reversal from 2019 podcast acquisitions to a 2023 podcast content realignment, then the first full-year operating-income profit in 2024. The story must keep those observations separate from an unproven claim that podcasts caused the profit.

## Definition of done

- [ ] A source-verified main film with measured substantive body ≥8:00, approximately 10-minute target, 30–45-second hooks, two standalone 25–55s Shorts, official 5s/21s bookends, Traditional Chinese optional CC, and reviewable source/script/visual evidence.
- [ ] Paid media and retries stay within the owner-authorized US$25 episode cap; actual upload links are filled only after a real upload.
- [ ] Draft PR only after independent source audit and two fresh blind reviews of the frozen script and Shorts.

## Steps

- [x] Compare Spotify, Airbnb, Kellogg against 100-topic plan, C01–C20 and X01–X12; select Spotify on evidence depth, unique reversal and non-overlap.
- [x] Fetch and hash SEC originals; write a six-chapter Treatment, exact source matrix and two independent Short concepts.
- [x] Have another agent audit this Treatment against independently fetched originals; fix all material claims.
- [ ] Draft line-sourced main script, visual plan, two Shorts and schemas; run content validation and two untouched blind reads of same frozen hashes. V3 drafts and reviews exist, but independent source audit HOLD and two fresh blind NO votes block production and PR.
- [ ] Produce and QA film and Shorts with official branding/audio/CC within budget, then submit PR and continue X14.

## How to verify

Read `docs/videos/story-everyday-spotify-x13/source-matrix.md`, redownload its nine SEC links and compare SHA-256 where available. Validate claims against originals, periods and denominators. At later stages run repository story/video schema, lint and QA; no generated media exists yet.

## Notes

2026-10-20 source feasibility packet in `docs/videos/story-everyday-spotify-x13/`. A six-chapter full draft exists but is undergoing narrative rewrite; no paid calls, upload, finished media or PR. Source originals were checked over SEC EDGAR; the annual 20-F pages are >3 MB and therefore reviewer-only for the host worker. Core claims are separately supported by <3 MB 6-Ks or a short earnings exhibit. The two Short concepts are independent of the long film. SEC 2025 Q2 changes podcast cost classification across Premium and Ad-Supported; never infer standalone podcast profit or savings from an Ad-Supported decrease. Independent feasibility source audit PASS is in `reviews/source-audit-independent.md`; its receipt binds the **earlier** source matrix `ebd46208…`, Treatment `918d9c13…`, Short hooks `1d3875a0…` only. The first PASS was invalidated after a writer noticed 2024 Q2 Ad-Supported total cost -€32m was confused with an €11m explanatory item; the later receipt explicitly superseded it and also checked 2025 Q2 total -€25m versus €21m podcast-cost component. Both feasibility receipts are **stale** after adding S9 and revising Treatment. The current full script and media need their own audit/reviews; a preproduction PASS cannot substitute for them.

The last line-source PASS binds narration `e9753f33…`, Shorts `a732bb31…`, and visual plan `ad17d571…` in `reviews/script-source-audit-independent.md`; it is **stale** after the v3 revision and addition of S9. Earlier A/B/C narrative reports helped revision but their reviewers inherited upstream discussion, so they are editorial feedback, **not** the two required fresh blind receipts. D noticed the same context contamination and issued no verdict. See `reviews/review-provenance.md`. Actually isolated readers F1/F2 and F3/F4 all returned NO on earlier frozen hashes.

V3 frozen SHA-256: source matrix `cb8d31b67262e2c03c946259f035a89531e8868cdb3b83937e0857a382fbba12`; Treatment `029f49e15055cc1aa67a295a6a72eaf0a909640bf0c7b85fa42719bafea54972`; narration `44b16a998bb5e35c1605d141d565705a0e4d124ba9d9dbd57b1d4bf6b9ada9b0`; Shorts `a732bb31101d5ec9facbecb015fcc70859c1025fe54c59b126f0fb12a65a27ef`; visual `f24711784fb4b9aae2df713061f9f483e63b2dfba4633a6d3a2bf1c2e2e99dac`. Independent audit `reviews/script-source-audit-v3-independent.md` fetched all nine SEC originals with matching hashes but returned **HOLD** for S9 July 25 availability being called same-quarter, unsupported age/visual details, and a chapter heading's quarterly-to-annual causal suggestion. Isolated F5 and F6 both returned **6/7, overall NO**, solely on a still chronological financial spine. Both found the number load, direct answer, six chapters, anonymous-card distinction and standalone Shorts acceptable on paper. Script remains unapproved; no JSON, paid calls, official media, upload or PR. `npm run test:docs-videos` passed 236/236 and `npm run check:tasks` exited 0 with existing repository warnings. V4 rewrite is deferred for a later wave; re-audit all modified hashes before production.
