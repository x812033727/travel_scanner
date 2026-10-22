---
id: 2026-10-22-source-and-draft-s61-halifax-second
title: Source and draft S61 Halifax second-blast warning episode
status: in-progress
priority: P2
area: docs
owner: codex-s61-new-episode
claimed_at: 2026-10-22T00:45:06Z
created_at: 2026-10-22T00:45:03Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s61
---

# Source and draft S61 Halifax second-blast warning episode

## Why

The owner asked to keep making new Curio history episodes. S61 asks why people in Halifax heard a warning of a **second** explosion after the 1917 harbour blast, and what the fixed 1920 relief participant's study actually proves about the fire-threatening naval magazine and its treatment. Do not turn a warning into an explosion or claim a complete independent military inquiry has been checked.

## Definition of done

- [x] A source-bound, distinct author candidate has a pinned full text, A/B outline, 97 spoken lines, line-level claims, 30–60-second condensed opening, 8–12-minute estimated body, music and end-screen plan, and zero-error/zero-warning video lint.
- [ ] Independent source and written-visual review, two fresh blind narrative readers, formal merge and policy gate accept the frozen script.
- [ ] Owner/site audio review, native illustrations, music, final long cut and Short, package QA and actual Studio end-screen links are complete.

## Steps

- [x] Check S01–S60 and the topic index for overlap; reject Carrington because direct 1859 sources were inaccessible here, and reject S48's 1858 Atlantic-cable story as overlap.
- [x] Pin Samuel Henry Prince's 1920 Halifax field study to GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`, raw `37580.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`; keep it clear that Prince's book itself combines his observations and cited descriptions.
- [x] Draft `brief.md`, `research.md`, `video.json`, `script.md`, `claims.md` and author handoff under `docs/videos/curio-s61/`.
- [x] Self-check every written picture against its own spoken line, then lint: 0 errors, 0 warnings; R5 has 97 lines, 87 illustrated shots, 7 information cards, 9.5261-minute full estimate, first chapter 59.03 seconds and 495.47-second post-opening body.
- [x] Independent R1 source/visual review found a naval-affiliation error; R2 author corrected it and another worker independently PASSed the fixed Prince attribution and all changed written visuals on frozen hashes.
- [x] Two isolated R2 blind readers and formal merge found shared narrative failures (`no_toc`, `chapters_link`, `payoffs`, `no_recap`, `no_detour`), despite R2 source/visual PASS.
- [x] R3 author repaired the narrative on new hashes, added P14 for source-bound rescue organization, and kept prompt/claim alignment and lint 0/0.
- [x] R3 independent source/visual review PASSed after a citation-only P14 extension through Prince L2023; formal R3 dual-blind merged 11/13 and held on shared `chapters_link` and `no_recap` (one reader also flagged `no_toc`, `one_thread`, `no_detour`).
- [x] R4 author rewrote chapter seams, removed repeated details, shortened relief/shelter to consequences of the warning, and kept the final Prince attribution source-bound.
- [x] R4 independent source/visual PASSed, but fresh formal dual-blind narrative OR merged 11/13 and held on shared `no_recap` and `no_detour`; reader A additionally flagged a missed injured-evacuee payoff.
- [x] R5 author moved the no-second-blast answer immediately after the all-clear, trimmed after-alert rescue/shelter to five lines with explicit opening callbacks, removed duplicate warning/return lines, and added fixed-text first-blast and early-aid details to keep the body over eight minutes.
- [ ] Have two new isolated blind readers and a new independent source/visual reviewer assess frozen R5, then follow media gates before spending.

## How to verify

From repository root: `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s61`; `npm run check:tasks`. The R5 author lint returned 0 errors/0 warnings, 97 lines, 9.5261 estimated minutes. Compare `claims.md` line text against `video.json` and the fixed text before any approval.

## Notes

2026-10-22: The GITenberg fixed copy was downloaded through the GitHub API to `/tmp/s61-halifax-prince.txt` and its SHA-256 checked. The book's preface (L90–110) says it is a social study, not a complete disaster history; Prince says he participated in Halifax rescue (L766–773). It records the powder-magazine warning (L951–974), crowd/army movement (L1356–1406), and attributes the absence of a second explosion to an entire artillery battery volunteering to flood the magazine in the naval yard (L1824–1836). The candidate explicitly attributes that causal claim to Prince; no independent military action log was obtainable in this task. It does not name a precise order, valve, distance, death toll from the warning, or identifiable survivor in art.

The source-rich fallback replaced 1859 Carrington: ADS and Wikisource were blocked by this environment's proxy 403, while GitHub search yielded later summaries but no fixed 1859 astronomy and telegraph first-person pair. S48 already covers the 1858 Atlantic cable. No paid TTS, MiniMax, judge, music, website approval, final video or YouTube upload has been performed for S61. Brand intro/outro assets and the actual clickable links are planned only; they are not outputs of this author draft.

2026-10-22 R2 independent [source/visual PASS](../../docs/videos/curio-s61/review/r2-independent-source-visual.md): video SHA-256 `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134`, no claimed navy affiliation for the volunteer battery, naval yard retained only as the magazine location; six repaired prompts omit unsupported hose operations. R2 lint 0/0. The R2 formal dual-blind merge held on five shared narrative failures. R3 removes the numbered exposition, makes chapter starts answer preceding questions, pays off fire proximity and who assumed command, defers the no-second-blast finding until the end, and replaces the rail/telegraph inventory with Prince’s assigned-area search account (P14). R3 independent source/visual PASSed after the P14 L2023 citation repair, but formal dual-blind merged only 11/13 and held on chapter linkage and repeated facts; one reader also flagged the broad relief/shelter detour. R4 fixed opening and closing seams and anchored new port and warning details to Prince; independent R4 source/visual PASSed, but formal dual-blind merged 11/13 and held on repetition and the post-alert rescue/shelter detour. R5 answers the second-blast question immediately after the all-clear, leaves only five short source-bound callback lines afterward, and uses additional Prince details of blast damage, communication loss and first aid to preserve an eight-minute body. Fresh R5 review is pending; no media gate is approved.
