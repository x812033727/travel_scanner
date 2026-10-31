---
id: 2026-10-20-s54-r15-scoped-narration-and-full
title: S54 R15 scoped narration and full audio gate
status: done
priority: P2
area: docs
owner: codex-root-s54-audio
claimed_at: 2026-10-20T22:51:34Z
created_at: 2026-10-20T22:51:31Z
completed_at: 2026-10-20T23:02:59Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/review/r15-audio-gate
  - docs/videos/curio-s54/verify-15.md
---

# S54 R15 scoped narration and full audio gate

## Why

S54 R14 的 148 句旁白音檢剩 17 旗標。R15 作者修 15 句後，須在同版獨立來源、雙盲合併和政策通過的條件下，重配變更句並做全量音檢，以 PASS 或明確 HOLD 交接。

## Definition of done

- [x] 精確 R15 史料、敘事、政策關卡通過後才執行 TTS。
- [x] 只對音檢旗標作至多兩輪有界重錄，每輪核對 WAV 變動範圍並全片複檢。
- [x] 原樣封存音檢、最終旗標及後續措辭交接；未過則恢復 STOP。

## Steps

- [x] 15 筆新語音／370 計費字元，131 筆快取；148 句首次音檢 7 旗標。
- [x] 7 ID 重錄／161 字元，複檢降至 3；再限縮 3 ID／68 字元，最終剩 2。
- [x] 兩輪前後 148 個 WAV 雜湊各只變動指定 ID；恢復 STOP，將 `s54002`／`s54013` 交給 R16 作者。

## How to verify

在 `VIDEO_WORKDIR=/workspace/.video-work` 且代理環境已啟用時，執行 `node tools/video/cli.mjs tts --slug curio-s54 --dry-run`、`tts --slug curio-s54` 和 `check-audio --slug curio-s54`；限縮重錄用本票保存的每輪 `check-flags*.json`。檢查原樣紀錄和雜湊見 [summary.md](../../docs/videos/curio-s54/review/r15-audio-gate/summary.md)，`npm run check:tasks` 核任務。

## Notes

**完成此音訊關卡，結果 HOLD。** R15 實測旁白 13:55，最終 2／148 旗標；兩次重錄後不再對同一稿反覆付費。未宣稱站主人耳／網站核准。R16 需處理一便士郵資的同音轉寫和什魯斯伯里地名，再重走變更版關卡。圖片、配樂、成片仍受月額度與後續審查限制。
