---
id: 2026-09-19-golden-week-nozomi-watch-2027
title: japan-golden-week-2027 2027 年 1 月起每月查 smart-ex.jp 的のぞみ全席指定席公告（japan-shinkansen-ticket-guide 同 PR）
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-golden-week-2027.json
  - apps/api/app/guides/content/japan-shinkansen-ticket-guide.json
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
---

# japan-golden-week-2027 2027 年 1 月起每月查 smart-ex.jp 的のぞみ全席指定席公告（japan-shinkansen-ticket-guide 同 PR）

## Why

`japan-golden-week-2027` 的 H2-2 寫のぞみ在黃金週尖峰期全席指定席、期間以 JR 東海公告為準；2027 年的實際期間要等スマートEX 公告。既有的 `japan-shinkansen-ticket-guide` 的 callout 還寫 2026 年度那一串日期。規格 `docs/travel-guides-batch-7/japan-golden-week-2027.md`「上線後與交叉檢查」要求上線 PR 同時開票，scope 含本篇與 `japan-shinkansen-ticket-guide` 兩個內容包，2027 年 1 月起每月查一次。

## Definition of done

- [ ] 公告出來後：(1) 本篇 H2-2 的段落與 callout 補上實際期間，callout 標題改成期間日期；(2) `japan-shinkansen-ticket-guide` 的 callout 在同一個 PR 更新成新年度；(3) `taiwan-long-weekends-2027-flight-planning` 撞期段「2027 年黃金週的期間以 JR 東海公告為準」那句可以一起補。
- [ ] 若到 2027-04-01 仍無公告，在本票記下查核日期，本篇維持「以公告為準」。
- [ ] 每次改動更新 `checked_on`，lint 通過。

## Steps

- [ ] **2027-01 起每月一次（1 月、2 月、3 月、4 月初）**：看 https://smart-ex.jp/topics/ 有沒有 2027 年黃金週的＜のぞみ全席指定席＞公告。參考時間點：JR 東海／JR 西日本 2026-05-21 發過 2026 年度的追加公告，スマートEX 的 GW 專門公告 2025 年是 3 月 12 日發布、年度期間頁是 4 月 1 日，所以 3 月前後最可能看到。
- [ ] 公告出來後照 Definition of done 的 (1)(2)(3) 改，三篇的のぞみ說法保持一致（尖峰期全席指定席、期間以公告為準）。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug japan-golden-week-2027 --slug japan-shinkansen-ticket-guide
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出改過的 slug 為 `update`，再 `--publish`；打開 `/zh-TW/guides/intel/japan-golden-week-2027` 看 H2-2 的 callout。

## Notes

- 來源：`docs/travel-guides-batch-7/japan-golden-week-2027.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。規格只要求兩個內容包，`taiwan-long-weekends-2027-flight-planning` 因 (3) 可能一起補而列進 scope；那個檔也在 `2026-09-14-batch-6-guides-dated-maintenance` 的 scope 裡，改之前看那張票有沒有人在動。
- 本篇 2027-05-10 到期；2027-02-21 刪開頭農曆新年那句在 `2026-09-19-lny-links-expire-2027-02-21`，2027-05-11 過期後的處理在 `2026-09-19-gw-sakura-links-expire-2027-05`。
- `tasks/BOARD.md` 不要提交。
