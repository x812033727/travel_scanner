---
id: 2026-09-28-video-shorts-worker-lab
title: Video shorts T2: the worker makes experiment Shorts by itself, plans the week and writes the weekly report
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-shorts-t2
claimed_at: 2026-10-02T06:12:06Z
created_at: 2026-09-28T03:45:00Z
completed_at:
branch: claude/video-shorts-worker-lab
depends_on:
  - 2026-09-28-video-shorts-automation-api
  - 2026-09-28-video-shorts-tools-push
scope:
  - tools/video/automation/shorts.mjs
  - tools/video/automation/shorts.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
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

- [x] 工人的迴圈每一輪先敲門（`ops/video/worker.sh` 跑 `shorts/cli.mjs tick`，T1 已經加了），`auto` 再跑 `shortsStep()`，排在「自動產線有沒有開」的檢查之前，由 Shorts 自己的設定決定做不做。教學影片與漫劇原本的迴圈讀清單時帶 `shorts=exclude`，行為不變。
- [x] `shortsStep()` 依 `shorts/next` 的工作做一個單位：`report`、`plan`、`brief`、`make`。庫存低於 `stock_days` 時 Shorts 排在漫劇與教學長片之前，否則排在後面。
- [x] 實測線的 `make`（`lab.mjs`）：
  - 凍結題目：把規格的輸入、答案、評分寫成 `protocol.json` 並記下雜湊，之後任何一步都不能改它。
  - 受測模型各跑一次（階段 `subject`、`variant` `a`／`b`，各自全新的對話）；原始回答、伺服器回報的模型名稱、時間、重試次數原樣寫成證據檔。技術失敗可以重試一次，兩次都留；模型答錯不是失敗。
  - 評分：數字與時間用程式對答案，其餘交查核模型；寫 `scores.json`。
  - 撰稿（`writer`、`variant: shorts-lab`）只拿到規格、證據與分數，寫出 Shorts 腳本（格式第 2 版）；兩組一樣就寫一樣，不准挑有利的樣本。
  - 查核（`verifier`、新對話）對照證據逐句檢查，寫 `verify.json`；有問題交撰稿改，最多照設定的輪數。
  - `build --speech server` → `check-audio` → `qa` → 自動修（每種最多 2 輪）→ `package` → `push`。
- [x] 每週排片（`planner`、`variant: shorts-plan`）與補題（`shorts-brief`）：輸入是題庫、配額、上週每支的 YouTube 原值、預算狀態；輸出寫回伺服器。
- [x] 每週報告（`planner`、`variant: shorts-report`）：發了什麼、每支的原值（照抄，附來源與讀取時間）、花費、卡住的事、下週排片與理由。**提示詞明寫不要輸出任何自己算的分數、排名、平均或百分比**；lint 擋掉報告裡出現而原值表裡沒有的數字。
- [x] 失敗處理沿用工人的規矩：模型交不出能用的答案時存原文、這一輪結束；同一步連續兩輪失敗就卡住並把原因報到站上；外部服務暫時失敗不算進卡住的次數；`STOP` 檔在每個單位之間檢查。
- [x] 提示詞的正本在 `tools/video/shorts/prompts.mjs`，給代理用的同一份在 skill 的 `references/prompts/shorts-*.md`。
- [x] `node --test tools/video/automation/*.test.mjs tools/video/shorts/*.test.mjs` 全過；測試用注入的 `fetch`、假的模型回答與程式產生的音檔，不碰任何服務。

## Steps

- [x] 讀 `tools/video/automation/flow.mjs`、`series.mjs`（作品模式怎麼接進迴圈）與 `docs/videos/ai-shorts/campaign/README.md`（實驗規範）。
- [x] `client.mjs` 的新方法、`cli.mjs` 的順序、`flow.mjs` 的清單篩選。
- [x] `lab.mjs`：凍結、受測、評分、撰稿、查核、自動修。
- [x] `shorts.mjs`：四種工作與庫存的優先順序。
- [x] 提示詞與 skill 的鏡射檔。
- [x] 測試。

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

