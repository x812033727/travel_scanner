---
id: 2026-10-30-h3-sh-start-ignores-colab-gpu
title: h3.sh start ignores COLAB_GPU, so h3_detached.py sessions land on A100
status: done
priority: P2
area: tools
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-30T14:33:13Z
created_at: 2026-10-30T13:54:01Z
completed_at: 2026-10-30T14:34:31Z
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab/scripts/h3.sh
  - .claude/skills/minimax-h3-colab/scripts/h3.sh
  - tools/minimax-h3-colab.test.mjs
  - .agents/skills/minimax-h3-colab/references/lessons.md
---

# h3.sh start ignores COLAB_GPU, so h3_detached.py sessions land on A100

## Why

`COLAB_GPU=G4 python3 -I scripts/h3_detached.py jobs.json --session zt33g` on 2026-10-30 (e033 route
pilot) ran its three 1920x1088 clips on an **A100**, not G4, and left the session up after the run.
`h3_detached.py` creates a missing session with `bash h3.sh start --session NAME`; `h3.sh` passes
`start` straight to the upstream `runner.py start`, whose `--gpu` defaults to `"A100"` and, unlike
`batch` and `single`, does not read `COLAB_GPU`. So every detached run silently uses A100, at a
higher CU rate, and the G4 minutes-per-clip numbers the Ref2VA ticket asked for were never measured.

## Definition of done

- [x] `COLAB_GPU=G4 h3.sh start --session X` opens a G4 session (and with `--no-high-mem`, as G4 needs).
- [x] An explicit `--gpu` on the command line still wins.
- [x] Both skill copies stay byte-identical.

## Steps

- [x] In `h3.sh`, for `start`, add `--gpu "$COLAB_GPU"` when the caller gave none, then the existing
      `single_shape_flag`.
- [x] A test in `tools/minimax-h3-colab.test.mjs` with a fake `runner.py` that records its argv.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
```

## Notes

- Workaround until fixed: open the session yourself first, `COLAB_GPU=G4 h3.sh start --session zt33g --gpu G4`
  (h3_detached reuses a live session), and confirm with `colab sessions` that it says `Hardware: G4`.
- `h3_detached.py` does not stop the session at the end; stop it with `h3.sh stop --session NAME`.
- 2026-10-30 fixed (claude-opus-5.5-zt-e033): `h3.sh start` appends `--gpu "$COLAB_GPU"` unless `--gpu` or
  `--gpu=` is already there; `single_shape_flag` then adds `--no-high-mem` for G4/L4 as before. The old test
  only checked `--no-high-mem`, so it passed while the runner still got A100; it now expects `--gpu`, and a new
  test covers the default, an explicit `--gpu` and `--gpu=`. Both fail against the old `h3.sh`.
- Live check: `COLAB_GPU=G4 h3.sh start --session zt-gpucheck` (no `--gpu`) -> `colab sessions` shows
  `Hardware: G4`; stopped right after.
- `.claude/skills/minimax-h3-colab/` holds only SKILL.md, so there is no second copy of h3.sh to keep in step.
- Not changed: `h3_detached.py` still leaves the session up at the end (documented in lessons.md §6).
