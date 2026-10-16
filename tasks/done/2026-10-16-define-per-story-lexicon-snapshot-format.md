---
id: 2026-10-16-define-per-story-lexicon-snapshot-format
title: Define per-story lexicon snapshot format without worker integration
status: done
priority: P2
area: tools
owner: codex-story-lexicon-snapshot
claimed_at: 2026-10-16T08:26:31Z
created_at: 2026-10-16T08:26:23Z
completed_at: 2026-10-16T08:53:27Z
branch: codex/story-lexicon-core-20261016
depends_on: []
scope:
  - tools/video/core/story-lexicon.mjs
  - tools/video/core/story-lexicon.test.mjs
---

# Define per-story lexicon snapshot format without worker integration

## Why

A01's historical source audit binds the entire shared `docs/videos/lexicon.json`.
Two terms added for another video changed that file without changing A01's
spoken words. This foundation defines content-addressed, per-story lexicon
versions and a strict reader, so a later worker integration can stop depending
on unrelated edits. The broader integration ticket currently lives in draft
PR #1510 (`2026-10-16-bind-story-audits-and-narration-to`); its `story.mjs`
scope overlaps active PR #1518, so this ticket deliberately owns only two new
core files.

## Definition of done

- [x] A fixture can create a first story snapshot and a reviewed revision as
      immutable, hash-addressed bytes, then read the same value after restart.
- [x] The reader verifies the current pointer, every event in its revision
      chain, and every referenced lexicon byte hash. Missing or corrupt pinned
      bytes fail closed; a legacy story without a snapshot reads the shared
      dictionary in an explicitly marked compatibility mode.
- [x] A shared dictionary edit alone leaves a pinned story's bytes and hash
      unchanged in the fixture. Path traversal, malformed names and a broken
      chain are rejected.
- [x] The module has no production writer, worker hookup, host operation,
      A01 audit migration, approval, or paid continuation. Deployment stays
      blocked until a separate reviewed integration and release plan.

## Steps

- [x] Specify strict snapshot and revision event schemas with pure planners.
- [x] Implement the read-only filesystem inspector with legacy fallback.
- [x] Test initial snapshot, revision, restart, unrelated shared edit,
      corruption and legacy compatibility in OS temporary fixtures.
- [x] Obtain independent review and run focused checks; prepare a draft PR with
      `no-auto-merge`.

## How to verify

Use bundled Node 24.19 for
`node --test tools/video/core/story-lexicon.test.mjs`, then run
`npm run test:tools` and `npm run check:tasks`. Confirm that no existing files
under `tools/video/automation/` changed and no live A01 audit was touched.

## Notes

No production data change is permitted by this ticket. The current A01
80-event inspector still expects the shared lexicon's old SHA and must remain
unchanged. A separate append-only transition, with its own approval and audit
writer protocol, is required before A01 can adopt any per-story snapshot.

Local validation on 2026-10-16: both modules passed `node --check`; focused
`node --test tools/video/core/story-lexicon.test.mjs` passed 8/8; `npm run
check:tasks` passed with 1,911 task files checked. The repository-wide
`npm run test:tools` finished with exit 1 due three `renameSync` EPERM errors in
unmodified TTS test fixtures under Windows Temp. A lower-concurrency run of
the two affected TTS files also failed with the same Temp rename error in a
different case; an isolated Temp directory still reproduced it. The core
module was not part of those failures. CI must run the complete suite.

Independent read-only review on the frozen module/test version accepted this
foundation. The revision planner checks the previous snapshot's shape and
content hash but does not authenticate its source; the later integration must
obtain it from a strict read and provide an exclusive writer protocol. This
module does not repair A01, activate a worker path, or authorize deployment.
