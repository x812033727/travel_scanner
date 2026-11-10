---
id: 2026-10-21-s59-r10-media-readiness
title: S59 R10 owner cards and bounded TTS
status: in-progress
priority: P2
area: docs
owner: s59-media-readiness
claimed_at: 2026-10-21T01:31:43Z
created_at: 2026-10-21T01:31:41Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s59/review/r10-media-readiness
---

# S59 R10 owner cards and bounded TTS

## Why

S59 R10 已通過史料與雙讀者文字關卡，需要讓站台看到同一版企劃與劇本，記錄受使用者委託的本地推薦決定，並在成本上限內試做旁白及技術音檢。

## Definition of done

- [ ] 站台大綱／劇本待審卡、本地精確雜湊決定、Jev 全稿政策、首輪語音和音檢都有可稽核收據，無創意檔漂移。

## Steps

- [x] 站台提交、Jev 政策一次判定與本地委派決定封存。
- [x] 語音乾跑及一次首輪上限計畫封存。
- [x] 首輪 TTS 後核字元、110 份音檔／時間軸及來源稿雜湊；12:31.87 旁白、3,182 計費字元。
- [x] 做一次全篇技術音檢並保留原始 31 旗標，不把文字轉寫差異當作已聽證的錯音。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s59 --json`、`node tools/video/cli.mjs tts --slug curio-s59 --dry-run`、站台 `review-push`／`review-pull` 回條、`node tools/video/cli.mjs check-audio --slug curio-s59`、`npm run check:tasks`。

## Notes

R10 五檔與正式合票見 `docs/videos/curio-s59/review/r10-merge-policy/summary.md`。網站卡 pending；本機兩筆決定不聲稱站主親審。Jev 全稿政策一次 PASS；Gemini Sulafat 首輪乾跑 110 次／3,182 字元，上限 US$0.25，零重配。

2026-10-22 首輪 TTS 與音檢已完結，見[原始媒體回條](../../docs/videos/curio-s59/review/r10-media-readiness/summary.md)及[音檢分流](../../docs/videos/curio-s59/review/r10-media-readiness/first-pass-audio-triage-20261022.md)。`check-audio` 110/110 有 heard 文字、31 旗標、退出碼 1；無重配，也無真人聽審或網站 audio 卡核准。優先核 `s59092`、`s59101` 等機器辨識出重大異義的句子，確認實際 WAV 才決定逐句補錄；音訊關 HOLD。私有 STOP 已建立，圖片／配樂／成片未開畫。
