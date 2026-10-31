---
id: 2026-10-30-seedvr2-notebook-re-upscales-every-clip
title: SeedVR2 notebook re-upscales every clip a session has seen
status: done
priority: P2
area: tools
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-30T22:14:22Z
created_at: 2026-10-30T22:14:14Z
completed_at: 2026-10-30T22:15:09Z
branch:
depends_on: []
scope:
  - tools/minimax-h3-colab.test.mjs
---

# SeedVR2 notebook re-upscales every clip a session has seen

## Why

`assets/seedvr2_upscale.ipynb` moves this run's uploads (`/content/s3in__*.mp4`) into `/content/s3_in/` and then
upscales every MP4 in that folder. Nothing ever empties it, so on a session that already ran one batch the next
`h3.sh upscale --session X` re-does the earlier batch's clips too. On e033 (2026-10-30), with batches of five on
one session, batch two upscaled ten clips and batch three started on fifteen: the cost grows with the square of
the batch count, and the extra minutes also make the long `colab exec` more likely to hit a dropped tunnel.

## Definition of done

- [x] Each run upscales only the clips uploaded for it (the notebook empties `s3_in/` and `s3_out/` first).
- [x] A test fails against the old notebook and passes against the new one.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
```

## Notes

- Found and fixed by claude-opus-5.5-zt-e033 the same day. Live cleanup of the running session used a small
  `colab exec --file` that removed `/content/s3_in` and `/content/s3_out` (15 clips were sitting there).
- Not changed: a dropped `colab exec` tunnel still makes `upscale.py` report failure even when the kernel finished;
  `/content/s3_out.tar` may exist on the runtime, so try `colab download` of it before re-running a batch.
