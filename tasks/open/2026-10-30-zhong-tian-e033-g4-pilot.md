---
id: 2026-10-30-zhong-tian-e033-g4-pilot
title: Zhong-tian e033: three-shot route pilot on Colab G4, then the whole episode
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-30T14:29:39Z
created_at: 2026-10-30T10:01:24Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e033.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/ff-dh-e033.json
---

# Zhong-tian e033: three-shot route pilot on Colab G4, then the whole episode

## Why

The owner asked (2026-10-30) to make episode 33 next and to continue it in a cloud session. Two lines
of work met here: the Ref2VA route of `2026-10-29-32-40-colab-ref2va` (episodes 31-32, native
1920x1088, no first frames) and the three-stage route of `2026-10-30-h3-colab-three-stage` (draft,
refine, SeedVR2). Nobody has run them against each other, and the second has only run from first
frames. Decide with three shots before spending on 41.

Check first that the session holding `2026-10-29-32-40-colab-ref2va`
(`claude-fable-5.1-zt-e031`, branch `claude/peaceful-johnson-l7rzzy`) is not running e033, and record the
e033 progress in that ticket too. It noted: from e033 use Colab G4, session `zt33g`, and the list
`zhong-tian-qu-qi-e033-dh/colab/ref/all-jobs.json` in its own work directory.

## Definition of done

