---
id: 2026-10-19-a01-readonly-capture
title: Capture current A01 host evidence without production writes
status: done
priority: P1
area: tools
owner: codex-gpt6-a01-capture
claimed_at: 2026-10-19T00:52:08Z
created_at: 2026-10-19T00:51:33Z
completed_at: 2026-10-19T02:57:56Z
branch: codex/a01-readonly-capture-20261019
depends_on: []
scope:
  - tools/video/a01-capture
---

# Capture current A01 host evidence without production writes

## Why

The old A01 export inspector pins exactly 80 audit events. The current offline
editorial proposal is based on 104 historical events, so it needs a fresh,
complete production readback before any chapter adoption or paid work. A single
local command should collect that readback through the existing PuTTY session,
without changing the host or displaying private data in chat.

## Definition of done

- [x] A bounded read-only command captures the exact A01 files, audit history,
      control state, DB jobs and budget into a new local directory.
- [x] The command rejects fewer than 104 audit events, missing required files,
      readback drift, unsafe destination paths and remote command failures.
- [x] Synthetic tests pass; no host connection is exercised in development.
- [x] A local verifier rejects unsafe tar members and checks every captured
      file, audit record and bound revision receipt without extraction.

## Steps

- [x] Implement the capture command, remote read-only scripts and SQL projection.
- [x] Add focused synthetic checks and document the one-command owner handoff.
- [x] Add a local archive integrity command for the fresh capture.

## How to verify

`node --test tools/video/a01-capture/capture.test.mjs tools/video/a01-capture/verify-archive.test.mjs` and
`node tools/video/a01-capture/capture.mjs --help`.

## Notes

The legacy `A01-host-export-candidate` requires exactly 80 links and remains
untouched. Capture output is evidence only, always HOLD; it is not a writer,
approval receipt, media trigger or deployment step.

The updated capture includes the A01 story-lexicon snapshot and immutable
running-worker image, release, Git tree and complete `tools/video` runtime file
inventory pins. The verifier requires all seven outputs while keeping an
operational job HOLD separate from evidence completeness. Synthetic checks:
`node --test` 14/14, `node --check`, Bash `-n` and the embedded Python AST
syntax check pass. The owner ran the fresh `-03` capture; its seven-file archive
passed local integrity verification with 104 audit events. Its status remains
`HOLD` because unrelated production jobs were active. This author has not
connected to the host.
An independent review identified that an unresolved `uncertain` stage job was
excluded from the global job projection; the SQL and a defensive A01 check now
hold for that status, with a focused regression test.
The task-board-wide check cannot be interpreted in this sparse worktree because
historical `tasks/done` files are omitted; it reports missing dependencies
outside this task. No host connection was used by the author. An interrupted
Git operation left an index lock; automatic policy review blocked its removal.
The owner removed that exact lock manually and the worktree now reports it absent.
