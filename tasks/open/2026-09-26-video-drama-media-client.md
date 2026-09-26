---
id: 2026-09-26-video-drama-media-client
title: Video drama T2: media client with cache, resumable jobs, cost ledger and QC parsers
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:30Z
completed_at:
branch:
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

- [ ] `media/client.mjs`：`mediaStatus`、`submitImage`、`submitClip`、`submitMusic`、`pollJob`（讀 `retry_after_seconds`、輪詢之間看 STOP 檔）、`downloadFile`（串流到 `.partial`、邊下載邊驗 sha256）、`putFile`（4 MiB 分段）、`judge`；`MediaError.who` 分站主／服務；預算耗盡不重試。
- [ ] `media/cache.mjs`：`mediaKey`、`media/cache.json`、`media/jobs.json`（中斷後重跑接著輪詢同一個 job）；`media/ledger.mjs`：`media/ledger.json` 與總計。
- [ ] `media/qc.mjs`：`parseBlackdetect`、`parseFreezedetect`、`parseSceneCuts`、`dHash`／`hamming`、`qcVerdict`。
- [ ] `media/cli.mjs` 分派 `media-status`（印伺服器預算與本支總計）；`look`／`keyframes`／`clips`／`music` 未做時結束碼 5。
- [ ] 測試用假 fetch：pending→ready、Retry-After、預算碼 who=owner、STOP 留下 jobs.json、sha 不符拒收、帳本總計。

## Steps

- [ ] 先跟 S2 對齊 `JobOut`／`JudgeOut`／`PUT files` 形狀。
- [ ] client → cache/ledger → qc → cli → 測試。

## How to verify

```bash
node --test tools/video/media/*.test.mjs
node tools/video/cli.mjs media-status --slug <SLUG>
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