- [x] Route A and route B compared on s08, s09 and s21; the owner picks from the side-by-side. (2026-10-30: route A.)
- [x] The three missing set pictures exist. (They did: the Ref2VA session's `refs-dh`, see Notes.)
- [ ] All 41 shots (236 s) made on the chosen route, bad shots retaken.
- [ ] e033 continues through recording, assembly, import and dubs as `2026-10-29-32-40-colab-ref2va` lists.

## Steps

Before anything: `claude/h3-colab-three-stage` (PR #1930) must be in your tree for `h3.sh refine` and
`upscale`, and the camera check is on `claude/clip-qc-camera-move` (PR #1932). Get a token with Colab
access (`node tools/video/cli.mjs login --colab`, the owner allows it on the admin card), then
`bootstrap.sh`. The Colab balance was 768.7 CU on 2026-10-30.

- [x] Manifests (Linux only: `ref2manifest.mjs`'s main guard does not fire on Windows), with
      `H=docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo`,
      `C=docs/videos/series-plans/zhong-tian-qu-qi/production/colab`, `<refs>` the series' `refs-dh` folder:
      `VIDEO_WORKDIR=<a> node $PWD/$C/ref2manifest.mjs $H/clips-dh-e033.json $H/ff-dh-e033.json 33 <a>/ref --refs <refs> --only s08,s09,s21 --seed 330000 --width 960 --height 544`,
      and the same into `<b>` without the size (1920x1088).
- [x] Route A, stage 1: `H3_PROFILE=hero bootstrap.sh patch`, then `COLAB_GPU=G4 h3.sh batch` on the 960x544
      manifest (run it from the manifest's folder).
- [x] Route A, stage 2: cut each draft's frame 0 to 1312x736 as its `first_frame`; the refine prompt is the
      first-frame body `clips-dh-e033.json["a33-sNN"][0]`, not the Ref2VA prompt, because the refine notebook
      uses the FL2VA model and that prompt names several `<Picture N>`. `h3.sh refine` with `sigma_start` 0.5,
      10 steps, no guide, the same seeds.
- [x] Route A, stage 3: `h3.sh upscale` (SeedVR2 7B is the default).
- [x] Route B: `bootstrap.sh patch` (smooth), `COLAB_GPU=G4` with `scripts/h3_detached.py` on the 1920x1088
      list, then cut to 1920x1080. It records G4's minutes per clip, which the Ref2VA ticket asked for.
- [x] Compare: same frames side by side, faces during head turns, frame-0 against the portraits, seconds and
      CU per clip, and `node tools/video/media/camera-motion.mjs <clip> --camera "<shot camera>"`.
- [x] ~~Set pictures with `h3.sh images`~~ not needed, using the `prompt` of `citang`, `shentan` and `xinqu` in
      `production/cast.json` (s01-s06, s10-s17, s25-s39 need them). Write scenes positively: Qwen paints
      negatives as signs (`references/lessons.md` §1).

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
```

Receipts: each batch's progress.json and the balance before and after, written below.

## Notes

- Known risk for route A: `references/lessons.md` §1 measured faces softening into someone else at 768p during
  head turns and holding at 1088p, so a 960x544 draft may lose identity that the refine cannot restore. The
  three-stage pilot on 2026-10-30 started from first frames (s21, s34, s42 of e030), so it did not test this.
- Route A numbers on G4 from that pilot, FL2VA at 6 s: draft about 2 min, refine about 2.5 min, SeedVR2 about
  2.5 min, about 0.9 CU in all; G4 about 7.6-8.4 CU/hr. Ref2VA may differ. Route B on A100: 12-17 min, 1.5-2 CU.
- G4 takes no `--high-mem`; `h3.sh`, `images.py`, `refine.py` and `upscale.py` already drop it.
- Refine draws use `colab exec` for 2-3 minutes each. A 1088p clip is long enough for the 1012 disconnects, so
  route B must use `h3_detached.py` (`references/lessons.md` §3).
- This machine's `refs-dh` (Windows, 2026-10-30) has 48 files and no `angles/` folder and lacks those three set
  pictures. Use the Ref2VA session's folder if it is reachable; it should hold them and the angle crops.
- PRs when this was written: #1928 and #1930 have auto-merge on and were catching up with main. #1932 is based
  on #1930's branch; when #1930 merges, confirm its base became main, then merge it.

## Pilot receipts and lessons (2026-10-30, claude-opus-5.5-zt-e033)

At first not claimable: the scope collided with three stale claims, which the owner had closed or released
the same day (their sessions had no credit left). The scope then moved to e033's own lists (the s08/s09 prompt
fixes go there); the doc and anchor fixes are `2026-10-30-zhong-tian-fold-the-e033-pilot`.

**Where the inputs came from.** The Ref2VA session runs under another account's cloud environment, so the
pictures came over git: it pushed an orphan branch `transfer/zt-e033-refs` (commit 219ca2f0, 113 files,
252 MB: `refs-dh/` 60 pictures plus `angles/` 9, and `e033-ref/` = all-jobs.json, three parts, 41 prompts).
Restored to the absolute paths the list hard-codes, `/root/mokaair-work/videos/_series/zhong-tian-qu-qi/refs-dh`
and `/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/ref/`; all 60 referenced paths exist, check 0/0.
`set-citang-t1`, `set-shentan-t1`, `set-xinqu-t1` were already there. Regenerating with main's
`ref2manifest.mjs` gives byte-identical parts. A cloud session can only push its own branch, so the
transfer branch must be deleted by the owner or the sending session.

**Numbers** (balance 768.70 -> 755.36, 13.3 CU in all):

| run | GPU | wall time | CU (estimated where runs overlapped) |
| --- | --- | --- | --- |
| A stage 1, 3 clips 960x544 hero | G4 | 9.4 min (first clip 5:39 with cold start, then 1:45 / 1:51) | ~1.5 |
| A stage 2, 3 clips sigma 0.5 | G4 | 10.2 min | ~1.3 |
| A stage 3, SeedVR2 7B | G4 | 10.6 min (s08 313 s incl. model download, 130 / 152 s) | ~1.4 |
| B, 3 clips 1920x1088 smooth, `h3_detached.py` | **A100** (not G4, see below) | 44.4 min (19.8 / 10.5 / 13.4) | ~5.5 |
| retake stage 1, 4 drafts (s08, s09 x 2 seeds) | G4 | 12.0 min | 1.67 |
| retake stages 2+3 in one session `zt33r` | G4 | 15.3 min (7.3 + 8.0) | 2.16 |

Route A warm is about 7 min and 0.9 CU per 6 s shot; the whole episode estimate is 35-40 CU plus retakes.

**What the side-by-side showed** (owner picked A):

- s08: B bent Xu Yan's knees and kept both topknots; A stood them straight. s09: A held the close-up as
  written; B pushed from medium to an extreme close-up with wide-angle distortion and a younger face.
  s21: A matched the static composition; B added cropped adults in the foreground.
- A's stage 2 and 3 do not change motion or identity: whatever the 544p draft has (s09's face drift, the
  missing topknot) survives to 1080p. Judge and retake at stage 1, where a draft costs ~0.5 CU.
- Both routes grinned through the strain beat in s08 and s09.

**Lessons**

1. The grin comes from the character anchors, not the route. `cast.json` describes Xu Yan with "eyes that
   crinkle when he grins ... a slightly mischievous smile" and Wang Erniu with "a wide white-toothed grin",
   and Erniu's portrait itself is a full grin, so "facial expressions follow the action, not the reference
   pictures" loses. Removing the smile words from the anchors and writing the wanted face positively
   ("face strained, brows knitted, teeth gritted"; "brows draw down, eyes narrow, lips press into a thin
   line") fixed both shots on the first retake.
2. Name the prop's size: "the old roof beam" became a hoe handle; "a squared dark weathered timber as thick
   as a man's thigh" became a beam.
3. Xu Yan's anchor says "hair loosely tied back", but his portraits have a topknot; at 544p the text won.
   Write "gathered up into a topknot on the crown".
4. "Pushes in with small amplitude" still pushed a close-up to an extreme close-up in 2 of 3 s09 drafts;
   adding "the framing stays a close-up of his face from start to end" helped only partly.
5. Two seeds per retake shot is worth it at stage 1: s08 seed 330001 had Xu Yan's hands on his knees with
   the beam on Erniu alone; seed 330000 was right. s09 the reverse.
6. `h3_detached.py` with `COLAB_GPU=G4` ran on A100 and left the session up: `h3.sh start` does not pass
   `COLAB_GPU` (ticket `2026-10-30-h3-sh-start-ignores-colab-gpu`). Open the session yourself with
   `--gpu G4`, check `colab sessions` says G4, and stop it after.
7. Run stages 2 and 3 back to back in one session (`--session`): one cold start instead of two.
8. Stage-3 outputs are named `<id>_1080.mp4`, not `<id>.mp4`.

Picks for the episode: s08 seed 330000, s09 seed 330001, s21 seed 330000 (first run), finals in
`/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/pilot-a/{final,retake/final}/`.

- 2026-10-30 full run, stage 1 started: s08/s09 fixes written into `ff-dh-e033.json` (composition) and `clips-dh-e033.json` (motion, camera; column 2 re-hashed), so `ref2manifest.mjs` rebuilds the verified retake prompts byte for byte. With the new cast anchors 17 of 41 prompts differ from the old all-jobs.json (Xu Yan anchor: s01 s02 s06 s10 s12 s25 s30 s31 s32 s37; Erniu: s18 s20 s23; both: s34 s36; plus s08 s09). 38 shots on session `zt33` (G4), seed 330000; s08, s09, s21 reuse the pilot finals.
