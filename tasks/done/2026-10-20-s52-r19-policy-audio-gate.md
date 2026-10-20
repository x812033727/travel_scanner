---
id: 2026-10-20-s52-r19-policy-audio-gate
title: S52 R19 policy and full audio gate
status: done
priority: P1
area: docs
owner: codex-gpt6-s52-r19-audio
claimed_at: 2026-10-20T21:47:10Z
created_at: 2026-10-20T21:47:08Z
completed_at: 2026-10-20T21:53:37Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s52/review/r19-policy
  - docs/videos/curio-s52/review/r19-audio
  - docs/videos/curio-s52/verify-19.md
---

# S52 R19 policy and full audio gate

## Why

S52 R19 已有精確五檔的獨立史料／書面畫面 PASS，以及真正無歷史脈絡的雙盲 OR 敘事 PASS。需要把政策與音訊檢查重新綁到 R19，不能沿用 R16 的舊政策、WAV 或音檢。

## Definition of done

- [x] 現稿 Jev 解說政策與正式敘事 CLI 均 PASS，保留精確輸入雜湊與原樣回覆。
- [x] 只對不在同文快取的 R19 語音付費合成，全篇 115 句正式音檢；旗標最多兩輪定點重配，保留每輪原始旗標。
- [x] 記錄實測開場／正文／片尾時長、WAV／timeline 雜湊與仍需人工聽審／網站核准的界線。

## Steps

- [x] 先核對五檔雜湊及 R19 盲讀，再重跑 `narrative --answers`。
- [x] `review-push --report-only` 同步站台分類，只送一次現稿 `policyRequest({doc,brief})`。
- [x] `tts --dry-run` → Gemini Sulafat TTS：13 新／100 快取。
- [x] 全篇音檢：初輪兩旗標，只對 `s52005`、`s52090` 重配一次，再全篇音檢 0 旗標。
- [x] 寫政策、語音及總驗證回條，保留兩輪原始旗標。

## How to verify

在 `/workspace/travel_scanner` 執行 `VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs narrative --slug curio-s52 --answers docs/videos/curio-s52/review/r19-clean-merged-answers.json --json`、`tts --slug curio-s52 --dry-run`、`check-audio --slug curio-s52`。當前音檢退出碼 0，115／115、0 旗標。原始證據與精確 SHA 見 `docs/videos/curio-s52/review/r19-policy.md`、`r19-audio.md`、`docs/videos/curio-s52/verify-19.md`。

## Notes

首次全檢兩旗標；一次定點重配後歸零，沒有觸及兩輪上限。未聲稱人工聽音、站主網站核准或完成影片。月額度仍擋住圖片評審／配樂；後續請從精確 R19 語音與文字收據接續，勿改動本稿而沿用其審核。
