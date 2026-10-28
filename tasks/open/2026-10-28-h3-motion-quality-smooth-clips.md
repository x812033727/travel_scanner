---
id: 2026-10-28-h3-motion-quality-smooth-clips
title: H3 motion quality: smooth clips, fewer failed takes (skill manual, Colab sampling profiles, zhong-tian prompt and cut tools)
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-28T04:43:58Z
completed_at:
branch: claude/pensive-cray-rko0pa
depends_on: []
scope:
  - .agents/skills/minimax-h3-colab
  - .claude/skills/minimax-h3-colab
  - tools/minimax-h3-colab.test.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/gen-dh.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/assemble-v4.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/README.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/storyboard-rules.md
  - tasks/open/2026-10-05-shot-plan-h3-body-official-i2va.md
---

# H3 motion quality: smooth clips, fewer failed takes (skill manual, Colab sampling profiles, zhong-tian prompt and cut tools)

## Why

The owner (2026-10-28) still sees 《種田娶妻打天下》 as "貼圖感、不流暢" after the 2026-10-16 fixes
(speaking shots, fewer stills) and asked for the MiniMax H3 animation skill to be strengthened
from other people's repos and write-ups, so clips come out smoother with fewer failed takes.
Measured causes, with sources read on 2026-10-28:

1. Every clip was bought at 4 s = 107 frames, under the 124–362 frames H3 was trained on (ComfyUI
   H3 guide; the upstream Colab notebook prints the same warning). Lines longer than the clip were
   covered by slowing it to 1.35x with duplicated frames and then freezing the last frame
   (`assemble-v4.mjs`): the stutter and the holds are the "sticker" feel.
2. The clip body in `gen-dh.mjs` had no official style word and no `<Picture 1>` anchor sentence,
   rewrote every `locked` camera into a slow push, and ended with a fixed "the camera keeps moving
   slowly the whole time" that contradicted the shot's own `fast pan right` or `tracking shot`.
   Community tests (fuser.studio, kapwing, digitalzoomstudio) blame stiff or floaty motion on
   exactly these: state instead of trajectory, no anticipation or weight, vague or stacked moves,
   `then` chains that H3 turns into cuts.
3. The Colab route (the one 修仙獎勵 will use) sampled Ref2VA with the 4-step `ref2v_turbo_4step_v0.1`
   LoRA, which the ComfyUI guide says can barely apply references; an 8-step 768p Ref2V v1.0 LoRA
   exists (lightx2v), and the official Comfy-Org 8-step FL2V v1.0 LoRA replaces the community drbaph
   file. A 16:9 keyframe was also stretched onto the 1344x768 (7:4) canvas.

## Definition of done

- [x] `.agents/skills/minimax-h3-colab/references/motion-quality.md`: the three causes, the body
      writing rules (style word + anchor, trajectory with anticipation and weight, one camera move
      in the official sentence, `holds a static shot`, no `then` chains, length), seconds and canvas
      table, the three Colab sampling profiles, an error catalogue, what to check on delivery, and
      every source with its read date.
- [x] `scripts/patch_notebook.py` rewrites the pinned upstream notebook's eight constant lines into
      profile `smooth` (default: 8-step Ref2V v1.0 + official 8-step FL2V v1.0, euler/simple), `hero`
      (20 steps, LoRA strength 0, res_multistep/simple) or `draft` (upstream); exact-match only,
      idempotent, exit 2 on upstream drift; `bootstrap.sh` restores and re-applies it after the clone
      (`H3_NOTEBOOK_PATCH=off` skips). Applied cleanly to the real notebook at `0a0d3b9c`.
- [x] `scripts/check_manifest.py` (and `h3.sh check`; `h3.sh batch` runs it first, `--no-check`
      skips) refuses before upload what would otherwise cost compute units: ids, modes, image files,
      `<Picture N>` beyond the images, 4–15 s, multiples of 32 and the area cap, `prompt_sha256`
      against the prompt file, duplicate outputs; warns on 4 s (107 frames), stretched first frames
      (ffprobe), `[Shot 2]`, `then the camera`, a first_frame prompt without `<Picture 1>`.
- [x] `scripts/fit_first_frame.sh` crops a keyframe to the canvas ratio; `h3.sh single --mode
      first_frame` defaults to 1312x736 (within 0.005 of 16:9, 0.97 MP, a multiple of 32; 1280x720
      is not a multiple of 32 and 1344x768 stretches).
