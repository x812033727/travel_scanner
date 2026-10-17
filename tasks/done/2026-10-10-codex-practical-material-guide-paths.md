---
id: 2026-10-10-codex-practical-material-guide-paths
title: Clarify Codex lesson 01 outer guide and baseline prompt paths
status: done
priority: P1
area: docs
owner: codex-gpt6-practice-design
claimed_at: 2026-10-10T18:20:42Z
created_at: 2026-10-10T18:20:36Z
completed_at: 2026-10-10T18:25:44Z
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - tools/codex-practical/labs.mjs
  - docs/videos/codex-practical-series/materials/lessons
---

# Clarify Codex lesson 01 outer guide and baseline prompt paths

## Why

Lesson 01 keeps exactly five original files in start. The outer baseline-prompt.txt,
README.md and acceptance.md are not inside that project. Its README named the
prompt without the parent path, and its App prompt asked the model to read guide
files that do not exist in start. Readers must know which files they read before
opening the project and which path the terminal uses afterwards.

## Definition of done

- [x] Lesson 01 explicitly uses ../baseline-prompt.txt while the current directory is start.
- [x] App readers read outer README/acceptance and provide requirements before opening the exact five-file start.
- [x] Original project files, recorded baseline prompt and authored video text remain outside this change.
- [x] Fresh build-07/build-08 contain 18 byte-identical learner ZIPs and matching manifests.
- [x] Course integration passes once with a new log/receipt; no historical evidence is overwritten.

## Steps

- [x] Claim only the generator and tracked material guides; coordinate separate lesson/episode corrections with their owner.
- [x] Change lesson 01 wording in the generator and regenerate the tracked guides.
- [x] Run the relevant course integration and build two fresh external deliveries.
- [x] Verify ZIP hashes, guide/source boundaries, preserve receipts and finish this ticket.

## How to verify

Run Node 24.19.0 --test tools/codex-practical.test.mjs once. Capture its actual exit
code and full log in a new external run folder. Rebuild all 18 packages in fresh
build-07/build-08 directories using the same materializer/packer, without updating
root-owned evidence files. Compare both delivery manifests and all ZIP SHA-256
values; compare each original project/prompt hash with the protected-before receipt.

## Notes

- Root explicitly authorized this narrow follow-up after the curriculum ticket was done.
- Only lesson 01 README.md, prompts.md and lesson.json changed after guide regeneration;
  other lesson guides stayed byte-identical. Source snapshots were not edited.
- Current course lesson/episode extraction instructions are being handled under
  2026-10-10-codex-practical-zip-root-followalong, a separate scope.
- External receipts use runs/material-guide-paths-20261011; root will update
  evidence/packages.json and evidence/validation.json centrally after handoff.
- Course integration ran once with bundled Node24.19.0: 11 tests, 11 pass, zero
  fail/skip/TODO, exit0, 55.46 seconds. New full log: course-guide-path-tests.log,
  SHA256 312b8aaba70cc468410a93d85cd46aa27da988c885be2034aa4762a72d1b1142.
  Actual command/runtime/exit are in course-test-receipt.json.
- build-07/build-08 each contain 18 ZIPs; both delivery manifests SHA256
  69fcfc669ec11b2d51ce488a3c032b4861677fc244c586e00e7a4d4d7fa119b6.
  All 18 ZIP hashes match across builds. All 1,030 snapshot files match build-05;
  only outer 01/README.md, 01/prompts.md and 01/lesson.json changed. The build
  wrapper uses the existing materializer and packer without touching root-owned
  evidence files; build-receipt.json records runtime and package hashes.
- Independent read-only guide audit confirmed all 49 pre-change protected hashes,
  original exact-five-file baseline and model prompt. The root subsequently made
  a separately authorized listener-wording change to video/script; that delta was
  independently checked and rebound under the pilot task, not this material task.
- A second independent read-only audit confirmed both new ZIP deliveries, the three
  updated guide files, all 54 unchanged snapshots and the new 11-PASS log hash.
- The first tasks done command wrote the completed task but could not remove its
  old open copy on Windows. Only this task's redundant open file was removed with
  an exact-file patch. The new tasks-after-open-copy-cleanup.log records check exit0,
  1,763 task files validated; the earlier failed check log is preserved.
