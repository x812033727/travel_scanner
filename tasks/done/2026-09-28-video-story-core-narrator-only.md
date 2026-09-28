---
id: 2026-09-28-video-story-core-narrator-only
title: 沒有角色的漫劇跳過設定圖，加上故事的 lint 規則
status: done
priority: P1
area: tools
owner: claude-opus-5-5-video-story-core
claimed_at: 2026-09-28T05:49:59Z
created_at: 2026-09-28T03:31:11Z
completed_at: 2026-09-28T07:03:37Z
branch: claude/video-story-core-narrator-only
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/story.mjs
  - tools/video/core/story.test.mjs
  - tools/video/core/fixtures/story
  - tools/video/core/fixtures/load.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/assemble/smoke.mjs
  - .github/workflows/video-tooling.yml
  - docs/videos/STORY.md
---

# 沒有角色的漫劇跳過設定圖，加上故事的 lint 規則

## Why

品牌故事（`docs/videos/STORY.md`）是只有旁白、全部靜態圖的漫劇。格式本身允許沒有角色（`tools/video/core/drama.mjs` 的 `validateCharacters` 寫著空陣列是 narrator-only），但產線走不過去：

- `stepsFor`（`tools/video/core/state.mjs`）永遠把「look generated」「look approved」排進步驟；
- `look` 在沒有角色時直接丟錯（`tools/video/media/look.mjs` 第 88 行）；
- `keyframes` 要求設定圖關卡已核准（`tools/video/media/keyframes.mjs` 第 97–104 行）。

故事另外需要幾條漫劇沒有的 lint 規則，才不會讓不合規格的稿子一路做到花錢的階段。

## Definition of done

- [x] `characters` 是空陣列的漫劇，`status` 的步驟裡沒有設定圖的兩步，`keyframes` 不要求設定圖關卡，其餘步驟照舊；有角色的漫劇行為不變。
- [x] `series.json` 的 `kind` 是 `story` 時，lint 多檢查：每個鏡頭都是 `visual: "still"`、每一句的 `speaker` 都是旁白、章節 5–7 個、`sources` 至少 3 個 https 網址、鏡頭的提示詞不含 `series.json` 的 `names` 裡任何一個名字；平均鏡長不在 5–11 秒是警告。原本寫的「至少 70 鏡」沒有做：長度由 `target_minutes` 管（見 Notes）。
- [x] `tools/video/core/fixtures/story/` 有一支最小的故事範例（`video.json`、`brief.md`、`series.json`），lint 零錯誤。
- [x] 煙霧測試能用故事範例從頭做到成片，每個鏡頭在 `checks.json` 都是 `kind: "motion"`。
- [x] `npm run test:tools` 通過。

## Steps

- [x] `state.mjs`：`stepsFor` 在沒有角色時拿掉設定圖的兩步；`pipelineStatus` 對應調整。
- [x] `keyframes.mjs`：沒有角色時跳過設定圖的核准檢查，參考圖只用風格錨定圖。
- [x] `core/story.mjs`：故事的 lint 規則，`lint.mjs` 在 `series.json` 是故事時呼叫。
- [x] 範例與測試；煙霧測試加 `--fixture story`。

## How to verify

```bash
node --test "tools/video/core/*.test.mjs" "tools/video/media/*.test.mjs" "tools/video/assemble/*.test.mjs"
node tools/video/cli.mjs lint --file tools/video/core/fixtures/story/video.json
node tools/video/assemble/smoke.mjs --fixture story   # Windows ARM64: add --channel msedge
npm run test:tools
```

（Node 24.13 的 `node --test tools/video/core` 把目錄當成模組找，會 MODULE_NOT_FOUND；用上面的 glob。）

## Notes

- `state.mjs` 是共享檔，只有這張票動它；PR #870 也改了這個檔 8 行，合併順序誰後誰 rebase。
- 故事可以有 0–3 個主角（只出現在畫面、不說話）；有主角時設定圖照常產生，由 judge 自動選（免關卡作品本來就這樣）。
- `MAX_SHOT_SECONDS = 12` 不動。

### 做了什麼、為什麼（2026-09-28，claude-opus-5-5-video-story-core）

