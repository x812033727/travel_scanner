---
id: 2026-10-08-complete-all-six-elementary-english-seasons
title: Complete all six elementary English seasons
status: done
priority: P2
area: tools
owner: codex-elementary-complete
claimed_at: 2026-10-08T01:07:58Z
created_at: 2026-10-08T01:07:07Z
completed_at: 2026-10-08T02:24:24Z
branch: codex/elementary-english-complete-20261008
depends_on: []
scope:
  - tools/video/elementary_series
  - docs/videos/english-elementary-complete
---

# Complete all six elementary English seasons

## Why

The user requested completion of the entire elementary English series after the first 12-episode season. The complete course is six seasons of twelve lessons: two lower-, two middle-, and two upper-elementary seasons. It develops classroom communication through daily vocabulary, places/time, stories/reasons, and guided reading/writing.

## Definition of done

- [x] All 72 episodes have complete source; the original first-season source and media remain unchanged.
- [x] The remaining 60 episodes have measured five-language audio, four translated CC tracks, embedded English, and validated films.
- [x] A 72-episode offline player, six independent season ZIPs, a combined ZIP, catalog and practice material are verified outside the repository.
- [x] Repository checks and independent source/art/pipeline reviews pass; complete source and delivery evidence are committed for the authorized draft continuation PR.

## Steps

- [x] Inspect environment, ownership, branches/worktrees, remote heads and open PRs; claim a narrow task and branch from completed season one.
- [x] Define six-season progression and authoring rules; copy original season-one delivery using separate files.
- [x] Author, cross-review and freeze all five new five-language seasons.
- [x] Add an isolated series renderer/profile with word/sentence, quantity, clock, weekday and place cards; preserve original renderer files.
- [x] Synthesize and render new episodes with bounded concurrency, full media decode and source-bound integrity records.
- [x] Validate all 72 films, package all seasons and practice material, and prepare the draft PR.

## How to verify

- Exact S1 episode JSON and final-file SHA comparison with the completed original season.
- Authoring structure, localized meaning, target/choices, neutral headers, reading/writing activity evidence and reveal timing checks.
- Profile/integrity regressions through `npm run test:tools`; `npm run check:tasks`.
- Whole-series verification, 72 per-episode successful full media decode records bound to SHA, and final 5-audio/4-CC stream checks.
- All seven ZIP CRC/hash/catalog/relative-player-asset checks and jsdom controls with correct season/episode counts.

## Notes

- Parent draft PRs #1376 (preschool) and #1377 (elementary S1) remain unmerged. The continuation branch intentionally builds on #1377, preserving its media/source profile.
- Media destination: `/workspace/elementary-series-output`; original first season at `/workspace/elementary-season01-output` is preserved. Copies are independent rather than hard links to prevent later caption writes affecting prior delivery.
- English remains embedded in the picture with no English CC; English demonstrations remain identical across original English plus Traditional Chinese, Simplified Chinese, Japanese and Korean voice tracks.
- New text-card questions are listening-and-reading choices, not independent reading assessments. Whole-word spelling patterns do not claim isolated phoneme training.
- Target remains ten short scenes, about 3–5 minutes measured, with five/six-second response intervals. This is the established short children's course profile, separate from general long-form videos.
- Trial voices are the existing Microsoft Edge read-aloud voices, not configured backend production voices. No upload or publication is included.
- Real browser local-file navigation was already blocked by administrator policy in the prior turn; this run will not bypass that policy or claim actual browser playback from jsdom checks.
- Authoring contracts and the complete curriculum are stored in this task's documentation scope; only new series tools are edited, keeping old renderer SHA dependencies immutable.

All six sources assembled and verified: 72 episodes, 720 scenes, 216 quizzes, 121 guided-reading scenes. New seasons passed independent cross-language review; S1 episode dictionaries are byte-equivalent in content to the preserved first-season source. Printable PDF/HTML practice is generated from each source task, with an embedded static Noto Sans TC TrueType font; 85-page combined PDF previews were visually inspected. Media production and independent delivery checks are complete.

- Local tools suite: 2,012 tests, 2,009 passed, three skipped, zero failed (exit 0). Latest standalone pipeline wrapper: all 17 Python checks passed. Task validation: 1,639 files, exit 0; unrelated stale-owner warnings only.
- S1 preservation check: all 228 copied files have their original SHA-256 and distinct inodes; original first-twelve lesson objects match exactly.
- Independent practice review: all 72 HTML tasks/answers and the 85-page PDF matched 432 source fields; upper-season answer pages were rendered and visually checked.
- Visual review found two-line guided-reading rectangles obscuring descenders. The new renderer was corrected before full production resumed, and all new episodes use its updated fingerprint. A permanent runtime regression checks 106 guided scenes / 104 distinct texts; all retain their solid glyph pixels, while the old drawing order fails the required negative controls. S1 renderer sources stay untouched.
- Independent packaging review caught acceptance of an internally consistent but stale resolved source. Packaging now requires current authoring, recursively compares all authored fields including practice, runs complete media verification, and checks source/resolved hashes again before publishing ZIPs. Regression tests reject altered practice, altered demonstrations and alternate resolved paths; re-review found no remaining P1/P2.
- Final source-bound art QA passed for all 60 new episodes: 600 scenes, 2,400 frames, 285 used visual tokens, 180 unrevealed-quiz invariance checks, 636 choice-text line bounds, 106 guided text pixel checks and 86 multiline spacing checks. The 137-token fixture set also passed after the final renderer change. Nine curriculum galleries were regenerated; manual sampling is distinguished from automated coverage in the report.

- Final media: 72/72 passed, zero errors, 13,049.675 seconds (3:37:29.675), 360 M4A masters, 288 SRT and 288 VTT files, no English CC. The full 72-episode audio producer and three-worker render batch both exited 0.
- Final packages: six season ZIPs (209 members each) plus the combined 918,960,271-byte ZIP (1,229 members). Independent delivery checker exited 0: CRC, every media member SHA, seven relative playback assets per episode, four embedded CC languages/cues, exact CSV and practice content all matched. Six 15-page PDFs and the 85-page combined PDF passed; final PDF text matches the visually reviewed version.
- Seven player variants passed jsdom controls (one 72-episode / six-season player and six 12-episode / one-season players). Packaged index hashes match their tested versions. Real-browser playback remains unverified because of the previously observed administrator policy; actual film decode is separately verified.
- Final encoded-film samples checked at ep17 choice wait, ep18 ten-cookie count, ep37 07:30 clock, and both ep66/ep69 multiline guided-reading cases; no overlap, clipped text or premature answer marking observed.
- Repeated remote/local branch and open-PR collision checks found only the existing parent preschool #1376 and elementary S1 #1377 work. Parent remote head remains 9f18eb7830fcb75585f5a9eedc83826d1cfaeb26. New draft PR targets `codex/elementary-english-season01-20261008`; no merge or publication.
- Portable validation summary and archive SHA-256 values are committed in `docs/videos/english-elementary-complete/delivery-verification.json`. All media and full validation receipts remain under `/workspace/elementary-series-output`.
