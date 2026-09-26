# 影片產線在主機上自動跑：設計

2026-09-25 定案。前提是 `docs/videos/DESIGN.md` 的產線（企劃 → 撰稿 → 查核 → 聽眾審稿 → 旁白 → 旁白檢查 → 畫面 → 成片 → 五語 CC → 送審）。原本整條由一個 Claude session 在站主的電腦上帶著代理跑；這份設計把它搬到正式站主機上，照後台的設定定時產生草稿。工作分成 5 張票，id 都是 `2026-09-25-video-auto-*`。

## 站主的決定

| 項目 | 決定 |
| --- | --- |
| 在哪裡跑 | 正式站主機 |
| 後台設定 | 各階段的 AI 模型、草稿排程與題材、成片參數、預算上限，都放在「影片審核」頁的「設定」分頁 |
| 關卡 | 選大綱、看成片、確認上架仍然等站主按；**旁白由 Jev 判斷，全數通過就自動核准** |
| 寫稿的模型 | **主機上登入的 Claude 訂閱帳號（Claude Code）**，預設 Claude Sonnet 5 寫、Claude Opus 5.5 查核。每個階段也可以改用網站的 API 金鑰 |
| 題目來源 | 先看站上已查證的新聞與已發布的文章，不夠再用 Brave 搜尋補 |

**訂閱帳號**：
- 站主先決定用 API 金鑰，後來改成用 `/admin/ai-accounts` 管的 Claude 訂閱帳號。之前提醒過：2026-09-24 的票（`tasks/done/2026-09-24-refresh-claude-plan-usage-automatically-from.md`）記錄，網站自己的功能放在個人訂閱上，可能違反 Anthropic 與 OpenAI 的消費者條款，而且額度用完就會整個停住。站主 2026-09-25 表示自己看過條款，決定用訂閱全自動。
- 額度那一點的處理：沒有用量上限（站主 2026-09-26 的決定）。帳號依 A、B、C… 的順序輪流，一個帳號的 5 小時或每週額度用滿才換下一個，最後一個用滿再回到 A。全部帳號都用滿就等額度重置，不會自己改用 API 金鑰。舊的「用到幾 % 就先停」欄位已拿掉，資料表欄位還在但不再讀取。
- **只提供 Claude Code**：`claude -p --tools ""` 可以關掉所有工具，只收文字、只回文字。`codex exec` 沒有關掉 shell 的開關，read-only 沙箱仍然讀得到這個服務能讀的所有檔案，包括網站的 `.env`；工人又會把網頁內容送進提示詞，所以 Codex 不提供。

## 架構

