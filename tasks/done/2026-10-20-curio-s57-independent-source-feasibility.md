---
id: 2026-10-20-curio-s57-independent-source-feasibility
title: Independently verify S57 Livingstone sources and meeting-date conflict
status: done
priority: P2
area: docs
owner: codex-s57-source-reviewer
claimed_at: 2026-10-20T22:28:53Z
created_at: 2026-10-20T22:28:14Z
completed_at: 2026-10-20T22:32:03Z
branch:
depends_on:
  - 2026-10-20-curio-s57-livingstone-stanley-preproduction
scope:
  - docs/videos/curio-s57/source-feasibility-1.md
---

# Independently verify S57 Livingstone sources and meeting-date conflict

## Why

The S57 Stanley/Livingstone A-case author brief and ten-claim research table are ready. Before scripting, a separate reader must test the actual fixed texts and their publication layers, particularly the conflicting meeting dates, single-source famous greeting and motivation for not returning.

## Definition of done

- [x] Publish `docs/videos/curio-s57/source-feasibility-1.md` with a PASS/HOLD decision on all ten P claims and the A-case answer, including source-layer and written-visual cautions. The reviewer must decide whether another original or institutional source is needed before scripting.

## Steps

- [x] Independently reopen both exact GITenberg commits named in `research.md` and verify their raw SHA-256 rather than adopting author excerpts as evidence.
- [x] Check P01–P10 against the texts, separate Stanley's abridged memoir from Livingstone's posthumously edited diary and Susi/Chuma's reported account.
- [x] Resolve or explicitly HOLD the November 10 versus October 28 meeting-date discrepancy; keep exact date out of speech if unresolved.
- [x] Check that cartoon scene concepts do not imply verbatim dialogue, a proved Nile-source hypothesis, only two people on the expedition, or invented ethnic details.
- [x] Record checks and handoff; leave the author files untouched in this task.

## How to verify

`sha256sum` of the two raw files; `nl -ba` against every referenced line; `npm run check:tasks`; `git diff --check -- docs/videos/curio-s57/source-feasibility-1.md`.

## Notes

Read `docs/videos/curio-s57/research.md` and `brief.md` only after fetching the original source files if practical. Fixed commits: Stanley `41828f7623e5ba1b0db0a4c96630bda15bb0b66e` / `5157.txt` (abridged), Livingstone/Waller `bd976e865f60f2bc17628640378e4510969a94ad` / `17024-0.txt` (1874 edited volume). Expected author hashes are in `research.md`. Johnstown candidate was rejected for weak warning-receipt evidence, as archived in `tasks/done/2026-10-20-curio-s57-johnstown-warning-preproduction.md`. No S57 script or paid media exists.

2026-10-20 review: both raw hashes matched. A case conditionally PASS; exact meeting day HOLD. The full P01–P10 audit and exact lines are in `docs/videos/curio-s57/source-feasibility-1.md`. Key author handoff: L5741–50 directly reports Stanley urged a return and Livingstone decided to finish work, while S's detailed dialogue remains single-source; S already places a homeward appeal before February resupply. Also correct S `Abridged` citation to lines 33–40, L meeting date's typography to italic parentheses, and P08 medicine citation to L5806–10. No third source is needed for a script that omits exact meeting day and literal dialogue; an original or institutional edition is needed if either is asserted. Author brief/research remained untouched.
