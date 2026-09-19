---
id: 2026-09-19-gw-sakura-links-expire-2027-05
title: 2027-05-11 黃金週與櫻花情報過期：sendai-matsushima-2-day-itinerary 拆櫻花連結、taiwan-long-weekends-2027 拆黃金週連結
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
  - apps/api/app/guides/content/sendai-matsushima-2-day-itinerary.json
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
---

# 2027-05-11 黃金週與櫻花情報過期：sendai-matsushima-2-day-itinerary 拆櫻花連結、taiwan-long-weekends-2027 拆黃金週連結

## Why

`japan-cherry-blossom-2027` 與 `japan-golden-week-2027` 兩篇 intel 都在 2027-05-10 到期。`sendai-matsushima-2-day-itinerary`（長青 howto）季節段春天那句連了櫻花篇；「既有文章補連第七批」會在 `taiwan-long-weekends-2027-flight-planning`（2027-12-31 到期）的撞期段加連黃金週篇，規格明說那屬於季節段例外、要同時開 2027-05-11 的刪除票。兩份規格（`docs/travel-guides-batch-7/sendai-matsushima-2-day-itinerary.md`、`docs/travel-guides-batch-7/japan-golden-week-2027.md`）都要求上線 PR 開票並寫明日期。

## Definition of done

- [ ] 2027-05-11 起：`sendai-matsushima-2-day-itinerary` 季節段春天那句的 `japan-cherry-blossom-2027` article inline 拆掉，句子保留；屆時若已有 2028 年版櫻花情報就改連新版。`related` 四篇都是長青 howto，不用動。
- [ ] 2027-05-11 起：`taiwan-long-weekends-2027-flight-planning` 撞期段「勞動節連假夾在日本黃金週裡」後面補的 `japan-golden-week-2027` article inline 拆掉，句子保留（那張票沒加就不用動）。
- [ ] lint 通過，`guides-links-check --locale zh-TW` 沒有壞連結。

## Steps

- [ ] 2027-05-11 或之後：確認兩篇 intel 在站上已過期。
- [ ] 改 `sendai-matsushima-2-day-itinerary` 與 `taiwan-long-weekends-2027-flight-planning`，只拆 inline、不動句子。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`，再跑 `guides-links-rebuild` 與 `guides-links-check --locale zh-TW`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug sendai-matsushima-2-day-itinerary --slug taiwan-long-weekends-2027-flight-planning
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出兩個 slug 為 `update`，再 `--publish`。

## Notes

- 來源：`docs/travel-guides-batch-7/sendai-matsushima-2-day-itinerary.md` 與 `japan-golden-week-2027.md` 的「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- `2026-09-14-batch-6-guides-dated-maintenance` 的 2027-05-11 項目同一天拆 `taiwan-long-weekends-2027-flight-planning` 與 `kanazawa-2-day-itinerary` 的櫻花篇連結，可以同一個 PR 一起做。
- 要不要寫 `japan-golden-week-2028`：內閣府寫明 2028 年的祝日在 2027 年 2 月刊載；真要寫就沿用第七批規格的結構，並把黃金週篇的反向連結轉過去。這是新文章的決定，不在本票做。
- `japan-cherry-blossom-2027` 撞期段連黃金週篇的那條，兩篇同一天到期，不必拆。`tasks/BOARD.md` 不要提交。