### 2026-10-02 做完（claude-opus-5-5-shorts-t2）

認領時 `--force`：擋住的三張都是已合併 PR 的舊認領（`2026-09-28-drama-listener-stale-check` 是 PR #978 的 codex-ten-drama、`2026-09-28-sothatswhy-shorts-from-episode` 是 PR #904/#950/#962、`2026-09-30-video-worker-moves-two-videos-at` 是 PR #999）。

**敲門**：照 PR #1088 之後的 `docs/videos/SHORTS.md`，`tick` 在 `ops/video/worker.sh` 自己的背景迴圈（`VIDEO_SHORTS_KNOCK_SECONDS`，`STOP` 暫停），`auto` 裡沒有再加一次。DoD 第一項其餘的部分照做。

**怎麼接進 `auto`（`cli.mjs`）**：先讀教學影片的設定（查核輪數、頻道立場要用），再讀 Shorts 設定（`GET /video/automation/shorts/settings`）判斷庫存；庫存不足就先跑 `shortsStep()`，否則排在教學影片與漫劇的單位之後；「自動產線沒開」時 Shorts 照樣跑（在那句話印出之前）。`STOP` 在每個單位之間檢查。舊站（Shorts 路由回 404）一個字都不印，既有 `auto` 測試的輸出不變。
- 庫存怎麼算：工人讀不到時段表，所以用 Shorts 設定的 `campaign_start`、`daily_pattern`、`slot_times` 算出接下來 `stock_days` 天該有幾格（`slotsAhead`，跟 `rules.build_slots` 同一個算法），跟片庫（`GET …/videos?shorts=only&state=library&limit=200`）的支數比。還沒開跑就不算不足。這比伺服器的 `stock_cover` 保守（已經指派了影片的格也算進去），偏向先做 Shorts。
- **清單篩選放在 `client.mjs`**：`videos()` 不帶參數時預設 `shorts=exclude`（`TUTORIAL_LIST`），教學與漫劇的迴圈、`tidy` 都走它；所以 `flow.mjs` 與 `automation.test.mjs` 一個位元組都沒改，`docs/videos/long-form/review.json` 綁定的檔案都沒動。測試在 `automation/shorts.test.mjs`。
- `client.test.mjs` 不在原 scope，加進來：它的假站對任何沒列的路由直接 `assert.fail`，`auto` 現在多讀一次 Shorts 設定，所以讓它的假站對 Shorts 路由回 404（舊站的樣子）並把那次呼叫加進預期的清單。

**`shortsStep()`（`automation/shorts.mjs`）**：每輪先跟進「成片在等站主」的 Shorts（核准了就再 `push` 送上傳包），再做 `shorts/next` 的一件工作。
- `plan`：企劃模型（`planner`／`shorts-plan`）排；工人只送伺服器收的 `slot_id`、`topic_slug`，並拿掉這個工人還不會做的內容線（`cut`、`drama`）與要生圖的實測題；理由存在 `_shorts/plans/<日期>.json`。伺服器 422 拒絕就把原因交回模型再試一次。連續兩輪不能用：送一份空的排片（伺服器記下 `last_plan_at`，半天內不再要）。
- `brief`：只寫實測題，送出前把每題整理成 `TopicIn` 收的欄位（伺服器是 strict，多一個欄位整批 422），不帶 `requires`。連續兩輪不能用：本機記 12 小時不再問（伺服器只有在寫入時才記 `last_brief_at`）。
- `report`：原值表由程式印（每支每個時間窗的原值、來源、讀取時間、錯過的時段、這週的帳、預算、下週時段），模型只寫表上方的判斷；lint 擋掉表裡沒有的數字與「中位數、排名、名次、分數、成長率、達成率、加權」；`rows` 由程式列（伺服器照存的值抄），`plan` 用下週的時段加模型給的理由。連續兩輪不能用：照實存一份「這週的報告沒有寫成」加原值表，免得報告一直排在最前面擋住其他工作。
- 「卡住報到站上」：只有 `make` 有影片可報（`PUT /video/reviews/{slug}` `stage: blocked`，分頁列在需要你）；`plan`、`brief`、`report` 沒有可報的地方，改成上面那三種處理並印出原因。

