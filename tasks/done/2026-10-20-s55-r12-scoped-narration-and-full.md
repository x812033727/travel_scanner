---
id: 2026-10-20-s55-r12-scoped-narration-and-full
title: S55 R12 scoped narration and full audio gate
status: done
priority: P2
area: docs
owner: codex-root-s55-audio
claimed_at: 2026-10-20T22:54:14Z
created_at: 2026-10-20T22:54:11Z
completed_at: 2026-10-20T23:05:13Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s55/review/r12-audio-gate
  - docs/videos/curio-s55/verify-12.md
---

# S55 R12 scoped narration and full audio gate

## Why

S55 R10 旁白經兩輪重錄後仍有 14 句機器旗標。R11/R12 作者修改了口說並經精確版獨立來源、雙盲合併和政策 PASS；須重新合成變更句、全量音檢與限縮重錄，讓新版有自己的真實結果。

## Definition of done

- [x] 只在 R12 三道前置關卡通過後使用 Gemini Sulafat 合成與音檢。
- [x] 對 140 句完整音檢；僅重錄旗標句，最多兩輪並核對 WAV 範圍。
- [x] 封存原樣回條、精確版雜湊及 PASS／HOLD，不將 R10 音檔當 R12 PASS。

## Steps

- [x] 13 新請求／344 字元、116 快取，首次 2 旗標。
- [x] 僅 `s55016`／`s55112` 各重錄兩輪；每輪兩個 WAV 變動，完整複檢 2 → 0。
- [x] 保存 140 個 WAV 前後雜湊、全量檢查及 13:09 timeline，回報機器音訊 PASS。

## How to verify

在 `VIDEO_WORKDIR=/workspace/.video-work`、`NODE_USE_ENV_PROXY=1`、`NODE_NO_WARNINGS=1` 下執行 `node tools/video/cli.mjs tts --slug curio-s55 --dry-run`、`tts --slug curio-s55` 和 `check-audio --slug curio-s55`；限縮重錄用本票各輪 `check-flags*.json`。原樣輸出和雜湊見[回條](../../docs/videos/curio-s55/review/r12-audio-gate/summary.md)。再跑 `npm run test:docs-videos` 及 `npm run check:tasks`。

## Notes

**本地機器音訊 PASS：140／140、0 旗標**。新合成共 422 計費字元、實測 13:09；無人耳或站台音訊核准的主張。圖片與配樂受本月額度阻擋，長片及 Shorts 均未完成。
