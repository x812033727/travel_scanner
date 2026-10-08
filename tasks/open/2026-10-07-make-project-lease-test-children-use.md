---
id: 2026-10-07-make-project-lease-test-children-use
title: Make project lease test children use portable Windows imports
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T10:24:13Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/project-lease.test.mjs
---

# Make project lease test children use portable Windows imports

## Why

On Windows with Node24.19, both cross-process lease tests fail because the holder
exits1 before reporting held. The generated ESM child imports a native absolute
path produced by fileURLToPath; Node rejects the c: URL scheme. This was observed
in the full tools run during article-localization validation.

## Definition of done

- [ ] Both cross-process holder tests complete on Windows and Linux.
- [ ] Real live/dead-holder and retained-byte assertions remain meaningful.
- [ ] Test children terminate on failures without touching unrelated processes.

## Steps

- [x] Pin the actual holder import and observed two failing tests.
- [ ] Use a portable file URL in the generated ESM test script.
- [ ] Run the affected file on Windows and the required Linux CI suite.

## How to verify

Run node --test tools/video/core/project-lease.test.mjs with the supported bundled
Node on Windows, then the exact-head Linux tools CI. No project-lease production
behavior has been changed or diagnosed as broken by these platform test failures.

## Notes

Full local tools run exited1. The separate existing automation test import,
reference-analysis range and from-drama brightness tickets remain unchanged.
