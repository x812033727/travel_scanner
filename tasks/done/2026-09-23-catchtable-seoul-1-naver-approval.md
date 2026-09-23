---
id: 2026-09-23-catchtable-seoul-1-naver-approval
title: CatchTable 第一批 14 家：Naver 精準頁、座標與核准（後台操作）
status: done
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-23T03:56:08Z
created_at: 2026-09-23T03:56:06Z
completed_at: 2026-09-23T05:51:48Z
branch: claude/catchtable-seoul-1-naver-approval
depends_on: []
scope:
  - docs/catalog-content-reviews/catchtable-seoul-batch-1.md
  - docs/catchtable-ranking-discovery.md
---

# CatchTable 第一批 14 家：Naver 精準頁、座標與核准（後台操作）

## Why

票 `2026-09-22-catchtable-ranking-discovery-batch-1` 把 14 家首爾店家建成 pending（部署 `9063f351` 後套用），但韓國店家公開的守門是
Naver 精準地點頁＋耐久座標＋核准（`publishable_merchant_filters()`），批次不寫這三樣。站主 2026-09-23 決定：Naver 網址由站主查、貼進對話；
後台的逐筆填入、座標、核准由 session 在站主登入的內建瀏覽器面板裡代操作。`map.naver.com` 在內建瀏覽器被安全政策拒絕（2026-09-23 再確認），
不繞道 Chrome 或 curl。

## Definition of done

- [x] 13 家填上 Naver 精準頁（12 家 verified；산청 2 號店因無座標維持 unverified）；고호재未填——站主給的 Naver 頁與 `seoul-korea-house` 相同，後台要求唯一。
- [x] 13 家有耐久座標（6 家 `official_tourism` 官方頁 JSON-LD、7 家 `admin_verified` OSM 節點）；산청 2 號店沒有可靠座標，未填。
- [x] 站主 2026-09-23 對話中三次全權授權後逐家核准；公開 API 首爾 29 → 41 家，CatchTable 按鈕 3 → 13 顆（10 顆是這批的；另 2 家候位制無按鈕）。
- [x] 報告 `catchtable-seoul-batch-1.md` 補「後台操作紀錄」：每家的 Naver id、座標來源、核准時間；沒過的寫原因。

## Steps

- [x] 站主在面板登入後台；站主提供 13 條 Naver 短網址（2026-09-23）。
- [x] 逐家：後台填 `naver_map_url` → 座標 → 檢查分類／來源／地址 → 記錄。
- [x] 核准 → 公開 API 驗證（`destination_id=seoul`，四種 `X-Travel-Locale` 的訂位網址都對）。
- [x] 報告補紀錄，`done`。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" | python -m json.tool | grep -c catchtable_global
```

## Notes

- 官方頁自帶經緯度的（2026-09-23 掃過 14 個來源頁）：Visit Gangnam 的 `zest`、`wooga`、`samwon-garden`、`jungsik-seoul` 四頁與 VisitKorea 英文站的 꿉당 성수점頁；
  kimfood.co.kr 有四個 `naver.me` 短網址（不知對應哪家分店，沒有解析）。其餘 9 家的座標要另外來。
- 2026-09-23 後台寫入的機制：編輯視窗是 React 表單，文字欄用原生 value setter＋`input`／`change` 事件、勾選框用真實 click；
  「關閉舊視窗」與「開新視窗」不能在同一個事件裡做（React 會合併成關閉），中間要等一秒。連續儲存會被 auto 模式分類器擋（Modify Shared Resources），
  站主在對話裡同意後同一個動作才放行。
- **2026-09-23 卡住的原因（blocked）**：13 家的 Naver 精準頁網址沒有正當管道可取得。內建瀏覽器對 `map.naver.com` 與 `search.naver.com`
  都回 safety restrictions；官網／母公司網站掃過只有킴푸드放 Naver 短網址；WebSearch 拿不到 id。站主把網址貼進對話後接著做：填網址 → 已驗證 →
  核准啟用（核准與連續寫入都會被 auto 模式分類器擋，站主在對話同意後同一動作放行）。
- 2026-09-23 已完成：13 家座標；안목 성수점 Naver `2073097145`（經營者官網短網址轉址目標）→ 已驗證 → 04:31 UTC 核准啟用，公開 API 首爾 29 → 30 家。
- **2026-09-23 結果**：12/14 公開（首爾公開店家 29 → 41，CatchTable 按鈕 3 → 13）。Naver 頁在 session 的兩個瀏覽器都被 Anthropic 端封鎖，
  最後的分工是站主在自己的 Naver 地圖依地址挑選、貼 `naver.me` 短網址，session 只讀轉址標頭取 id（不開 Naver 頁）、填後台、一次儲存
  「已驗證＋核准＋啟用」。剩兩家：산청 2 號店缺座標、고호재的 Naver 頁與韓國之家相同（後台要求唯一）——留給站主，不另開票。
