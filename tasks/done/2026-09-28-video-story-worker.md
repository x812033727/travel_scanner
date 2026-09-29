---
id: 2026-09-28-video-story-worker
title: 工人的故事流程：逐章撰稿、查核、審稿與提示詞
status: done
priority: P1
area: tools
owner: claude-opus-5-5-video-story-worker
claimed_at: 2026-09-28T11:54:26Z
created_at: 2026-09-28T03:31:14Z
completed_at: 2026-09-28T13:43:54Z
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

- [x] `tools/video/automation/story.mjs`：從集數的 `beats` 寫 `brief.md` 與 `series.json`，大綱在本機核准；之後逐章撰稿（`writer:story`）、逐章查核（`verifier:story`，抓來源網址、回主張表與句子 patch）、逐章聽眾審稿（`listener:story`，只回 patch）；工人合併、分配句子 id、跑 lint。
- [x] 每一次模型呼叫都在 295 秒與輸出上限以內；測試用假的模型回應走完六章。
- [x] 故事不寫前情、不送劇本關卡、不做合集；設定圖與分鏡照免關卡作品自動核准；keyframes 沒過時的提示詞修正只回被點名的鏡頭。
- [x] 提示詞在 `.agents/skills/youtube-video/references/prompts/` 有一份給人讀的版本，`references/story.md` 寫操作步驟；`.claude/skills` 的鏡像逐字相同。
- [x] `docs/videos/AUTOMATION.md` 多一節說明故事的流程。
- [x] `npm run test:tools` 通過。

## Steps

- [x] 讀 `STORY.md`、`flow.mjs` 的 `draftEpisode`／`advance`／`verify`、`series.mjs` 的 `seriesStep`。
- [x] `story.mjs` 與 `story-prompts.mjs`；在 `flow.mjs` 與 `series.mjs` 加最少的掛鉤。
- [x] 來源規則寫進提示詞：官方頁面，或兩個互相獨立的可靠來源；軼事要交代出處；負面說法照 `STORY.md` §查核與來源規則。
- [x] 圖像規則寫進提示詞：不出現 `names` 裡的名字、不畫商標文字、真人畫成一般化的卡通人物。
- [x] 測試、skill 文件與鏡像。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"   # 目錄寫法在 Node 24 會失敗，用 glob
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

### 2026-09-28 做完（claude-opus-5-5-video-story-worker）

