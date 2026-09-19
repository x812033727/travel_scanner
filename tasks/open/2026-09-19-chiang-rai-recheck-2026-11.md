---
id: 2026-09-19-chiang-rai-recheck-2026-11
title: chiang-rai-2-day-itinerary 上線後複查：每年 11 月前 TAT 東京景點頁，Greenbus 與各官網恢復後補數字（清邁篇同 PR）
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
  - apps/api/app/guides/content/chiang-rai-2-day-itinerary.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
---

# chiang-rai-2-day-itinerary 上線後複查：每年 11 月前 TAT 東京景點頁，Greenbus 與各官網恢復後補數字（清邁篇同 PR）

## Why

`chiang-rai-2-day-itinerary` 撰稿時 Greenbus、AOT 清萊機場交通頁、Air4Thai、黑屋官網、doitung.org、singhapark.com、chiangraicity.go.th 都連不上，正文多處寫「以官網／現場為準」；白廟 200 泰銖與清邁到清萊 3 小時 20 分兩個數字也出現在既有的 `chiang-mai-3-day-itinerary`。規格 `docs/travel-guides-batch-7/chiang-rai-2-day-itinerary.md`「上線後與交叉檢查」要求開 tasks/open 票追蹤，並在每年 11 月旺季開始前重查。

## Definition of done

- [ ] 2026-11-01 前做完一輪 TAT 東京五個景點頁與清萊頁交通時間的複查；白廟 200 泰銖或 3 小時 20 分有變，本篇與 `chiang-mai-3-day-itinerary` 同一個 PR 改。
- [ ] Greenbus 恢復後：清邁往清萊的實際發車站、班次與票價核對完，本篇交通表改成實際票價；若不是「第 1 巴士站」，清邁篇 Day 3 那句同 PR 修正。
- [ ] 其他官網任一個恢復後，對應的「以現場為準」改成數字（見 Steps）。
- [ ] 每次改動更新 `sources` 的 `checked_on`，lint 通過。做完一輪就 done，下一年度另開票。

## Steps

- [ ] **每年 11 月旺季開始前（第一次 2026-11-01 前）**：重查 TAT 東京的五個景點頁（白廟、藍廟、黑屋、花園、辛哈公園）與清萊頁的交通時間。白廟 200 泰銖或清邁到清萊 3 小時 20 分有變，改本篇並在同一個 PR 改 `chiang-mai-3-day-itinerary`。
- [ ] **Greenbus 官網恢復後**：核對清邁往清萊的實際發車站、班次與票價。若確認不是「第 1 巴士站」，同時修正清邁篇 Day 3 那一句與本篇的交通表；本篇把「以官網為準」換成實際票價。
- [ ] **AOT 清萊機場交通頁、Air4Thai、黑屋官網 thawan-duchanee.com、doitung.org、singhapark.com、chiangraicity.go.th 任一個恢復後**：補機場到市區的價目、黑屋門票、董山套票、辛哈公園的付費項目、鐘樓燈光秀場次，並把對應的「以現場為準」改成數字。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug chiang-rai-2-day-itinerary --slug chiang-mai-3-day-itinerary
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出改過的 slug 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/chiang-rai-2-day-itinerary` 看交通表。

## Notes

- 來源：`docs/travel-guides-batch-7/chiang-rai-2-day-itinerary.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 燒田季口徑：本篇與 `southeast-asia-seasons-when-to-go` 都只寫「2 月到 4 月前後」與「查 Air4Thai」，不寫「3 月最嚴重」；Air4Thai 讀得到之後的補寫在 `2026-09-19-sea-seasons-recheck-2027-01`。
- `chiang-mai-3-day-itinerary` 的反向連結與「3 月最嚴重」待修在「既有文章補連第七批」那張票；`foods?city=chiang-mai` 的統一等 `2026-09-14-food-links-city-param-ignored`。
- `tasks/BOARD.md` 由工具產生，不要提交。
