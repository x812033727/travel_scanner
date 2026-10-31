---
id: 2026-10-31-zhong-tian-e043-e060-brief-script
title: Zhong-tian e043-e060: brief, script, storyboard, video.json and clip lists to the end of season 1 (no generation)
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-e033
claimed_at: 2026-10-31T09:26:06Z
created_at: 2026-10-31T09:25:51Z
completed_at: 2026-10-31T10:50:04Z
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e043
  - docs/videos/zhong-tian-qu-qi-e044
  - docs/videos/zhong-tian-qu-qi-e045
  - docs/videos/zhong-tian-qu-qi-e046
  - docs/videos/zhong-tian-qu-qi-e047
  - docs/videos/zhong-tian-qu-qi-e048
  - docs/videos/zhong-tian-qu-qi-e049
  - docs/videos/zhong-tian-qu-qi-e050
  - docs/videos/zhong-tian-qu-qi-e051
  - docs/videos/zhong-tian-qu-qi-e052
  - docs/videos/zhong-tian-qu-qi-e053
  - docs/videos/zhong-tian-qu-qi-e054
  - docs/videos/zhong-tian-qu-qi-e055
  - docs/videos/zhong-tian-qu-qi-e056
  - docs/videos/zhong-tian-qu-qi-e057
  - docs/videos/zhong-tian-qu-qi-e058
  - docs/videos/zhong-tian-qu-qi-e059
  - docs/videos/zhong-tian-qu-qi-e060
  - docs/videos/series-plans/zhong-tian-qu-qi/production/cast.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/s01-e043-e060-registry.md
---

# Zhong-tian e043-e060: brief, script, storyboard, video.json and clip lists to the end of season 1 (no generation)

## Why

The owner (2026-10-31): 「劇情直接做到第一季結束吧，並且應該要有留第二季的伏筆」. Episodes 43-60 follow e041/e042
(ticket 2026-10-31-zhong-tian-e041-e042-brief-script, PR draft) from season-01.json, authoring.md and
production/storyboard-rules.md; no clip is generated until the owner reviews.

## Definition of done

- [x] New characters and sets of e043-e060 registered once (cast.json, gen-dh.mjs, ref2manifest.mjs, dub-glossary)
      and mapped in production/s01-e043-e060-registry.md.
- [x] docs/videos/zhong-tian-qu-qi-e043 ... e060: brief, script, storyboard, video.json, overlays; lint,
      drama_craft_check and shot_reading clean.
- [x] hailuo/ff-dh-eNNN.json and clips-dh-eNNN.json for each.
- [x] Season-2 seeds: e056-e060 plant, without revealing, what season-02.json opens on (s02-t01 假禁軍是誰派來的,
      s02-t03, m05 still open), and e060 ends on the reversal the outline fixes.
- [x] production/README.md section 4 updated.
- [x] The owner reviews (2026-10-31: 「不用審你檢查完就好」).

## How to verify

Same commands as the e041-e042 ticket, for each episode.

## Notes

- 2026-10-31: written by four parallel writers (43-46, 47-50, 51-55, 56-60) from production/writer-brief-e043-e060.md after
  one agent registered 8 characters and 13 sets (production/s01-e043-e060-registry.md). Builders are in
  production/writer-tools/. Every episode: lint 0 errors, drama_craft_check 30/30, shot_reading 0 traps.
- Continuity pass: affection values already matched season-01.json (e059 ends 阿令 68 / 秦霜 66 / 唐小棠 61); fixed
  e040 天下歸心 5%→2%, e056 day 5, e058 「後天就到」 (season-01.json changed to match), e050 jade hand-off, e041 jade
  walnut-sized, Xu Yan's left-forearm bandage e058-e060, e053 Erniu's line, Du Tie's crutch under the right arm
  (cast.json); 43 glossary terms added.
- Owner decisions 2026-10-31: season 2 follows e060 (常公公 kneels, 韓七 at his side runs the fake guards, Xu Yan holds
  the 配婚令; season-02.json e061 and guest s02-chang-gonggong); Qin Shuang stays brown in every season (黑紅→深棕 in
  setting and all season outlines); season-02 adds 唐小棠 +4 (e062), +7 (e074) and 秦霜 +3 (e068) to reach e090's totals.
- Pictures still to paint before e043+ can be made: 25 (10 portraits, 15 sets), listed in the registry.
- e057 panel wording 「阿令與糧倉，都要保住」 vs voice 「人與糧」 and e053's generous countdown were left as they are.