- [x] SKILL.md (rules 5–7, flow, where-to-read), `cloud-pairing.md` §5–6, `pipeline-handoff.md` §2
      updated; `.claude/skills/minimax-h3-colab/SKILL.md` byte-identical.
- [x] `tools/minimax-h3-colab.test.mjs`: patcher (smooth, hero, draft, dry-run, idempotency, drift,
      env overrides), manifest check (good, warnings, every error), wrapper (check, batch refusal,
      `--no-check`, first_frame size). 11 tests pass.
- [x] `gen-dh.mjs`: style word + `<Picture 1>` anchor, speaking clause, motion with trailing camera
      clauses dropped (and listed), one camera sentence from `data.camera` with `locked` kept, no
      fixed moving-camera tail; seconds 5 by default, 6 for ~3 s of on-screen speech or a two-beat
      motion, `data.buy_seconds` overrides; points printed per seconds bought. e027 and e013 generate.
- [x] `assemble-v4.mjs`: slow-down capped at 1.25 (`slow_max`) and done with `minterpolate` optical
      flow instead of duplicated frames (`interpolate: false` restores the old path); chain proven on
      a synthetic clip (24 fps out, 1 min 42 s of CPU for a 5.8 s 1080p shot in the cloud container).
- [x] `storyboard-rules.md` and `hailuo/README.md` carry the new rules and the reasons.
- [ ] First real Colab batch under profile `smooth` (owner's pairing and compute units; ticket
      `2026-10-27-minimax-h3-on-colab-from-a`): record CU and minutes per profile in
      `cloud-pairing.md` §4 and whether the 8-step Ref2VA holds faces.

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
npm run test:tools && npm run check:tasks
node docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/gen-dh.mjs docs/videos/zhong-tian-qu-qi-e027/video.json \
  docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/empty-lock.json 27 /tmp/ff.json /tmp/clips.json
#  a27-s06 (locked) ends with "The camera holds a static shot."; a27-s04 (slow pan left) has no "keeps moving slowly"; speaking shots are 6 s
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh install   # clones upstream and prints "patched … profile=smooth"
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py docs/videos/series-plans/xiuxian-jiangli/production/colab/h3/manifest-pilot.json
#  three "4 s is 107 frames" warnings and three missing first-frame errors until the frames are placed and the manifest says 5 s
```

## Notes

- 2026-10-28: PR #1904 carries everything above except the last item (a real Colab batch needs the
  owner's pairing and compute units), so the ticket goes back to `open` on merge, like
  `2026-10-27-minimax-h3-on-colab-from-a`: whoever runs the first batch under profile `smooth` ticks it.

- Scope overlaps `2026-10-19-30-1-24` (`docs/videos/series-plans/zhong-tian-qu-qi/production`), whose
  claim was nine days stale; claimed with `--force` per the board's 24-hour rule and only the four
  listed files under `production/` were touched.
- No paid pilot: the owner decided (2026-10-28) that episodes from 31 on use the new body directly
  and old episodes are not reshot. The first cut with the new tools is where the effect shows.
- Points per episode rise: e027 goes from 38 × 48 = 1,824 to 14 × 60 + 24 × 72 = 2,568 clip points;
  the alternative was slow-motion and freezes.
- Not done, on purpose: switching upstream to `wonghanz/minimax-h3-colab-skill` v0.2.0-hardened (17
  reliability fixes, not merged, no LICENSE either); adding a shift node (neither the official
  ComfyUI templates nor the notebook have one); wiring Motion-Context or the anti-burn LoRA into the
  notebook (continuation workflows, ComfyUI >= 0.34); changing `shot_plan.mjs` (ticket
  `2026-10-05-shot-plan-h3-body-official-i2va` now carries the findings); the server route's
  `tools/video/assemble/drama.mjs` fit logic.
- `xiuxian-jiangli` e001's `h3/manifest*.json` still say 4 s and 1344x768: the owner of
  `2026-10-27-xiuxian-e001-colab-pilot-to-cut` should move them to 5 s and 1312x736 (and run
  `fit_first_frame.sh` on the keyframes) before the pilot; `h3.sh batch` will warn, not refuse.
- Fact that surprised: 1280x720 is not usable on this notebook (720 is not a multiple of 32); the
  manifest checker caught it while being tested.
