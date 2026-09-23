---
id: 2026-09-23-catchtable-seoul-1-naver-approval
title: CatchTable 第一批 14 家：Naver 精準頁、座標與核准（後台操作）
status: in-progress
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-23T03:56:08Z
created_at: 2026-09-23T03:56:06Z
completed_at:
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

- [ ] 14 家都填上站主給的 `https://map.naver.com/p/entry/place/<id>`，`map_match_status` 依後台規則變成 verified。
- [ ] 14 家都有耐久座標（官方頁自帶經緯度的用 `official_tourism` 來源；其餘走座標佇列或後台的 admin_verified，來源網址是 https）。
- [ ] 核准前把要公開的清單（店名、地址、Naver 網址、分類、訂位狀態）給站主看過；核准後公開 API 查得到，12 顆 verified 訂位按鈕出現。
- [ ] 報告 `catchtable-seoul-batch-1.md` 補「後台操作紀錄」：每家的 Naver id、座標來源、核准時間；沒過的寫原因。

## Steps

- [ ] 站主在面板登入後台；站主提供 14 條 Naver 精準頁網址。
- [ ] 逐家：後台填 `naver_map_url` → 座標 → 檢查分類／來源／地址 → 記錄。（2026-09-23：13 家座標已存，見報告「後台操作紀錄」；Naver 網址等站主）
- [ ] 清單給站主看 → 核准 → 公開 API 驗證（`destination_id=seoul`，四種 `X-Travel-Locale`）。
- [ ] 報告補紀錄，`done`。

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
