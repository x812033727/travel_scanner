---
id: 2026-09-28-video-story-worker
title: 工人的故事流程：逐章撰稿、查核、審稿與提示詞
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:31:14Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-api-series-kind
  - 2026-09-28-video-story-core-narrator-only
  - 2026-09-28-video-story-storyboard-sheets
scope:
  - tools/video/automation
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/AUTOMATION.md
---

# 工人的故事流程：逐章撰稿、查核、審稿與提示詞

## Why

伺服器會回「下一集是某個品牌故事」（票 `2026-09-28-video-story-api-series-kind`），但工人不會做：它的漫劇流程是為 2–4 分鐘的虛構故事寫的。

- 撰稿、查核、聽眾審稿都是整份 `video.json` 來回；13 分鐘、90 個鏡頭的稿子一次寫不完（轉送 295 秒逾時、輸出上限 32,000），逾時還會被重試四次。
- 漫劇的提示詞禁止真實品牌（`tools/video/automation/prompts.mjs` 的 `DRAMA_COMMON`），查核查的是連貫性不是事實。
- 長篇作品的集數會寫前情、等劇本關卡；故事都不需要。

## Definition of done

- [ ] `tools/video/automation/story.mjs`：從集數的 `beats` 寫 `brief.md` 與 `series.json`，大綱在本機核准；之後逐章撰稿（`writer:story`）、逐章查核（`verifier:story`，抓來源網址、回主張表與句子 patch）、逐章聽眾審稿（`listener:story`，只回 patch）；工人合併、分配句子 id、跑 lint。
- [ ] 每一次模型呼叫都在 295 秒與輸出上限以內；測試用假的模型回應走完六章。
- [ ] 故事不寫前情、不送劇本關卡、不做合集；設定圖與分鏡照免關卡作品自動核准；keyframes 沒過時的提示詞修正只回被點名的鏡頭。
- [ ] 提示詞在 `.agents/skills/youtube-video/references/prompts/` 有一份給人讀的版本，`references/story.md` 寫操作步驟；`.claude/skills` 的鏡像逐字相同。
- [ ] `docs/videos/AUTOMATION.md` 多一節說明故事的流程。
- [ ] `npm run test:tools` 通過。

## Steps

- [ ] 讀 `STORY.md`、`flow.mjs` 的 `draftEpisode`／`advance`／`verify`、`series.mjs` 的 `seriesStep`。
- [ ] `story.mjs` 與 `story-prompts.mjs`；在 `flow.mjs` 與 `series.mjs` 加最少的掛鉤。
- [ ] 來源規則寫進提示詞：官方頁面，或兩個互相獨立的可靠來源；軼事要交代出處；負面說法照 `STORY.md` §查核與來源規則。
- [ ] 圖像規則寫進提示詞：不出現 `names` 裡的名字、不畫商標文字、真人畫成一般化的卡通人物。
- [ ] 測試、skill 文件與鏡像。

## How to verify

```bash
node --test tools/video/automation
npm run test:tools
```

## Notes

- 共享檔 `tools/video/core/schema.mjs`、`state.mjs`、`cli.mjs` 不在這張票動；需要的核心改動在票 `2026-09-28-video-story-core-narrator-only`。
- PR #870 大改了 `flow.mjs`（約 450 行）與 `prompts.mjs`；這張票從它合併後的 main 開工。
- 旁白長度：tts 之後量到的長度要在 11:30–15:30 之間；太短或太長先交撰稿模型增刪一章，兩輪仍不過才卡住。
- 訂閱額度用完（`video_ai_subscription_paused`）時這一輪結束，不改用付費 API。
