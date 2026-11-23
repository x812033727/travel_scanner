---
id: 2026-11-06-story-series-close-without-outro-card
title: 奇聞檔案局與品牌故事沒有片尾卡時，lint 也要讀結尾三句
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-06T00:09:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# 奇聞檔案局與品牌故事沒有片尾卡時，lint 也要讀結尾三句

## Why

站主 2026-11-05 定：奇聞檔案局（`curio-`）與品牌故事（`story-`）不用卡片、畫面不放任何文字，片尾也不放
`outro` 卡（`register.mjs` `STORY_SERIES_SCREEN_RULE`；撰稿提示已改，PR 分支 `claude/curio-story-heimao-rules`）。
但 lint 是靠 `template: "outro"` 那一景找「結尾」的：

- `lint.mjs` `episodeScriptProblems`：結尾有沒有「訂閱」、是不是三句。
- `narrative.mjs` `outroNextVideoProblems`：結尾有沒有講「下一集／下一支／下一份檔案」（這條是錯誤）。
- `narrative.mjs` 的鉤子間隔與 `loopProblems`：正文算到 outro 前、outro 裡不能埋 loop。

沒有 outro 卡的新集，這幾條就都不跑了：結尾提到下一支不會被擋，結尾三句也沒人數。

## Definition of done

- [ ] curio- 與 story- 的影片沒有 `outro` 景時，lint 把最後一章的最後三句當成結尾，照原本的規則檢查（訂閱、三句、不提下一支、不在結尾埋 loop、鉤子間隔不算結尾）。
- [ ] 有 `outro` 景的舊集行為不變。

## Steps

- [ ] 在 `narrative.mjs` 加一個「結尾是哪幾句」的 helper（outro 景，或這兩個系列最後一章的最後三句），讓上面四處共用。
- [ ] 測試：一支沒有 outro 卡的 curio- 範例，結尾講「下一集」要被擋、沒有「訂閱」要警告。

## How to verify

`node --test tools/video/core/narrative.test.mjs tools/video/core/lint.test.mjs`

## Notes

- `lint.mjs` 與 `lint.test.mjs` 綁在 `docs/videos/long-form/review.json` 的時長覆核裡：改了要由**另一個**代理重新覆核綁定，不能自己綁。
- 同一批還沒做的小事：品牌故事工人給 hook 章的預算仍是 45 秒（`automation/story.mjs` `HOOK_SECONDS`），落在新的第一章範圍
  （40–90 秒，`lint.mjs` `STORY_OPENING_CHAPTER_SECONDS`）裡，所以沒動；承諾句要落在 0:40–1:05，若實測常常太早，再考慮調到 55–60 秒。
