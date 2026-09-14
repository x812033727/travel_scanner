---
id: 2026-09-14-kanazawa-21-museum-closure-2027-05
title: 2027-05-06 起金澤篇的 21 世紀美術館改寫成休館中，2028 年 3 月重開後改回
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-14T13:37:34Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/kanazawa-2-day-itinerary.json
---

# 2027-05-06 起金澤篇的 21 世紀美術館改寫成休館中，2028 年 3 月重開後改回

## Why

`kanazawa-2-day-itinerary` Day 1 下午排 21 世紀美術館。館方官網（來館資訊頁的ミュージアムリンク・パス公告，2026-09-14 讀）寫明因大規模修繕工事，預定 2027 年 5 月 6 日起休館到 2028 年 3 月。正文已加一句預告；休館期間 Day 1 的段落、H2 標題、總覽表與圖解上的「21 世紀美術館」站名要改寫，重開後再改回。這個日期不在 `2026-09-14-batch-6-guides-dated-maintenance` 的清單裡，所以另開一張。

## Definition of done

- [ ] 2027-05-06 起：Day 1 下午改成替代（例如鈴木大拙館、金澤城公園多留一小時），H2 標題與總覽表不再列 21 世紀美術館為當天景點；圖解右半部周遊巴士環線的站名可以保留（巴士照停），但正文要說明館內休館。交流區是否開放以館方公告為準。
- [ ] 2028 年 3 月館方公告重開後：改回原本的段落，票價與時段重查。
- [ ] 每次更新 `checked_on`，lint 通過（圖上的數字都要在正文），主機 `--publish`。

## Steps

- [ ] 2027-04 讀 https://www.kanazawa21.jp/data_list.php?g=7&d=1 確認休館日期沒變。
- [ ] 改內容包（需要時改 SVG）；跑 lint 與內容包測試；部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug kanazawa-2-day-itinerary
uv run pytest tests/test_guides_content_pack.py -q
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run` 應列出 `kanazawa-2-day-itinerary` 為 `update`，再加 `--publish`；打開 `/zh-TW/guides/howto/kanazawa-2-day-itinerary` 看改過的段落。

## Notes

- 改內容包時，同時把重新查證過的 sources 的 `checked_on` 改成查證當天；`tasks/BOARD.md` 由工具產生，不要提交。
- 本篇的規格（來源網址、當初讀到的數字、撰稿注意事項）在 `docs/travel-guides-batch-6/<slug>.md`，先讀它再改。
