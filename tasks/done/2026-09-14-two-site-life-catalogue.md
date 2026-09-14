---
id: 2026-09-14-two-site-life-catalogue
title: Two-site title inventory and original life editorial catalogue
status: done
priority: P2
area: docs
owner: codex-two-site-life
claimed_at: 2026-09-14T02:12:08Z
created_at: 2026-09-14T02:12:07Z
completed_at: 2026-09-14T13:02:01Z
branch:
depends_on: []
scope:
  - docs/content-research/two-site-life
  - .codex/two-site-life/qa
---

# Two-site life editorial production

## Why

Implement the approved full title inventory and all unique original article packs.

## Definition of done

- [x] All 474 title records collected and 54 archive pages checked; API-only discrepancy retained.
- [x] Complete mapping to 232 new articles, 17 covered AI topics and one site-specific recruitment exclusion.
- [x] Twelve batch tasks with exact scopes.
- [x] All 232 original article packs and images complete, reviewed, and validated.

## How to verify

Run collect.py to refresh metadata; build_catalogue.py checks coverage and slug collisions. Each batch uses guides.pack_cli ingest and scoped lint plus content-pack tests.

## Notes

The article catalogue is an assignment, not a completion report. No production import, publication, deployment, or merge is authorized by this task. Existing .codex/ files predate this work.

2026-09-14 完成：12 批合計 232/232 篇完成正文、配圖、查證、ingest、lint、464 張逐張 QA 與批次測試。全部 474 筆來源均有處理結果；最終 1,624 項檔案雜湊核對一致，新增正文共 504,295 字。交付入口 docs/content-research/two-site-life/README.md，完整驗收 delivery-audit.json。每批 9 passed、5 skipped，五項 PostgreSQL 整合測試未配置資料庫而略過；沒有正式站匯入、發布、部署或 Git 提交。
