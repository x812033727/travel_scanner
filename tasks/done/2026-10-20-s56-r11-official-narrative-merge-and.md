---
id: 2026-10-20-s56-r11-official-narrative-merge-and
title: S56 R11 official narrative merge and policy gate
status: done
priority: P2
area: docs
owner: codex-s56-r11-merge-policy
claimed_at: 2026-10-20T22:52:38Z
created_at: 2026-10-20T22:52:36Z
completed_at: 2026-10-20T22:54:53Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/review/r11-merge-policy
---

# S56 R11 official narrative merge and policy gate

## Why

R11 獨立來源已通過，兩位只讀劇本的盲讀者各自凍結原票；在語音開工前，須用固定 OR 規則正式合併並對同一版全文跑政策判定。

## Definition of done

- [x] 核五檔凍結雜湊、來源 PASS、兩票綁定；保存有異議的正式合併回條。
- [x] 正式敘事 CLI 13／13 PASS；一次 Jev 完整政策請求 PASS，保存去憑證原樣回條。

## Steps

- [x] A 在 `no_recap` 投否、B 全是；用 `mergePanelVerdicts` 原規則合併，不改原票或作者稿。
- [x] 以官方 CLI 驗合併答案，再向已登記為 `explainer`／`drama` 的站台送唯一一次 R11 政策請求。

## How to verify

`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s56 --answers /workspace/travel_scanner/docs/videos/curio-s56/review/r11-merge-policy/merged-answers.json --json` 退出 0；原樣回條見 [summary](../../docs/videos/curio-s56/review/r11-merge-policy/summary.md)。另以 `node tools/video/cli.mjs lint --slug curio-s56 --json`、`npm run check:tasks` 查本凍結版與任務。

## Notes

R11 精確版史料、敘事及政策 PASS；本票沒有 TTS、插圖、配樂或網站站主核准。A 的 `s56036` 高架街段重述疑慮已保留，剪輯聽感可再注意；R6 舊音檔仍是 HOLD，不能沿用。
