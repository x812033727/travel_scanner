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

2026-10-07 17:15 UTC selected-dub checkpoint（追加，保留上方歷史）：EN最新 native QA 142/142、0 flags，免費完整媒體／逐sample／current cache audit已完成，69筆實際HTTP 200／9,551合成字符收據見 `dub-review-20261007.md`。JA ordinary r1為23筆實際HTTP 200／523字符；r2原程序因本機confirmed journal rename EPERM而exit1，已保留完整ag131答案後零網路恢復，再以獨立同r2 continuation authority只派剩5句（4新請求／95字符、1既付答案reuse），17:10:53真正exit0；這不是ordinary r3。免費R2 media audit SHA `ae41af42f990bc80799697a7ea647ca5d35808ec1c0ac203b27ae431081794c6` 證明全142 current raw/cache/source、原15目標全換音且其他127 WAV byte-identical、84windows fit/max1.08及完整PCM身分；17:13:15實際native QA仍142/0unchecked/9flags，Jev accepted15與secondary cleared13，未宣稱JA完成或核准，listener改稿待實際獨審與後續收據。KO 51份原raw與ag121 held unknown request保留、未獲owner重試授權；不可當skipped或完成。當前source `6b9bb4db44c6199254c7c84e411e84618c4eeeed77e22469ed1fcb8f44c99235`／繁中movie `6e07ad6f915e35b49df565fceabe42ebee3f78821668f698b6bfc74cbeb7b9d9` 未變。selected captions/package helper僅static READY，實際新cue數、selected package QA／language review UUID及YouTube status須待fresh收據再補；13:30 owner語言選擇保留，沒有站主全片聽音／播放器驗收／上傳發布聲明。其他影片ci037 STOP／unknown及任何原生score、flag、threshold均未動。


2026-10-07 18:36 UTC selected delivery：新五語字幕712cues、五語metadata與EN完整配音已通過實際 native captions/package0、4/4及獨立來源／時序／全檔copy audit；新metadata SHA `4d1d9f57327aa1205c0abe187297e02d7ce9a1a88e77f383f4835587f74f2ce6`，publish review `285cfe5b-c0ab-4cf9-86ef-db4214b33c35`同SHA自動核准。JA真正兩輪ordinary及兩輪listener改稿後，最新142已檢查／0unchecked／1flag097；獨審與完整paid/raw/track證據完成，按DUBS正常 bounded skip，完整最佳音軌保留，未宣稱JA音訊QA或站主聽核通過。KO原51句及ag121 unknown held維持原樣，仍待站主未知計費重試決定，未跳過／完成／重送。Language review `2f2d801d-a877-473c-af00-932b8fa9f142`已實際提交pending，後台ENready／JA配音skipped／KO配音working，其餘選語metadata與CCready；YouTube ID／sync null、ready_to_upload false。完整current來源metadata、實際rounds／成本與收據見dub/caption review；maintask保持review，selected語言尚未全部完成，沒有merge／deploy／Studio上傳／發布或其他影片hold變動。
