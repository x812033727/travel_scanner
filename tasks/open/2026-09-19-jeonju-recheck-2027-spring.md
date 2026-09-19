---
id: 2026-09-19-jeonju-recheck-2027-spring
title: jeonju-hanok-village-day-trip-from-seoul 上線後複查：每年春季慶基殿與南部市場夜市、kobus 與全州公車票價恢復後補數字
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
  - apps/web/public/guides/jeonju-hanok-village-day-trip-from-seoul
---

# jeonju-hanok-village-day-trip-from-seoul 上線後複查：每年春季慶基殿與南部市場夜市、kobus 與全州公車票價恢復後補數字

## Why

`jeonju-hanok-village-day-trip-from-seoul` 的慶基殿三段開放時間、3,000／2,000／1,000、最後一個週三免費、第四個週六韓服日半價（半價只有 tour.jeonju.go.kr 那一頁寫）與南部市場夜市週五六 17:00–23:00 都會換年度；kobus.co.kr 與全州市公車票價附件撰稿時讀不到，表 1 與 H2-2 寫「以官網為準」。規格 `docs/travel-guides-batch-7/jeonju-hanok-village-day-trip-from-seoul.md`「上線後與交叉檢查」要求每年重查，建議排在春季、慶基殿換季前。

## Definition of done

- [ ] 2027 年春季（慶基殿換季前，建議 2027-03）：上述時間與票價核對完；任一項有變，正文、三張表、summary、FAQ、diagram-1 一起改。
- [ ] kobus.co.kr 恢復後：表 1 的高速巴士票價與班次從「以官網為準」改成數字。
- [ ] 全州市公車票價附件抓到後：H2-2 的公車票價與可用交通卡從「以全州市官網為準」改成數字。
- [ ] 每次改動更新 `checked_on`，lint 通過。做完一輪就 done，下一年度另開票。

## Steps

- [ ] **每年春季（第一次 2027-03）**：重查慶基殿的三段開放時間與 3,000／2,000／1,000、最後一個週三免費、第四個週六韓服日半價（規格來源 (6) 那一頁；頁面改版就要重新找依據）、南部市場夜市的週五六 17:00–23:00。
- [ ] **kobus.co.kr 恢復後**：補高速巴士票價與班次；`daegu-airport-ktx-subway-guide` 如果也寫了高速巴士，一起核對口徑。
- [ ] **全州市公車票價附件抓到後**：補公車票價與可用的交通卡。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug jeonju-hanok-village-day-trip-from-seoul
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `jeonju-hanok-village-day-trip-from-seoul` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/jeonju-hanok-village-day-trip-from-seoul` 看三張表與圖。

## Notes

- 來源：`docs/travel-guides-batch-7/jeonju-hanok-village-day-trip-from-seoul.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- SRT 改點、Korail 恢復的複查在 `2026-09-19-sr-korail-recheck-daegu-jeonju`（含 `korea-ktx-srt-ticket-guide`）。
- 目錄缺口：本篇 `destination_id` 是 seoul，全州在第七批之前 0 篇。上線後打開 `destinations/jeonju` 確認相關文章區塊列得出本篇；列不出來就是目錄只看 `destination_id`，要另開票討論一日遊文章在城市頁的露出方式，不要為了露出把 `destination_id` 改成 jeonju。這項 2026-09-19 開票時還沒有人確認過。
- 反向連結（`korea-ktx-srt-ticket-guide` blocks[25]、`seoul-4-day-itinerary` Day 3、可選的韓服兩篇）在「既有文章補連第七批」那張票。`tasks/BOARD.md` 不要提交。
