---
id: 2026-09-28-video-shorts-worker-lab
title: Video shorts T2: the worker makes experiment Shorts by itself, plans the week and writes the weekly report
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:45:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-automation-api
  - 2026-09-28-video-shorts-tools-push
scope:
  - tools/video/automation/shorts.mjs
  - tools/video/automation/shorts.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/shorts/lab.mjs
  - tools/video/shorts/lab.test.mjs
  - tools/video/shorts/prompts.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-plan.md
  - .agents/skills/youtube-video/references/prompts/shorts-brief.md
  - .agents/skills/youtube-video/references/prompts/shorts-lab.md
  - .agents/skills/youtube-video/references/prompts/shorts-report.md
---

# Video shorts T2: the worker makes experiment Shorts by itself, plans the week and writes the weekly report

## Why

站主要 Shorts 全自動。第一期只是把本機做好的接進後台；這張票讓主機工人自己做「AI 真的可以？」實測：照題目的規格真的跑一次測試、留下證據、照實寫稿、查核、配音、出片、品管、送上站，並且每週排片、寫每週報告。

現在工人的迴圈一讀到「自動產線沒開」就結束（`tools/video/automation/cli.mjs`），也完全不知道 Shorts；`tools/video/shorts` 沒有任何一步會自己寫稿或跑測試。

設計全文在 `docs/videos/SHORTS.md`（§三條內容線、§自動品管、§排片與時段、§成效與每週報告、§工具端）。

## Definition of done

- [ ] `auto` 每一輪敲門（`POST shorts/tick`，T1 已經加了）之後跑 `shortsStep()`；兩者都在「自動產線有沒有開」的檢查之前，由 Shorts 自己的設定決定做不做。教學影片與漫劇原本的迴圈讀清單時帶 `shorts=exclude`，行為不變。
- [ ] `shortsStep()` 依 `shorts/next` 的工作做一個單位：`report`、`plan`、`brief`、`make`。庫存低於 `stock_days` 時 Shorts 排在漫劇與教學長片之前，否則排在後面。
- [ ] 實測線的 `make`（`lab.mjs`）：
  - 凍結題目：把規格的輸入、答案、評分寫成 `protocol.json` 並記下雜湊，之後任何一步都不能改它。
  - 受測模型各跑一次（階段 `subject`、`variant` `a`／`b`，各自全新的對話）；原始回答、伺服器回報的模型名稱、時間、重試次數原樣寫成證據檔。技術失敗可以重試一次，兩次都留；模型答錯不是失敗。
  - 評分：數字與時間用程式對答案，其餘交查核模型；寫 `scores.json`。
  - 撰稿（`writer`、`variant: shorts-lab`）只拿到規格、證據與分數，寫出 Shorts 腳本（格式第 2 版）；兩組一樣就寫一樣，不准挑有利的樣本。
  - 查核（`verifier`、新對話）對照證據逐句檢查，寫 `verify.json`；有問題交撰稿改，最多照設定的輪數。
  - `build --speech server` → `check-audio` → `qa` → 自動修（每種最多 2 輪）→ `package` → `push`。
- [ ] 每週排片（`planner`、`variant: shorts-plan`）與補題（`shorts-brief`）：輸入是題庫、配額、上週每支的 YouTube 原值、預算狀態；輸出寫回伺服器。
- [ ] 每週報告（`planner`、`variant: shorts-report`）：發了什麼、每支的原值（照抄，附來源與讀取時間）、花費、卡住的事、下週排片與理由。**提示詞明寫不要輸出任何自己算的分數、排名、平均或百分比**；lint 擋掉報告裡出現而原值表裡沒有的數字。
- [ ] 失敗處理沿用工人的規矩：模型交不出能用的答案時存原文、這一輪結束；同一步連續兩輪失敗就卡住並把原因報到站上；外部服務暫時失敗不算進卡住的次數；`STOP` 檔在每個單位之間檢查。
- [ ] 提示詞的正本在 `tools/video/shorts/prompts.mjs`，給代理用的同一份在 skill 的 `references/prompts/shorts-*.md`。
- [ ] `node --test tools/video/automation/*.test.mjs tools/video/shorts/*.test.mjs` 全過；測試用注入的 `fetch`、假的模型回答與程式產生的音檔，不碰任何服務。

## Steps

- [ ] 讀 `tools/video/automation/flow.mjs`、`series.mjs`（作品模式怎麼接進迴圈）與 `docs/videos/ai-shorts/campaign/README.md`（實驗規範）。
- [ ] `client.mjs` 的新方法、`cli.mjs` 的順序、`flow.mjs` 的清單篩選。
- [ ] `lab.mjs`：凍結、受測、評分、撰稿、查核、自動修。
- [ ] `shorts.mjs`：四種工作與庫存的優先順序。
- [ ] 提示詞與 skill 的鏡射檔。
- [ ] 測試。

## How to verify

```bash
node --test tools/video/automation/*.test.mjs tools/video/shorts/*.test.mjs
npm run test:tools
```

在這台電腦上對正式站跑一輪（`node tools/video/cli.mjs auto --once`）要站主同意，而且會用到模型額度；先用測試替身。

## Notes

- 工人讀不到 repo 的 Shorts 文件（`video_docs` volume 是舊的）：題目、規格、脈絡只從 `shorts/next` 拿，不要讀 `docs/videos/ai-shorts`。
- 工人抓網頁只用固定的編輯用 User-Agent（`tools/video/automation/fetch.mjs`），不登入任何網站，不帶任何個人信箱。
- `earlierVideos()` 會把 `docs/videos` 底下每個資料夾都當成一支做過的影片，`ai-shorts` 也在內（票 `2026-09-28-video-planner-counts-the-ai-shorts-folder`）。
- 先做只用文字的 8 題（01、03、06、07、09、13、14、15）與產出 HTML 的 2 題（02、05）；HTML 成品只在關掉 JavaScript、擋掉所有網路請求的瀏覽器裡渲染（`build` 既有的做法），05 的遊戲要執行程式，留到有隔離的執行環境再做。
- skill 的 reference 只能提到已經存在的路徑，也不能出現本機工作區的路徑；`npm run test:tools` 會檢查。
