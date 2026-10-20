---
id: 2026-10-20-brand-story-spotify-x13
title: Brand story Spotify X13
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-20T20:01:30Z
completed_at:
branch: codex/brand-story-spotify-x13
depends_on: []
scope:
  - docs/videos/story-everyday-spotify-x13
  - docs/videos/lexicon.json
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
- [x] Draft the source-tagged main script, visual plan, two Shorts and schemas; revise through v7 with offline structural validation. The current author packet is frozen for independent review, not approved.
- [ ] Independently audit v7 against SEC originals and obtain two fresh blind narrative ballots on the same video/Shorts hashes; revise again if a material source issue or shared mandatory NO remains.
- [ ] Produce and QA film and Shorts with official branding/audio/CC within budget as available; submit a truthful draft PR for the approved offline packet, then continue the next missing brand.

## How to verify

Read `docs/videos/story-everyday-spotify-x13/source-matrix.md`, redownload its nine SEC links and compare SHA-256 where available. Validate claims against originals, periods and denominators. At later stages run repository story/video schema, lint and QA; no generated media exists yet.

## Notes

2026-10-20 source feasibility packet in `docs/videos/story-everyday-spotify-x13/`. A six-chapter full draft exists but is undergoing narrative rewrite; no paid calls, upload, finished media or PR. Source originals were checked over SEC EDGAR; the annual 20-F pages are >3 MB and therefore reviewer-only for the host worker. Core claims are separately supported by <3 MB 6-Ks or a short earnings exhibit. The two Short concepts are independent of the long film. SEC 2025 Q2 changes podcast cost classification across Premium and Ad-Supported; never infer standalone podcast profit or savings from an Ad-Supported decrease. Independent feasibility source audit PASS is in `reviews/source-audit-independent.md`; its receipt binds the **earlier** source matrix `ebd46208…`, Treatment `918d9c13…`, Short hooks `1d3875a0…` only. The first PASS was invalidated after a writer noticed 2024 Q2 Ad-Supported total cost -€32m was confused with an €11m explanatory item; the later receipt explicitly superseded it and also checked 2025 Q2 total -€25m versus €21m podcast-cost component. Both feasibility receipts are **stale** after adding S9 and revising Treatment. The current full script and media need their own audit/reviews; a preproduction PASS cannot substitute for them.

The last line-source PASS binds narration `e9753f33…`, Shorts `a732bb31…`, and visual plan `ad17d571…` in `reviews/script-source-audit-independent.md`; it is **stale** after the v3 revision and addition of S9. Earlier A/B/C narrative reports helped revision but their reviewers inherited upstream discussion, so they are editorial feedback, **not** the two required fresh blind receipts. D noticed the same context contamination and issued no verdict. See `reviews/review-provenance.md`. Actually isolated readers F1/F2 and F3/F4 all returned NO on earlier frozen hashes.

V3 frozen SHA-256: source matrix `cb8d31b67262e2c03c946259f035a89531e8868cdb3b83937e0857a382fbba12`; Treatment `029f49e15055cc1aa67a295a6a72eaf0a909640bf0c7b85fa42719bafea54972`; narration `44b16a998bb5e35c1605d141d565705a0e4d124ba9d9dbd57b1d4bf6b9ada9b0`; Shorts `a732bb31101d5ec9facbecb015fcc70859c1025fe54c59b126f0fb12a65a27ef`; visual `f24711784fb4b9aae2df713061f9f483e63b2dfba4633a6d3a2bf1c2e2e99dac`. Independent audit `reviews/script-source-audit-v3-independent.md` fetched all nine SEC originals with matching hashes but returned **HOLD** for S9 July 25 availability being called same-quarter, unsupported age/visual details, and a chapter heading's quarterly-to-annual causal suggestion. Isolated F5 and F6 both returned **6/7, overall NO**, solely on a still chronological financial spine. Both found the number load, direct answer, six chapters, anonymous-card distinction and standalone Shorts acceptable on paper.

**V4 author checkpoint, 2026-10-20:** independently re-fetched all nine SEC original HTML files; bytes and SHA match the source matrix (S3/S9 cached original files likewise hash-matched). Rewrote the long film around one testable question—can the two 2019 acquisitions be shown to have paid back?—with the same viewer-side evidence folder through all six chapters. Fixed all five v3 source audit blockers: S9 count belongs to the 2023-07-25 announcement time, not Q2 end; no invented old-content age, program schedule/count, 2019 video viewing path, or Q2-margin-to-full-year causality. Added deterministic `video.json`/two `shorts.json` schemas, 9:16 shot list, native-stat descriptions, source links, estimate and official-animation handoff. Frozen hashes and scope are in episode README: main `22e9a6f21ecddbce71066dd798843db7eec612030e53b69b2975198bf2dc9317`, Shorts `07950bc98a030f359d0137e733a531b45f8ba0ab8452864b01c7f6eb83562142`. Lint 0 errors/0 warnings; each Short validates; docs-video tests and tasks validation exit 0. These are author-side checks only. **Still HOLD:** new independent full-source audit and two blind reviews of these exact v4 hashes, then only if PASS can paid media begin. No media, official animation copies, upload, PR or real video links.

