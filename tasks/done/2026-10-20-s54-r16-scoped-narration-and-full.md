---
id: 2026-10-20-s54-r16-scoped-narration-and-full
title: S54 R16 scoped narration and full audio gate
status: done
priority: P2
area: docs
owner: codex-root-s54-r16-audio
claimed_at: 2026-10-20T23:11:50Z
created_at: 2026-10-20T23:11:47Z
completed_at: 2026-10-20T23:15:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r16-audio-gate
  - docs/videos/curio-s54/verify-16.md
---

# S54 R16 scoped narration and full audio gate

## Why

R15 兩輪定點重錄後仍有兩句音訊旗標。R16 已對同版通過史料、雙盲合併及政策關卡，須重新合成兩句並全片驗證。

## Definition of done

- [x] 僅合成 R16 改寫的兩句，保存完整 TTS 回條及前後 WAV SHA-256 清單。
- [x] 148 句全部音檢並保存原樣回條、timeline、PASS／HOLD 及站台審核狀態。

## Steps

- [x] 精確五檔、獨立來源、正式敘事及 Jev 政策前置關卡均 PASS。
- [x] 2 新請求／50 計費字元，144 快取；只變更 `s54002`、`s54013` 兩個 WAV。
- [x] 全片音檢 148／148、0 旗標；站台大綱／音訊卡已送出，均 pending。

## How to verify

核對 `docs/videos/curio-s54/review/r16-audio-gate/summary.md` 及原樣回條；執行 `npm run test:docs-videos`、`npm run check:tasks` 與 `git diff --check`。

## Notes

本地機器音訊 PASS，不是人耳或站台核准；圖片 judge 與配樂額度耗盡，影片未組片。
