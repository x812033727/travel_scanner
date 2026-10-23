---
id: 2026-10-18-curio-host-route-knows-the-s
title: Curio host route knows the S pillar (history figures and famous scenes)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-18T23:11:23Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
---

# Curio host route knows the S pillar (history figures and famous scenes)

## Why

奇聞檔案局 2026-10-18 加了第六軸 S（歷史人物與名場面，`docs/videos/history-curiosity/README.md` §S 軸），
主機的解說路線卻只認得 H、M、P、U、L：`tools/video/automation/explainer-series.mjs` 的 `MYSTERY.pillars`、
`opening`（"a historical mystery, a strange phenomenon, …"）、`thumbnailGuide` 的標籤清單、`bibleSections` 的
「主軸：」清單、`bibleJson` 的 `"pillar"` 列舉。在補上之前，從後台開一集 S 軸會被歸到 H（歷史懸案），縮圖標籤也會寫歷史懸案。

## Definition of done

- [ ] 後台開一集 S 軸的題目時，故事聖經寫「主軸：歷史人物與名場面」、`outline.pillar` 是 `"S"`、縮圖標籤是 S 的標籤（建議「歷史名場面」）。
- [ ] 提示詞說明 S 軸的「流傳的版本」是演義、軍記物、課本與軼事，「紀錄」是正史、當時的書信與近年研究；
      小說情節講成小說，不講成「假的」；今天兩國或兩群人還在爭的題目不講（README §S 軸 §不收的題目）。
- [ ] `explainer-series.test.mjs` 釘住的 mystery 雜湊照新文字更新，並在測試註解寫明為什麼變。

## Steps

- [ ] 開工前確認沒有進行中的奇聞檔案局集數（改提示詞會讓那些 journal 重問一次、重付一次），有的話等它們過了寫稿與查核階段。
- [ ] 確認 `2026-10-14-ai-and-tech-videos-tell-one` 已經不持有 `explainer-series.test.mjs`（它在 scope 裡；工具會擋重疊的認領）。
- [ ] 改 `MYSTERY`（pillars、opening、contentRules、thumbnailGuide、bibleSections、bibleJson）。
- [ ] `npm run test:tools`。

## How to verify

`node --test tools/video/automation/explainer-series.test.mjs` 過；`grep -n '"S"' tools/video/automation/explainer-series.mjs` 找得到主軸與 pillar 列舉。

## Notes

這張票由 `2026-10-18-curio-s-axis-history-figures-and` 拆出來。
