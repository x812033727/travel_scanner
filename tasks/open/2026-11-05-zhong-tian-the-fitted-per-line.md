---
id: 2026-11-05-zhong-tian-the-fitted-per-line
title: zhong-tian: the fitted per-line dubs travel with the recordings
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-11-05T01:21:48Z
created_at: 2026-11-05T01:21:16Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/import/recordings.mjs
  - tools/video/import/recordings.test.mjs
  - tools/video/import/import.mjs
  - tools/video/automation/review-package.test.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/README.md
---

# zhong-tian: the fitted per-line dubs travel with the recordings

## Why

`import --publish` packs each episode's raw per-line takes (`audio/`, `audio-<locale>/`) into the
upload package's `recordings/` for the Drive backup, but not the takes as they were fitted into
the cut: `segments-v4/lines/` (zh-TW, each line padded/trimmed for its slot) and
`segments-v4/dub-<locale>/` (each line's `.raw.wav` and tempo-fitted `.wav`, the whole
`dialogue.wav` track and `fit.json`, which says where every line starts, its slot and tempo).
They are 280-450 MB an episode and only lived in the cloud session's workdir, so a later fix of
one dubbed line in e033-e039 would have had to refit the whole track by hand (owner, 2026-11-05).

## Definition of done

- [ ] `packRecordings` also packs every `segments*/lines` and `segments*/dub-<locale>` folder,
      one playable wav each (`fit-lines.wav`, `fit-<locale>.wav`, role `recording_fit-…`, a
      role the site and `placeOf` already take), and their `fit.json`, in the same manifest;
      `unpack` gives every file back byte for byte.
- [ ] Each of e033-e039's `fit.json` is in the repo under `colab/runs/e0NN/dub/`.
- [ ] e033-e039's upload packages are sent again with them, the owner approves, and the Drive
      backup holds `recordings/fit-*.wav`.

## How to verify

`node --test tools/video/import/recordings.test.mjs tools/video/automation/review-package.test.mjs`;
`node tools/video/import/recordings.mjs pack <workdir> <out>` then `unpack <out> <copy>` and
`diff -r` the folders.

## Notes

- e043-e048 were made by another session; that session packs and sends its own.
