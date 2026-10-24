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
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - apps/api/app/guides/content/chiang-rai-2-day-itinerary.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
  - apps/web/public/guides/chiang-rai-2-day-itinerary/diagram-1.svg
  - apps/web/public/guides/chiang-mai-3-day-itinerary/diagram-1.svg
  - docs/chiang-rai-transport-recheck-20261024.md
---

# chiang-rai-2-day-itinerary 上線後複查：每年 11 月前 TAT 東京景點頁，Greenbus 與各官網恢復後補數字（清邁篇同 PR）

## Why

`chiang-rai-2-day-itinerary` 撰稿時 Greenbus、AOT 清萊機場交通頁、Air4Thai、黑屋官網、doitung.org、singhapark.com、chiangraicity.go.th 都連不上，正文多處寫「以官網／現場為準」；白廟 200 泰銖與清邁到清萊 3 小時 20 分兩個數字也出現在既有的 `chiang-mai-3-day-itinerary`。規格 `docs/travel-guides-batch-7/chiang-rai-2-day-itinerary.md`「上線後與交叉檢查」要求開 tasks/open 票追蹤，並在每年 11 月旺季開始前重查。

## Definition of done

- [x] 2026-11-01 前做完一輪 TAT 東京五個景點頁與清萊頁交通時間的複查；白廟 200 泰銖或 3 小時 20 分有變，本篇與 `chiang-mai-3-day-itinerary` 同一個 PR 改。
- [ ] Greenbus 恢復後：清邁往清萊的實際發車站、班次與票價核對完，本篇交通表改成實際票價；若不是「第 1 巴士站」，清邁篇 Day 3 那句同 PR 修正。
- [ ] 其他官網任一個恢復後，對應的「以現場為準」改成數字（見 Steps）。
- [ ] 每次改動更新 `sources` 的 `checked_on`，lint 通過。做完一輪就 done，下一年度另開票。

## Steps

- [x] **每年 11 月旺季開始前（第一次 2026-11-01 前）**：重查 TAT 東京的五個景點頁（白廟、藍廟、黑屋、花園、辛哈公園）與清萊頁的交通時間。白廟 200 泰銖或清邁到清萊 3 小時 20 分有變，改本篇並在同一個 PR 改 `chiang-mai-3-day-itinerary`。
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
- `chiang-mai-3-day-itinerary` 的反向連結在票 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批），「6 月到 10 月是雨季」與「3 月最嚴重」的待修在 `2026-09-16-existing-guides-season-sources`；`foods?city=chiang-mai` 的統一等 `2026-09-14-food-links-city-param-ignored`。
- `tasks/BOARD.md` 由工具產生，不要提交。


### 2026-10-24 coordinated execution

Parent verified current open-task scopes and open-PR ownership before taking the listed narrow paths. This is a local implementation task; no production, paid or media approval is implied. Existing unrelated producers and evidence remain intact.


### 2026-10-24 source-maintenance readback

TAT六頁當日複查完成；Greenbus已恢復，Terminal3/Arcade至清萊Terminal1、通常3–4小時。兩篇JSON與兩張SVG已同步本機校正，schema/lint實際exit0；兩輪不同審查者核對最終四檔hash，兩張PNG均目視檢查。詳見[校正與雜湊收據](../../docs/chiang-rai-transport-recheck-20261024.md)。尚未發布，原票保留：實際日期／車種票價尚未取得，其他頁面沒有可驗證費率；仍需限定兩slug的正式dry-run、核准、發布與公開讀回。不得以本機稿替代這些關卡。

Release this source-check claim after the persisted handoff; retain all remaining acceptance and media/account/production gates.


2026-10-24 final publication preparation: inherited repository-vs-public differences were separately verified against official sources, then exactly5checked_on fields refreshed with independent raw-byte proof. Final JSON SHA256fd9b99e55222e79792d665d08d063cc61e407ef770595bcac5700a7f4239181e/b595bb6485e27062261b4b3713f57485a04dfeaeb1d3b179869190c3e112c3be. Installedcontenttests9pass/5skipactual0; bothschema/lint0. READONLY DBsource rows onlyzhTW, currentdraft=publicv4/v8. Actualplan_importreadonlyexit0:2updates/2publishtrue/0taxonomychanges/0creates/0otherlocales/noholds. No apply or publication. See portable receipt for pinned versions/public hashes; approval, deployed assets, action-time dry-run and public verification still required.
