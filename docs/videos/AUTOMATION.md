# 影片產線在主機上自動跑：設計

2026-09-25 定案。前提是 `docs/videos/DESIGN.md` 的產線（企劃 → 撰稿 → 查核 → 聽眾審稿 → 旁白 → 旁白檢查 → 畫面 → 成片 → 五語 CC → 送審）。原本整條由一個 Claude session 在站主的電腦上帶著代理跑；這份設計把它搬到正式站主機上，照後台的設定定時產生草稿。工作分成 5 張票，id 都是 `2026-09-25-video-auto-*`。

## 站主的決定

| 項目 | 決定 |
| --- | --- |
| 在哪裡跑 | 正式站主機 |
| 後台設定 | 各階段的 AI 模型、草稿排程與題材、成片參數、預算上限，都放在「影片審核」頁的「設定」分頁 |
| 關卡 | 選大綱、看成片、確認上架仍然等站主按；**旁白由 Jev 判斷，全數通過就自動核准** |
| 寫稿的模型 | 用網站後台的 API 金鑰，按用量計費。預設 Claude Sonnet 5 寫、Claude Opus 5.5 查核 |
| 題目來源 | 先看站上已查證的新聞與已發布的文章，不夠再用 Brave 搜尋補 |

**為什麼不用主機上已登入的 Claude Code／Codex 訂閱帳號**：`/admin/ai-accounts` 管的是站主個人的訂閱。把網站自己的自動化功能放到個人訂閱上違反 Anthropic 與 OpenAI 的消費者條款，而且額度用完就整個停（見 `tasks/done/2026-09-24-refresh-claude-plan-usage-automatically-from.md`）。所以寫稿與查核走 `ai_vendors` 的 API 金鑰，跟每小時自動新聞相同。

## 架構

```
後台「影片審核 → 設定」──寫入──> video_automation_settings（一列）
                                      │
video-worker 容器（Node＋Chromium＋ffmpeg，compose profile video）
  每 5 分鐘：GET /video/automation/next ──> 這一輪該做什麼（新草稿？哪支影片的下一步？）
  文字階段 ──> POST /video/ai/run（伺服器用該階段設定的模型；金鑰不出伺服器）
  查核     ──> 工人自己抓 claims.md 列的網址（Mokaair-editorial UA），把頁面文字交給查核模型
  旁白     ──> 既有的 /video/speech、/video/speech/transcribe、/video/speech/judge
  畫面／成片／字幕 ──> 容器裡的 tools/video（render、assemble、captions）
  送審     ──> 既有的 /video/reviews（review-push）；站主在 /admin/videos 決定，工人 review-pull
```

- **工人是現在的本機工具搬進容器**。`tools/video` 的每個階段照舊，只是企劃、撰稿、查核、聽眾審稿、翻譯這些原本由代理做的步驟，改成呼叫 `/video/ai/run`，提示詞沿用 skill 裡的 `references/prompts/*.md`。站主的電腦上也能跑同一個指令（`node tools/video/cli.mjs auto`），方便除錯。
- **金鑰只在 API 容器**。工人只持有一組影片工具權杖，用既有的配對流程取得：工人第一次啟動時印出驗證碼，站主在後台按「允許」，權杖存在工人的 volume。
- **排程在工人裡**，不另開 scheduler 容器：工人每 5 分鐘問 API 下一步，API 依設定判斷，同一時間只做一件事。這跟新聞自動化的 60 秒迴圈同一個思路，但影片一輪要跑幾十分鐘，用單一工人就夠了。
- **工作區**是具名 volume `video_work`（取代本機的 `~/mokaair-work/videos`）。成片、音檔不進資料庫，送審時照舊上傳到 `video_reviews`。

## 設定（`video_automation_settings`）

