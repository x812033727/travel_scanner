---
id: 2026-09-20-korea-autumn-leaves-2026-intel
title: 韓國賞楓 2026 時效情報：10 月上旬山林廳預測地圖發布後再寫（第八批規劃時官方來源還沒開張）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T00:24:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/korea-autumn-leaves-2026.json
---

# 韓國賞楓 2026 時效情報：10 月上旬山林廳預測地圖發布後再寫

## Why

站上有 `japan-autumn-leaves-2026`、`korea-winter-events-2026`、`korea-ski-resorts-2026-2027`，就是沒有韓國的秋天。
第八批規劃（2026-09-20）時兩個官方來源都還沒開張：山林廳「산림단풍 예측지도」尚未發布（forest.go.kr 首頁是 1.6 KB 的殼，
보도자료 列表讀得到但還沒有今年那一則），氣象廳的單楓現況頁也還沒有 2026 年資料，所以這題被 drop，不是題目不好。

## Definition of done

- [ ] 10 月上旬重讀山林廳보도자료（`https://www.forest.go.kr/kfsweb/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_1036&mn=NKFS_04_02_01`）與氣象廳單楓頁；
      讀得到各山的預測高峰日才寫，讀不到就再延後並記下試過的網址。
- [ ] intel、zh-TW、800–1,500 字、`valid_until` 約 2026-11-30；互連 `seoul-4-day-itinerary`、`nami-island-petite-france-day-trip`、`korea-ktx-srt-ticket-guide`。
- [ ] 過期處理：`valid_until` 隔天拿掉其他文章連過來的連結（照第七批 README 的時效規則）。

## Steps

- [ ] 重讀官方來源 → 規格 → 撰稿 → 獨立查核 → 出圖與照片 → PR → 匯入

## How to verify

`pack_cli lint --kind intel --slug korea-autumn-leaves-2026`；正式站頁面 200、可索引。

## Notes

- 對外請求 UA 一律 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不得帶任何人的 email 或個人資料。
