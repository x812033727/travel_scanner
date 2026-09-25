---
id: 2026-09-25-video-auto-rollout-pair-the-worker
title: Video auto rollout: pair the worker, start the video profile on deploy, run the first automatic draft
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-25T07:38:52Z
completed_at:
branch:
depends_on:
  - 2026-09-25-video-auto-settings-models-schedule-video
  - 2026-09-25-video-auto-model-runner-the-server
  - 2026-09-25-video-auto-orchestrator-one-command-that
  - 2026-09-25-video-auto-worker-image-node-chromium
scope:
  - docs/videos/AUTOMATION.md
---

# Video auto rollout: pair the worker, start the video profile on deploy, run the first automatic draft

## Why

前四張做完之後，要在正式站把工人跑起來。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [ ] 部署腳本加 `--profile video`（改主機腳本要站主同意，備份舊版）。
- [ ] 工人配對成功（站主在後台按「允許」）。
- [ ] 站主在設定分頁開啟，第一支自動草稿送到「選大綱」。
- [ ] 實際的 token 用量、耗時記進 `docs/videos/AUTOMATION.md`。

## Steps

- [ ] 部署前唯讀預檢；部署；驗證工人容器。
- [ ] 第一支跑完後檢討提示詞與預設值。

## How to verify

/admin/videos 出現一支由工人產生的草稿，設定分頁顯示本月用量。