| 群組 | 欄位 | 預設 |
| --- | --- | --- |
| 開關 | `enabled` | 關 |
| 排程與題材 | 多久產生一次新草稿（小時） | 72 |
| | 每次幾個題目 | 1 |
| | 等站主的草稿達到幾支就先不產生新的 | 3 |
| | 題材範圍（關鍵詞清單） | AI、科技、AI 工具教學 |
| | 要避開的題材 | 投資建議、醫療建議、選舉政治 |
| | 題目來源：站上新聞與文章／Brave 搜尋 | 都開 |
| 各階段模型 | 企劃、撰稿、查核、聽眾審稿、字幕翻譯、字幕審稿，各選「廠商＋模型」（只列有金鑰、且支援結構化輸出的） | 企劃、撰稿、翻譯：Claude Sonnet 5；查核、聽眾審稿、字幕審稿：Claude Opus 5.5 |
| 成片參數 | 旁白聲音、風格、語速 | Gemini Sulafat，沿用 `docs/videos/README.md` |
| | 目標長度（分鐘） | 8–12 |
| | 字幕語系 | en、ja、ko、zh-CN |
| 預算 | 每月最多幾支草稿 | 8 |
| | 每月模型 token 上限（百萬） | 20 |
| | 每支最多查核幾輪、旁白最多重錄幾輪 | 3、2 |
| | 旁白每月字數、Jev 每日次數 | 沿用既有欄位，這裡只顯示用量 |
| 關卡 | 旁白 Jev 全數通過就自動核准 | 開 |

超過任何一個預算時，工人停在目前的步驟，審核頁顯示原因，不會悄悄降級成較便宜的模型。

## 一支影片的自動流程

1. **選題**：從站上最近 14 天已發布的 AI／科技新聞與文章，加上 Brave 搜尋結果，排除已經做過的題目與避開的題材。由企劃模型挑出題目、寫 `brief.md`（含 2–3 個大綱與「站主觀點」草稿）→ 送審「選大綱」。**停下來等站主。**
2. **站主選了大綱**之後：撰稿 → lint（錯誤會把 lint 訊息餵回撰稿模型，最多改 3 次）→ 查核（改超過 3 個事實就再查一輪，每輪都是新的對話、看不到上一輪的結論，等於換人查；最多照設定的輪數）→ 聽眾審稿 → lint。
3. **旁白**：tts → check-audio → 被標的句子重錄，最多照設定的輪數。全數通過且設定開著，就自動核准旁白；否則送審等站主。
4. **成片**：render → assemble → 翻譯 → 字幕審稿 → captions → 送審「看成片」。**停下來等站主。**
5. **站主核准成片**之後：package → 送審「確認上架」。上傳到 YouTube 與按公開仍然是站主在 Studio 做。

站主退回時，退回的理由存在審核紀錄。工人會把它交給下一次撰稿或聽眾審稿的模型；站主也可以直接放棄那支影片。

## 安全與成本

- `/video/ai/run` 只接受設定裡列出的階段名稱，模型由伺服器依設定決定，不能由工人指定；每次呼叫記下階段、模型、token 數與影片代號，超過每月上限就回 429。
- 工人抓網頁只用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` 當 User-Agent，每個網域間隔至少 1 秒，不登入任何網站。
- 工人容器照其他服務的加固方式：`cap_drop: ALL`、`no-new-privileges`、非 root 使用者、唯讀根目錄加上工作區 volume。
- 模型費用粗估：一支影片大約 40 萬輸入、10 萬輸出 token（企劃、撰稿、兩輪查核、聽眾審稿、四語翻譯與審稿）。實際數字在第一支自動影片之後記進這份文件。

## 分期與票

| 票 | 內容 | scope |
| --- | --- | --- |
| `video-auto-settings` | 設定表（遷移）、後台 API、工具讀取端點、「設定」分頁、旁白自動核准的規則 | `apps/api/app/video_automation`、遷移、`apps/web` 的影片審核元件與 admin.json |
| `video-auto-model-runner` | `/video/ai/run`、用量紀錄與每月上限、`/video/automation/topics`（站上新聞與文章＋Brave） | `apps/api/app/video_automation` 的 ai 與 topics 模組 |
| `video-auto-orchestrator` | `tools/video/automation`：自動流程的狀態機、呼叫模型、抓查核網頁、`auto` 指令 | `tools/video/automation`、`tools/video/cli.mjs` |
| `video-auto-worker-image` | 工人映像（Node＋Chromium＋ffmpeg＋字型）、compose 服務與 volume、工人迴圈 | `ops/video`、`docker-compose.prod.yml` |
| `video-auto-rollout` | 部署腳本加 `--profile video`（要站主同意）、配對工人、開啟設定、跑第一支 | 主機；repo 只改文件 |

前兩張依序做（都會改 `apps/api/app/models.py` 並各帶一個遷移）；第三張靠前兩張的端點；第四張可以和第三張同時做。
