---
id: 2026-09-28-video-story-worker
title: 工人的故事流程：逐章撰稿、查核、審稿與提示詞
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-video-story-worker
claimed_at: 2026-09-28T11:54:26Z
created_at: 2026-09-28T03:31:14Z
completed_at:
branch: claude/video-story-worker
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
- **工人讀得到什麼（2026-09-28 量過，寫在 `STORY.md` §查核與來源規則）。** `fetch.mjs` 的 `pageReader` 不讀 PDF、不讀超過 3 MB 的頁面、一頁只留前 40,000 個字；企劃清單讀得到的頁面裡約一成比這個長。這張票要做兩件事：
  - 逐章查核時，用那一章要查的事實裡的年份、數字、名字，在整頁文字裡找到那一段再交給查核模型，不是交頁面開頭的 40,000 字。`pageReader` 現在在回傳前就截斷，要嘛加一個回傳全文的選項，要嘛讓它接受要找的字。
  - 工人讀不到的來源，交給查核模型的是企劃裡那個來源的 `supports`，並註明是企劃查核時讀到的。
  - `must_verify` 裡標了 `reviewer_only: true` 的事實，沒有任何工人讀得到的來源。查核模型不去找來源，只確認稿子說的跟企劃那一條一樣；數字、年份一個字都不能多。
  - 要不要讓工人讀 PDF（主機映像加 `pdftotext`，或加一個 JS 函式庫）先不做：企劃清單已經保證每個必查事實至少有一頁讀得到。試作如果發現查核模型常常因為讀不到 PDF 而拿掉事實，再開票。
- 官方頁面常用昭和、民國紀年，外文頁面的數字單位不同（billion 與億）：查核的提示詞要叫模型自己換算。粗略量過，有數字又有讀得到頁面的 773 條事實裡，660 條的每個數字字面上都在工人留下的文字裡，17 條一個都找不到，多半就是這個原因。
- **企劃的事實是查核過的。** `beats.must_verify` 每一條都有人對過來源（`reviews/<代號>.json`）。查核模型的工作是確認稿子說的跟企劃一樣，以及撰稿模型自己加的數字、年份、人名在來源裡找得到。`attributed: true` 的事實，旁白要說是誰的說法；查核要擋掉把它講成定論的句子。
- `beats.caveats` 是查核的人留給撰稿的注意事項（哪個軼事查不到出處不要講、哪個數字各來源說法不一）。撰稿與查核的提示詞都要帶上它，並且要求照做。
- 票 `core-narrator-only`（PR #897）留下的合約：`series.json` 要有頂層的 `kind: "story"` 與 `names`；`video.json` 有 `series` 時要有對得上的 `slug`／`episode`、`characters`、`visual_tier: "stills"`。PR #870 之後每支漫劇都有 `script approved` 這一步，故事由工人在本機核准。`review-push` 要明確帶 `--gate`。
- 票 `check-audio-batching`（PR #896）之後，一個故事的旁白檢查最多 3 次 Jev 呼叫；Jev 額度用完時 `check-audio` 以 4 結束，已經付過的判定會留著。
- 票 `storyboard-sheets`（PR #895）之後，超過 47 鏡的分鏡送審只送聯絡表與待修的鏡頭；聯絡表的頁是 `keyframes/manifest.json` 的 `contact_sheets`。
- 2026-09-28 認領（claude-opus-5-5-video-story-worker）用了 `--force`：相依的 `video-story-api-series-kind` 的 PR #910 已在 2026-09-28T11:49Z 合併（main 的 `3156370b8`），只是票還沒跑 `done`；scope 與 PR #870 的三張 `review` 票（`video-dubs-worker`、`video-drama-room-worker`、`video-split-settings-worker`）重疊，#870 早已合併。那幾張票沒有動。
