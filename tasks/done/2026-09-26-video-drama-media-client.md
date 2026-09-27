---
id: 2026-09-26-video-drama-media-client
title: Video drama T2: media client with cache, resumable jobs, cost ledger and QC parsers
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T05:28:27Z
created_at: 2026-09-26T01:53:30Z
completed_at: 2026-09-26T05:34:30Z
branch: claude/video-drama-media-client
depends_on:
  - 2026-09-26-video-drama-core
scope:
  - tools/video/media/client.mjs
  - tools/video/media/cache.mjs
  - tools/video/media/ledger.mjs
  - tools/video/media/qc.mjs
  - tools/video/media/cli.mjs
  - tools/video/media/media.test.mjs
---

# Video drama T2: media client with cache, resumable jobs, cost ledger and QC parsers

## Why

設定圖、關鍵影格、片段、音樂、judge 都經伺服器的 `/api/video/media/*`（S2）。這張票做工具端共用的 HTTP 用戶端（比照 `tools/video/tts/client.mjs` 的重試分類）、快取（同一個請求不付兩次錢）、可續跑的工作清單（session 中斷後接著輪詢）、花費帳本，以及片段品檢用的 ffmpeg 輸出解析器；各階段（T4、T5）只組請求與判斷。

## Definition of done

- [x] `media/client.mjs`：`mediaStatus`、`submitImage`、`submitClip`、`submitMusic`、`pollOnce`／`waitForJob`（讀 `retry_after_seconds`、輪詢之間看 STOP 檔，中斷時 `MediaError.job` 帶最後狀態）、`runJob`、`downloadFile`（串流到 `.partial`、邊下載邊驗 sha256）、`putFile`（4 MiB 分段）、`judge`；`MediaError.who` 分站主／工具／服務；預算耗盡不重試；`RETAKE_CODES`。
- [x] `media/cache.mjs`：`mediaKey`、`media/cache.json`（`cached`／`remember`／`forget`）、`media/jobs.json`（`pendingJob`／`rememberJob`／`forgetJob`）；`media/ledger.mjs`：`media/ledger.json`、`ledgerTotals`、`capProblem`。
- [x] `media/qc.mjs`：ffmpeg 參數與解析器（probe、blackdetect、freezedetect、切鏡、PSNR、dHash）、`hamming`、`duplicates`、`clipVerdict`、`pictureVerdict`、`THRESHOLDS`。
- [x] `media/cli.mjs` 分派 `media-status`（印伺服器預算與本支總計）；`look`／`keyframes`／`clips`／`music` 未做時指名票、結束碼 5。
- [x] 測試用假站：重試分類、輪詢與 STOP 與逾時、下載驗雜湊、分段上傳、快取、帳本與上限、解析器、判定、CLI（`media.test.mjs`，10 個；整套 287 個綠）。

## Steps

- [x] 形狀照 S2 票 Notes 的 `JobOut`／`JudgeOut`（`passed`）／`PUT files`。
- [x] client → cache/ledger → qc → cli → 測試。

## How to verify

```bash
node --test tools/video/media/*.test.mjs
node tools/video/cli.mjs media-status --slug <SLUG>
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

- 2026-09-26 做完。給 T4／T5：一個生成的骨架是 `key = mediaKey(kind, fields)` → `cached(workdir, key)` 命中就用 → 否則 `pendingJob(workdir, key)` 有就 `waitForJob` 接著等 → 否則 `capProblem` 過了才 `runJob({ submit, request, stop })`，`rememberJob` 在送出後、`forgetJob` 在拿到檔案後；`downloadFile` 到 `<stage>/<id>-<key>.<ext>`；`remember` 與 `appendLedger` 各記一筆。片段品檢：`probeArgs`／`blackdetectArgs`／`freezedetectArgs`／`sceneCutArgs`／`framePsnrArgs` 用 `assemble/ffmpeg.mjs` 的 `runTool` 跑，把 stderr 交給對應的 parser，最後 `clipVerdict`。judge 的檔案先 `putFile`（或本來就是生成結果）再以 sha256 引用；片段超過 20 MB 先用 ffmpeg 縮成 720p 代理檔再送。
- `waitForJob` 的等待最短 3 秒、最長 60 秒，一支工作最多等 20 分鐘（`timeoutMs`）。
