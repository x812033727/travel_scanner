---
id: 2026-09-27-ai-video-batch-first-week-analytics
title: Compare first-week performance of four AI videos
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T16:36:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-video-batch-20260927
---

# Compare first-week performance of four AI videos

## Why

站主要求四支 AI 影片上架後，用本頻道既有影片當基準，觀察前七天點閱率、前 30 秒留存及流量來源，再決定下一批題材。四片尚未上架，必須等公開與七天資料到齊。

## Definition of done

- [ ] 在 `docs/videos/ai-video-batch-20260927/metrics.md` 記錄四支影片及可比較的既有影片：公開日、前七天曝光／點閱率、前 30 秒留存、主要流量來源與資料取得時間。
- [ ] 說明基準影片挑選理由與樣本限制，提出下一批題材及標題／縮圖要保留或調整的具體決策。

## Steps

- [ ] 四片公開後記下 YouTube ID、公開時間與對應的上架包版本。
- [ ] 每片公開滿七天後，在 YouTube Studio 匯出相同時間窗的數據，和本頻道已上架 AI 類影片比較；若有資料缺口，明列為缺口，不填估計值。

## How to verify

逐片核對 Studio「觸及率」的曝光與點閱率、「互動」的前 30 秒留存曲線及「流量來源」；在報告中標示截圖或匯出檔的日期與影片 ID。

## Notes

影片 slug：`ai-agent-vs-chatbot`、`ai-citation-check`、`ai-coding-tools-same-task`、`ai-bug-fix-pr-review`。觀看數不是預測值，公開排程由站主決定；未公開前不要建立假數據。
