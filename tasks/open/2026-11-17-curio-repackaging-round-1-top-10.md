---
id: 2026-11-17-curio-repackaging-round-1-top-10
title: Curio repackaging round 1: top 10 high-impression low-CTR videos
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-11-17T17:12:27Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/packaging-refresh-20261111/round-1
---

# Curio repackaging round 1: top 10 high-impression low-CTR videos

## Why

奇聞檔案局有 YouTube 推薦曝光，但沒人點：〈赤壁〉自然曝光 8,656、點閱率 0.68%；〈長篠〉6,151、1.01%；s04 4,530、0.55%（`channel-review-20261111-promotion` §4）。YouTube 說一半的頻道落在 2%–10%。規則已經寫在 `docs/videos/packaging-refresh-20261111/README.md`，這張票是 A 頻道 90 天計畫第 1 週的第一輪實作（`docs/videos/channel-os-20261117/A-storytelling/02-90-day-plan.md`）。

## Definition of done

- [ ] 依自然曝光多、點閱率低排序，前 10 支每支有新標題，以及 2–3 組照 layout e 重畫的縮圖。
- [ ] 站主在 Studio「測試與比較」上傳。
- [ ] 7 天後記錄每支的勝出組與觀看時間占比，寫回本票。

## Steps

- [ ] 讀 `packaging-refresh-20261111/README.md` 和 `curio-episode` §標題與縮圖。
- [ ] 縮圖用 `tools/video/templates/templates.mjs` 的 `thumbnailHtml`，產出放在 scope 目錄。
- [ ] 縮圖五項評分新舊並列（`scorecards.md`）。

## How to verify

scope 目錄有 10 支的新舊對照與評分；7 天後的結果寫在 Notes。

## Notes

從 `docs/videos/channel-os-20261117/` 開出（2026-11-17）。
