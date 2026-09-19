---
id: 2026-09-19-daegu-airport-recheck-2026-q4
title: daegu-airport-ktx-subway-guide 上線後複查：2026-10-26 後 TW663／664 冬季班表、2026-12-31 前 DTRO 票價與一日券
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:38Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/daegu-airport-ktx-subway-guide.json
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
---

# daegu-airport-ktx-subway-guide 上線後複查：2026-10-26 後 TW663／664 冬季班表、2026-12-31 前 DTRO 票價與一日券

## Why

`daegu-airport-ktx-subway-guide` 寫了台灣虎航 TW663／TW664 的班期（運航期間到 2026-10-24／25）與大邱地鐵 1,500／1,700／1,950、30 分鐘轉乘、「沒有一日券」；兩者都在 2026 年第四季會換版。規格 `docs/travel-guides-batch-7/daegu-airport-ktx-subway-guide.md`「上線後與交叉檢查」要求上線 PR 同時開票並寫明日期。

## Definition of done

- [ ] 2026-10-26 之後：冬季班表查到就改 H2-1 表格、summary 第二句與 H2-3 的清晨、深夜那段；查不到就把時間改成「以航空公司官網為準」。
- [ ] 2026-12-31 以前：DTRO 運賃頁與轉乘頁重讀完，1,500／1,700／1,950 與 30 分鐘轉乘確認，整站仍無「1일권」；若出現一日券或觀光通票，H2-4、summary 與 FAQ 第 2 題三處同時改。
- [ ] 每次改動更新 `checked_on`，lint 通過。

## Steps

- [ ] **2026-10-26 之後**：TW663／TW664 的運航期間到 2026-10-24／25。冬季班表出來後用規格「撰稿時要小心」第 (3) 條的 AJAX 端點重查一次，改 H2-1 表格、summary 第二句與 H2-3 的清晨、深夜那段；查不到就把時間改成「以航空公司官網為準」。
- [ ] **2026-12-31 以前**：重讀 DTRO 運賃頁與轉乘頁（頁面標的最近更新是 2026-01-15，票價通常在年初調），確認 1,500／1,700／1,950 與 30 分鐘轉乘沒變，並再確認一次整站仍然沒有「1일권」。若大邱推出一日券或觀光通票，H2-4、summary 與 FAQ 第 2 題三處要同時改，並看 `daegu-2-day-itinerary`（那篇也寫「沒有一日券」，兩篇共用的數字必須同一套）要不要同 PR 跟改。
- [ ] **businfo.daegu.go.kr 或機場的公車 AJAX 之後讀得到時**：把機場往市區的公車路線、班距與末班補進 H2-3，把「以現場站牌為準」換成實際數字。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug daegu-airport-ktx-subway-guide
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `daegu-airport-ktx-subway-guide` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/daegu-airport-ktx-subway-guide` 看 H2-1 表格與 H2-4。

## Notes

- 來源：`docs/travel-guides-batch-7/daegu-airport-ktx-subway-guide.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- SR 票價表／時刻表換版與 Korail 恢復後的複查在 `2026-09-19-sr-korail-recheck-daegu-jeonju`；反向連結（`korea-ktx-srt-ticket-guide` blocks[25] 等）在「既有文章補連第七批」。
- diagram-1 只畫 1.8 公里／28 分、9 分、1 小時 38 分／1 小時 31 分、41 分，不畫票價與首末班，本票兩項通常不必改圖。
- `tasks/BOARD.md` 不要提交。
