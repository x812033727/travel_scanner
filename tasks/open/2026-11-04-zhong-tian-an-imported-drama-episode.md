---
id: 2026-11-04-zhong-tian-an-imported-drama-episode
title: Zhong-tian: an imported drama episode carries its build data (edit log, edit table, music cues, first frames) and the series assets into the Drive backup
status: open
priority: P2
area: tools
owner:
claimed_at:
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
  - apps/api/app/video_reviews/clips.py
  - apps/api/tests/test_video_review_clips.py
  - docs/videos/BACKUP.md
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
  the first frames (`first-frames/`, paid to draw), and the edit table as it was when cut.
- Series assets live only on the production machine: `<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/refs-dh/` and
  `refs/` (character and set references, incl. Tang Xiaotang's high-collar `tangxiaotang-portrait-t2.png` that
  every costume fix needs, 259 MB + 81 MB) and `sfx/` (the synthesized library, its rain and water are random).
- e043–e048's edit tables exist only on the unmerged branch `origin/claude/trusting-shannon-g7dl74`
  (from cf73f4307); e031–e039 have no `final.log` anywhere; their music cues were not found.

What was copied by hand on 2026-11-05 (md5-checked), so this task need not redo it:
`G:\我的雲端硬碟\AI\備份\drama\zhong-tian-qu-qi\_series\` (refs-dh, refs, sfx: 167 files) and
`...\drama\zhong-tian-qu-qi\_組片資料\` (e040–e042 `final.log` + `music/`, e043–e048 edit tables, README.md).
e001–e030 work folders were already archived whole under `AI\備份\種田娶妻打天下\` and
`AI\備份\drama\zhong-tian-qu-qi\_原始備份\`.

## Definition of done

- [ ] `import --publish` of a drama episode also sends its build data: `cut/final.log`, the edit table it was cut
      with, `music/cue-*.mp3`, and the first frames as `kf_*` keyframes; the host accepts them and the full tier
      copies them to `AI/備份/<series>/<episode>/` (e.g. `build/final.log`, `build/edit.json`, `build/music/`,
      `keyframes/`). An episode without them still imports, and the report says what was missing.
- [ ] Series-level assets (`_series/<series>/refs*`, `sfx`) have a documented, repeatable way into
      `AI/備份/<category>/<series>/_series/` (a `prep-import` step or a separate command), run on every import.
- [ ] e043–e048 edit tables are on main.
- [ ] `docs/videos/BACKUP.md` lists, for an imported drama episode, every file a re-cut needs and where it lands.

## Steps

- [ ] Read how `review-push` already sends `kf_*`, `full_timeline` and `recordings_*` (BACKUP.md §匯入的影片 4–5,
      `tools/video/review/full-tier.mjs`) and reuse those roles where they fit; add new roles in
      `apps/api/app/video_reviews/clips.py` only for what does not fit (edit log, edit table, music).
- [ ] Extend `tools/video/import` / `prep-import.mjs` to collect the build data from the work directory.
- [ ] Bring the six edit tables over from `origin/claude/trusting-shannon-g7dl74` (check that branch's other
      commits first; it may hold more unmerged e043–e048 work).
- [ ] Tests: review-package fetch of the new roles, import packing with and without the build data.

## How to verify

`npm run test:tools`; then `node tools/video/cli.mjs import --from <e042 import folder> --publish` against the site
and, after the next backup round, `rclone lsf` (or the G: mount) shows `build/final.log`, `build/music/` and
`keyframes/` under `AI/備份/drama/zhong-tian-qu-qi-e042/`.

## Notes

- The edit log's shot times drift late against the real cut (about 0.3 s by the end of e023): the per-shot
  lengths are rounded to 24 fps. Anything that places captions or dubs should use real cut points.
- e010's `final.log` repeats a block of s38–s42 after its `total` line.
- Episodes 31–48 come in 23.976 / 24 / 48 / 120 fps; a compilation must normalize to 24 fps.
