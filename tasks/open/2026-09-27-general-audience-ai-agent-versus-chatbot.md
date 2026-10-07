---
id: 2026-09-27-general-audience-ai-agent-versus-chatbot
title: General audience AI agent versus chatbot video
status: review
priority: P2
area: docs
owner: codex-ai-agent-continuation
claimed_at: 2026-10-07T11:09:17Z
created_at: 2026-09-27T15:25:59Z
completed_at:
branch: codex/ai-agent-continuation-20261007
depends_on: []
scope:
  - docs/videos/ai-agent-vs-chatbot
---

# General audience AI agent versus chatbot video

## Why

觀眾常把聊天回答、固定流程與會依工具結果調整的代理混為一談。用公開、無個資的台北半日行程案例示範差別，並交付可製作的影片文字包。

## Definition of done

- [x] 8–12 分鐘繁中影片、縮圖與五語字幕通過產線檢查，完整上傳包可交站主。
- [x] 示範來源、實際執行紀錄與意見分清楚，獨立查核完成。

## Steps

- [x] 查重、查官方資料，取得可回查的實際行程決策證據。
- [x] 完成 brief、video.json、claims 與查核交接。
- [x] 完成聲音、畫面、字幕、品管與上傳包。

## How to verify

`node tools/video/cli.mjs lint --slug ai-agent-vs-chatbot`；成片再跑 `qa`、`package`、人工逐段檢查。

## Notes

2026-09-27 已查國立臺灣博物館官網：例行週一休館，但 2026-09-28 教師節特別開館；這是示範「依工具回饋改變決策」的實際資料。遠端未合併的 `claude/video-batch-2` 有 `ai-agent-permissions`，主題是安全權限，不重複本片。

文字包在 `docs/videos/ai-agent-vs-chatbot/`。`lint` 0 錯 0 警、預估 10.4 分鐘（142 句）；四語 `.todo.json` 已生成於 repo 外 `C:\Users\x8120\mokaair-work\videos\ai-agent-vs-chatbot\i18n\`。獨立 `verify-1.md`、大綱核准、翻譯審稿、TTS、成片及上傳包仍未完成；`status` 逐項顯示缺口。臺北市觀光局頁面 403，已改用臺博館可開的本館地址頁。
2026-09-28：獨立查核、Gemini Sulafat 旁白、五語字幕與 1080p 成片完成；`check-audio` 142/142 句、零標記，成片 18,435 影格、約 10:14、-14 LUFS，`lint` 零錯誤零警告。站主大綱核准、正式站審核、11 項品管及待上架包仍待完成。

2026-09-27 獨立查核寫入 `verify-1.md`，更正 `video.json.sources` 和 `claims.md` 原本誤指南門館 `n=5459` 的來源連結為本館 `n=5445`。`brief.md` 與 `demo-log.md` 的同一舊連結待撰稿者同步；開館日等旁白事實通過查核，`lint` 重跑仍為 0 錯 0 警。畫面渲染正在跑，音訊、字幕和上架包仍未完成。
2026-09-28：舊來源連結已同步修正。五語字幕經獨立交叉審稿並重新合併；繁中旁白 10:18，五語 SRT 無速度警告。36 張字卡與縮圖已目視檢查，1080p 組裝中。大綱、旁白與成片審核及上架包仍待完成。
2026-09-28：旁白逐句檢查初次標記 17 句；兩輪局部重錄後餘 6 句，已改寫歧義語句、獨立覆核四語翻譯並重新合成。最新 check-audio 142/142 已檢查、0 flagged；旁白約 10:14，五語字幕無速度警告。成片正在按新音軌重組。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-video-review (since 2026-09-27T15:47:54Z) was stale and is released so it stops locking its scope. Landed: #867. Still open: 8–12 min video, thumbnail and five-language subtitles pass the pipeline; full upload package handed to owner; Finish audio, visuals, subtitles, QA and upload package (render done; owner outline approval, prod review, 11-.


2026-10-07 continuation：新繁中成片 1080p／約10:30，142句 native音訊QA zero flags，84逐步字卡／縮圖、五語718cues、當前來源查核metadata、11/11 QA與4/4基本上傳包全部完成。source SHA `6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235`，movie SHA `6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9`；outline/audio/final/publish正式審核皆相同artifact SHA，audio/final/publish依既有設定自動核准。完整 evidence見同scope的continuation/caption/visual/offline-audio review及verify-3。基本包在repo外`<home>/mokaair-work/ai-agent-continuation-20261007/media/ai-agent-vs-chatbot/upload/`，Studio步驟在UPLOAD.md。

13:30:52 UTC新儲存EN/JA/KO配音加CC/metadata、zh-CN CC/metadata選擇；基本包已完成但新配音尚需fit/QA/languages package。13:32 GET YouTube ID null、ready_to_upload=false；沒有站主全片聽音／播放器驗收或YouTube上傳／發布。任務狀態review等draft PR，未合併／部署；其他影片unknown／STOP／hold原樣保留。Windows confirmed-answer恢復工具缺口另已開P2票，沒有宣稱已修復原生工具。