**V4 independent outcome:** [source audit](../../docs/videos/story-everyday-spotify-x13/reviews/script-source-audit-v4-independent.md) re-fetched S1–S9 with exact matching SHA but returned HOLD on wording that could imply the new Premium video experience was limited to newly subscribed members. [Blind A](../../docs/videos/story-everyday-spotify-x13/reviews/blind-a-v4-independent.md) returned 5／12 YES and [Blind B](../../docs/videos/story-everyday-spotify-x13/reviews/blind-b-v4-independent.md) 6／12 YES, both HOLD for early spoilers, procedural and repeated financial narration, weak chapter-two pickup and side trips. These reviews remain historical and do not approve v5.

**V5 author checkpoint, 2026-10-20:** opening reveals the 2019 Anchor/Gimlet purchases and price, then plants three distinct later moments without results (2023 content record, 2024 whole-company annual line, 2025 video cost column). Ch2 answers with the two purchased capabilities. Removed The Ringer and market-list detours; condensed 2024 accounting into business consequences and placed a native 2024 whole-company annual-result card at the actual reveal. Corrected every authored Premium new-experience wording so it does not classify members by signup age, and changed the 2025 cost image so no measured true-savings amount disappears. Source URLs and original SEC hashes remain in the matrix. Frozen author hashes in episode README: main `f7b3e849b448bcd7f5d868c84586760abf102111e03981f28be3f17682a6fa75`, Shorts `1cc56e53cf5c34b457d4b462daa282dbd21b80924c11fe01a433e39c09ba2603` (refresh if generated files change). Compiler: 125 lines, 111 shots, 10 native stats cards, 2,613 body characters. Long-video lint 0 errors/0 warnings; both Shorts validate; docs-video tests 236／236 pass; tasks check exit 0 with existing cross-task warnings. **Still HOLD:** independent v5 source audit and two fresh blind reads of the frozen JSONs, followed by actual ≥8-minute body audio, 25–55-second Shorts, visual QA, official animation and paid-budget gate. No paid media, upload or PR.

**V5 independent outcome:** [source audit](../../docs/videos/story-everyday-spotify-x13/reviews/script-source-audit-v5-independent.md) re-fetched S1–S9 and matched all source bytes/SHA, but returned **HOLD** because the podcast-content-cost question was answered with the entire Ad-Supported business's income and **total** cost numbers. [Blind A](../../docs/videos/story-everyday-spotify-x13/reviews/blind-a-v5-independent.md) returned 6／12 YES and [Blind B](../../docs/videos/story-everyday-spotify-x13/reviews/blind-b-v5-independent.md) 7／12 YES; both HOLD on repeated 2019 exposition, chapter handoff, 2023 video-supply detour and presentation timing. Those receipts bind v5 only.

**V6 author checkpoint, 2026-10-20:** kept the single question of whether the two 2019 acquisitions can be shown to have paid back. Chapter 2 now follows the purchased audio from separate creation desks into one player and two broad revenue lines, reveals the noncash component only after the opening price card, and ends on the 2020 advertising account. Chapter 3 opens with the whole advertising line's gross profit turning negative, compares the same line's revenue +€22m and **total** cost +€42m, then separately reveals podcast content cost +€12m as one component. Chapter 4 directly answers that the later partial content-asset write-off cannot be traced to either acquisition, and removes the 2023 video-availability side story. Short 2 names Premium members, opens with only the Ad-Supported −€21m scope, and uses a blank transfer-amount visual for the unknown split. Source matrix and SEC-original hashes are unchanged. Current v6 hashes, counts, official-bookend handoff, tests and the remaining source/dual-blind review gate are in the episode README. This is authored offline preproduction only: no paid media, animation copies, measured audio, upload or PR.

**V6 independent outcome:** [source audit](../../docs/videos/story-everyday-spotify-x13/reviews/script-source-audit-v6-independent.md) re-fetched S1–S9 and passed the corrected Ad-Supported +€22m income / +€42m **total** cost comparison. Fresh [blind A](../../docs/videos/story-everyday-spotify-x13/reviews/blind-a-v6-independent.md) scored 10/12 with Q4/Q8 NO; [blind B](../../docs/videos/story-everyday-spotify-x13/reviews/blind-b-v6-independent.md) scored 10/12 with Q5/Q8 NO, Q9 advisory NO. Their common Q8 NO on repeated cost and account explanations makes v6 narrative HOLD under the brand-story two-reader rule. B also found two Short statistics lacked explicit native portrait layout. These receipts bind v6 only.

**V7 author checkpoint, 2026-10-20:** made the three opener futures concrete while withholding outcomes, placed the deal-payback question as the final opener line, and opened Chapter 2 by following the acquired audio toward listeners and revenue. Removed the Q8 repetitions: `x130213` now distinguishes ad impressions from mere uploads; `x130313` follows other royalty pressure rather than re-announcing podcast-cost classification; `x130617` tests whether broad service accounts can expose per-deal results. Added the S2 royalty +€20m as a **different component** of the whole Ad-Supported +€42m total-cost increase, never an independent podcast result. The last act treats new creator payments separately from old purchase returns, with an anonymous present-day outside reader physically separating incompatible public evidence cards; no invented Spotify meeting or true show identity. The two `stats` shots reused by Shorts have exact 1080×1920 native card text, positions and subtitle safety areas in the portrait plan. Current hashes and paper counts are in the episode README. Source matrix S2 expanded to document the royalty component and ad-impression mechanism. No paid media or finished film. **Next gate:** independent v7 SEC re-fetch/line/visual audit and two wholly fresh first-blind narrative reviews of frozen JSON; older receipts cannot approve v7.
