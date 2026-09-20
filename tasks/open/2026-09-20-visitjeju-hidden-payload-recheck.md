---
id: 2026-09-20-visitjeju-hidden-payload-recheck
title: Recheck live articles quoting Visit Jeju after its site redesign
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T13:05:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
---

# Recheck live articles quoting Visit Jeju after its site redesign

## Why

`visitjeju.net` 改版了。每一頁現在都有一個隱藏區塊：

```html
<div style="display:none" id="__SEARCH_DATA__"> … </div>
```

裡面是**舊版的長介紹**（`sbstseo` 欄位）、兩種地址與營業時間。畫面上的 `상세정보` 已經換成比較短的新摘要。

2026-09-20 寫韓國美食特輯時發現：濟州黑豬肉篇的規格與撰稿筆記逐字抄下來的「官方原文」**有一半在那個隱藏區塊裡**，草稿有 **12 項事實只有隱藏區塊撐得住**，全部刪掉或改寫。

**這兩篇已經在正式站上的文章也引用 Visit Jeju**，寫作時間比改版早，所以很可能有同樣的問題：

| 文章 | 引用的 Visit Jeju 頁 |
| --- | --- |
| `jeju-3-day-itinerary` | 성산일출봉的開放時間、休息日、登頂時間（韓文頁＋英文頁） |
| `korea-food-guide-must-eat` | Traditional Jeju Island Foods、Jeju's Signature Heukdwaeji、Great Dine-alone Spots on Jeju |

`korea-food-guide-must-eat` 的風險比較高：它引的正是特輯這次撞到的那幾個主題頁（黑豬肉、돔베고기、고기국수）。

**這不是「引文位置」的問題。** 那個 div 就在 `<body>` 裡，位置對，但畫面上看不到。真正的標準一直都是**讀者打開那一頁看得到的字**。

## Definition of done

- [ ] 兩篇文章裡每一條出自 Visit Jeju 的主張，都確認在**可見**文字裡站得住
- [ ] 只有隱藏區塊撐得住的主張已刪除或改寫
- [ ] 營業時間類的資訊（성산일출봉）與官方可見頁一致

## Steps

- [ ] 用 `C:\Users\x8120\mokaair-work\korea-food-specials\tools\split_visible.py` 把每一頁切成「可見」與「隱藏」兩份
- [ ] 逐條比對兩篇文章的主張
- [ ] 只有隱藏那份撐得住的，當作沒有來源處理
- [ ] 更新 `sources` 的 `checked_on`

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤，且兩篇的每一條 Visit Jeju 主張都能在可見文字裡找到對應。

## Notes

- 外部請求的 User-Agent 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料；同網域間隔至少 1 秒。
- 這個陷阱也寫在韓國特輯的 `prompts/SOURCE-TIPS.md`（「visitjeju.net 把舊版內容藏在 `display:none` 的區塊裡」一節）。
- 同批還沒寫的濟州文章（涯月咖啡、舊左・細花咖啡、濟州豬肉湯麵）已經在各自的撰稿指令裡帶上這條，不需要這張票處理。
- 值得順手想一下：**別的官方站有沒有同樣的做法**。這類 SEO 隱藏區塊不是 Visit Jeju 獨有的手法。
