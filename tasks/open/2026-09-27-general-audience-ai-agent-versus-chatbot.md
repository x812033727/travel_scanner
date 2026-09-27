---
id: 2026-09-27-general-audience-ai-agent-versus-chatbot
title: General audience AI agent versus chatbot video
status: in-progress
priority: P2
area: docs
owner: codex-video-review
claimed_at: 2026-09-27T15:47:54Z
created_at: 2026-09-27T15:25:59Z
completed_at:
branch: codex/ai-general-videos
depends_on: []
scope:
  - docs/videos/ai-agent-vs-chatbot
---

# General audience AI agent versus chatbot video

## Why

觀眾常把聊天回答、固定流程與會依工具結果調整的代理混為一談。用公開、無個資的台北半日行程案例示範差別，並交付可製作的影片文字包。

## Definition of done

- [ ] 8–12 分鐘繁中影片、縮圖與五語字幕通過產線檢查，完整上傳包可交站主。
- [x] 示範來源、實際執行紀錄與意見分清楚，獨立查核完成。

## Steps

- [x] 查重、查官方資料，取得可回查的實際行程決策證據。
- [x] 完成 brief、video.json、claims 與查核交接。
- [ ] 完成聲音、畫面、字幕、品管與上傳包。

## How to verify

`node tools/video/cli.mjs lint --slug ai-agent-vs-chatbot`；成片再跑 `qa`、`package`、人工逐段檢查。

## Notes

2026-09-27 已查國立臺灣博物館官網：例行週一休館，但 2026-09-28 教師節特別開館；這是示範「依工具回饋改變決策」的實際資料。遠端未合併的 `claude/video-batch-2` 有 `ai-agent-permissions`，主題是安全權限，不重複本片。

文字包在 `docs/videos/ai-agent-vs-chatbot/`。`lint` 0 錯 0 警、預估 10.4 分鐘（142 句）；四語 `.todo.json` 已生成於 repo 外 `C:\Users\x8120\mokaair-work\videos\ai-agent-vs-chatbot\i18n\`。獨立 `verify-1.md`、大綱核准、翻譯審稿、TTS、成片及上傳包仍未完成；`status` 逐項顯示缺口。臺北市觀光局頁面 403，已改用臺博館可開的本館地址頁。

2026-09-27 獨立查核寫入 `verify-1.md`，更正 `video.json.sources` 和 `claims.md` 原本誤指南門館 `n=5459` 的來源連結為本館 `n=5445`。`brief.md` 與 `demo-log.md` 的同一舊連結待撰稿者同步；開館日等旁白事實通過查核，`lint` 重跑仍為 0 錯 0 警。畫面渲染正在跑，音訊、字幕和上架包仍未完成。
2026-09-28：舊來源連結已同步修正。五語字幕經獨立交叉審稿並重新合併；繁中旁白 10:18，五語 SRT 無速度警告。36 張字卡與縮圖已目視檢查，1080p 組裝中。大綱、旁白與成片審核及上架包仍待完成。
