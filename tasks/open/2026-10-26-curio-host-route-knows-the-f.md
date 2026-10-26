---
id: 2026-10-26-curio-host-route-knows-the-f
title: Curio host route knows the F and G pillars
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-26T13:43:58Z
completed_at:
branch:
depends_on:
  - 2026-10-18-curio-host-route-knows-the-s
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
---

# Curio host route knows the F and G pillars

## Why

奇聞檔案局 2026-10-26 加了 F 軸（童話、神話與怪談的原版）與 G 軸（靈異事件），`docs/videos/history-curiosity/README.md` §F 軸與 G 軸。
主機解說路線 `tools/video/automation/explainer-series.mjs` 的 `MYSTERY.pillars` 只認得 H、M、P、U、L；S 軸的同一件事是
`2026-10-18-curio-host-route-knows-the-s`，這張接在它後面，兩次改提示詞不要分開讓進行中的 journal 重問兩次——能一起做就一起做。

## Definition of done

- [ ] 後台開一集 F 或 G 的題目時，故事聖經寫對主軸名、`outline.pillar` 是 `"F"`／`"G"`、縮圖標籤是該軸的標籤（建議「童話原版」「靈異檔案」）。
- [ ] 提示詞寫明 F 軸的三段（流傳的版本是迪士尼、課本與電影；紀錄是初版與原典；後三分之一講誰改了什麼）、說書版的形狀、
      不畫改編作品的造型；G 軸照 README §靈異守則（不講成真的、不教儀式、不提命案受害者）。
- [ ] `explainer-series.test.mjs` 釘住的 mystery 雜湊照新文字更新，測試註解寫明為什麼變。

## Steps

- [ ] 開工前確認沒有進行中的奇聞檔案局集數，並看 S 那張票做了沒；沒做就一起做（那張的 scope 跟這張一樣，先認領那張）。
- [ ] 改 `MYSTERY`（pillars、opening、contentRules、thumbnailGuide、bibleSections、bibleJson）。
- [ ] `npm run test:tools`。

## How to verify

`node --test tools/video/automation/explainer-series.test.mjs` 過；`grep -n '"F"\|"G"' tools/video/automation/explainer-series.mjs` 找得到主軸與 pillar 列舉。

## Notes

這張票由 `2026-10-26-curio-f-and-g-axes-fairy` 拆出來。
