---
id: 2026-09-19-andaman-ferry-recheck-2026-11
title: 2026 年 10 到 12 月旺季前複查 Andaman Wave Master 班表：krabi 兩篇與 phuket 跳島篇同一張票，附斯米蘭開放日
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:40Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/krabi-airport-transport-where-to-stay.json
  - apps/web/public/guides/krabi-airport-transport-where-to-stay
  - apps/api/app/guides/content/krabi-ao-nang-railay-4-islands.json
  - apps/web/public/guides/krabi-ao-nang-railay-4-islands
  - apps/api/app/guides/content/phuket-phi-phi-james-bond-island-hopping.json
  - apps/web/public/guides/phuket-phi-phi-james-bond-island-hopping
---

# 2026 年 10 到 12 月旺季前複查 Andaman Wave Master 班表：krabi 兩篇與 phuket 跳島篇同一張票，附斯米蘭開放日

## Why

喀比兩篇與普吉跳島篇的渡輪班次與票價都來自 Andaman Wave Master 與 Tigerline 的頁面（喀比 Klong Jilad⇄皮皮 09:00／13:00 去、10:30／15:30 回、450／350；普吉⇄皮皮 08:30／13:45 去、11:00／14:30 回、700 起），旺季班表常變。規格 `docs/travel-guides-batch-7/krabi-airport-transport-where-to-stay.md` 要求 2026-12-01 上線 PR 開票並寫明日期，`krabi-ao-nang-railay-4-islands.md` 寫明「和第 3 篇同一張票」，`phuket-phi-phi-james-bond-island-hopping.md` 要求每年 11 月旺季開始時重查同一家的兩頁；三篇共用的數字任何一篇改，同一個 PR 改另一篇。

## Definition of done

- [ ] 2026-11-01 前後：普吉篇的 Andaman Wave Master 兩頁班表與票價核對完（08:30／13:45 去、11:00／14:30 回、700 起），有變就改正文、summary 與圖。
- [ ] 2026-12-01：喀比交通篇 H2-5 表格、summary 與 FAQ 第 3 題三處一致；喀比跳島篇的正文、summary、FAQ 與 diagram-1 同 PR 對齊；13:00 那班的時數欄看過有沒有補上。
- [ ] 每次改動更新 `checked_on`，lint 通過（圖上的數字都在正文）。做完這一季就 done，下一年度另開票。

## Steps

- [ ] **2026-11 旺季開始時（普吉篇）**：重查 Andaman Wave Master 的 `/ferry/phuket-to-phiphi/` 與 `/ferry/phiphi-to-phuket/`；有變就改 `phuket-phi-phi-james-bond-island-hopping` 的正文、summary 與 diagram-1。
- [ ] **2026-12-01（喀比兩篇）**：重看 Andaman Wave Master 四個頁面（`/ferry/phuket-to-phiphi/`、`/ferry/phiphi-to-krabi/`、`/ferry/krabi-to-phiphi/`、`/ferry/phiphi-to-phuket/`）、航線總表與 Tigerline 首頁。有變同時改 `krabi-airport-transport-where-to-stay` 的 H2-5 表格、summary 與 FAQ 第 3 題（三處必須一致），以及 `krabi-ao-nang-railay-4-islands` 的正文、summary、FAQ 與 diagram-1；順便看 13:00 那班的時數欄有沒有補上。
- [ ] **2026-10-15 前後（可選）**：DNP 或 TAT 若公告 2026–27 季斯米蘭實際開放日，在普吉篇 H2-4 補一句「本季 X 月 X 日開放」，並記得 2027 年 5 月拿掉（記進 `2026-09-19-dnp-park-closures-2027-01-15` 的 Notes）。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug krabi-airport-transport-where-to-stay --slug krabi-ao-nang-railay-4-islands --slug phuket-phi-phi-james-bond-island-hopping
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出改過的 slug 為 `update`，再 `--publish`；三篇的皮皮渡輪班次與票價逐字相同。

## Notes

- 來源：`docs/travel-guides-batch-7/krabi-airport-transport-where-to-stay.md`、`krabi-ao-nang-railay-4-islands.md`、`phuket-phi-phi-james-bond-island-hopping.md` 的「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 喀比交通篇的 diagram-1 只畫哪幾段只能搭船、沒有時刻，通常不必改；列進 scope 是因為喀比跳島篇的規格把「diagram-1」寫在兩篇共同的那句裡。
- 國家公園封園日期與 DNP 門票的 2027-01-15 複查在 `2026-09-19-dnp-park-closures-2027-01-15`；喀比機場官網重試在 `2026-09-19-krabi-airport-sites-2027-01`。
- 反向連結（`phuket-airport-transport-where-to-stay` H2-5、`thailand-esim-sim-wifi`）在「既有文章補連第七批」那張票。`tasks/BOARD.md` 不要提交。
