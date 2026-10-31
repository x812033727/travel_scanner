---
id: 2026-10-30-h3-colab-three-stage
title: Three-stage H3 on Colab G4: draft, refine and SeedVR2 to 1080p
status: done
priority: P2
area: tools
owner: claude-opus-5-5-h3-three-stage
claimed_at: 2026-10-30T06:20:52Z
created_at: 2026-10-30T06:20:44Z
completed_at: 2026-10-30T14:14:12Z
branch: claude/h3-colab-three-stage
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab
  - .claude/skills/minimax-h3-colab/SKILL.md
  - tools/minimax-h3-colab.test.mjs
---

# Three-stage H3 on Colab G4: draft, refine and SeedVR2 to 1080p

## Why

The owner asked (2026-10-30) for a three-stage H3 route: draft at 960x544 with 20 steps to fix
composition and motion, refine the drafts that pass at 1312x736 with the last steps only, then
SeedVR2 the refined clips to 1920x1080, on a Colab G4 (RTX PRO 6000 Blackwell 96 GB) through the
admin's video tool token. The pilot ran end to end that day in a scratchpad; this puts it in the
skill so the next batch is one command per stage.

## Definition of done

- [x] G4 (and L4) sessions are created without `--high-mem` by `h3.sh` (batch, single, start) and by
      `images.py`, because Colab rejects G4 with a high-RAM shape.
- [x] `h3.sh refine` (`scripts/refine.py` + `assets/h3_refine.ipynb`): a manifest of drafts is checked
      offline (`--check`), then refined on one session from `sigma_start` (default 0.5, 10 steps) with the
      first frame as keyframe; progress.json keeps frames, sigmas and seconds per job.
- [x] `h3.sh upscale` (`scripts/upscale.py` + `assets/seedvr2_upscale.ipynb`): SeedVR2 at a pinned
      commit, the prepended frames trimmed, exactly 1920x1080, frame count checked.
- [x] `references/three-stage.md` with the flow, why the refine starts at a sigma, the pilot numbers
      and the pitfalls; SKILL.md (and its `.claude` copy) and `cloud-pairing.md` §4 point to it.
- [x] Offline tests with a fake `colab` for all of the above.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs   # Linux/macOS (the file skips on Windows)
```

## Notes

- Pilot (2026-10-30, account A, Pro+, G4, zhong-tian e030 s21/s34/s42): stage 1 1.07 CU, stage 2
  2.51 CU (both sigmas), stage 3 1.48 CU; about 7 minutes and 0.9 CU per 6-second clip once warm.
  Numbers and pitfalls in `references/three-stage.md`. First frames were cut from the site's e030
  final preview (`review-files --gate final`), so nothing from this pilot was imported.
- "The last 10 of 20 steps" cannot be taken literally: with H3's shift 12 the 10th sigma is about
  0.92. The refine starts at a sigma instead; 0.5 kept the faces, 0.7 changed them.
- The refine graph follows Henge (alisson-anjos/Henge, MIT) `full_refiner_graph`; only core ComfyUI
  nodes are used.
- On Windows the Colab CLI runs in WSL; these tests ran there with a user-local Node 22.
