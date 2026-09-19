---
id: 2026-09-19-vietnam-rail-recheck-2027-01
title: vietnam-domestic-flights-train-guide 2027-01-01 前後複查鐵路票價與退換票政策頁、SE1–SE8 時刻（hue 篇同 PR）、航空行李規則
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/vietnam-domestic-flights-train-guide.json
  - apps/web/public/guides/vietnam-domestic-flights-train-guide
  - apps/api/app/guides/content/hue-day-trip-from-da-nang.json
---

# vietnam-domestic-flights-train-guide 2027-01-01 前後複查鐵路票價與退換票政策頁、SE1–SE8 時刻（hue 篇同 PR）、航空行李規則

## Why

`vietnam-domestic-flights-train-guide` 的票價與退換票規則來自鐵路運輸股份公司每年換一次的政策頁（2026 年那版是 2026-01-01 發布），表三的票價是「2026 年 9 月查 9 月 20 日的 SE1」；SE1 到 SE8 的時刻也和 `hue-day-trip-from-da-nang` 共用（本篇列「到站（發車）」雙時刻，順化篇列發車時刻，括號裡的發車時刻要一模一樣）。規格 `docs/travel-guides-batch-7/vietnam-domestic-flights-train-guide.md`「上線後與交叉檢查」要求 2027-01-01 前後重查，任何一篇改時刻或說法，同一個 PR 改其他篇。

## Definition of done

- [ ] 2027-01-01 前後：48 小時加價的 7%／5%、退換票 10% 到 20%（春節 30%）、身障 30%、越南籍 60 歲 15%、夏季運輸期 5 月 20 日到 8 月 16 日與客服電話核對完；SE1 到 SE8 時刻與河內出發票價重查，有變就一起改表一、表三、summary、FAQ 與 `diagram-1.svg`，順化篇 H2-1 的發車時刻同 PR 對齊。
- [ ] 每次改票價都重查兩件事：表三的查詢日改成新的查詢日，票價是否仍「含保險與增值稅」。
- [ ] 航空行李規則：越南航空手提規則綁在 2025-05-05 的開票日，官網換了生效日或額度就改括號；Bamboo 國內線託運表格若改成合理的對應，第 (8) 條的保守寫法換成實際數字；越捷若放上 Deluxe、SkyBoss 的託運額度，補進表二。
- [ ] 每次改動更新 `checked_on`，lint 通過（圖上的數字都在正文）。做完 2027 年這一輪就 done，下一年度另開票。

## Steps

- [ ] **2027-01-01 前後**：重讀鐵路運輸股份公司的票價與退換票政策頁、giotaugiave.dsvn.vn 的統一線時刻與 eticket 票價 API（票價表單查完一次站別會跳回端點，重選再讀，見 `docs/travel-guides-batch-7/ERRATA.md`）。
- [ ] **航空公司頁**：越南航空、Bamboo、越捷的行李規則。
- [ ] **futabus.vn 之後讀得到的話**：H2-4 補上官方路線、票價與班次，並回頭看 H2-5 大叻段要不要補機場巴士；在那之前兩段維持「以各車公司官網或 App 為準」。**acv.vn／vietnamairport.vn 讀得到的話**：補蓮姜機場的官方資訊，並確認 30 公里這個數字。
- [ ] **大叻專篇（第八批）上線後**：H2-5 加一個 article inline，把「站上還沒有大叻的專篇」那句改掉，並考慮把 `related` 的第四個換成大叻篇。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug vietnam-domestic-flights-train-guide --slug hue-day-trip-from-da-nang
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出改過的 slug 為 `update`，再 `--publish`；兩篇的 SE 發車時刻逐字相同，「順化到峴港約 2 小時半到 2 小時 45 分（依班次不同）」與「票價以 dsvn.vn 當日查詢為準」三篇（含 `ha-long-bay-cruise-from-hanoi`）一致。

## Notes

- 來源：`docs/travel-guides-batch-7/vietnam-domestic-flights-train-guide.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- `ha-long-bay-cruise-from-hanoi` 只共用說法、不共用時刻，所以沒列進 scope；若改了說法，把它加進 scope 同 PR 改。
- 順化篇自己的門票法規、HĐ 觀光列車複查在 `2026-09-19-hue-recheck-2027-01`。反向連結（四篇既有越南文）在`2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批）。`tasks/BOARD.md` 不要提交。
