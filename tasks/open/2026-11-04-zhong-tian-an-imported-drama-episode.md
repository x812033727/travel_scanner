---
id: 2026-11-04-zhong-tian-an-imported-drama-episode
title: Zhong-tian: an imported drama episode carries its build data (edit log, edit table, music cues, first frames) and the series assets into the Drive backup
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-season-review
claimed_at: 2026-11-05T03:36:45Z
created_at: 2026-11-04T16:13:48Z
completed_at:
branch:
depends_on:
  - 2026-10-31-zhong-tian-clip-backup
scope:
  - tools/video/import
  - tools/video/cli.mjs
  - tools/video/automation/review-package.mjs
  - tools/video/automation/review-package.test.mjs
  - tools/video/automation/backup.mjs
  - tools/video/automation/backup.test.mjs
  - apps/api/app/video_reviews/clips.py
  - apps/api/tests/test_video_review_clips.py
  - docs/videos/BACKUP.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/prep-import.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e043.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e044.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e045.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e046.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e047.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e048.json
---

# Zhong-tian: an imported drama episode carries its build data (edit log, edit table, music cues, first frames) and the series assets into the Drive backup

## Why

The owner (2026-11-04) is merging 種田娶妻打天下 season 1 into one video and asked for a full review first
(`docs/videos/series-plans/zhong-tian-qu-qi/production/season1-review.md`, 96 must-fix items in e1–30 alone).
Fixing those means re-cutting episodes, and the owner's rule is that a backup must hold everything a later
session needs ("以後就不會漏"). It does not:

- The site's full-tier backup (`tools/video/automation/backup.mjs`, `docs/videos/BACKUP.md`) only copies what
  the host holds. An imported drama episode reaches the host through `node tools/video/cli.mjs import --publish`,
  which sends the cut, captions, dubs, thumbnail, per-shot `clips/` and the line `recordings/`, nothing else.
