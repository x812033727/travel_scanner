---
id: 2026-09-19-sr-korail-recheck-daegu-jeonju
title: SR 改點或 Korail 恢復後複查：daegu-airport-ktx-subway-guide、jeonju-hanok-village-day-trip-from-seoul 與 korea-ktx-srt-ticket-guide 同 PR
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
  - apps/api/app/guides/content/daegu-airport-ktx-subway-guide.json
  - apps/web/public/guides/daegu-airport-ktx-subway-guide
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
  - apps/web/public/guides/jeonju-hanok-village-day-trip-from-seoul
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
---

# SR 改點或 Korail 恢復後複查：daegu-airport-ktx-subway-guide、jeonju-hanok-village-day-trip-from-seoul 與 korea-ktx-srt-ticket-guide 同 PR

## Why

`daegu-airport-ktx-subway-guide` 與 `jeonju-hanok-village-day-trip-from-seoul` 的 SRT 票價、班次與時刻（37,000／53,600／15,600；25 班、1 小時 28 分、23:11→00:46、水西 4 班、30,300／43,900）都來自 SR 的票價表與時刻表附件，既有的 `korea-ktx-srt-ticket-guide` 也寫同一組數字；KTX 的票價兩篇都因 Korail 官網讀不到而寫「以 Korail 官網為準」。兩份規格都要求：SR 改版或 Korail 恢復時，三篇同一個 PR 改。

## Definition of done

- [ ] SR 公布新票價表或改點後：兩篇與 `korea-ktx-srt-ticket-guide` 的 SRT 數字同一個 PR 對齊；全州篇的表 1、summary、FAQ、diagram-1 一起改。
- [ ] Korail 官網恢復後：KTX 首爾→東大邱票價補進大邱篇 H2-1 表格、KTX 龍山→全州票價補進全州篇，三篇的「以 Korail 官網為準」同 PR 換成數字。
- [ ] 每次改動更新 `checked_on`，lint 通過（圖上的數字都在正文）。

## Steps

- [ ] **SR 每次公布新票價表（現行是 2026-09-01 起）**：大邱篇的 37,000／53,600／15,600 與 `korea-ktx-srt-ticket-guide` 的 37,000／53,600 同一個 PR 改完。
- [ ] **SR 改點後（每次時刻表改版）**：重讀 SR 的 `atchNo=29` 時刻表與 `atchNo=18` 票價表，核對全州篇的 25 班、1 小時 28 分、23:11→00:46、水西 4 班、30,300／43,900；有變就同時改全州篇的表 1、summary、FAQ、diagram-1，並檢查 `korea-ktx-srt-ticket-guide` 要不要一起改（那篇若順便補水西 4 班或 SRT 30,300，要和全州篇同一個 PR）。大邱篇 diagram-1 上的「SRT 1 小時 31 分」也要對。
- [ ] **Korail 官網恢復後**：把 KTX 首爾→東大邱的票價補進大邱篇 H2-1 表格、KTX 龍山→全州票價補進全州篇，並把三篇的「以 Korail 官網為準」同一個 PR 換成數字。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug daegu-airport-ktx-subway-guide --slug jeonju-hanok-village-day-trip-from-seoul --slug korea-ktx-srt-ticket-guide
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出三個 slug 為 `update`，再 `--publish`。

## Notes

- 來源：`docs/travel-guides-batch-7/daegu-airport-ktx-subway-guide.md` 與 `docs/travel-guides-batch-7/jeonju-hanok-village-day-trip-from-seoul.md` 的「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。沒有固定日期，由 SR 公告觸發；SR 通常年初換票價表。
- `korea-ktx-srt-ticket-guide` blocks[25] 的反向連結（第 13、15 篇合併成同一次編輯）在票 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批）；若那張票還沒做，先做它，否則 block 編號會變。
- 大邱篇 2026 年第四季的班表與 DTRO 複查在 `2026-09-19-daegu-airport-recheck-2026-q4`；全州篇的慶基殿年度複查在 `2026-09-19-jeonju-recheck-2027-spring`。
- `tasks/BOARD.md` 不要提交。
