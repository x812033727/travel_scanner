---
id: 2026-09-26-video-hands-off-qa
title: 影片交給 AI 決定：成片自動品管指令 qa
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-qa
claimed_at: 2026-09-26T22:26:34Z
created_at: 2026-09-26T16:18:29Z
completed_at: 2026-09-26T22:45:52Z
branch: claude/video-hands-off-qa
depends_on: []
scope:
  - tools/video/qa
  - tools/video/cli.mjs
  - tools/video/automation/client.mjs
---

# 影片交給 AI 決定：成片自動品管指令 qa

## Why

自動品管是把「看成片」交給機器的依據（`docs/videos/HANDS-OFF.md` §自動品管）。11 項裡大部分的檢查已經散在 assemble、render 與 lint 裡。還缺的是：一個把結果收齊的指令，以及畫面停留時間、連結、縮圖、查核殘留這四項檢查。

## Definition of done

- [x] `node tools/video/cli.mjs qa --slug <slug> [--workdir <W>]`：
  - 寫出 `<workdir>/review/qa.json`：`{ ok, final_sha256, items: [{ id, ok, detail, warnings? }] }`；
  - 結束碼：0 是全過，1 是有項目沒過，4 是外部服務失敗。
- [x] 項目 id 固定為 assemble、render、narration、pace、captions、metadata、facts、links、thumbnail、policy、disclosure。
  - `policy` 呼叫 judge 端點。端點還沒上線時標成 `ok: false`，細節寫「judge endpoint not available」，不能假裝通過。（做完之後補：頻道立場空白時站台回 409，也標成 `ok: false`；合約見下面 Notes。）
- [x] `pace`：由時間軸與畫面計畫算出每個畫面狀態停留幾秒，超過 15 秒的列出場景 id 與秒數。
- [x] `links`：用 GET 抓說明欄的每個網址，會跟著轉址，列出不是 2xx 的網址。
  - User-Agent 固定用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；
  - 同一個網域間隔 1 秒，逾時 15 秒。
- [x] `thumbnail`：1280×720、小於 2 MB；縮到 320 寬時，標題字高仍然夠大。門檻值寫在程式裡，並註明怎麼訂出來的。
- [x] `facts`：最後一輪查核標成 NOT FOUND 的 claim id，已經沒有場景引用。
- [x] `captions`：lint 的過期警告（句子、章節、標題、說明、標籤）在品管裡算失敗；每秒字數超標只放進 warnings。
- [x] 所有純函式都有單元測試，I/O 包在薄薄一層裡；CI 沒有 Chromium 或 ffmpeg 也能跑測試。

## Steps

- [x] `tools/video/qa/`：各項檢查、`qa.json` 的組裝、CLI 子指令。
- [x] `pace`：2026-09-26 重排第二批時，是用本機腳本算停留時間的，做法見下面 Notes。把它改寫成純函式並加測試。
- [ ] 拿第二批三支（`chatgpt-ads-upgrade`、`gemini-student-offer`、`ai-agent-permissions`）實跑，應該全過；`pace` 應該是 0 個。
  - 還沒做：三支的工作區在正式主機上，這台機器沒有。等這張票合併、部署後，在主機的 worker 容器跑 `node tools/video/cli.mjs qa --slug <slug>` 三次。judge 端點上線前（或頻道立場還沒填時），`policy` 會是 11 項裡唯一沒過的（結束碼 1），其他 10 項應該全過、`pace` 0 個。

## How to verify

```bash
node --test tools/video/qa/*.test.mjs
npm run test:tools
node tools/video/cli.mjs qa --slug ai-agent-permissions
```

## Notes

- `pace` 的算法：每個場景的第一句開始時，畫面進入第一個狀態；之後每一句帶 `reveal` 的句子開始時，進入下一個狀態。一個狀態的停留時間，就是下一個狀態（或下一個場景）的開始時間減去它自己的開始時間。句子時間來自 `timeline.json`，場景與 reveal 來自 `video.json`。
- 連結檢查的網址不能帶任何個人資料；User-Agent 不能放個人 email。

### 2026-09-27 做完之後（claude-fable-5-1-video-qa）