- Left behind in the work directory (`<VIDEO_WORKDIR>/zhong-tian-qu-qi-eNNN-dh/`), and gone when a cloud
  container ends: `cut/final.log` (which clip and take each shot used, where it starts, any hold), the music cues
  `music/cue-*.mp3` (Lyria; a regenerated cue is a different piece, e040's cues already differ from e001's),
  the first frames (`first-frames/`, paid to draw), the edit table as it was when cut, the per-line voice files
  `audio/` and `audio-<lang>/` (the site keeps only the mixed `recordings/`, so a re-cut cannot re-time one line),
  and the dub timing logs `cut/dub-<lang>.log` (each line's length and speed-up).
- Series assets live only on the production machine: `<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/refs-dh/` and
  `refs/` (character and set references, incl. Tang Xiaotang's high-collar `tangxiaotang-portrait-t2.png` that
  every costume fix needs, 259 MB + 81 MB) and `sfx/` (the synthesized library, its rain and water are random).
- e043–e048's edit tables exist only on the unmerged branch `origin/claude/trusting-shannon-g7dl74`
  (from cf73f4307). e033–e039's music is the set in `production/assets/music/` (hash-identical); e031–e032 used an
  older set, kept on branch `transfer/zt-e031-e032-media` and in PR #2017.
- Trap: the root `.gitignore` has `*.log`. PR #2017 says it adds e031–e039 `cut/final.log` and `dub-*.log`, but the
  branch holds none of them. Anything that keeps build logs in git must `git add -f` them and count them afterwards.
  On 2026-11-05 e033–e039 and e043–e048 `final.log` existed only in cloud work folders (asked those sessions to push).

What was copied by hand on 2026-11-05 (md5-checked), so this task need not redo it:
`G:\我的雲端硬碟\AI\備份\drama\zhong-tian-qu-qi\_series\` (refs-dh, refs, sfx: 167 files) and
`...\drama\zhong-tian-qu-qi\_組片資料\` (e031–e032 whole build data from the transfer branch: edit table, `cut/*.log`,
`music/`, `first-frames/`, `audio*/`; e040–e042 `final.log` + `music/`; e043–e048 edit tables; README.md). The owner also
keeps an identical copy of `_series` at `AI\備份\種田娶妻打天下\_series\zhong-tian-qu-qi\`.
e001–e030 work folders were already archived whole under `AI\備份\種田娶妻打天下\` and
`AI\備份\drama\zhong-tian-qu-qi\_原始備份\`.

## Definition of done

- [x] `import --publish` of a drama episode also sends its build data: `cut/final.log`, the edit table it was cut
      with, `music/cue-*.mp3`, `cut/dub-*.log`, the per-line `audio*/` files, and the first frames as `kf_*` keyframes; the host accepts them and the full tier
      copies them to `AI/備份/<series>/<episode>/` (e.g. `build/final.log`, `build/edit.json`, `build/music/`,
      `keyframes/`). An episode without them still imports, and the report says what was missing.
- [x] Series-level assets (`_series/<series>/refs*`, `sfx`) have a documented, repeatable way into
      `AI/備份/<category>/<series>/_series/` (a `prep-import` step or a separate command), run on every import.
- [x] e043–e048 edit tables are on main (with this PR).
- [x] `docs/videos/BACKUP.md` lists, for an imported drama episode, every file a re-cut needs and where it lands.

## Steps

- [x] Read how `review-push` already sends `kf_*`, `full_timeline` and `recordings_*` (BACKUP.md §匯入的影片 4–5,
      `tools/video/review/full-tier.mjs`) and reuse those roles where they fit; add new roles in
      `apps/api/app/video_reviews/clips.py` only for what does not fit (edit log, edit table, music).
- [x] Extend `tools/video/import` to collect the build data from the work directory (`build.mjs`; prep-import needed no change: the data is read from the clips' workdir).
- [x] Bring the six edit tables over from `origin/claude/trusting-shannon-g7dl74` (check that branch's other
      commits first; it may hold more unmerged e043–e048 work).
- [x] Tests: review-package placement of the new roles, import packing with and without the build data, the API's limits, series-backup.
- [ ] Deploy (API + video-worker image) so the site takes `build_` files and the worker places them; until then a package with them is refused by the API (422).

## How to verify

`npm run test:tools`; then `node tools/video/cli.mjs import --from <e042 import folder> --publish` against the site
and, after the next backup round, `rclone lsf` (or the G: mount) shows `build/final.log`, `build/music/` and
`keyframes/` under `AI/備份/drama/zhong-tian-qu-qi-e042/`.

## Notes

- The edit log's shot times drift late against the real cut (about 0.3 s by the end of e023): the per-shot
  lengths are rounded to 24 fps. Anything that places captions or dubs should use real cut points.
- e010's `final.log` repeats a block of s38–s42 after its `total` line.
- Episodes 31–48 come in 23.976 / 24 / 48 / 120 fps; a compilation must normalize to 24 fps.
- **Done 2026-11-05 (claude-opus-5.5-season-review).** Roles `build_log-<name>` (text/plain), `build_music-<name>`
  (audio/mpeg|wav), `build_edit-<name>` (application/json), at most 40, publish gate only; the worker places them under
  `recut/` (not `build/`: that name is the pipeline's remakeable output, which no tier backs up) and the full tier copies
  `recut/`. First frames go as `kf_<name>` into `keyframes/`. `metadata.json` carries `build_sha256`. Missing build
  data is logged and returned as `missing`, never refused. Series assets: `tools/video/import/series-backup.mjs` (run on
  the production machine, copies what differs, writes SHA256SUMS); a real run against the hand copy found 167/167 already there.
- The cloud sessions making e049+ import from `origin/claude/trusting-shannon-g7dl74`, whose tools predate this; they get it
  only after rebasing on main, and must add `--edit .../hailuo/edit-dh-eNNN.json` (the edit table lives in the repo there).
- Backup tests on Windows: 4 failures in `tools/video/automation/backup.test.mjs` (symlink EPERM and friends) fail the
  same way on a pristine origin/main copy; CI on Linux is the check.
