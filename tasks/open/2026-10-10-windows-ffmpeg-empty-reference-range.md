---
id: 2026-10-10-windows-ffmpeg-empty-reference-range
title: Handle empty video frames in Windows ffmpeg reference range comparison
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-10T17:38:43Z
completed_at:
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - tools/reference-analysis.test.mjs
  - .agents/skills/youtube-video/scripts/reference_analysis.mjs
  - .claude/skills/youtube-video/scripts/reference_analysis.mjs
---

# Handle empty video frames in Windows ffmpeg reference range comparison

## Why

The existing reference-analysis test fails on Windows when its 4–6 second range selects no video frames. ffmpeg exits 4294967274 with wrapped_avframe/Invalid argument, although the range should produce an empty cut comparison. Found while validating the Codex course; none of this task's implementation files were changed by that course.

## Definition of done

- [ ] The real synthetic 4–6 second range succeeds and produces the expected empty comparison without masking genuine ffmpeg errors.
- [ ] Windows and supported POSIX behavior remain covered; shared skill copies stay byte-identical.

## Steps

- [ ] Reproduce with the current Windows ffmpeg build and inspect the exact no-frame filter/output command.
- [ ] Distinguish empty selected frame output from invalid media, fix the smallest relevant behavior, rerun the targeted test and full tools suite.

## How to verify

`node --test --test-name-pattern="--compare matches" tools/reference-analysis.test.mjs` reproduces at line447. Full `npm run test:tools` also reports the same failure. Use bundled Node24.19 on this host.

## Notes

2026-10-11: Reproduced twice, including a standalone run (1 test/1 fail). Root course changes do not alter these files. Logs: `<home>/mokaair-work/codex-practical-series/runs/reference-analysis-rerun.log` and `test-tools.log`. Test failure contains `Nothing was written into output file, because at least one of its streams received no packets`. This is a recorded unresolved broader-check failure, not a passing course check. No fix attempted in this ticket.

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
