---
id: 2026-10-30-three-brand-stories-move-to-curio
title: Three brand stories move to curio and are remade under the new rules
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-10-30T18:06:50Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-w01-dolby-licensing
  - docs/videos/curio-w02-michelin-guide-stars
  - docs/videos/curio-w03-garmin-smartphone-pivot
  - docs/videos/history-curiosity/brand-files-remake-20261031
---

# Three brand stories move to curio and are remade under the new rules

## Why

站主 2026-10-31 要把杜比、米其林、Garmin 三支品牌故事移到奇聞檔案局，並依現行規則重製。題目、規則差異、路線與預算在
`docs/videos/history-curiosity/brand-files-remake-20261031/README.md`。

## Definition of done

- [ ] `curio-w01`、`curio-w02`、`curio-w03` 三集成片經站主核准，類別是 `explainer`，標題結尾是「｜奇聞檔案局」。
- [ ] 舊的三支 `story-` 影片已處理：沒上架的放棄，已上架的照站主決定。

## Steps

- [ ] 站主核准預算；讀三支舊片在網站上的狀態。
- [ ] 每集 brief 與大綱，站主選。
- [ ] 稿子 → 獨立查核 → 盲評 → lint 0 錯誤。
- [ ] 旁白 → 站主聽 → 插圖 → 分鏡 → 配樂 → 成片 → 品管 → 上架包。
- [ ] 新片核准後處理舊片；Garmin 舊片不再解卡做語言。

## How to verify

`node tools/video/cli.mjs lint --slug curio-w01-dolby-licensing`（w02、w03 同樣）0 錯誤；`/admin/videos` 三集成片為已核准。

## Notes

- 後台 2026-10-31 讀到：杜比（uv-CQOKDMOI）、米其林（BSsyQ8HAVVg）、Garmin 舊片都已放棄；杜比、米其林沒有 remake，Garmin 有尚未開始的 `story-garmin-smartphone-pivot-worker-2026-remake-20261025`，W03 開工前要先處理，避免重複。
- 不走主機後台路線：主機單集的 slug 是 `one-off-…`，lint 與備份的系列判斷都靠 `curio-` slug；`MYSTERY` 也不認 W 軸。
- 查核收據綁舊企劃的雜湊，新稿要重查。Dolby 2026 財年 10-K 預計 2026 年 11 月公布。