**實測線（`shorts/lab.mjs`）**：檔案在 `<work base>/_shorts/<slug>/`（開頭的 `_` 讓 tidy 與教學迴圈不碰）。
- 凍結：查核模型（`verifier`／`shorts-lab-key`）從規格列出答案鍵，程式檢查每一項的 `source` 是規格的原文、數字與時間真的在那段原文裡，才寫 `protocol.json`（規格、答案鍵、兩組要送的請求）並記雜湊；之後每一步先核雜湊，對不上就卡住。受測模型的請求是「輸入＋該組的問題」，不含答案。條件 b 寫「同一個 context 追加」（06 自我檢查）時，b 的請求是 a 的請求、a 的原始回答、b 的問題，一次送出（`/automation/run` 沒有對話記憶），照實記在證據裡。
- 受測：用一個不自己重試的 client（`attempts: 1`），每一次請求都記在證據檔；技術失敗下一輪再試一次，兩次都留；兩次都失敗就照規格的失敗處理卡住（沒有原始輸出不做結論）。站主沒選受測模型、預算、暫停的訂閱帳號這幾種「什麼都沒跑」的不算一次。`video_ai_subject_not_chosen` 加進 client 的站主錯誤。
- 評分：查核模型（`shorts-lab-score`）只負責指出回答裡哪一段是答案（逐字引用）與那段寫的值，程式核對引用真的在回答裡、值真的在引用裡，再拿值跟答案鍵比；文字題才採查核的判斷。
- 撰稿只拿規格、證據、分數（測試檢查 payload 的鍵）；lint 擋掉證據裡沒有的數字、不是 HTML 證據的素材。查核在新的呼叫裡逐句對證據，寫 `verify.json`（綁腳本雜湊），沒過交回撰稿，最多照教學設定的 `max_verify_rounds`（預設 3）。
- 成片：`build --speech server`；長度不對、字卡放不下交撰稿修；`check-audio` 被標的句子第 1 輪重錄（`--redo`）、第 2 輪交撰稿改寫；`qa` 沒過依序修 `facts`、`layout`、`metadata`、`narration`，每種最多 2 輪；修不好照樣 `package`、`push`，留給站主。`usage.json` 補上各階段的呼叫次數與 token。成片送出就回報 `done`（題目算做完，月曆不等它）；成片等站主的，之後每輪跟進。
- 生圖、看圖、修圖、要執行程式的題目（含 05）工人不開始做，印出原因；HTML 回答（02）只有不含 script、不連網路的才當證據圖。

**另開的票**：`2026-10-02-video-shorts-next-stops-offering-the` —— 伺服器的 `next_job_for` 對卡住的那支照樣回 `make`，會擋住月曆後面的 Shorts。

**驗證**：`node --test tools/video/automation/*.test.mjs tools/video/shorts/*.test.mjs` 362 過、1 略過。`npm run test:tools` 1193 過，6 個失敗都是已知的：`tools/video/tts/check.test.mjs` 的 Windows 限定那一個，以及 `tools/video/render/render.test.mjs` 5 個（這個 worktree 連到的共用 node_modules 少了 `@fontsource-variable/noto-sans-{kr,sc,jp}`）。測試全用注入的 fetch、假的模型回答、程式產生的正弦波音檔與注入的 ffprobe 量測；沒有對正式站跑過。部署到主機的工人之後才生效；真的跑一輪要站主同意並用到模型額度。
