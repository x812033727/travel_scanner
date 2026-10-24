---
id: 2026-10-20-curio-s56-r12-official-narrative-merge
title: Curio S56 R12 official narrative merge and policy gate
status: done
priority: P2
area: docs
owner: codex-s56-r12-merge-policy
claimed_at: 2026-10-20T23:16:03Z
created_at: 2026-10-20T23:16:01Z
completed_at: 2026-10-20T23:20:06Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/review/r12-merge-policy
---

# Curio S56 R12 official narrative merge and policy gate

## Why

S56 R12 已有獨立史料／書面畫面 PASS，但兩張無前情敘事盲票各有一項否決。需依工具固定雙讀者 OR 規則正式合併，若過關再對同五檔做一次 Jev 政策判定；R11 票與音訊不能代替 R12。

## Definition of done

- [x] 於 [R12 正式關卡摘要](../../docs/videos/curio-s56/review/r12-merge-policy/summary.md)保留五檔 SHA、雙讀者原票／轉寫／合併、CLI 精確版回條及唯一政策 POST 的請求與原樣回覆，分別判 PASS／HOLD。

## Steps

- [x] 原樣封存 A、B 盲票，逐題轉寫 13 項並以 `panelVerdict`、`mergePanelVerdicts` 固定 OR 規則正式合併。
- [x] 對同版執行 `narrative --answers`；正式 PASS 後預寫完整政策請求與雜湊，只送一個 `policyRequest({doc,brief})` POST，留原樣回覆與解析回條。
- [x] 驗五檔凍結、lint、敘事與政策工具測試、文件影片測試、任務格式及新檔空白。

## How to verify

`sha256sum docs/videos/curio-s56/{brief.md,research.md,claims.md,video.json,script.md}`；`node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r12-merge-policy/merged-answers.json --workdir /tmp/s56-r12-official-narrative-20261020 --json` 的**已封存一次性回條**（重跑會另增輪次，驗證時讀回條）；`node tools/video/cli.mjs lint --slug curio-s56 --json`；`node --test tools/video/core/narrative.test.mjs tools/video/qa/checks.test.mjs`；`npm run test:docs-videos`；`npm run check:tasks`。政策請求已送一次，驗證只讀 `policy-request-meta.json`、`policy-response.raw.json`、`policy-receipt.json`，不可再送。

## Notes

2026-10-20 UTC：A 否 `no_recap`、B 否 `payoffs`，固定 OR 合併 13／13 PASS；正式 CLI exit 0 且精確版綁定成立。Jev 唯一 POST HTTP 200、`passed:true`，政策 PASS。沒有改作者五檔或合成語音。R11 音檢兩旗標不能移轉，R12 全新音訊與 154／154 句全檢仍未做，STOP 仍在。
