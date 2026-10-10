---
id: 2026-10-10-codex-practical-zip-root-followalong
title: Fix Codex practical ZIP root follow-along paths
status: done
priority: P1
area: docs
owner: codex-gpt6-claude-reference
claimed_at: 2026-10-10T18:18:30Z
created_at: 2026-10-10T18:18:24Z
completed_at: 2026-10-10T18:22:12Z
branch: codex/codex-practical-series-20261011
depends_on:
  - 2026-10-10-codex-practical-curriculum
scope:
  - docs/videos/codex-practical-series/lessons
  - docs/videos/codex-practical-series/episodes
---

# Fix Codex practical ZIP root follow-along paths

## Why

Every delivered lesson ZIP extracts directly to README.md/start/reference/challenge. The 18 lesson specifications and 36 paired episode briefs instead told readers to choose a lessons directory and append NN/start. A reader using the linked single-lesson ZIP could not follow that setup. Correct only the course setup paragraphs, source-path snippets and snapshot labels; preserve all authored project code, feature prompts and frozen production scripts.

## Definition of done

- [x] All 54 course setup snippets use the single-lesson extraction root and its direct start directory, with a guard for README.md and start.
- [x] The actual 18 build-05 ZIPs extract correctly and all 54 setup/copy snippets produce byte-identical complete start copies.
- [x] Course completeness, relative links, Markdown fences and whitespace checks pass; latest lesson 18 hashes are reported for independent receipt refresh.

## Steps

- [x] Confirm the delivery ZIP root and claim the narrow lesson/episode follow-up scope.
- [x] Replace lessonPackages/NN-start setup with lessonRoot/start and correct per-ZIP snapshot labels.
- [x] Replay the exact setup/copy steps against freshly extracted ZIPs, compare all copied file hashes and preserve the receipt outside Git.
- [x] Run task validation and archive this follow-up for the draft PR; do not commit or push from this subtask.

## How to verify

Run `node tools/codex-practical/course.mjs check` and `npm run check:tasks`. Check all 54 course documents for balanced fences, existing relative links and absence of lessonPackages. Extract each `build-05/delivery/codex-practical-NN-materials.zip` into a new external directory; substitute only lessonRoot and lessonWork in its setup snippet, execute through Set-Location, then compare every source/copy path and SHA-256. This verifies ZIP setup/copy instructions; it does not rerun feature tests, models or media.

## Notes

2026-10-11: independent delivery audit identified this required follow-along fix after the main curriculum task had been archived. The task CLI explicitly rejects claim/status/release on done tasks, so this new narrowly scoped follow-up depends on the completed curriculum and preserves that history. All 54 snippets now require the reader to select the single-lesson root containing README.md, start, reference and challenge; they no longer instruct a single-ZIP reader to locate a nonexistent lessons/NN wrapper.

Only course lessons/episodes are changed. `docs/videos/codex-practical-01-cli` video.json/script.md/production brief and every production ticket remain untouched. The final lesson 18 functional prompt/scaffold scope remains the same; its three changed document hashes were sent to the independent reviewer and parent for source-bound receipt refresh, with historical hashes retained.

The first external PowerShell replay attempt had an audit-runner array construction error before any setup copy executed. Its partially extracted directory was preserved; the corrected replay uses a new external directory. No source, copied result or existing output was deleted or overwritten.

Actual corrected replay: `<home>/mokaair-work/codex-practical-series/runs/zip-root-followalong-20261011-182045/receipt.json` records 18 ZIP extractions and 54 parsed/executed setup-copy snippets. `content-check.json` records 1,029 source/copy file path and SHA-256 comparisons, all PASS; its SHA-256 is `dfcd8a9c610194be8789a36846ef8ca4eceb7e34b887fc0a543c9f45eec6f4f9`. All 18 input ZIP hashes match the existing build-05 manifest. The reader-replaced lessonRoot and fresh lessonWork are the only substituted snippet lines; baseline feature tests, models, native App and media were not rerun.

Fresh course check reports 18 lessons/36 episodes/errors []; all 54 relative links, fences and ZIP-root path assertions pass. `git diff --check` is clean. `npm run check:tasks` passes with only unrelated stale-claim warnings. Main curriculum remains done and paired production tickets remain open; the new follow-up completion records only this verified ZIP setup correction.

Final lesson 18 provenance audit: external `lesson18-zip-root-audit.json` (SHA-256 `12ef68a194a0e568243506d376dd8f668dfb75fe252d45e5db1c1866da656828`) and `lesson18-zip-root-diff.patch` in the same replay directory retain the three previous independently audited hashes and three current hashes. Reversing only the explicit ZIP-path edits reproduces each previous raw-byte hash exactly; all three functional main prompts remain identical. The existing core/archive TODO, author-scaffold and allowed-scope review judgment still applies. Refresh of tracked independent-final-review metadata belongs to the parent/independent reviewer; the previous hash is not presented as current.

On Windows the done command wrote the final record but left the old open copy. After verifying both bodies differed only in status/completed_at, native PowerShell removed only that duplicate open file. The done record and all evidence are retained.

公開定位說明：`<home>` 與 `<repo>` 是去識別佔位，不供直接執行。精確路徑與未遮罩原始收據保存在 repo 外；既有收據 SHA-256 仍綁定原始位元組。
