---
id: 2026-09-20-bangkok-4-day-wat-arun-dress
title: bangkok-4-day-itinerary：大皇宮服裝清單漏「褲裙」、鄭王廟改成觀光局的 200 泰銖與 08:00 到 18:00
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:13:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
---

# bangkok-4-day-itinerary：大皇宮服裝清單漏「褲裙」、鄭王廟改成觀光局的 200 泰銖與 08:00 到 18:00

## Why

`bangkok-4-day-itinerary` 有兩件讀者看得到的事實問題，都在第一天那一段與門票表上，同一個 PR 改。

**1. 大皇宮服裝清單漏一項。** `blocks[5]`（paragraph）現在列**十項**：無袖上衣、背心、露肚上衣、透膚上衣、短褲、破洞褲、緊身褲、單車褲、迷你裙、睡衣式服裝。
官網是**十一項**：https://www.royalgrandpalace.th/en/visit/practical-information 2026-09-20 可見內容逐條為
No sleeveless shirts / No vests / No short top / No see through tops / No short hot pants or short pants / No torn pants / No tight pants / No bike pants /
No mini skirts / **No pants skirts** / No sleeping suit——漏掉的是「褲裙」，位置在「迷你裙」與「睡衣式服裝」之間。

**2. 鄭王廟寫「以官網為準」，但泰國觀光局有數字。** 現在三處都沒有數字：`blocks[5]`「門票以官網為準（2026 年 9 月官網連不上，看售票處告示）」、
`blocks[18]` 表格那一列「以官網為準／以官網為準」、`blocks[0]` 還把鄭王廟門票列進「查不到官方數字的（鄭王廟門票、Jim Thompson House 門票、恰圖恰的營業時間）」。
泰國觀光局東京辦事處鄭王廟頁 https://www.thailandtravel.or.jp/wat-arun/ 2026-09-20 讀到 営業時間「08:00～18:00」、料金「200バーツ」。
鄭王廟自己的網域（watarun1.com／watarun.net）連不上，所以採政府觀光機構的數字——這正是第八批 README 的通則。
第八批第 14 篇 `thailand-temple-etiquette-dress-code` 的表格會寫 200 泰銖與 08:00 到 18:00，**兩篇不能一篇寫數字、一篇寫「以官網為準」**。

## Definition of done

- [ ] `blocks[5]` 的服裝清單變十一項（「迷你裙」與「睡衣式服裝」之間插「褲裙」），順序照官網。
- [ ] 鄭王廟三處一起改成「200 泰銖（外國人）／每天 08:00 到 18:00」並寫明出處是泰國觀光局（2026 年 9 月）：`blocks[5]` 那一句、`blocks[18]` 表格那一列的兩格、`blocks[0]` 的「查不到官方數字的」清單裡拿掉鄭王廟。
- [ ] `sources` 補上 TAT 東京鄭王廟頁、更新大皇宮 Practical Information 的 `checked_on`；`blocks[18]` 的 caption 查證來源加上泰國觀光局。
- [ ] 沒有動 `blocks[19]` 的 800／1,600（500＋300 的加總，本身正確，只是調價時的連動點）、沒有動 `blocks[16]`（activities offer）、沒有動臥佛寺的 300 泰銖與 08:00 到 19:30。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug bangkok-4-day-itinerary` 是 `update` 再 `--publish`。

## Steps

- [ ] `blocks[5]`：補「褲裙」；把鄭王廟那句改成「門票 200 泰銖、每天 08:00 到 18:00（泰國觀光局，2026 年 9 月）」。
- [ ] `blocks[18]`（table）：鄭王廟那一列的「票價（成人）」與「開放或營運時間」兩格填上數字，備註保留「從 Tha Tien 碼頭搭渡船過河」。
- [ ] `blocks[0]`（rich_paragraph）：把鄭王廟從「查不到官方數字的」那一串拿掉（Jim Thompson House 與恰圖恰留著）。
- [ ] 圖不用改：`apps/web/public/guides/bangkok-4-day-itinerary/diagram-1.svg` 2026-09-20 確認只寫「河西岸的鄭王廟用渡船過河」，沒有票價。
- [ ] 與第八批第 14 篇對：鄭王廟 200 泰銖／08:00 到 18:00、臥佛寺 08:00 到 19:30、大皇宮十一條清單三組要一字不差。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug bangkok-4-day-itinerary --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug bangkok-4-day-itinerary --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

- 來源：審查記錄 `plan8/review/review-thailand-a.md` C3 第 1、2 列（彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節），由第八批第 14 篇規格的審查帶出。
- **`blocks[0]` 是審查記錄沒列到的第三處**，這次彙整時打開內容包才發現；只改 `blocks[5]` 與 `blocks[18]` 會留下一句自相矛盾的前言。
- scope 與「既有文章補連第八批」重疊：那張票要在 `blocks[5]` 插一個連第 14 篇的 inline（整塊改 `rich_paragraph`）、在 `blocks[15]` 插一個連第 13 篇的 inline。**`blocks[5]` 的兩件事併成一次編輯**，哪一張票先做就一起做完；兩張票不能同時 claim。
- `blocks[24]` 的 `foods?city=bangkok` **不要改**（協調者 2026-09-20 裁決）。
- 泰國門票常在年初調：2027-01 以前還有一張複查票（第八批 FOLLOWUPS 第 1 節第 30 列），那張票會重讀同樣這幾個官方頁。
