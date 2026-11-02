---
id: 2026-11-01-curio-w-axis-batch-2-scripts
title: Curio W axis batch 2 scripts: Doraemon, Seiko, Dyson, Bubble Wrap (no paid generation)
status: in-progress
priority: P2
area: ops
owner: claude-opus-5-5-curio-w-axis
claimed_at: 2026-11-01T18:25:20Z
created_at: 2026-11-01T18:24:46Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-w04-doraemon-after-fujiko
  - docs/videos/curio-w05-seiko-quartz-astron
  - docs/videos/curio-w06-dyson-japan-first
  - docs/videos/curio-w07-bubble-wrap
---

# Curio W axis batch 2 scripts: Doraemon, Seiko, Dyson, Bubble Wrap (no paid generation)

## Why

站主 2026-11-01 決定：W 軸已做好的直接做，沒做好的先改成新規則稿，之後有空再成片。這張票是第二批四支：哆啦A夢、Seiko、Dyson、Bubble Wrap。只做到稿子，**沒有任何付費生成**。

## Definition of done

- [x] 四集各有查核過、盲評過、lint 0 錯誤的新規則稿，放在 `docs/videos/curio-w0[4-7]-*`。

## Steps

- [x] 撰稿與獨立查核（W04 58 項、W05、W06 47 項、W07 46 列，錯誤都已改）。
- [x] 盲評（W04 五輪、W05 六輪、W06 四輪、W07 六輪，共 36 位讀者，每位約 8 萬 token）。
- [x] lint 與 `script` 重新產生。

## How to verify

`node tools/video/cli.mjs lint --slug curio-w04-doraemon-after-fujiko`（w05、w06、w07 同樣）0 錯誤。

## Notes

- 成片前要站主核准生成費；各集下一步在各自的 `NOTES.md`。
- 盲評改過的句子沒有再查核一輪；成片前應對照 `claims.md`。
- 其餘 12 支（W09–W13、W14–W17、W19、W20、W22）還沒開工，各批開自己的票，見 `2026-10-30-three-brand-stories-move-to-curio.md`。