```
後台「影片審核 → 設定」──寫入──> video_automation_settings（一列）
                                      │
video-worker 容器（Node＋Chromium＋ffmpeg，compose profile video）
  每 5 分鐘：GET /video/automation/next ──> 這一輪該做什麼（新草稿？哪支影片的下一步？）
  文字階段 ──> POST /video/automation/run（伺服器照該階段的設定）
                 ├─ 訂閱：API ──HMAC──> 主機的 AI 帳號代理（ai_accounts_agent.runs）──> claude -p --tools ""
                 └─ API 金鑰：API 直接呼叫廠商（金鑰不出 API 容器）
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
| 各階段模型 | 企劃、撰稿、查核、聽眾審稿、字幕翻譯、字幕審稿，各選「Claude Code（訂閱帳號）」或某家 API 的模型 | 全部用 Claude Code 訂閱帳號；企劃、撰稿、翻譯用 Claude Sonnet 5，查核、聽眾審稿、字幕審稿用 Claude Opus 5.5 |
| 各階段常設指示 | 企劃、撰稿、查核、聽眾審稿、字幕翻譯、字幕審稿各一段文字（每格最多 4000 字），工人接在該階段提示詞之後，投影片與漫劇都適用；清空就是不加。分頁的「目前的提示詞」顯示工人最後送出的完整指示（`video_stage_prompts`，每階段每格式各留最新一份，跑過才有） | 空 |
| 成片參數 | 旁白聲音、風格、語速 | Gemini Sulafat，沿用 `docs/videos/README.md` |
| | 目標長度（分鐘） | 8–12 |
| | 字幕語系 | en、ja、ko、zh-CN |
| 預算 | 每月最多幾支草稿 | 8 |
| | 每月模型 token 上限（百萬），只算 API 金鑰的呼叫 | 20 |
| | 訂閱帳號用到幾 % 就先停（5 小時或每週額度） | 80 |
| | 每支最多查核幾輪、旁白最多重錄幾輪 | 3、2 |
| | 旁白每月字數、Jev 每日次數 | 沿用既有欄位，這裡只顯示用量 |
| 關卡 | 旁白 Jev 全數通過就自動核准 | 開 |

超過任何一個預算時，工人停在目前的步驟，審核頁顯示原因，不會悄悄降級成較便宜的模型。

模型交不出能用的答案時：
- 原文會存到 `<工作區>/<slug>/answers/`，這一輪就結束，不會馬上重試。
- 同一個階段連續兩輪都失敗，這支影片就標成卡住，審核頁清單的第一項會寫出原因。
- 外部服務暫時失敗，例如旁白檢查或送審，同樣會結束這一輪，但不算進卡住的次數。

2026-09-25 曾經有一輪在兩分鐘內重問撰稿模型 6 次，花了約 10.6 萬 token，所以加上這條規則。

要讓工人整個停下來，在工作區放一個 `STOP` 檔：`docker compose -f docker-compose.prod.yml exec -T video-worker touch /var/lib/mokaair/video-work/STOP`。刪掉這個檔，下一輪就會繼續。

## 一支影片的自動流程

1. **選題**：從站上最近 14 天已發布的 AI／科技新聞與文章，加上 Brave 搜尋結果，排除已經做過的題目與避開的題材。由企劃模型挑出題目、寫 `brief.md`（含 2–3 個大綱與「站主觀點」草稿）→ 送審「選大綱」。**停下來等站主。**
2. **站主選了大綱**之後：撰稿 → lint（錯誤會把 lint 訊息餵回撰稿模型，最多改 3 次）→ 查核（改超過 3 個事實就再查一輪，每輪都是新的對話、看不到上一輪的結論，等於換人查；最多照設定的輪數）→ 聽眾審稿 → lint。
3. **旁白**：tts → check-audio → 被標的句子重錄，最多照設定的輪數。全數通過且設定開著，就自動核准旁白；否則送審等站主。
4. **成片**：render → assemble → 翻譯 → 字幕審稿 → captions → 送審「看成片」。**停下來等站主。**
5. **站主核准成片**之後：package → 送審「確認上架」。上傳到 YouTube 與按公開仍然是站主在 Studio 做。

站主退回時，退回的理由存在審核紀錄。工人會把它交給下一次撰稿或聽眾審稿的模型。

**放棄一支影片**：影片頁最下面有「放棄這支影片」，要寫原因，並再確認一次。
- 放棄之後，等站主決定的項目都會關掉，預覽檔會刪除，工具也不能再送審這支影片。
- 工人下一輪會把它標成「已放棄」，不再處理，它也不再佔「等站主的草稿」名額。
- 這支影片的題目仍算做過。
- 放棄不能復原。退回大綱的話，工人會用同一個代號重寫，所以題目本身不對時要用放棄，不要用退回。

**不重複選題**（2026-09-25 第一支自動草稿挑到第二批已經做好的題目之後加上）：
- 企劃模型會收到以下幾類影片，每支附上它改寫的站內文章（`source_guide`）：
  - `docs/videos` 裡的影片；
  - 工人自己做過的影片；
  - `/admin/videos` 上的每一支影片，包括分支上做的、已放棄的。
- 企劃的主要文章（`source_guide`，沒有的話取它引用的第一篇站內文章）如果跟前面任何一支相同，這份企劃就不採用。
- 分支上的影片用 `review-push --report-only` 登記到審核頁，這個指令不會送出任何審核項目。

## 漫劇（2026-09-26 加，設計在 `DRAMA.md`）

工人也會做 AI 漫劇。它不挑題：**站主在 `/admin/videos` 發起**（故事前提或改編的文章、風格、長度），伺服器排進 `video_drama_requests`，工人每輪在做排程草稿之前先問 `GET /video/automation/drama-requests/next`，有就用漫劇版的企劃提示寫故事聖經與大綱、`POST …/{id}/start` 認領（寫下影片代號），然後照投影片的規矩送審「選大綱」。設定分頁的「AI 漫劇」要開著，否則工人不會問。

之後的步驟是 `DRAMA_STEPS` 的順序（`status` 會印）：撰稿（漫劇版提示：每鏡英文提示詞、一句一個說話者）→ 連貫性查核 → 聽眾審稿 → **look**（設定圖，judge 打分）→ 站主在後台每個角色選一張（`look` 關卡）→ tts（依說話者分批）→ check-audio → 旁白關卡 → **keyframes**（judge 不過換 seed）→ **storyboard 關卡**（設定開「分鏡自動核准」且 judge 全過時伺服器自己核准）→ render（卡片、字幕條、縮圖）→ **clips**（最貴，送出前對單支上限把關）→ music → assemble → 五語 CC → 成片關卡 → package → 上架確認；上架確認後工人 `POST …/{id}/done`。

三種失敗各有處理：

- **品檢沒過（結束碼 1）**：`look`／`keyframes`／`clips` 把沒過的角色或鏡頭連 judge 的評語留在 manifest（`needs_review`），工人交給撰稿模型的 FIX 模式改提示詞（只改那幾個 id），下一輪重跑該階段；每種最多 2 輪，之後卡住並在審核頁寫原因。站主退回 look 或 storyboard 時也走同一條，退回的話一起交給模型。
- **要站主（結束碼 3）**：單支上限、漫劇沒開、沒金鑰、關卡沒核准——卡住，理由寫在審核頁的清單第一列。
- **供應商或額度（結束碼 4）**：這一輪結束，下一輪再試；每月預算由伺服器以 429 擋，請求不會送到供應商。

`settle()` 依設定寫進 `video.json`：`format: "drama"`、`look.preset`（模型沒寫時用設定的風格預設）、`subtitles.burn_in`、關掉音樂時拿掉 `music`。工人回報影片時帶 `format`，後台列表才分得出漫劇並顯示 `media_usd`。

## 安全與成本

- `/video/automation/run` 只接受設定裡列出的階段名稱，模型由伺服器依設定決定，工人不能指定。每次呼叫都記下階段、模型、token 數與影片代號。上限有兩個，超過都回 429：
  - 每月 token 上限，只算 API 金鑰的呼叫；
  - 每月草稿數，訂閱與 API 都算。
- 訂閱帳號的執行一律經過主機的 AI 帳號代理，帶 HMAC 簽章，走 Unix socket。
  - 代理用 `--tools ""` 關掉所有工具，也不載入任何 MCP、不留 session。
  - 執行環境從零建立，帶不到代理的金鑰；工作資料夾用完就刪。
  - 同一時間只跑一個。
  - 工人容器碰不到帳號的登入憑證。
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
