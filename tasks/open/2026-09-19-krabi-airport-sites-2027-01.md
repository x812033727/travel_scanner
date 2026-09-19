---
id: 2026-09-19-krabi-airport-sites-2027-01
title: krabi-airport-transport-where-to-stay 2027-01-31 前重試喀比機場官網與 บขส.；Grab 上車區與 Tubkaek 目錄變動時跟改
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
  - apps/api/app/guides/content/krabi-airport-transport-where-to-stay.json
  - apps/web/public/guides/krabi-airport-transport-where-to-stay
---

# krabi-airport-transport-where-to-stay 2027-01-31 前重試喀比機場官網與 บขส.；Grab 上車區與 Tubkaek 目錄變動時跟改

## Why

`krabi-airport-transport-where-to-stay` 撰稿時喀比機場官網（krabi.airports.go.th、minisite.airports.go.th/krabi、www.airports.go.th）與 บขส.（transport.co.th）都讀不到，機場巴士票價與時段、計程車櫃台固定價、普吉⇄喀比巴士都寫「以現場為準」。規格 `docs/travel-guides-batch-7/krabi-airport-transport-where-to-stay.md`「上線後與交叉檢查」要求上線 PR 同時開票，2027-01-31 以前再試一次。

## Definition of done

- [ ] 2027-01-31 以前重試上述四個站；讀得到就把機場巴士票價與時段、計程車櫃台固定價、普吉⇄喀比巴士補進 H2-2 與 H2-5，「以現場為準」改成實際數字；仍讀不到就在本票記下查核日期。
- [ ] Grab 若公告喀比機場設官方上車區（目前 Inside Grab 只有普吉、清邁）：H2-2 與 H3 的寫法改掉，並與 `phuket-airport-transport-where-to-stay` 的口徑對齊。
- [ ] 目錄若把 Tubkaek 加進喀比 areas：本文分區表與 diagram-1 的標籤一起更新。
- [ ] 每次改動更新 `checked_on`，lint 通過。

## Steps

- [ ] **2027-01-31 以前**：再試 krabi.airports.go.th、minisite.airports.go.th/krabi、www.airports.go.th 與 transport.co.th；補數字或記下日期。
- [ ] **Grab 公告變動時**：改 H2-2 與 H3。
- [ ] **目錄變動時**（`apps/api/app/destinations/catalog.py`、`apps/api/app/foods/area_catalog.py`、`apps/api/app/hotspots/areas.py` 目前是「奧南、喀比鎮、萊雷、克隆芒」）：改分區表與 diagram-1 標籤；萊雷改名的話 `krabi-ao-nang-railay-4-islands` 的地名、`aliases` 與圖要一起改（那篇不在本票 scope，屆時補進）。
- [ ] 跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug krabi-airport-transport-where-to-stay
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `krabi-airport-transport-where-to-stay` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/krabi-airport-transport-where-to-stay` 看 H2-2 與 H2-5。

## Notes

- 來源：`docs/travel-guides-batch-7/krabi-airport-transport-where-to-stay.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 渡輪班表的旺季複查在 `2026-09-19-andaman-ferry-recheck-2026-11`（與喀比跳島篇、普吉跳島篇同一張票）。
- 與 `krabi-ao-nang-railay-4-islands` 共用的數字（機場到奧南約 50 分、奧南到萊雷長尾船約 30 分、喀比⇄皮皮 450／350 與 09:00、13:00）任何一篇改，同一個 PR 改另一篇。
- `tasks/BOARD.md` 不要提交。
