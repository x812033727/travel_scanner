---
id: 2026-10-08-video-planners-thumbnail-headline-six
title: Video planners: thumbnail headline limit 12 to the channel's six (compilation, drama, brand story)
status: in-progress
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-10-08T02:36:58Z
created_at: 2026-10-08T03:40:00Z
completed_at:
branch: claude/focused-hopper-t3zgz9
depends_on:
  - 2026-10-07-video-thumbnails-one-subject-six-characters
  - 2026-10-07-video-script-rules-outro-with-a
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - tools/video/story-plans/validate.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
---

# Video planners: thumbnail headline limit 12 to the channel's six (compilation, drama, brand story)

## Why

票 `2026-10-07-video-thumbnails-one-subject-six-characters` 把 `qa` 的 thumbnail 項改成頻道規則：大字
最多 6 個字（`templates.mjs` `THUMB_HEADLINE_MAX`，`headlineCount`：CJK 各 1、英文詞或數字各 1、最多 2 個），
超過是 **fail**。但全自動路線替站主寫大字的企劃還允許 12 個字：`automation/compilation.mjs:29`
`HEADLINE_MAX_CHARS = 12`（第 144 行驗、第 249 行交給工人）、`automation/prompts.mjs:574` 漫劇
`headline ≤ 12 chars`、`prompts.mjs:1275` 合集 `≤ 12 characters`、`automation/story.mjs:709` 品牌故事
`clip(…, 12)`、`story-plans/plan.mjs:36` `LIMITS.headline: 12`。一支工人企劃的合集或漫劇寫了 7–12 字的大字，
lint 與 render 都過，到 `qa` 才 fail：成片關卡不會自動核准（`final_qa_passed` 要 qa ok），卡片停在後台等
站主改 `video.json`（BINGE.md §43、§46 本來是 qa → 成片自動核准）。審稿 2026-10-08 指出這個落差；本票不在
原票 scope，所以另開。

## Definition of done

- [ ] `HEADLINE_MAX_CHARS`、`LIMITS.headline`、`story.mjs` 的 `clip(…, 12)` 改成 `THUMB_HEADLINE_MAX` 與
      `headlineCount` 的算法（字數是 `headlineCount(headline).count`，不是 `.length`；英文詞或數字最多
      `THUMB_HEADLINE_WORDS_MAX`），`validate.mjs` 跟著。
- [ ] `prompts.mjs` 漫劇（第 574 行附近）與合集（第 1275 行附近）的大字規則改成「≤ 6 個字、一個英文詞或數字算
      1、最多 2 個、`\n` 只放在詞的邊界、不重複標題前 10 字」，與 `.agents/skills/youtube-video/references/visuals.md`
      §縮圖同一套字。
- [ ] `core/lint.mjs` 對非系列（`thumbnailSeries(doc)` 是 null）的縮圖大字做同一條檢查當 **警告**（qa 才 fail），
      讓撰稿階段就看得到，不要等到成片關卡。
- [ ] 企劃的回答超過 6 字時重問一次（`compilation.mjs` 的 `ANSWER_ATTEMPTS` 機制已有），仍超過就把大字截到詞邊界
      而不是硬切。
- [ ] 各自的測試覆蓋；`npm run test:tools`。

## Steps

- [ ] 先讀 `tools/video/qa/thumbnail.mjs` `thumbnailChecks` 與 `templates.mjs` `headlineCount`，規則以它們為準。
- [ ] 票 `2026-10-07-video-script-rules-outro-with-a` 還在 `prompts.mjs` 上，等它結案再 claim。

## How to verify

`cd /home/user/travel_scanner && node -e 'import("./tools/video/qa/thumbnail.mjs").then(async m=>{const {jpegBytes}=await import("./tools/video/qa/test-images.mjs");console.log(m.thumbnailChecks({bytes:jpegBytes(1280,720,2000),headline:"仙門風雲第一部全集"}))})'`
現在是 `ok: false`，而 `compilation.mjs:144` 接受這 9 個字；做完後企劃不可能交出 qa 會擋的大字。

## Notes

- 合集的大字本來就是系列名（「仙門風雲 全集」對標題「仙門風雲 全集：第一部完整版」），所以 `qa/cli.mjs`
  `thumbnailItem` 對合集不做重複標題的警告（2026-10-08 審稿後改的）；這張票不用再碰那一條。
- 各語言自己的縮圖（`thumbnail_locales`）不套中文字數與斷詞規則（`thumbnailChecks` 的 `locale`），企劃給翻譯的
  大字規則不在本票。
