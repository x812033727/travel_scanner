---
id: 2026-09-19-bangkok-stay-recheck-2027-01
title: bangkok-where-to-stay 上線後複查：2027-01-05 BTS 時刻表、2027-01-15 聯合票價、BEM 首末班（曼谷交通篇與四天篇同 PR）
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-where-to-stay.json
  - apps/web/public/guides/bangkok-where-to-stay
  - apps/api/app/guides/content/bangkok-bts-mrt-boat-guide.json
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
---

# bangkok-where-to-stay 上線後複查：2027-01-05 BTS 時刻表、2027-01-15 聯合票價、BEM 首末班（曼谷交通篇與四天篇同 PR）

## Why

`bangkok-where-to-stay`（2026-09-17 上線）的 BTS 服務時間、MRT 首末班與「住 BTS 沿線還是 MRT 沿線比較划算」的結論都綁在會換版的官方頁與政策上。規格 `docs/travel-guides-batch-7/bangkok-where-to-stay.md`「上線後與交叉檢查」要求上線 PR 同時開票並寫明日期；其中兩項牽動既有的 `bangkok-4-day-itinerary` 與 `bangkok-bts-mrt-boat-guide`，要同一個 PR 改。

## Definition of done

- [ ] 2027-01-05 的 BTS 複查做完：summary、表 A、H2-8 與 diagram-1 的服務時間、暹羅站末班、售票處時段一致，`bangkok-4-day-itinerary` 裡同一組數字同 PR 對齊。
- [ ] 2027-01-15 的聯合票價複查做完：新制上路則 H2-9 檢查清單與 faq 第一題重寫，`bangkok-bts-mrt-boat-guide` 同 PR 改；沒上路就在本票記下查核日期與現況。
- [ ] BEM 的 MRT 首末班讀到了就補進 H2-8 與表 A，並同步改 `bangkok-bts-mrt-boat-guide`；仍讀不到就記下日期。
- [ ] 每次改動更新 `sources` 的 `checked_on`，lint 通過（圖上的數字都在正文）。

## Steps

- [ ] **BEM（可立即做，之後每次複查再試一次）**：開 https://metro.bemplc.co.th/Train-Service-Time 。讀到了就把實際首末班補進 H2-8 與表 A，並同步更新 `bangkok-bts-mrt-boat-guide` 最後那句「MRT 各站末班時間不同，深夜出門先查 BEM 官網」。兩篇要一起改。
- [ ] **2027-01-05**（BTS「Effective from 1 January 2026」版時刻表滿一年）：重看 https://www.bts.co.th/eng/traintime-frequency/ 的服務時間、暹羅站末班、售票處時段，以及首班車表是否已從 COMING SOON 換成實際時刻。有變就同時改 summary、表 A、H2-8 與 diagram-1（三處必須一致），並把 `bangkok-4-day-itinerary` 裡同一組數字一起改。
- [ ] **2027-01-15**：泰國政府 2026-06-23 內閣決議撤銷 20 泰銖均一票價，改規劃「每趟最高 45 泰銖、跨線不重收起跳費」的聯合票價，部令預定 2026 年 12 月前完成。查新制是否上路；上路就重寫本篇 H2-9 的檢查清單與 faq 第一題（住 BTS 沿線還是 MRT 沿線划算的結論會變），`bangkok-bts-mrt-boat-guide` 同一個 PR 改。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug bangkok-where-to-stay --slug bangkok-bts-mrt-boat-guide --slug bangkok-4-day-itinerary
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機 `python -m app.cli guides-import --actor-email <admin> --dry-run` 應列出改過的 slug 為 `update`，再加 `--publish`；打開 `/zh-TW/guides/howto/bangkok-where-to-stay` 看表 A、H2-8 與圖。

## Notes

- 來源：`docs/travel-guides-batch-7/bangkok-where-to-stay.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出；先讀規格再改。
- AOT 的 S1 巴士末班（20:00 與 17:00 兩個版本）不在本票定案：下次重查 `bangkok-airport-to-city` 時一起確認，兩篇同時改。
- 潑水節：本篇依規格不寫日期，每年官方活動日期公布後不用動。
- 既有三篇曼谷文的反向連結，以及 `bangkok-4-day-itinerary`「5 月到 10 月雨季」沒有出處的待修，都在「既有文章補連第七批」那張票，不在本票。
- `tasks/BOARD.md` 由工具產生，不要提交。
