---
id: 2026-10-06-itinerary-osaka-kyoto-nara-full-recheck
title: 大阪京都奈良四天行程全篇重查：九月查證字樣、summary 與自稱次數
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-06T01:57:49Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/osaka-kyoto-nara-4-day-itinerary.json
---

# 大阪京都奈良四天行程全篇重查：九月查證字樣、summary 與自稱次數

## Why

`osaka-kyoto-nara-4-day-itinerary` 是 2026-09-13 一次查證寫成的，之後只換過局部：KANSAI RAILWAY PASS LITE（#1258，
2026-10-05）與 Day 4 環球影城的營業時間與票價（票 `2026-10-05-itinerary-usj-september-hours`，2026-10-06）。
讀者看得到的地方還寫著整篇「2026 年 9 月查證」：

- `description`：「清水寺、東大寺、大阪城、環球影城的門票與開放時間（2026 年 9 月查證）」，其中環球影城已經是 10 月 6 日的數字。
- 開頭段落：「門票、開放時間、車程都在 2026 年 9 月從官網查證過」。
- 交通票券表的 caption「2026 年 9 月查證，票價為各官網公告；…」與區間車程表的 caption「票價 2026 年 9 月查證」。
- `sources` 20 筆裡 16 筆的 `checked_on` 還是 2026-09-13。

另外兩個編輯規則的老問題：全篇沒有 summary 區塊（`pack_cli lint` 的 `no_summary` 警告、`intake_check.py --from-content`
的「first block is not summary」），「這篇／本文」出現兩次（開頭段落「這篇給一份…」、JR 周遊券那一列「照本文行程不需要」），
house rule 上限一次。

## Definition of done

- [ ] 清水寺、伏見稻荷、東大寺、大阪城、交通區間與周遊券的每個價格、時間都在改寫當天的官方頁重讀過，`sources` 的 `checked_on`
      是真的打開那頁的日期；讀不到的照 `docs/travel-guides-batch-8/README.md` §「讀不到的官方站」更新的做法，留舊文並寫進 Notes。
- [ ] `description`、開頭段落、兩張表的 caption 不再寫跟實際查證日不符的月份（寫成當次重查的月份，或拿掉月份）。
- [ ] 第一個區塊是 2 到 5 句的 summary，數字逐字照正文（`docs/travel-guides-batch-7/README.md` §`pack.json`）。
- [ ] 「這篇／本文」全篇最多一次。
- [ ] 合併後由協調者在站主同意下跑 `guides-import --slug osaka-kyoto-nara-4-day-itinerary`（dry-run 再 publish）。

## Steps

- [ ] 讀 `.agents/skills/content-pipeline/SKILL.md` 與 `references/travel-batch.md`（在 `.agents/skills/content-pipeline/` 下）。
- [ ] 逐一重開 `sources` 的 16 筆 2026-09-13 來源（JS 殼的頁面用真瀏覽器渲染，見下面 Notes）。
- [ ] 改正文、caption、description、開頭段落，補 summary。
- [ ] `cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary`、
      `.venv/Scripts/python.exe ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug osaka-kyoto-nara-4-day-itinerary --from-content`、
      `PYTHONUTF8=1 uv run pytest tests/test_guides_content_pack.py -q`。

## How to verify

```bash
cd apps/api
grep -n "9 月" app/guides/content/osaka-kyoto-nara-4-day-itinerary.json   # 沒有跟 checked_on 不符的月份
PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --slug osaka-kyoto-nara-4-day-itinerary   # 0 errors，沒有 no_summary
PYTHONUTF8=1 .venv/Scripts/python.exe ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug osaka-kyoto-nara-4-day-itinerary --from-content
```

## Notes

- 從 `2026-10-05-itinerary-usj-september-hours` 的 Notes 開出來：那張票只改了 Day 4 的環球影城段落與三筆 USJ 來源，
  照它的 Notes 沒動 description 與開頭段落，結案後這兩條就不在佇列裡了。
- `intake_check.py` 另報「link block uses ?city=」（美食目錄連結 `?city=osaka-kyoto`）：`travel-batch.md` 說既有文章的
  `?city=` 不是錯，不用改。
- 環球影城的三頁（`usj.co.jp` 兩頁、`usjticketing.com`）curl 只拿到 app shell；2026-10-06 用 Playwright 的
  `chromium_headless_shell` 加編輯 UA 渲染讀得到（營業時間日曆要點月份標題右邊的箭頭換月）。
