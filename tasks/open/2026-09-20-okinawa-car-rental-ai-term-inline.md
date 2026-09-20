---
id: 2026-09-20-okinawa-car-rental-ai-term-inline
title: okinawa-car-rental-guide：blocks[13] 驗車那句的「標記」誤連到 AI 名詞解釋 ai-term-token
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-20T03:12:36Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/okinawa-car-rental-guide.json
---

# okinawa-car-rental-guide：blocks[13] 驗車那句的「標記」誤連到 AI 名詞解釋 ai-term-token

## Why

`okinawa-car-rental-guide` 的 `blocks[13]`（`rich_paragraph`）講的是那霸機場租車櫃檯到驗車的流程，其中
「驗車時繞車一圈，把原有的刮痕全部拍照並請對方在紀錄單上**標記**」——「標記」這兩個字是一個 `article` inline，
指向 `{"kind": "life", "slug": "ai-term-token"}`（AI 名詞解釋）。讀者在租車教學裡點「標記」會跳到一篇講 token 的文章，
是誤植。2026-09-20 逐字確認於 `apps/api/app/guides/content/okinawa-car-rental-guide.json` 的 zh-TW `blocks[13]`
（該篇 zh-TW 共 28 個區塊）。

## Definition of done

- [ ] `blocks[13]` 的那個 inline 改回純文字 `{"type": "text", "text": "標記"}`，**不換成別的連結**；同一塊的其他文字與數字一個都沒動。
- [ ] `grep -n "ai-term-token" apps/api/app/guides/content/okinawa-car-rental-guide.json` 0 命中；全篇沒有其他指向 `life` kind 的 inline。
- [ ] lint 與內容包測試綠；部署後 `guides-import --slug okinawa-car-rental-guide` 是 `update` 再 `--publish`。

## Steps

- [ ] 打開內容包，在 zh-TW `blocks[13]` 的 `inlines` 找到 `{"type": "article", "text": "標記", "kind": "life", "slug": "ai-term-token"}`。
- [ ] 換成 `{"type": "text", "text": "標記"}`；前後兩個 `text` 因此相鄰時可以合併成一個（文字內容與順序不變）。
- [ ] 確認合併後整段文字與改動前逐字相同（只少了連結）。
- [ ] lint、pytest、PR；部署後匯入。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind howto
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機上（站主同意後）：

```bash
uv run python -m app.cli guides-import --slug okinawa-car-rental-guide --dry-run   # 計畫應該只有這幾篇的 zh-TW 是 update
uv run python -m app.cli guides-import --slug okinawa-car-rental-guide --publish
uv run python -m app.cli guides-links-check --locale zh-TW
```


## Notes

- 來源：第八批審查記錄 `review-okinawa.md` C3 第 2 條（彙整在 `docs/travel-guides-batch-8/FOLLOWUPS.md` 第 3 節），由第 7 篇 `okinawa-without-a-car` 的規格審查順手查到，與第八批的內容無關，所以獨立一張票。
- scope 與「既有文章補連第八批」重疊：那張票要把同一篇的 `blocks[23]`（paragraph）改成 `rich_paragraph` 並插一個連 `okinawa-without-a-car` 的 inline。**兩張票不能同時 claim**，先做哪一張都可以。
- `blocks[27]` 的 `foods?city=okinawa` **不要改**（協調者 2026-09-20 裁決：`?city=` 不是錯）。
- `blocks[24]`（photo-2）與 `okinawa-4-day-itinerary` `blocks[16]` 是同一張 Commons 照片；要處理重複就是換這一張，但那是另一件事、非必要。