- `stepsFor`：原本的函式改名成 `formatSteps`（它的內容一行都沒動），新的 `stepsFor` 包在外面，`narratorOnly(doc)` 時拿掉 `LOOK_STEPS`。這樣 PR #870 改的那幾行（劇本關卡的條件與註解、`const script = …`）跟這張票的改動之間都隔著沒動的行：先對 #870 的分支試合併是乾淨的，#870 合併後接到含它的 head 上也沒有衝突。`pipelineStatus` 多一個 `cast` 旗標：沒有角色時不問 look 關卡、不讀 `characters/manifest.json` 與 `characters/choice.json`（測試用解析不了的檔案證明它沒讀）。
- `narratorOnly(doc)`、`LOOK_STEPS` 從 `state.mjs` 匯出：漫劇、不是合集、`characters` 是空的。
- 「至少 70 鏡」改成平均鏡長 5–11 秒的警告：鏡頭數跟著長度走，長度已經由 `target_minutes` 管；單鏡上限還是 `MAX_SHOT_SECONDS`。
- 禁名規則多查角色的 `name`、`appearance`、`sheet_prompt`：它們會被 `shotPrompt` 與 `sheetPrompt` 放進圖片提示詞，主角的名字寫成真人姓名一樣會讓圖片模型去畫那個人。比對是整個詞、不分大小寫、空白可多可少；拉丁字母的名字不比對到更長的字裡（`Marsh` 不會打中 `marshmallow`），中文名字直接找子字串。
- 聯絡表分頁：24 鏡以內照舊一張 `keyframes/contact-sheet.png`；超過就是 `keyframes/contact-sheet-01.png`、`-02.png`…每頁最多 24 格（`CONTACT_SHEET_TILES`、純函式 `contactSheetPages`）。`manifest.contact_sheets` 永遠有，依序列出每一頁（24 鏡以內就是 `["keyframes/contact-sheet.png"]`）；`manifest.contact_sheet` 指第一頁；瀏覽器開不起來時兩個都是空的（`null`、`[]`）。上一次跑留下、這次沒畫的 `contact-sheet*.png` 會刪掉，免得 `sync.mjs` 現在寫死的 `keyframes/contact-sheet.png` 送出過期的圖。
- 查過 `clips`、`music`、`render`、`assemble`：都不需要改。`clips` 讀角色設定時容許沒有檔案（`?? {}`）；全靜態圖只寫 manifest、不買片段，但仍要權杖並向伺服器問一次狀態，片段供應商必須是設定好的（主機上用同一把 Gemini 金鑰，沒問題），沒改。`look` 對沒有角色的漫劇仍丟 UsageError，但它已經不在步驟裡。
- 範例是「條碼」的故事：10 個靜態鏡頭、5 章、3 個 Wikipedia 來源、沒有角色、有配樂、`video.json` 有 `series`（`brand-stories` 第 1 集），估計 1.7 分鐘，lint 零錯誤零警告。事實來自那三篇條目；這個 session 不能連網，來源沒有重新抓，`checked_on` 是範例的日期。

### 給工人票（`2026-09-28-video-story-worker`）的合約

- 故事的步驟（沒有主角）：brief、outline approved、script passes lint、fact-checked、script approved、narration synthesized、narration approved、keyframes drawn、storyboard approved、frames rendered、clips generated、music generated（有 `music` 才有）、video assembled、captions written、final video approved、upload package、on YouTube。有主角時在 script approved 後面多 look generated、look approved。
- `script approved`：`video.json` 有 `series` 的一集都有這一步，PR #870 之後每支漫劇都有。故事不送劇本關卡，由工人在本機核准（`writeScreenplay` 之後 `approve({ gate: "script" })`，寫法同 `draftEpisode` 核准大綱）。
- `series.json` 必須有頂層的 `kind: "story"` 與 `names`（字串陣列，從 `beats.names` 抄）；`video.json` 有 `series` 時還要有相同的 `slug`、`episode`，`characters`（主角，照抄進 `video.json`；沒有就是空陣列），`visual_tier: "stills"`。
- 規則清單：`tools/video/core/story.mjs` 的 `STORY_RULES`，每條 `{ id, level, rule }`，`rule` 是一句英文，可以直接放進撰稿提示詞。
- `review-push` 不帶 `--gate` 時（`sync.mjs` 的 `nextGate`）每支漫劇都會排 look，沒有角色設定檔就停在那裡；工人一律帶 `--gate`。
- `.agents/skills/youtube-video/references/drama.md` 的「keyframes 要 look 核准」還沒寫沒有角色的例外，skill 文件在工人票。

### 驗證（2026-09-28，Windows ARM64）

- How to verify 的四個指令與 `npm run check:tasks` 都在本機跑過，結束碼寫在 PR 說明。`lint --file` 對範例是 0 errors、0 warnings；故事的煙霧測試（`--channel msedge`）做到上架包，`checks.json` 的 10 個鏡頭都是 `kind: "motion"`，七種運鏡都用到，push-in 與 drift 的第 0 格 PSNR 約 41–42 dB。
- PR #870 在這張票做到一半時合併進 main，#888 的分支也併了 main；這張票的 commit 接在 #888 目前的 head 上，檢查是在接上之後跑的。
- 新的 25 鏡分頁測試會把 `keyframes/manifest.json` 連續改寫 25 次；Windows 上第一次跑遇過一次 `atomicWrite` 的 rename EPERM（跟 `media/cache.json` 同一種檔案鎖），重跑就過，CI 是 Linux。
