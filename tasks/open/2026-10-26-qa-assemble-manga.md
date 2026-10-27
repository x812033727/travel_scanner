---
id: 2026-10-26-qa-assemble-manga
title: qa 的 assemble 項對 manga 漫劇保留的關鍵影格也加警告
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-26T16:03:44Z
completed_at:
branch:
depends_on:
  - 2026-10-25-manga-blocked
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
---

# qa 的 assemble 項對 manga 漫劇保留的關鍵影格也加警告

## Why

票 `2026-10-25-manga-blocked` 讓 manga 等級的漫劇在提示詞改完兩輪後也保留 judge 最佳張
（`media/keyframes.mjs keepsBestPictures`）。成片審核那邊已經跟上：`review/sync.mjs acceptedPicturesOf`
列出保留的鏡、`flow.mjs gate` 帶 `--manual-review`。但 `qa/cli.mjs` 的 assemble 項只在
`pictures = illustrated(doc)` 時讀 `accepted_with_problems` 加 `keptPicturesWarning`，所以 manga
漫劇的 qa 報告不會寫「有幾張圖是保留的」。成片仍然等站主看（manual review 不靠這條），
只是品管報告少一行提示。

## Definition of done

- [ ] manga 漫劇有 `accepted_with_problems` 的鏡時，qa 的 assemble 項帶同一句 `keptPicturesWarning`。
- [ ] 判法和 `keepsBestPictures` 一致（插圖投影片，或 video.json／series.json 的 `visual_tier` 是 `manga`）；
      `pictures` 另外用在節奏（cadence）與 stale 文字，那兩處不要跟著改。

## Steps

- [ ] `qa/cli.mjs`：`acceptedPictures` 的條件改成 `keepsBestPictures(doc, project.series)`，keyframes manifest
      也要在 manga 時讀（目前 `keyframes` 變數只在 illustrated 時讀，留意 `checksCurrent` 的用法不要變）。
- [ ] `qa.test.mjs` 加一個 manga 漫劇的 case。

## How to verify

`node --test tools/video/qa/qa.test.mjs`。

## Notes

- 2026-10-26 由 `2026-10-25-manga-blocked` 的作者發現，在那張票的 scope 外所以另開。
