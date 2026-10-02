---
id: 2026-10-02-sothatswhy-intro-approval
title: Record approved So Thats Why series intro
status: done
priority: P2
area: docs
owner: codex-sothatswhy-intro
claimed_at: 2026-10-02T13:39:47Z
created_at: 2026-10-02T13:39:42Z
completed_at: 2026-10-02T13:45:31Z
branch: codex/sothatswhy-intro-approval-20261002
depends_on: []
scope:
  - docs/videos/branding-release/2026-10-02-sothatswhy-intro-approval.md
---

# Record approved So Thats Why series intro

## Why

站主已選定 6.9 秒穿插版作為原來如此系列片頭。保存可核對的素材選用紀錄與剪輯包，避免後續誤用舊版或把系列片頭套到所有影片。

## Definition of done

- [x] 定案素材複本、SHA-256、站主原話與剪輯順序保存於 git 外素材包。
- [x] 文件明確區分素材選用、正式產線接入與單支影片核准。
- [x] 未完成的系列預設接入已建立獨立待辦。

## Steps

- [x] 封存原開場加系列段落 11.9 秒、獨立系列段落 6.9 秒與原片尾。
- [x] 使用既有素材驗證器 dry-run，保留來源雜湊與驗證紀錄。
- [x] 撰寫 docs/videos/branding-release/2026-10-02-sothatswhy-intro-approval.md。

## How to verify

`node tools/tasks.mjs check`、`git diff --check`。
外部工作目錄的 `finalize-approved.mjs` 使用 `installPackage(..., dryRun: true)` 驗證素材；結果位於 `approved/package-verification.json`。

## Notes

站主原話：「好 當作原來如此系列的開頭影片」。6.9 秒版本保留 14 個國家／地區、7 男聲與 7 女聲、加速穿插字卡與配樂。全頻道品牌預設尚無系列路由；後續工作為 2026-10-02-sothatswhy-series-branding-default。本次只完成素材封存及文件，沒有正式安裝或影片上架。