- **做了什麼**：`tools/video/automation/story.mjs`（流程）、`story-prompts.mjs`（四個 variant：`writer:story`、`verifier:story`、`listener:story`、`writer:story-fix`）、`story.test.mjs`（16 個測試，全部用替身：沒有網路、沒有模型、沒有媒體服務）。共用檔只加掛鉤：`flow.mjs` 四處（import、`episodeVariant` 排除 story 所以不寫前情、`advance()` 裡轉給 `advanceStory`、`fixPrompts()` 轉給 `fixStoryPrompts`）、`series.mjs` 兩處（import、`startEpisode` 轉給 `startStory`）、`prompts.mjs` 兩處（import、`instructionsFor` 查 `STORY_INSTRUCTIONS`；沒動 `VARIANT_INSTRUCTIONS` 那一行，因為 #904 會改它）、`fetch.mjs`（`pageReader({ whole: true })` 多回 `whole`，其他呼叫者拿到的物件一個鍵都沒變，有測試）、`discuss.mjs`（故事的劇本討論串回一則說明、不呼叫模型）。2026-09-28 試合併 #904 的分支沒有衝突。
- **呼叫次數與大小**：正常一支 18 次模型呼叫（撰稿、查核、聽眾審稿各 6），每次都帶 variant；多出來的只有 lint 退回、查核第二輪、長度修正（每輪 3 次）、圖片修正、`listener:rewrite`。用真實企劃的形狀量（A01、A06、B18、T03，替身頁面每頁 60,000 字、數字與名字散在第 40,000 字之後，這是段落上限會用滿的最壞情況）：最大的一次請求約 71 KB（A06 起點章的撰稿，23 個來源），提示詞最長 7,752 字，一章的回答不到 10,000 字。
- **票沒定、我定的**：
  - lint 錯誤：每寫完一章就先 lint 已寫的幾章（記憶體裡，不寫檔），錯在那一章就先修那一章再寫下一章，下一章接的是修好的句子；六章齊了才寫 `video.json`、`claims.md`、`script.md`。lint 錯在章外（工人自己組的欄位）就卡住。
  - 長度的數字（`chapterBudgets`）：鉤子固定 30 秒，其餘五章權重 起點 5、點子 4.5、生意 7、轉折 5、現在 3.5，每鏡平均 8.7 秒 → 13 分鐘 3,250 字、89 鏡。tts 後的範圍從目標算（−1:30、+2:30，13 分鐘就是 11:30–15:30）。長度修正不動鉤子；砍最多砍那章的 45%，補最多補一倍。
  - 段落：每邊 500 字；一頁最多 8,000 字、一次呼叫最多 40,000 字；少於 4,000 字的頁面整頁給；少於 400 字算讀不到（跟企劃的檢查一樣）。年份另外找明治、大正、昭和、平成、令和與民國（含「114年」這種）寫法。讀過的頁面存在 `story/pages/`，暫時的失敗不存。
  - 哪條事實屬於哪一章：事實與各章要點共同的數字（權重 3）與名字（權重 1）最多的那章；撰稿模型看得到全部事實與這個對應，對應只拿來選頁面。
  - 查核「改超過 3 個事實」算 CHANGED、ATTRIBUTED、NOT FOUND 三種。主張表 id 用章的字母（`h1`、`e12`），修稿時保留。
  - `video.json` 的欄位由工人組：標題用企劃的 `title`，說明是 `logline` 加 `question`，標籤是「品牌故事」、主題、類別與 `names`（最多 12 個），分類 27，縮圖用企劃的 `thumbnail.headline` 疊在鉤子選的那一鏡上，配樂用固定的紀錄片提示詞（設定關掉音樂就沒有），字幕一律燒錄。
  - 人物：名字用 id 的字（拿掉 `names` 裡的名字，因為名字會進圖片提示詞），聲音用旁白的（沒人說話，但 lint 要）。
  - 站主退回旁白：聽眾審稿帶著備註把六章再聽一次（6 次呼叫）；聽完什麼都沒改就卡住。站主退回分鏡只有備註、沒有待修鏡頭：把全部鏡頭交給修正，只收備註說到的。作品沒有 `look` 在開始時就卡住。
- **給 `video-story-tidy-finished`**：故事的工作區多了 `story/chapters/`（很小，是逐章撰稿與查核的紀錄）與 `story/pages/`（讀過的頁面整頁文字，一支可能數 MB 到數十 MB）。上架後 `story/pages/` 可以刪（重抓得到），`story/chapters/` 建議留。`video.json` 由各章合併而來，不要只改它。
- **給 `video-story-pilot`**：(1) 合成語速實測約每分鐘 300 字、工具估 250，3,250 字加停頓估計落在 12–13 分鐘；試作兩支若都偏短，調 `STORY_CPM`／權重，不要放寬範圍。(2) 漫劇設定的「各階段常設指示」會接在故事的提示詞後面（格式是 drama，而且寫明衝突時以它為準），試作前先看裡面寫了什麼。(3) 作品的 `look` 沒有 `style_frames`（伺服器的欄位只有 style、negative、motion），90 張圖的畫風一致只靠提示詞；飄掉的話再開票加參考圖。(4) 稿子的年份與數字用阿拉伯數字（跟企劃一樣，查核與改寫檢查才對得上）；若 Jev 常標年份唸錯，考慮讓撰稿寫 `say`（工人已經會補 `say_for`）。(5) `look.motion` lint 上限 300 字、伺服器收 400，超過的會被截。(6) 長度卡住的影片沒有「接受這個長度」的開關，重試會再卡一次，只能放棄或人改。
- **給 `video-story-admin`**：故事沒有劇本卡片（大綱與劇本都在本機核准，備註寫原因），劇本討論串工人只回說明；後台可以不給故事顯示劇本討論。卡住的原因（清單第一列）與站主能做的整理在 skill 的 `references/story.md` §卡住與站主能做的。
- **給 `video-story-api-policy-languages`**：工人只把 `image_model` 寫進 `series.json`，沒有帶給媒體 API；圖片模型要由伺服器照影片所屬作品決定（那張票的 scope）。
- **沒做**：讀 PDF（照上面的決定先不做）；主機上的真實試作（pilot 票）。
