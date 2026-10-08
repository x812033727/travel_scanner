---
id: 2026-10-08-complete-university-workplace-english
title: Complete university and workplace English courses
status: in-progress
priority: P2
area: tools
owner: codex-adult-english-series
claimed_at: 2026-10-08T05:26:30Z
created_at: 2026-10-08T05:26:29Z
completed_at:
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
- [ ] 96 checked videos, 480 audio tracks and 384 SRT/VTT pairs.
- [ ] Two complete and eight seasonal ZIPs, players, catalogs and printable practice.
- [ ] Required checks passed, portable evidence recorded and draft continuation PR opened.

## Steps

- [x] Author and review all eight seasons; freeze each source before speech production.
- [x] Create isolated adult-course renderer, validators, player and packaging tools.
- [ ] Produce and verify both courses, worksheets and all ten delivery archives.
- [ ] Close this task in the final commit and open a draft PR.

## How to verify

Run tools and task checks, source and artwork QA, actual FFprobe and full-decode
receipts, exact caption timing, source-bound hashes, independent ZIP/PDF/player QA.

## Notes

Claimed after checking local branches, worktrees, all remote branches and open PRs;
no competing university/workplace task. Base senior-high branch at
0f723c137be334649494f7b4dc2366bcc795720a (draft PR #1383).
Scope is only the two new documentation directories, tools/video/adult_english,
and this task. Preserve every previous course, tool and media file.
User authorizes full continuation and draft PR, not merging or publishing.
The accepted ten-scene micro-lesson format applies; generic technology-video
8-minute guidance does not apply. Fixed English picture text, no English CC;
English original audio plus zh-TW/zh-CN/ja/ko teaching voices and four CC sets.
Use established Edge trial voices, honestly distinguished from backend voices.
Outputs: /workspace/university-series-output and /workspace/workplace-series-output.
No need for actual browser access: prior administrator block remains in force;
use true FFmpeg/ffprobe and explicitly mocked jsdom control checks.

Adult runtime frozen: sunny-pip-adult-english-v1, profile1/sharedengine3; 15fps
fingerprint 57d70a9f555a482281c126c864b70d3fd20da9943a336c6462b6122fc91fa54b.
Both actual brand pilots directly inspected and fixture QA passed; same-ID/course/stage
cache isolation and glyph-erasure negative control are covered.
Confirmed repository checks exited0 at 2026-10-08T05:45:33Z: 2015 tests,2012pass,3skip,0fail;
40 adult Python regressions. Logs/exit receipt: /tmp/adult-english-confirmed-checks.
Independent reviews use /tmp/adult-authoring-review-<course>-sNN.json; only clear source
SHAs enter production. Root reviewed UniversityS3 andWorkplaceS3 completely and verified
all requested corrections; generic university cues now teach episode-specific concepts.
Production starts WorkplaceS1 andUniversityS3, eachwith itsown output/privatecache,
one audio producer peroutput. Existing completed speech is reused through immutable
MP3/WAV hardlinks with separate copied metadata; no earlier course media is changed.

All eight seasons independently cleared and frozen. Full university source SHA
a425e6cdb6443e7830ebcb776a8a713a0199d7e8ad6d55b287373b73b10175d4;
full workplace source SHA
75b306e8e84e87bbf8c809d0641ee583797678a5f8a5061b6254645bbbf53b39.
Portable authoring-review.json in each new course directory binds all four final
season sources and records review scope, corrections and zero unresolved P1/P2.
Actual full-course production is in progress; all media/package completion items
remain open until the corresponding final evidence is verified.
