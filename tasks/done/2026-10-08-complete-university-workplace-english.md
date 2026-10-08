---
id: 2026-10-08-complete-university-workplace-english
title: Complete university and workplace English courses
status: done
priority: P2
area: tools
owner: codex-adult-english-series
claimed_at: 2026-10-08T05:26:30Z
created_at: 2026-10-08T05:26:29Z
completed_at: 2026-10-08T07:01:47Z
branch: codex/university-workplace-english-20261008
depends_on:
  - 2026-10-08-complete-all-six-senior-high-english
scope:
  - docs/videos/english-university-complete
  - docs/videos/english-workplace-complete
  - tools/video/adult_english
---

# Complete university and workplace English courses

## Why

Continue the user's completed high-school course with university and workplace
English. Each course has four seasons of twelve lessons, 96 videos total.

## Definition of done

- [x] Two original 48-lesson courses, independently reviewed in all five languages.
- [x] 96 checked videos, 480 audio tracks and 384 SRT/VTT pairs.
- [x] Two complete and eight seasonal ZIPs, players, catalogs and printable practice.
- [x] Required checks passed, portable evidence recorded and draft continuation PR opened.

## Steps

- [x] Author and review all eight seasons; freeze each source before speech production.
- [x] Create isolated adult-course renderer, validators, player and packaging tools.
- [x] Produce and verify both courses, worksheets and all ten delivery archives.
- [x] Close this task in the final commit and open a draft PR.

## How to verify

Run tools and task checks, source and artwork QA, actual FFprobe and full-decode
receipts, exact caption timing, source-bound hashes, independent ZIP/PDF/player QA.

## Notes

Both courses are complete: university 48 videos / 11,027.027 seconds; workplace
48 videos / 10,729.699 seconds. Each course has four thematic stages, 480 scenes,
240 audio tracks and 192 SRT/VTT pairs. Fixed English text, English original audio
plus zh-TW/zh-CN/ja/ko teaching voices, four translated CC tracks, no English CC.
The accepted ten-scene micro-lesson format applies; generic technology-video
8-minute guidance does not apply.

Eight full five-language sources were independently reviewed and frozen before
speech production. All 960 scenes / 2,880 phase frames passed artwork QA. Both
courses passed actual full-media verification, and 12 selected episodes / 36
encoded frames were directly inspected across A/B/C answer positions. Runtime
correctness review found no unresolved P1/P2; all reviewed code hashes remain
unchanged. Source fingerprint includes the full authored episode and speech settings.

Each course has four season ZIPs (209 members each) and one complete ZIP (821
members), with independent CRC, SHA, exact membership, fresh ffprobe metadata and
1,632 comparisons to checked root media. All 48 readings, 144 questions/answers
and 48 writing tasks/models per course match the final 145-page/full and 37-page/
season PDFs. Activities precede separate answers. jsdom checks use mocked media
events; actual browser playback was previously blocked by administrator policy
and was not retried by another route. Samples do not establish full-film viewing
or complete manual audio listening. Voices are Microsoft Edge trial voices,
not the configured backend voices; no backend publication or deployment occurred.

Actual full audio, batch, strict verification and packaging processes all exited 0.
Independent delivery checks also exited 0 for both courses, with zero errors.
Confirmed repository checks exited 0 at 2026-10-08T05:45:33Z: 2,015 tests,
2,012 passed, three skipped, zero failed, including 40 adult regressions.
Code did not change after that check. Logs: /tmp/adult-english-confirmed-checks.
Portable authoring, runtime, artwork, encoded-frame and delivery evidence is in
each new course documentation directory. Large media/archives stay outside Git at
/workspace/university-series-output and /workspace/workplace-series-output.

Claimed after initial branch, worktree, remote-head, open-PR and scope checks.
Pre-PR recheck found one worktree, no competing local/remote course branch or PR,
and no main/other-branch changes in the new scopes. Base remains the senior-high
branch at 0f723c137be334649494f7b4dc2366bcc795720a (draft PR #1383).
Only the two new documentation directories, tools/video/adult_english and this
task change; every earlier course source/tool/media is preserved. Each new course
uses a private speech cache; immutable earlier MP3/WAV files were reused with
separate copied metadata. User authorizes complete delivery and a draft
continuation PR, not merging or publishing. Draft PR #1385 was created successfully:
https://github.com/x812033727/travel_scanner/pull/1385
This task closes in the final commit in that PR. No merge or deployment occurred.
