---
id: 2026-10-20-curio-s57-livingstone-stanley-preproduction
title: Prepare S57 Livingstone and Stanley history episode
status: done
priority: P2
area: docs
owner: codex-s57-preproduction
claimed_at: 2026-10-20T22:25:56Z
created_at: 2026-10-20T22:25:56Z
completed_at: 2026-10-20T22:28:11Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57
---

# Prepare S57 Livingstone and Stanley history episode

## Why

The owner asked for further original, nonduplicate Curio history episodes. S57 needs a sourced, single-question story that can later enter the normal script and media gates. The earlier Johnstown candidate did not pass source feasibility.

## Definition of done

- [x] Produce a fixed-source S57 research pack and an A/B brief with an evidence-bound answer, story beats and established channel bookends.
- [x] Expose unresolved source conflicts and leave an independent source-audit gate before any script or paid media.

## Steps

- [x] Deduplicate against existing Curio stories and read two independently authored original accounts.
- [x] Freeze GITenberg revisions and SHA-256, map ten narrow claims with line links.
- [x] Write `docs/videos/curio-s57/{research,brief}.md`; mark the exact meeting date and quoted dialogue as unresolved.
- [x] Validate task board and create a separate unclaimed source-audit task.

## How to verify

`git status --short docs/videos/curio-s57`; `git diff --check -- docs/videos/curio-s57`; `npm run check:tasks` (passed on 2026-10-20, unrelated stale-task warnings). Source files fixed at Stanley commit `41828f7623e5ba1b0db0a4c96630bda15bb0b66e` SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`, Livingstone/Waller commit `bd976e865f60f2bc17628640378e4510969a94ad` SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`.

## Notes

2026-10-20: S57 candidate changed from Johnstown flood warnings to Stanley finding Livingstone but not bringing him home; the Johnstown source assessment is archived in `tasks/done/2026-10-20-curio-s57-johnstown-warning-preproduction.md`. The two S57 texts independently record the meeting, joint travel, resupply and March 1872 separation, but Stanley's e-text is explicitly abridged and Livingstone's diary was edited after his death. Stanley's Nov 10 meeting date conflicts with the diary's parenthesized Oct 28; neither the famous greeting nor return-home dialogue is independently verbatim verified. The brief uses the 1871 season, attributes the dialogue to Stanley, and keeps exact date off narration until source audit. No script, audio, illustrations, music, or upload work was done. Site MiniMax judge and music quota remains exhausted until expected November reset. Next gate is the separate S57 independent source-audit task.
