---
id: 2026-10-09-windows-process-birth-closure
title: Use captured Windows process birth for persisted closure checks
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T22:49:08Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/process-identity.mjs
  - tools/video/core/process-identity.test.mjs
---

# Use captured Windows process birth for persisted closure checks

## Why

On Oct10 06:47 Taipei, an Embedding zero-write review check started as PID
45076, which Windows had reused from an already closed V8 supervisor. The
private exact-CIM closure helper correctly saw a live PID but called the new
check the old producer, and refused at caller line32 before any API or native
command. The old producer's terminal and separate physical closure were retained.
The new check exited1 and a fresh read-only check used unchanged guards.
Persisted PID numbers alone cannot distinguish these two process lifetimes.

## Definition of done

- [ ] A reusable Windows identity records PID, executable and real birth ticks
      before launch evidence is accepted; no historical birth is invented.
- [ ] Closure distinguishes a confirmed different lifetime from the original
      live lifetime, while missing identity or failed CIM reads still refuse.
- [ ] Provider identity, no-replay rules, round limits and stage guards remain
      unchanged; this follow-up does not redo delivered recordings or reviews.

## Steps

- [ ] Add the narrowly scoped identity/closure primitive and an explicit contract
      for future guarded callers; do not adopt private sources wholesale.
- [ ] Check original-live, exited, reused-PID, missing-birth and read-failure cases.

## How to verify

Use the bundled Node24.19 runtime for focused tests. Include actual owned child
birth/closure reads and deterministic distinct-lifetime fixtures, without host,
API or provider calls. A new process with the same numeric PID must not establish
that the original process is live; a matching original birth must still refuse.

## Notes

Further Oct10 checks encountered numeric PID reuse at42788 and42388.
Immutable original-four chronology (8af2559f) and the13-PID closed checkpoint
260c9bdb prove the original lifetimes ended before later successful CIM births.
Private registry b228cdce restricts acceptance to these17 frozen predecessors,
rejects original/equal/future/malformed birth evidence, and passes58 offline
cases. New owned stages/receivers retain canonical physical-closure checks even
if their numeric IDs overlap. Unrelated processes were not killed. This private
registry is not the reusable product primitive; this P2 stays open/unclaimed.


The retained actual process record is
terminal-review-V8-segment3-postproduction-SH4-v1-dry-process.actual.json
(PID45076,exit1,actual subsequent CIM rows0). Its empty stdout and stderr
ca06a1c7227f0e8a891297e30bec9d853801523550ac14d8860c830d9c5f3b1c
prove the pre-command refusal; caller d4014c5b and helper bdc4fa5b are frozen.
Evidence stays outside Git under mokaair-work/stalled-video-completion-20261008/
embedding-audio/listener-round2/selected-language-finishing-20261009.
This ticket is unclaimed and contains no source or production change.
