---
id: 2026-09-19-sendai-matsushima-recheck-2026-q4
title: sendai-matsushima-2-day-itinerary 2026 年 10 到 12 月複查：圓通院點燈、光のページェント、遊覽船與福浦橋冬季、瑞巖寺、瑞鳳殿
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/sendai-matsushima-2-day-itinerary.json
---

# sendai-matsushima-2-day-itinerary 2026 年 10 到 12 月複查：圓通院點燈、光のページェント、遊覽船與福浦橋冬季、瑞巖寺、瑞鳳殿

## Why

`sendai-matsushima-2-day-itinerary` 的季節段與表格 2 寫了圓通院紅葉點燈、SENDAI光のページェント、松島遊覽船冬季安排、福浦橋冬季時間、瑞巖寺閉門時間與瑞鳳殿冬季開館時間，這些都在每年 10 到 12 月換年度。規格 `docs/travel-guides-batch-7/sendai-matsushima-2-day-itinerary.md`「上線後與交叉檢查」列了每一項的月份。

## Definition of done

- [ ] 2026-10：圓通院紅葉點燈當年度日期查過，季節段那一句改好。
- [ ] 2026-11 前後：光のページェント 2026 年檔期公布後，季節段冬天那句補上日期或維持只寫月份。
- [ ] 2026-11：遊覽船冬季安排（16:00 停航、9:00 中型船）、福浦橋冬季時間（11 月到 3 月 8:30–16:30）、瑞巖寺 11 月與 12 月的閉門時間核對完，有變就改表格 2 與季節段。
- [ ] 2027 年 1 月前：瑞鳳殿冬季開館時間（12/1–1/31 9:00–16:20）與仙台市博物館年末年始休館日核對完。
- [ ] 每次改動更新 `checked_on`，lint 通過。做完這一輪就 done，下一年度另開票。

## Steps

- [ ] **每年 10 月**：重查圓通院紅葉點燈的當年度日期，改季節段那一句。
- [ ] **2026 年 11 月前後**：SENDAI光のページェント 官網公布 2026 年檔期後補日期；`japan-winter-illumination-2026` 若加入仙台，那篇可以反向連本篇，但本文不連它（2027 年到期）。
- [ ] **每年 11 月**：遊覽船、福浦橋、瑞巖寺三項。
- [ ] **2027 年 1 月前**：瑞鳳殿與仙台市博物館。
- [ ] **丸文松島汽船票價若讀到官方頁**：H2-3 那句從「協會 FAQ 寫兩家同價」改成明確引用丸文官網，sources 換來源。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug sendai-matsushima-2-day-itinerary
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `sendai-matsushima-2-day-itinerary` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/sendai-matsushima-2-day-itinerary` 看表格 2 與季節段。

## Notes

- 來源：`docs/travel-guides-batch-7/sendai-matsushima-2-day-itinerary.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 春季的 JR 改正（仙石線班次、仙台まるごとパス）與 jreast 票價在 `2026-09-19-sendai-four-spring-2027`；2027-05-11 拆櫻花篇連結在 `2026-09-19-gw-sakura-links-expire-2027-05`。
- 與第 9 篇共用的るーぷる、まるごとパス數字任何一篇改，同一個 PR 改另一篇；本票的項目不碰那些數字。
- 反向連結在「既有文章補連第七批」那張票。`tasks/BOARD.md` 不要提交。
