---
id: 2026-09-23-catchtable-29-no-official-source-merchant
title: CatchTable 平台層級批次：兩批 29 家 no_official_source 依 merchant_platform 重判、匯入、公開
status: done
priority: P2
area: ops
owner: claude-fable-5-1
claimed_at: 2026-09-23T10:52:47Z
created_at: 2026-09-23T10:52:44Z
completed_at: 2026-09-23T12:13:36Z
branch: claude/catchtable-platform-tier
depends_on: []
scope:
  - apps/api/app/foods/data/catchtable/2026-09-23-catchtable-platform-tier
  - docs/catalog-content-reviews/catchtable-platform-tier.md
---

# CatchTable 平台層級批次：兩批 29 家 no_official_source 依 merchant_platform 重判、匯入、公開

## Why

CatchTable 兩批（首爾最佳榜 1–40、候位榜 1–10、釜山最佳榜 1–20）有 29 家找不到官網或觀光局頁（第一批 15、第二批 14），停在候選檔的
`no_official_source`。站主 2026-09-23 決定開較弱來源層級 `merchant_platform`（票 `2026-09-23-merchant-platform`，PR #686）：店家自己登記的
CatchTable 店頁／`/info` 分頁、或它「網站」欄指向的社群帳號可當來源，公開頁標「平台／社群登記」。這張票把 29 家依新規則重判、建店家、
套用平台列，再照第 7 步（座標、站主貼 Naver 短網址、核准）公開。

## Definition of done

- [x] `apps/api/app/foods/data/catchtable/2026-09-23-catchtable-platform-tier/`：`rankings.json`（沿用兩批的擷取證據）、`candidates-seoul.json`（20 筆）、
      `candidates-busan.json`（9 筆）、兩個城市的 `merchants-*.json` 與 `platform-reviews-*.json`；每筆 `import` 的來源是這家的 `/info` 分頁（`merchant_platform`），
      引文含韓文店名與道路名地址，`catchtable.website` 照抄「網站」欄。
- [x] 複核抽三分之一；轉檔 `--check` 零錯誤；正式站部署到含 migration 0083 之後才 `--apply`。
- [x] 第 7 步：座標（同 skill 的順序）、站主貼 Naver 短網址、後台核准；公開 API 前後計數與每家去向寫進報告 `docs/catalog-content-reviews/catchtable-platform-tier.md`。

## Steps

- [x] 從兩批候選檔抓出 29 筆，先產草稿記錄（訂位判定與榜單證據沿用），研究代理只補 `/info` 的現況、網站欄、引文、分類、商圈、英文名。
- [x] 複核 → 合併 → 轉檔 → PR 一（候選檔、店家匯入檔、報告初稿）。
- [x] 等 PR #686 部署（`alembic current` 0083）→ stdin dry-run／apply → worklist → 平台列 → PR 二。
- [x] 座標代理 → 站主貼 Naver → 後台逐家儲存 → 公開 API 驗證 → 報告 → `done`。

## How to verify

```bash
python tools/catchtable_build_batches.py --candidates apps/api/app/foods/data/catchtable/2026-09-23-catchtable-platform-tier/candidates-seoul.json --check
python tools/catchtable_build_batches.py --candidates apps/api/app/foods/data/catchtable/2026-09-23-catchtable-platform-tier/candidates-busan.json --check
```

## Notes

- 第一批候位榜的 5 家（아티스트베이커리 안국、조조칼국수 성수점、부촌육회 별관、스탠다드브레드 성수점、무구옥 성수점）是候位制，平台列會存 disabled；
  站主要的是訂位連結，這 5 家進目錄但沒有按鈕，報告要分開算。
- 轉檔腳本的責任鏈：`merchant_platform` 的網址只能是這個 alias 的 CatchTable 店頁／`/info`，或等於 `catchtable.website`；統一用 `/info`（地址在頁上看得到）。
- 2026-09-23：29 筆重判完成（複核 11 筆全同意）、PR #688；部署 0083 後 stdin 套用：店家 created 20／9，平台列 created 20（verified 15、disabled 5）／9；29 個 Naver id 已解出（27 站主貼、2 店家登記）。
- 2026-09-23 第 7 步完成：OSM 座標 18/29、Naver 29/29（27 站主貼＋2 店家登記），18 家公開（首爾 54→69、釜山 24→27），11 家缺座標維持 pending；細節在報告「後台操作紀錄」。
