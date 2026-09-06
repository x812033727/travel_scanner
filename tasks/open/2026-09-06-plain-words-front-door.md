---
id: 2026-09-06-plain-words-front-door
title: 首頁與規劃表單的字換成長輩看得懂的說法
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T22:18:32Z
created_at: 2026-09-06T22:18:32Z
completed_at:
branch: claude/ux-plain-words
depends_on: []
scope:
  - apps/web/messages/zh-TW/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/newTrip.json
  - apps/web/messages/zh-CN/newTrip.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/en/legacy.json
  - apps/web/messages/ja/legacy.json
  - apps/web/messages/ko/legacy.json
  - apps/web/messages/zh-CN/legacy.json
  - apps/web/messages/zh-TW/legacy.json
  - apps/web/components/new-trip-form.test.tsx
---

# 首頁與規劃表單的字換成長輩看得懂的說法

## Why

2026-09-07 的長輩情境稽核裡，「讀不懂字」是唯一一條在八個 slice 中出現過五次的問題。
從第一行就開始：

| 原本 | 問題 |
| --- | --- |
| 完整旅程決策工作台 | 「工作台」不是一般人講旅行會用的詞 |
| AI 選項式旅行規劃 | 「選項式」是產品內部的分類名稱 |
| 整趟總預算 TWD（可留空） | TWD 是貨幣代碼，不是「台幣」 |
| 避開紅眼航班 | 「紅眼」要先知道才看得懂 |
| 公寓／民宿只顯示實際 Provider 回傳資料，不直接爬取 Airbnb，也不以模擬資料冒充即時庫存。 | 一句給工程師看的話，中間還夾一個英文字 |
| 自動安排每日動線 | 「動線」是室內設計與展場的詞 |

## Definition of done

- [x] 首頁、規劃精靈、建立行程表單裡的上述說法換成日常中文（繁中與簡中）。
- [x] 英日韓不動——TWD、red-eye、Provider 在那些語系本來就是正常用字。
- [x] `legacy.json` 裡兩個對不到來源的舊鍵一併移除。

## How to verify

```bash
cd apps/web && npx vitest run components/new-trip-form components/search-workbench   # 16 passed
```

## Notes

- 訊息檔要用「取代字串」的方式改，不要 `json.dumps` 重寫整份：`search.json` 的
  `workbench` 是壓成一行的物件，重新格式化會讓 14 行的改動變成 100 行的 diff，跟其他
  session 撞得更兇。
- 還沒改的：`trips.json` 編輯器裡十幾處「動線」、「扣次／扣點」、`Provider 未設定`
  這類狀態字串。那些是登入後才看得到的畫面，跟這張任務的「第一次來的人」分開處理。
