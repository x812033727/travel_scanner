---
id: 2026-10-22-source-and-draft-s60-south-pole
title: Source and draft S60 South Pole letter history episode
status: in-progress
priority: P2
area: docs
owner: codex-s60-new-episode
claimed_at: 2026-10-22T00:27:08Z
created_at: 2026-10-22T00:27:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s60
---

# Source and draft S60 South Pole letter history episode

## Why

The owner asked for another genuinely new Curio history film with a condensed opener, fixed brand intro/outro and clickable end links. The proposed Johnstown warning angle was previously rejected for unverifiable warning delivery; S60 needs a different story with direct sources and an honest media gate.

## Definition of done

- [x] A source-bound S60 author candidate has a distinct topic, A/B outline, 30–60-second condensed opener, full >8-minute estimated body, brand and Studio link plan, fixed sources, line-to-claim mapping, and zero-error video lint.
- [ ] Independent source review, two blind narrative readers and a formal merge have accepted the frozen script.
- [ ] Approved audio, illustrations, music, final video and upload package exist with actual media QA.

## Steps

- [x] Search S01–S59 briefs, the history-curiosity topic index and tickets for overlaps; reject Johnstown based on S57's prior source failure.
- [x] Fix Amundsen and Scott first-person publications to immutable Git commits; download and verify two raw SHA-256 digests.
- [x] Draft `brief.md`, `research.md`, `video.json`, `script.md`, and author `claims.md` under `docs/videos/curio-s60/`.
- [x] Correct the Jan 18 Scott / Jan 25 Amundsen chronology during author self-check; align visual date cards to their corresponding lines.
- [x] Run script and lint; R2 has 0 errors, 0 warnings, 49-second condensed opener, 110 lines, 104 shots / 6 cards, 11 loops, estimated 10.836-minute body.
- [x] Read the independent R1 source/visual HOLD and author a source-bound R2 repair with an exact structured diff and frozen hashes.
- [x] Have a different worker verify every source-bound line and written visual against the fixed editions (R2 paper PASS).
- [x] Run two independent R2 narrative readers and formally merge their ballots; the four shared failures are recorded.
- [ ] Repair the four concrete R2 narrative failures and obtain a fresh independent source/visual and two-reader narrative PASS.
- [ ] Obtain actual content/media gate receipts before paid narration, pictures or music, then produce and QA the full cut.

## How to verify

From repository root: `VIDEO_WORKDIR=/tmp/s60-video-work node tools/video/cli.mjs script --slug curio-s60`; `VIDEO_WORKDIR=/tmp/s60-video-work node tools/video/cli.mjs lint --slug curio-s60 --json` returned `errors: []`, `warnings: []`, estimated body `10.836` minutes. `python /tmp/s60_r2_diff.py` compared R2 against baseline commit `806f4493d` and wrote the exact [structured diff](../../docs/videos/curio-s60/review/r2-author-structured-diff.json); the temporary comparison script is not part of the source package. `npm run check:tasks` passed globally for R2 with unrelated stale/overlapping-task warnings. Reopen the two fixed texts and compare each `claims.md` row before treating it as a verified fact. The CLI `narrative --json` emits the reader questionnaire; it is not itself a reader verdict.

## Notes

2026-10-22: Prior attempted S57 Johnstown warning concept was rejected in `tasks/done/2026-10-20-curio-s57-johnstown-warning-preproduction.md`: contemporary compilations repeated reports but did not show that the dam warning reached specific residents. Do not reintroduce that causal claim. S60 instead follows two 1911–12 South Pole participants' accounts. It differs from S34 Endurance (1915–16 shipwreck/recovery). Fixed GITenberg Amundsen revision `242036c254a5ff483c59e5dc4c66a97f4486f70c`, raw `4229.txt` SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`; fixed Scott revision `06ff155e7ebf76842906286ae8aa85487ac6a87d`, raw `11579.txt` SHA-256 `ddf48b1e0fc296b4862bad161bada2797a964ac6e6c7a0a7306a0a73940f8b26`. Local downloads live only in `/tmp/curio-s60-sources`; immutable URLs and per-line anchors are in `research.md` and `claims.md`.

Key dates: Amundsen's first flag was 1911-12-14, the small tent and two addressee letters were left by 1911-12-17; Scott saw the black flag 1912-01-16 and found the tent 1912-01-18; Amundsen returned to Framheim 1912-01-25. Scott's note says he kept Amundsen's request to forward a letter to King Haakon. Neither fixed book establishes that the king actually received it. The script's last chapter follows this chronology. MiniMax has not been called, no TTS or music has been generated, and no approval or independent PASS has been claimed. Exact `video.json` content hash should be recorded after independent acceptance and again before any paid-media gate; edits invalidate later receipts.

2026-10-22 R1 independent source/visual review is [HOLD](../../docs/videos/curio-s60/review/r1-independent-source-visual.md). The author then corrected four spoken lines, added the P09 actual night-departure anchor, and replaced all 104 shot prompts so rescue, two Pole camps, letters, return, and Scott's fate follow the narrated chronology. The [R2 author receipt](../../docs/videos/curio-s60/review/r2-author-visual-repair.md) and exact JSON diff freeze `video.json` SHA-256 `bf8d95565857f0a8b976ef6f2d89e730fd88fabcab44201e75a05bd67dabba9c`. **R2 source/visual paper PASS** is recorded in `review/r2-independent-source-visual.md`; all 110 lines and 104 prompts were checked. Two isolated readers voted 9/13 and 8/13 on the same frozen speech. Their [formal OR merge](../../docs/videos/curio-s60/review/r2-formal-merged-narrative.json), [audit](../../docs/videos/curio-s60/review/r2-formal-merge-audit.json), and official CLI replay remain **FAIL** on `no_spoiler`, `chapters_link`, `payoffs`, `no_recap`. R3 author repair is in progress. No paid media or owner gate has been claimed.
