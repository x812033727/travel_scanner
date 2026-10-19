---
id: 2026-10-18-dubs-cc-titles-and-descriptions-in
title: 種田娶妻 dubs, CC, titles and descriptions in es, pt, id, vi, th for episodes 6–24
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-five-dubs
claimed_at: 2026-10-18T22:58:44Z
created_at: 2026-10-18T22:58:28Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.es.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.pt.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.id.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.vi.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-glossary-additions.th.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/dub-force.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e001.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e002.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e003.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e004.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e005.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e006.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e007.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e008.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e009.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e010.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e011.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e012.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e013.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e014.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e015.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e016.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e017.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e018.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e019.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e020.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e021.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e022.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e023.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e024.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/README.md
  - docs/videos/zhong-tian-qu-qi-e006
  - docs/videos/zhong-tian-qu-qi-e007
  - docs/videos/zhong-tian-qu-qi-e008
  - docs/videos/zhong-tian-qu-qi-e009
  - docs/videos/zhong-tian-qu-qi-e010
  - docs/videos/zhong-tian-qu-qi-e011
  - docs/videos/zhong-tian-qu-qi-e012
  - docs/videos/zhong-tian-qu-qi-e013
  - docs/videos/zhong-tian-qu-qi-e014
  - docs/videos/zhong-tian-qu-qi-e015
  - docs/videos/zhong-tian-qu-qi-e016
  - docs/videos/zhong-tian-qu-qi-e017
  - docs/videos/zhong-tian-qu-qi-e018
  - docs/videos/zhong-tian-qu-qi-e019
  - docs/videos/zhong-tian-qu-qi-e020
  - docs/videos/zhong-tian-qu-qi-e021
  - docs/videos/zhong-tian-qu-qi-e022
  - docs/videos/zhong-tian-qu-qi-e023
  - docs/videos/zhong-tian-qu-qi-e024
---

# 種田娶妻 dubs, CC, titles and descriptions in es, pt, id, vi, th for episodes 6–24

## Why

Owner 2026-10-19, after listening to the e001–e005 dubs: "聽過了可以，接著做第 6–24 集的西、葡、印尼、越、泰配音和標題說明".
Same method as 2026-10-18-dubs-and-cc-in-es-id (tasks/done), episodes 6–24.

## Definition of done

- [ ] Episodes 6–24 have `dub.<locale>.json` for es, pt, id, vi, th, recorded and fitted, every
      track as long as the zh audio, loudness within about 1 LU.
- [ ] Each episode's import folder has `dub.<locale>.m4a`, `<locale>.srt` and `description.<locale>.txt`.
- [ ] youtube-locales/<locale>.json has titles and descriptions for episodes 6–24.
- [ ] dub-glossary-additions.<locale>.json covers every term of the en additions file.

## Steps

- [ ] Glossary pass per locale (all terms of e006–e024 before any episode is translated).
- [ ] e006–e015 and e016–e024 per locale, ten agents, dub.sh's own per-episode lock.
- [ ] Merge titles and descriptions; verify every track.

## How to verify

Per episode and locale `cut/dub-<locale>.log` shows the summary, equal zh/<locale> audio
lengths and loudness; the import folders hold 8 dubs, 9 srt and 8 descriptions each.

## Notes

2026-10-19: every e006 assembly stopped with ENOENT: the sfx library
`<VIDEO_WORKDIR>/ou-de-jianghu-e001/browser-production/20261009/sound-library` had moved with the
whole ou-de-jianghu-e001 folder to `G:/我的雲端硬碟/AI/偶的江湖/videos/` (531 files, 286 MB).
Copied (not moved) to `<VIDEO_WORKDIR>/zhong-tian-qu-qi-sfx/sound-library` and repointed all 24
edit-dh-e*.json, so this series no longer depends on another series' workdir.
