---
id: 2026-11-17-curio-repackaging-round-1-top-10
title: Curio repackaging round 1: top 10 high-impression low-CTR videos
status: done
priority: P1
area: docs
owner: claude-opus
claimed_at: 2026-11-18T00:53:40Z
created_at: 2026-11-17T17:12:27Z
completed_at: 2026-11-18T00:57:29Z
branch:
depends_on: []
scope:
  - docs/videos/packaging-refresh-20261111/round-1
  - docs/videos/channel-changes/README.md
---

# Curio repackaging round 1: top 10 high-impression low-CTR videos

## Why

奇聞檔案局有 YouTube 推薦曝光，但沒人點：〈赤壁〉自然曝光 8,656、點閱率 0.68%；〈長篠〉6,151、1.01%；s04 4,530、0.55%（`channel-review-20261111-promotion` §4）。YouTube 說一半的頻道落在 2%–10%。規則已經寫在 `docs/videos/packaging-refresh-20261111/README.md`，這張票是 A 頻道 90 天計畫第 1 週的第一輪實作（`docs/videos/channel-os-20261117/A-storytelling/02-90-day-plan.md`）。

## Definition of done

- [x] 依自然曝光多、點閱率低排序，前 10 支每支有新標題，以及 2–3 組照 layout e 重畫的縮圖。（縮圖只交規格，見 Notes）
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

2026-11-18：交付檔是 `docs/videos/packaging-refresh-20261111/round-1/curio-round-1.md`。
- 10 支（s02、s03、s04、s05、s06、s08、s09、s17、s18、s29）都有兩版標題、兩組縮圖規格和八語標題。s01、s11 上一輪已經做過，這輪不重做。
- 縮圖成品沒有畫：成片在雲端硬碟 `curio-rebrand-<slug>/out/final.mp4`，每支約 160 MB，雲端 session 下載不了。要在能讀雲端硬碟的環境照規格畫。
- 八語標題還沒經過逐語審。
- 沒有站台權杖，除了 s04 以外，換前的自然數字要站主從 Studio 抄。
