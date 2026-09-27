---
id: 2026-09-27-general-audience-ai-citation-checking-video
title: General audience AI citation checking video
status: in-progress
priority: P2
area: docs
owner: codex-videos-general
claimed_at: 2026-09-27T15:27:01Z
created_at: 2026-09-27T15:26:42Z
completed_at:
branch: codex/ai-general-videos
depends_on: []
scope:
  - docs/videos/ai-citation-check
---

# General audience AI citation checking video

## Why

有連結的 AI 回答仍可能把來源說反。以明確標示的錯誤示意回答，逐步核對 Anthropic 官方原文，教一般觀眾檢查引用。

## Definition of done

- [ ] 8–12 分鐘繁中影片、縮圖與五語字幕通過產線檢查，完整上傳包可交站主。
- [ ] 示意回答與真實來源清楚標示，獨立查核完成。

## Steps

- [x] 查重並打開官方來源，建立可回查的三步查核示範。
- [x] 完成 brief、video.json、claims 與查核交接。
- [ ] 完成聲音、畫面、字幕、品管與上傳包。

## How to verify

`node tools/video/cli.mjs lint --slug ai-citation-check`；成片再跑 `qa`、`package`、人工逐段檢查。

## Notes

示範錯誤句是編輯刻意製作，不宣稱為真實模型輸出。2026-09-27 已打開 Anthropic 官方 Reduce hallucinations 頁與 Building effective agents 頁。前者要求引用能回查，並說這些方法不能完全消除錯誤。

文字包在 `docs/videos/ai-citation-check/`。`lint` 0 錯 0 警、預估 9.9 分鐘（143 句）；四語 `.todo.json` 已生成於 repo 外 `C:\Users\x8120\mokaair-work\videos\ai-citation-check\i18n\`。獨立 `verify-1.md`、大綱核准、翻譯審稿、TTS、成片及上傳包仍未完成；`status` 逐項顯示缺口。
