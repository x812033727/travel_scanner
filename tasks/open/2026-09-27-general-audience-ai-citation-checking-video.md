---
id: 2026-09-27-general-audience-ai-citation-checking-video
title: General audience AI citation checking video
status: in-progress
priority: P2
area: docs
owner: codex-video-review
claimed_at: 2026-09-27T15:48:03Z
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
- [x] 示意回答與真實來源清楚標示，獨立查核完成。

## Steps

- [x] 查重並打開官方來源，建立可回查的三步查核示範。
- [x] 完成 brief、video.json、claims 與查核交接。
- [ ] 完成聲音、畫面、字幕、品管與上傳包。

## How to verify

`node tools/video/cli.mjs lint --slug ai-citation-check`；成片再跑 `qa`、`package`、人工逐段檢查。

## Notes

示範錯誤句是編輯刻意製作，不宣稱為真實模型輸出。2026-09-27 已打開 Anthropic 官方 Reduce hallucinations 頁與 Building effective agents 頁。前者要求引用能回查，並說這些方法不能完全消除錯誤。

文字包在 `docs/videos/ai-citation-check/`。`lint` 0 錯 0 警、預估 9.9 分鐘（143 句）；四語 `.todo.json` 已生成於 repo 外 `C:\Users\x8120\mokaair-work\videos\ai-citation-check\i18n\`。獨立 `verify-1.md`、大綱核准、翻譯審稿、TTS、成片及上傳包仍未完成；`status` 逐項顯示缺口。

2026-09-27 獨立查核已寫入 `verify-1.md`：Anthropic 官方文件現頁 HTTP 200，必要短引文、限制與示意標示一致；`lint` 重跑為 0 錯 0 警。音訊、畫面、字幕與上架包仍待完成。
2026-09-28：五語字幕經獨立交叉審稿；兩句顯示過快的英、日文字幕已縮短，五語 SRT 無速度警告。繁中旁白 10:22；36 張字卡與縮圖已目視檢查。成片、品管、審核與上架包仍待完成。
2026-09-28：改寫五句並同步五語字幕，獨立覆核後重錄；`check-audio` 143/143 句、零標記。新版成片 18,749 影格、約 10:24、-14 LUFS，`lint` 零錯誤零警告。站主大綱核准、正式站審核、11 項品管及待上架包仍待完成。
