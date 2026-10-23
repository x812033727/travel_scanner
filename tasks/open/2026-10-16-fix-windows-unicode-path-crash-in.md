---
id: 2026-10-16-fix-windows-unicode-path-crash-in
title: Fix Windows Unicode path crash in imported video runtime packaging
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-16T03:13:39Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/imported-long-languages/package-runtime.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

# Fix Windows Unicode path crash in imported video runtime packaging

## Why

In a Windows checkout whose path contains `ㄐ` (for example
`<home>/.codex/worktrees/curio-next-five/travel_scanㄐ`), system Node
v24.13.0 crashes while `package-runtime.mjs` recursively copies `tools/video`
to a temporary portable batch. The test at `runner.test.mjs:363` exits at its
first `execFileSync` (`:367`) with Windows status `3221226505` (`0xC0000409`)
and empty stdout/stderr. This leaves the destination `root/tools/video` empty
and no `runtime-receipt.json`. Locally, `npm run test:docs-videos` therefore
passes 214/215 tests. The affected runtime and test files are unchanged from
`origin/main`; this is unrelated to the Curio episode document changes.

## Definition of done

- [ ] Runtime freezing completes from a Windows checkout with a non-ASCII path
      under the supported Node version, writes a verifiable receipt, and still
      refuses to overwrite an existing runtime.
- [ ] The regression test covers the non-ASCII path without weakening the
      existing portable-root and no-overwrite checks.

## Steps

- [ ] Confirm the Node/Windows recursive-copy failure and choose a compatible
      copy path for `package-runtime.mjs`, preserving its current safety checks.
- [ ] Add a focused Unicode-path regression to `runner.test.mjs` and verify it
      with system Node v24.13.0 and the repository's bundled Node v24.19.0.

## How to verify

On Windows from a checkout with a non-ASCII path, record `node --version`, then
run:

```powershell
node --test --test-name-pattern="initial runtime freezing resolves a portable relative root and refuses to overwrite an existing runtime" docs/videos/imported-long-languages/runner.test.mjs
npm run test:docs-videos
```

Inspect the generated fixture's `runtime-receipt.json` assertions and confirm
that the second invocation still fails with `Runtime already exists`.

## Notes

- 2026-10-16 read-only diagnosis: `fs.cpSync(src, dst, {recursive:true})` in a
  child process copied a minimal ASCII temporary source successfully. Moving
  the same one-file source under a `unicodeㄐ` directory reproduced status
  `3221226505`, empty streams, and an empty destination. A no-op
  `filter: () => true` made that minimal copy succeed; treat it as a diagnostic,
  not a verified production fix.
- Copying existing `tools/video/assemble` and `docs/videos/curio-h10` directories
  from this checkout reproduced the same failure. `package-runtime.mjs:20`
  is the first recursive copy. A scratch invocation left no receipt. The
  repository test case and package runtime have no branch diff against
  `origin/main`.
- Existing task notes report that the isolated test passes with bundled Node
  v24.19.0 (`tasks/open/2026-10-13-remake-curio-h04-h05-h06-with.md`) and that
  the full suite passes 215/215 under that runtime
  (`tasks/open/2026-10-14-five-curio-style-brand-story-video.md`). Recheck
  those observations when implementing; this task targets the reproducible
  system-Node failure.
- `tasks/open/2026-10-07-imported-long-videos-language-batches-carry.md` also
  scopes `runner.test.mjs` but was open and unclaimed when this task was filed.
  Coordinate scope before claiming either task.
