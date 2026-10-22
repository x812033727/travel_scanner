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

- [x] A source-bound, distinct author candidate has a pinned full text, A/B outline, 107 spoken lines, line-level claims, 30–60-second condensed opening, 8–12-minute estimated body, music and end-screen plan, and zero-error/zero-warning video lint.
- [ ] Independent source and written-visual review, two fresh blind narrative readers, formal merge and policy gate accept the frozen script.
- [ ] Owner/site audio review, native illustrations, music, final long cut and Short, package QA and actual Studio end-screen links are complete.

## Steps

- [x] Check S01–S60 and the topic index for overlap; reject Carrington because direct 1859 sources were inaccessible here, and reject S48's 1858 Atlantic-cable story as overlap.
- [x] Pin Samuel Henry Prince's 1920 Halifax field study to GITenberg commit `befb706982ba1be631a52d4f686be301c2de7f34`, raw `37580.txt` SHA-256 `97484e988437d13a4f5a72d5c2edbf1c594ea8dff4c5b239d8b17b7c62c29b52`; keep it clear that Prince's book itself combines his observations and cited descriptions.
- [x] Draft `brief.md`, `research.md`, `video.json`, `script.md`, `claims.md` and author handoff under `docs/videos/curio-s61/`.
- [x] Self-check every written picture against its own spoken line, then lint: 0 errors, 0 warnings; 107 lines, 95 illustrated shots, 9 information cards, 10.28-minute full estimate, first chapter 57 seconds.
- [x] Independent R1 source/visual review found a naval-affiliation error; R2 author corrected it and another worker independently PASSed the fixed Prince attribution and all changed written visuals on frozen hashes.
- [x] Run two isolated R2 blind narrative readers and formal merge; the five shared required failures are recorded.
- [ ] Repair the shared R2 narrative failures, obtain fresh independent source/visual and two-reader narrative PASS, then follow media gates before spending.

## How to verify

From repository root: `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s61 --json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s61`; `npm run check:tasks`. The author lint returned 0 errors/0 warnings, 107 lines, 10.2806 estimated minutes. Compare `claims.md` line text against `video.json` and the fixed text before any approval.

## Notes

2026-10-22: The GITenberg fixed copy was downloaded through the GitHub API to `/tmp/s61-halifax-prince.txt` and its SHA-256 checked. The book's preface (L90–110) says it is a social study, not a complete disaster history; Prince says he participated in Halifax rescue (L766–773). It records the powder-magazine warning (L951–974), crowd/army movement (L1356–1406), and attributes the absence of a second explosion to an entire artillery battery volunteering to flood the magazine in the naval yard (L1824–1836). The candidate explicitly attributes that causal claim to Prince; no independent military action log was obtainable in this task. It does not name a precise order, valve, distance, death toll from the warning, or identifiable survivor in art.

The source-rich fallback replaced 1859 Carrington: ADS and Wikisource were blocked by this environment's proxy 403, while GitHub search yielded later summaries but no fixed 1859 astronomy and telegraph first-person pair. S48 already covers the 1858 Atlantic cable. No paid TTS, MiniMax, judge, music, website approval, final video or YouTube upload has been performed for S61. Brand intro/outro assets and the actual clickable links are planned only; they are not outputs of this author draft.

2026-10-22 R2 independent [source/visual PASS](../../docs/videos/curio-s61/review/r2-independent-source-visual.md): video SHA-256 `800a8c7476bee77fad9b97e8a23e5b7e26007cfcf32e5ee471db371257fec134`, no claimed navy affiliation for the volunteer battery, naval yard retained only as the magazine location; six repaired prompts omit unsupported hose operations. R2 lint 0/0. Two isolated readers each voted 6/13 YES on R2, and the [formal OR merge](../../docs/videos/curio-s61/review/r2-formal-merged-narrative.json) is 7/13 YES, **FAIL** on `no_toc`, `chapters_link`, `payoffs`, `no_recap`, `no_detour`, with advisory `chapters_are_events` also NO. The [audit](../../docs/videos/curio-s61/review/r2-formal-merge-audit.json) binds both official receipts; official CLI replay exits 1 on those same five required IDs. R3 author repair is in progress; no media gate is approved.

2026-10-22 R3 author restructuring is frozen at video SHA-256 `12820d44f6a213eaa0a312721d16b645807bbe0f0b8fd20ac5fba3b56ef36cdf`, script `6cf2fce1d864a772f8e5e456cc55f63d2fc3a160ba9e4198d98617289eb8d6a9`, 102 spoken lines, 90 shots/9 cards, estimated 56.87-second opener and 8.61-minute body. An independent [source/visual review](../../docs/videos/curio-s61/review/r3-independent-source-visual.md) passed after a citation-only extension of Prince P14 to L2023; research and claims SHA-256 are in the review. [Blind A](../../docs/videos/curio-s61/review/r3-isolated-blind-a.official-narrative.json) voted 11/13 and [blind B](../../docs/videos/curio-s61/review/r3-isolated-blind-b.official-narrative.json) 8/13. The [formal OR merge](../../docs/videos/curio-s61/review/r3-formal-merged-narrative.json) remains **FAIL 11/13**, shared required items `chapters_link` and `no_recap`; [audit](../../docs/videos/curio-s61/review/r3-formal-merge-audit.json) binds the official receipts to identical creative/panel hashes, and official CLI replay exits 1. R4 author repair is underway; no media gate or paid call has been approved.

2026-10-22 R4 [author-only narrative repair](../../docs/videos/curio-s61/review/r4-author-narrative-repair.md) is frozen at `video.json` SHA-256 `9a76f8880c75a04ef1322ac7264323ffb92b7dd8e648a1ffa992212f4c7d72a6`, `script.md` `c677b03f9c45c8f4d3d788d73381253e4bb574cb9e420c136b8761cbb9658650`; [reversible R3→R4 delta](../../docs/videos/curio-s61/review/r4-author-delta.json) documents the tighter chapter seams and shelter tail. Author lint 0/0, 96 lines and 84 illustrated prompts, estimated 56.6-second opener and 8.15-minute body after it. Fresh independent source/visual and two isolated narrative readers are reviewing these hashes; no R4 PASS, website gate or paid media is claimed yet.

2026-10-22 R4 [independent source/visual review](../../docs/videos/curio-s61/review/r4-independent-source-visual.md) **PASSed** the pinned Prince text, reversible delta, 96/96 narration/claim/script rows, 84/84 written prompts and lint 0/0. Two fresh [blind A](../../docs/videos/curio-s61/review/r4-isolated-blind-a.official-narrative.json) and [blind B](../../docs/videos/curio-s61/review/r4-isolated-blind-b.official-narrative.json) ballots voted 10/13 and 11/13 on identical creative/panel bindings. The [formal OR merge](../../docs/videos/curio-s61/review/r4-formal-merged-narrative.json) is **HOLD 11/13** on shared `no_recap` and `no_detour`; the [audit](../../docs/videos/curio-s61/review/r4-formal-merge-audit.json) and official CLI replay exit 1 preserve this verdict. R5 author must remove repeated warning/return facts and the shelter detour while preserving a sourced >8-minute body and clear payoff. No paid media or website gate is claimed.