- 檔案：`tools/video/qa/cli.mjs`（薄 I/O 層：讀工作區、呼叫 judge、寫 `review/qa.json`）、`checks.mjs`（assemble、render、narration、captions、metadata、disclosure 與 `qaReport`）、`pace.mjs`、`links.mjs`、`thumbnail.mjs`、`facts.mjs`、`policy.mjs`（judge 的請求與答案）、`test-images.mjs`（測試用的 JPEG／PNG 檔頭），每個模組一個 `*.test.mjs`，`qa.test.mjs` 用假的工作區跑整條指令。
- 範圍多加了 `tools/video/automation/client.mjs`：`policy` 要「透過既有的站台 client」呼叫 judge，client 的 `request` 沒有匯出，所以加了一個 `judgePolicy` 方法（只是新增一個方法，沒有動其他行為）。worker 那張票（scope `tools/video/automation`）之後可以照樣改這個檔。
- 結束碼：0 全過、1 有項目沒過、4 judge 端點連不上或 5xx（外部服務）。另外沿用整個 CLI 的慣例，權杖沒設或被撤銷（401）回 3（需要站主）。三種情況都照樣寫出 `qa.json`。`video.json` 有 lint 錯誤時和其他階段一樣：印「run lint first」、回 1、不寫檔。
- `final_sha256` 用 `core/approvals.mjs` 的 `sha256File`，和 `review/sync.mjs` 送成片關卡時算 `content_sha256` 的是同一個 helper，伺服器可以直接比。
- `policy` 的合約照 judge 那張票（PR #832）`apps/api/app/video_automation/judge.py` 的 `JudgePolicyIn`／`PolicyVerdict`，2026-09-27 依協調者的訊息改過一次。請求模型是 strict（多一個欄位就 422），所以只送三個欄位：`slug`；`script` 是旁白全文，每一句依序一行、場景之間空一行（`narrationScript`，最多 60,000 字）；`viewpoint` 是 `brief.md`「## 站主觀點」段落的文字（`ownerViewpoint`，用 `core/lint.mjs` 的 `briefSections` 取，沒有就空字串，最多 8,000 字）。字數用 code point 算，和 Python 的 `len` 一樣。答案 `{ stance, demo, advice, sponsored, passed, note }`：`passed` 是判定，`note`（像「Jev：符合立場 0.82、有示範 0.70、建議 0.05、業配 0.10，通過」）直接當 detail，過或沒過都是；沒有 `note` 才自己用四個分數組一句。沒有 `passed` 的答案算沒過。四個分數沒有另外放進 item（審核 payload 的 item 模型可能也是 strict，note 裡已經有數字）。
- `policy` 的錯誤對應：404（端點還沒部署）detail 固定 `judge endpoint not available`；409 `video_judge_not_enabled`（頻道立場空白）detail `channel stance is blank; the judge has nothing to judge against`，兩者都是沒過的項目、結束碼 1，不算外部失敗；429（`jev_budget_exhausted` 或工具的每小時上限）、502 `video_judge_upstream_failed`、其他 5xx 是外部服務失敗、結束碼 4（client 會先照既有規則重試 4 次再丟出來）；401 或沒權杖回 3。
- `facts`：讀 `docs/videos/<slug>/verify-<N>.md` 裡編號最大的那份，表格的判定欄是 `NOT FOUND`（大寫，後面可以接「（已改寫）」之類）的列，拿第一欄當 claim id，`12`、`c12`、`#12` 都當同一個，對照每個場景的 `claims`。第二批的人工查核報告第一欄是查核者自己的流水號，不是 claims.md 的 c 編號，所以在那三支上這一項只會擋到編號恰好相同的情況；自動產線的 verifier 拿得到 claims.md，報告表格用 c 編號就會真的擋到。沒有任何 `verify-*.md` 算沒過（沒查核）。
- `captions`：直接沿用 lint 對 `i18n/<locale>.json` 的警告（句子缺或過期、標題／說明／標籤／章節缺、過期或沒雜湊），全算失敗；只有「不再是章節的多餘章節標題」放 warnings（i18n-merge 會自己丟掉）。字幕檔要五個語系（`schema.mjs` 的 `LOCALES`）都有；`captions/manifest.json` 裡 `checkCues` 的問題，每秒字數超標放 warnings，其他（重疊、太寬、太多行）算失敗。
- `thumbnail`：尺寸與位元組自己讀 JPEG／PNG 檔頭。字高是估的：render 沒有記錄縮圖最後用的字級，所以照 `theme.css` 的 `.thumb h1`（136px、行高 1.1、最高 460px、可用寬 1280−72−340）和 `browser.mjs` 的 fitText 規則（每次縮 2px、最低 60%）重算一次，再乘 320/1280。門檻 `MIN_HEADLINE_PX_AT_PHONE = 24`（理由寫在常數旁邊：介於版型原尺寸的 34px 與 render 容許下限的 20px 之間，大約是三行滿版標題會縮到的大小；第一批交給機器的影片做完後再對照站主的判斷調整）。測試會對照 `theme.css` 與 `browser.mjs` 的原始碼，版型一改測試就紅。之後若 render 把縮圖實際字級記進 manifest，這裡可以改讀那個值。
- `disclosure`：依 `UPLOAD.md` 的規則，投影片＋一般 TTS 不勾、`format: drama` 一律勾，寫進 `upload/metadata.json` 的 `contains_synthetic_media`（對應 YouTube API 的 `containsSyntheticMedia`）與 `disclosure_reason`。寫入是冪等的（值相同就不動檔案），因為 `publish` 關卡的核准綁的是這個檔的雜湊。
- `render` 這一項讀 `frames/manifest.json`（visual_hash 要對得上，漫劇燒字幕時 speech_hash 與 subtitles_hash 也要）和 `frames/cache.json` 裡各狀態留下的版面問題（超框、缺字、字型沒載入、程式碼框切行）。render 只有在沒問題時才寫 manifest，所以 cache 是第二道確認。
- 這台機器沒有三支影片的工作區，所以「實跑」那一步留給主機（見 Steps）。
- `npm run test:tools` 在這個 worktree 一開始紅 15 項，全是 `pinyin-pro` 與 `@fontsource-variable/*` 沒安裝（worktree 沒有自己的 node_modules，Node 讀到主 checkout 舊的那份）；`npm ci` 之後 380 項全綠。
