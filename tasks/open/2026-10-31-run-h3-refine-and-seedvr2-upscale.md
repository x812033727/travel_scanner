---
id: 2026-10-31-run-h3-refine-and-seedvr2-upscale
title: Run H3 refine and SeedVR2 upscale detached on the Colab runtime
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-31T02:38:38Z
created_at: 2026-10-31T02:38:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/route-a
---

# Run H3 refine and SeedVR2 upscale detached on the Colab runtime

## Why

`refine.py` and `upscale.py` run their notebook with one `colab exec` that holds a websocket for the whole job
(2-3 minutes a refine, 10-15 minutes a five-clip upscale). Colab's runtime proxy drops that tunnel (1012) or the CLI
stops receiving messages while the kernel keeps working, so the GPU finishes and the CLI waits until its timeout.
On e033/e034 (2026-10-30/31) that happened six or seven times in one night: a 20-minute and a 55-minute hang, and a
10-minute watchdog kill roughly every hour, each one paid GPU time. The owner asked for the detached route.

## Definition of done

- [x] `refine.py --detached` and `upscale.py --detached` start the notebook as a detached script on the runtime and
      poll it with short execs; a dropped tunnel costs one poll. Without the flag nothing changes.
- [x] Offline tests with a fake `colab`: settings reach the detached script, polls until done, a run that dies
      without the done marker fails with its log.
- [ ] Live: a refine batch and an upscale batch finish detached on G4 (e034).
- [ ] `route-a/st23.sh` uses it (done), `three-stage.md` says so.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
```

## Notes

- `scripts/colab_detached.py` is shared: notebook cells joined into `<prefix>_job.py` with `os.environ` set at the top
  and a done marker at the end, started with `Popen(start_new_session=True)`, log in `<prefix>.log`, pid in
  `<prefix>.pid`; probes are `colab exec` of a few lines with a 90 s timeout. Three unanswered probes in a row and a
  dead session end the run. Same idea as `h3_detached.py` for the H3 notebook.
- Both notebooks use no IPython magics, so plain `python3` runs them.
- 2026-10-31 02:42 first live job: e034 s18 refine, 2:50 from launch to download, 1312x736, 158 frames.
