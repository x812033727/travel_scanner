# 供應商與方案：伺服器 API、Hailuo 網頁訂閱、Kling CLI／MCP

給用手寫、用手導、用手跑漫劇的代理：同一個鏡頭的素材今天有三條路可以買，這一篇把三條並排、算一鏡與一集各要多少錢、說外部素材現在怎麼進產線（以及產線會不知道什麼）、最後是權利與安全。它不重複別處已經寫好的事：產線的步驟、指令與結束碼在 `.agents/skills/youtube-video/references/drama.md`；第一版的供應商決定與設計在 `docs/videos/DRAMA.md`；Veo 3.1 Lite 的鏡頭契約與十部動畫的製作規格在 `.agents/skills/youtube-video/references/animation-production.md`；一個鏡頭的 `camera`／`motion`／`prompt` 怎麼寫、同一鏡怎麼改寫給 Hailuo 的表單與 Kling 的鏡頭控制，在 animation-camera skill。

每個數字都標來源：**價目**是官方頁或目錄檔讀到的（附日期）；**工具規定**是 `tools/video` 或 `apps/api` 裡的常數（附檔名）；**模型限制**是供應商文件寫的；**實測**是在站主的帳號上送出、下載或讀到的（附日期；2026-10-04 是 Hailuo 的一支片段與 Kling CLI 的輸出）；**推算**是本文從前兩者算出來、沒有在生成器裡核對過的；**未驗證**是第三方整理或根本讀不到的。價目與積分會不預告就改：定一場戲的錢之前，先把本文 §5 的頁面再讀一遍，把日期更新。

## 1. 三條路線並排

| | 伺服器 API（產線本來的路） | Hailuo 網頁訂閱（hailuoai.video） | Kling（官方 CLI 或 MCP；社群 MCP＋開發者 API） |
| --- | --- | --- | --- |
| 誰在呼叫 | `node tools/video/cli.mjs clips` 經網站的媒體端點叫 Gemini／MiniMax；金鑰只在站上 | 代理在內建瀏覽器裡操作 SPA，用**站主的登入**；要上傳本機的關鍵影格（圖生影片）得改用 Claude in Chrome 或 Playwright（§1.2，還沒試） | 官方 CLI `kling`（站主 2026-10-04 選的）或官方 MCP 連接器，都登入**站主的 Kling 帳號**，同一個助理只裝一種（§1.3）；社群 MCP：開發者 API 的 access key／secret key |
| 計價 | 每秒：`usd_per_second × seconds`，解析度不改價（工具規定，`apps/api/app/video_media/meter.py` `usd_for`） | 月費換積分，積分月底歸零；用完可加購 | 會員月費換積分；開發者 API 另賣資源包，兩邊不互通 |
| 片段模型 | `apps/api/app/video_media/catalog.py` 列的：Omni 1.1 Flash、Veo 3.1／Fast／Lite、MiniMax-H3 | H3、H3 Max、Hailuo 2.0／2.3／1.0、Sora 2、Veo 3.1 | CLI 列的 `kling-video-v3_0`、`v3_0_omni`、`v3_0_turbo`、`o1`、`v2_5`、`v2_6`，另有 `motion_control`（實測 2026-10-04，§1.3） |
| 首尾格與參考圖 | 首格必帶；參考圖最多 4（`MAX_REFERENCES`，`apps/api/app/video_media/schemas.py`；目錄寫 H3 9 張、Pro Image 14 張是供應商上限，不是我們送得出的）；Lite 不收參考圖 | 首格與末格；參考上傳區「參考 (0/12)」 | `kling-video-v3_0`：`first_image`＋`tail_image`、elements；`v3_0_omni`／`o1`：`image_1`…`image_7`；`v3_0_turbo` 只有 `first_image`（實測 2026-10-04） |
| 品檢 | ffmpeg（`tools/video/media/qc.mjs`）＋ judge 自動跑，不過換 seed，最多 2 次（`MAX_CLIP_TAKES`，`tools/video/media/clips.mjs`） | 站方沒有；`clips import` 匯入時跑同一組 ffmpeg 檢查，judge 要帶 `--judge` | 同左 |
| 快取、帳本、預算 | `media/cache.json`（同一請求不付兩次）、`media/ledger.json`（每筆花費）、伺服器的每月預算與單支上限 | 沒有快取與伺服器預算；`clips import` 把點數與秒數記進帳本（`status: "imported"`） | 同左 |
| 進產線 | 直接 | 下載後 `clips import`（§3） | 同左 |
| 浮水印、商用 | 無浮水印；依各供應商條款 | 免費下載有浮水印；Standard 以上沒有，且保留 IP 含商用（條款，2026-10-03 讀）。付費帳號也要走「無水印下載」：結果卡 `<video>` 的 src 是有浮水印的版本（實測 2026-10-04，§1.2） | 付費方案去浮水印、「Generated content is for commercial use」（會員頁，2026-10-03 讀） |
| 併發 | 伺服器每小時 240 次圖片送出、360 次 judge（`apps/api/app/video_media/admin_api.py`）；每月 3,000 片段秒、1,500 張圖、3,000 次 judge、60 首音樂（預設，`apps/api/app/video_automation/models.py`） | 方案表：8–12 個排隊、1–2 個執行；條款另寫付費「最多五個同時」 | 付費方案：排隊不限、fast-track |
| 今天能用在 | 任何漫劇；有 production profile 的作品只能用 profile 指定的模型 | **沒有** production profile 的漫劇（§3：profile 會拒絕非指定的供應商） | 同左；repo 沒有 Kling adapter（`tasks/open/2026-09-26-video-drama-kling-provider-card.md`，P3） |

### 1.1 伺服器 API

產線的每一筆錢都走這裡：`look`、`keyframes`、`clips`、`music` 四個階段各自 `--dry-run` 印估價，送出前用 `media/ledger.json` 對單支上限 `max_usd_per_video`（預設 US$200）把關，超過結束碼 3；每月預算由伺服器以 429 擋，請求不會送到供應商（`tools/video/media/stages.mjs` `Stage.spend`、`apps/api/app/video_media/meter.py`）。judge 門檻 `judge_min_score` 預設 7（`apps/api/app/video_automation/models.py`）。

| 模型 | 目錄價（`catalog.py`，2026-09-26 讀，圖片 2026-09-28 再讀） | 目錄限制 | 官方頁的差異 |
| --- | --- | --- | --- |
| gemini-3-pro-image | US$0.134／張，1K 與 2K 同價 | 參考圖 14（我們送 4） | — |
| gemini-omni-1.1-flash | US$0.15／秒 | 4–10 秒、720p／1080p、參考圖 3、原生音訊 | 預設片段模型 |
| veo-3.1-lite-generate-preview | US$0.08／秒 | 4／6／8 秒；1080p 固定 8 秒；無參考圖；preview | 官方 720p 是 US$0.05／秒，目錄按 1080p 計（目錄註解） |
| veo-3.1-fast-generate-001 | US$0.12／秒 | 4／6／8 秒 | — |
| veo-3.1-generate-001 | US$0.40／秒 | 4／6／8 秒；1080p 只有 8 秒 | — |
| MiniMax-H3 | US$0.13／秒 | 目錄 4–10 秒、768p／2k、參考圖 9 | 官方 768P US$0.08／秒、2K US$0.13／秒、4–15 秒整數（platform.minimax.io，2026-10-03 讀）；`meter.usd_for` 不看解析度，768p 也記 0.13 |
| lyria-3.5 | US$0.08／首 | — | — |
| judge | US$0.01／次（`JUDGE_USD_PER_CALL`） | — | 伺服器按實際 token 計，帳本記這個常數 |

買幾秒由 `clipSeconds`（`tools/video/media/clips.mjs`）決定：Veo 3.1 系列 1080p 固定 8 秒，其他是 `clamp(ceil(frames/30), 4, 10)` 再往上貼齊模型的秒數表；伺服器對不在表裡的秒數回 422（`apps/api/app/video_media/jobs.py`）。一個 3 秒的對白鏡在 Omni／H3 買 4 秒、在 Lite 1080p 買 8 秒。帳本記的是伺服器的 `usd_estimate`（目錄價），不是供應商帳單：試作到現在 `actual_billed_usd` 還是空的（`docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`）。

負面限制依模型處理：`apps/api/app/video_media/providers/gemini_video.py` 對 Lite 省略不支援的 `parameters.negativePrompt`，完整 `look.negative` 接成 `\n\nAvoid: …` 進主提示；非 Lite 保留原參數。不要沿用清空已核准 look 的舊權宜（歷史失敗與修正在 `error-catalogue.md` #23）。MiniMax 的 adapter 仍沒有負面欄位，把它接成 `. Avoid: …` 送進 prompt（`apps/api/app/video_media/providers/minimax.py`）。

### 1.2 Hailuo 網頁訂閱

訂閱頁 `/zh-Hant/subscribe` 是 React SPA，WebFetch 只拿得到殼；下面的數字是 2026-10-03 在內建瀏覽器讀到的，條款來自 `hailuoai.video/doc/payment-policy.html`（同日 WebFetch 再讀一次，一致）。標「實測 2026-10-04」的都來自同一件事：那天在站主的 Max 帳號上送了一支文生影片（MiniMax H3、2K、5 秒、16:9），量到的東西集中在本節的「實測的一支」。

| 方案 | 月繳 | 年繳（換算每月） | 積分／月 | 排隊／執行 | 圖片 | 無限生成 |
| --- | --- | --- | --- | --- | --- | --- |
| Free | US$0 | — | 一次性試用積分，只有 Hailuo 系列 | 4／1 | — | — |
| Standard | US$14.99 | US$8.40（US$100.80／年） | 1,000 | 8／1 | — | — |
| Pro | US$54.99 | US$30.40 | 4,500 | 8／2 | 1K 無限（Nano Banana Pro／2、Seedream 4.5、GPT Image 1.5） | — |
| Master | US$119.99 | US$71.20 | 10,500 | 12／2 | 2K 無限 | — |
| Max | US$199.99 | US$184.00（US$2,208／年） | 27,000 | 12／2 | 4K 無限 | 積分用完後無限生成、進較慢的隊列。**哪些模型，兩個來源說法不同**（2026-10-03 同日讀）：方案表寫「海螺 2.0／2.3 模型 無限制」，FAQ 寫「MAX 會員可以使用海螺 1.0 和 2.0 系列模型無限制生成」；H3 兩邊都不在。`SKILL.md`、`cost-model.md` 與 `episode_estimate.mjs` 的 PLANS 都指這一格 |

條款（價目，2026-10-03）：會員積分一個月到期；加購 US$1 換 70 積分，有效到購買後第二個日曆年的 12 月 31 日；付費方案「retain any and all intellectual property rights to such content, including the right to use it for commercial purposes」；免費下載有浮水印、Standard 以上沒有；取消不退款；生成失敗或**內容審查不過**自動退積分（所以有內容審查）。條款頁還列著舊方案 Unlimited US$94.99 與 Ultra US$124.99，訂閱頁沒有。

**積分怎麼換秒**：H3 2K 每秒 12 積分是**實測 2026-10-04**——建立列「創建」旁邊顯示這次送出要扣的積分，H3 2K 5 秒顯示 60，送出後餘額 27,150 → 27,090；跟先前用訂閱頁每方案「約可做幾秒」反推的數字一致。H3／H3 Max 768P 每秒 7 積分、H3 Max 480P 每秒 4 積分仍是**推算**（同一個反推，四個方案都對得上；768P 沒有量）。所以一段 8 秒 2K 是 96 積分（12 × 8），8 秒 768P 是 56 積分（推算）。訂閱頁自己標的「每秒美元」（Standard：2K US$0.101、768P US$0.059；Pro 以上：2K US$0.081、768P US$0.047、480P US$0.027）**只在年繳價成立**（375 秒 × 0.081 ≈ US$30.40，就是 Pro 的年繳月價）；月繳要用下表。

| 每秒 | Standard | Pro | Master | Max | 加購積分 |
| --- | --- | --- | --- | --- | --- |
| 美元／積分 | 月繳 0.0150；年繳 0.0084 | 0.0122；0.0068 | 0.0114；0.0068 | 0.0074；0.0068 | 0.0143 |
| H3 2K（12 積分，實測 2026-10-04） | 0.180；0.101 | 0.147；0.081 | 0.137；0.081 | 0.089；0.082 | 0.171 |
| H3 768P（7 積分，推算） | 0.105；0.059 | 0.086；0.047 | 0.080；0.047 | 0.052；0.048 | 0.100 |
| 每月 2K 秒數 | 84 | 375 | 875 | 2,250 | — |
| 每月 768P 秒數 | 143 | 643 | 1,500 | 3,857 | — |

模型與方案（訂閱頁）：H3 4–15 秒 768p／2K；H3 Max 5–15 秒 480p／768p；Hailuo 2.3 6 秒 768p／1080p（Pro 以上 10 秒）；Hailuo 2.0（首尾格）6 秒 512p／768p／1080p（Pro 以上 10 秒）；Sora 2 4／8／12 秒 720p；Veo 3.1 8 秒 720p／1080p；Hailuo 1.0 6 秒 720p。各模型每段扣幾積分在生成器的建立列（「創建」旁）看得到：H3 2K 實測過（上段），H3 768P 與 H3 Max 是推算；Hailuo 2.3、Sora 2、Veo 3.1 在這裡的積分**未驗證**。注意 H3 沒有 1080p：2K 的輸出是 2560×1440（實測 2026-10-04），768P 在 1080p 之下（輸出尺寸沒量）；production profile 要求原生 1920×1080（§3）。

**實測的一支**（2026-10-04，站主的 Max 帳號，文生影片，MiniMax H3、2K、5 秒、16:9；只有這一支，768P 與圖生影片都沒量）：

- 積分：扣 60（12／秒），餘額 27,150 → 27,090。
- 時間：送出到完成約 4 分 40 秒，當時沒有別的在排隊。
- 輸出：2560×1440、24 fps、124 格、5.167 秒、h264 約 6 Mbps，帶一條 AAC 音軌。所以 2K 不是 1920×1080，production profile 的原生 1080p 檢查不收（§3）；尺寸與 fps 都在 `tools/video/media/qc.mjs` 的下限（1280×720、23 fps）之上。音軌是模型生成的，成片不能用：`assemble` 的畫面段落只取影像、帶 `-an`（`tools/video/assemble/drama.mjs` 的 `encodeArgs`），在別處用這個檔要自己去掉。
- 設定面板的選項：比例 自動／21:9／16:9／4:3／1:1／3:4／9:16，解析度 768p／2K，時長 4–15 秒整數。**比例預設是 21:9，要改。**
- 浮水印：結果卡 `<video>` 的 src 是有浮水印的版本；乾淨的檔怎麼拿在下面第 6 步。

**怎麼操作**（SPA 要在瀏覽器裡跑；登入都是站主做的，代理不輸入密碼、不經手 cookie 與權杖、不建帳號、不用自己的帳號）。哪個瀏覽器做得到什麼（實測 2026-10-04）：

- **文生影片**在 Claude 桌面版的內建瀏覽器裡做得完；站主的登入會留在 pane。
- **圖生影片要上傳這一鏡的關鍵影格，內建瀏覽器做不到**：它沒有檔案上傳的工具，頁面對 loopback 伺服器的 fetch 也被擋（`net::ERR_BLOCKED_BY_CLIENT`），幾 MB 的圖沒有別的路進表單。要用 Claude in Chrome 的檔案上傳（站主在那個 Chrome 裡登入），或 Playwright 用 `launchPersistentContext` 指向站主自己登入過的 profile。**這一條還沒試過**（未驗證）。

1. 站主登入後開建立頁（圖生影片是 `/create/image-to-video`，2026-10-03 讀；實測的那一支是文生影片）。pane 要顯示著：隱藏時選單打不開、截圖會逾時。
2. 圖生影片：把這一鏡通過 judge 的關鍵影格（`keyframes/manifest.json` 的 `file`，sha256 一起抄下來）上傳成首格；需要末格就上傳 `end_frame.file`。上傳不在內建瀏覽器裡做（上面第二點）。
3. 選模型，再開設定面板選比例、解析度、時長（選項在「實測的一支」）：**比例預設 21:9，改成 16:9**；H3 的時長是整數 4–15，用 `clips --dry-run` 印的需求秒數，不要照 Lite 的固定 8。pane 的窄寬度下那顆寫著比例／解析度／時長的設定鈕被藏起來；把視窗模擬成 1280×800 之後它在 DOM 裡，但座標點擊點不中，要在頁面 JS 裡點——設定鈕是含「21:9」字樣的 `div.cursor-pointer`，面板裡的選項也用 JS 點（實測 2026-10-04）。
4. 提示詞貼 `--dry-run` 印出的 clip prompt（`motion` ＋ `camera` ＋ `look.motion`，`tools/video/media/clips.mjs` `clipPrompt`）。提示框是 Slate 編輯器（`#video-create-textarea`）：先在頁面 JS 裡 focus，再用鍵盤輸入（實測 2026-10-04）。表單有沒有負面提示欄位沒有核對；沒有就照 MiniMax adapter 的做法，在最後接 `Avoid: …`。
5. 「創建」旁邊顯示這次送出要扣的積分（實測：H3 2K 5 秒顯示 60）；送出前後各記一次餘額核對，扣了多少就是這一鏡的價。1–2 個執行、8–12 個排隊，一集 60 鏡要分批等。一支 H3 2K 5 秒、沒有別的在排隊時，送出到完成約 4 分 40 秒（實測 2026-10-04，只有這一支）；Max 用完積分後的無限生成不含 H3（哪些模型見上表 Max 列），進較慢的隊列，那個隊列多久沒有量過。
6. 下載：**不要抓結果卡上 `<video>` 元素的 src**。那個檔（檔名含 `_video_raw_`）是有浮水印的版本，右下角有「MINIMAX | Hailuo AI」。乾淨的檔走「全部下載 → 無水印下載」：它呼叫 `POST /v2/api/multimodal/video/batch_download`，回應的 `downloadURLWithoutWatermark` 是 `cdn.hailuoai.video` 上的公開網址（實測 2026-10-04）。
7. `clips import --provider hailuo-web --plan <方案> --credits <第 5 步的差額>`（程序只寫在 `stage-preconditions.md` 最後一節）：它跑 `qc.mjs` 的黑格／凍格／切鏡／PSNR、寫 manifest 條目、記帳本。**這些 ffmpeg 檢查看不出浮水印**：第 6 步下載錯版本，匯入照樣通過；只有 `--judge` 的 `no_text` 題（`tools/video/media/clips.mjs` 的 `clipRubric`）可能抓到，所以下載完自己看一眼右下角。站方的任務 id、送出與完成時間、提示詞的雜湊工具不記，要留就寫進 `--note`，或照試作的 `docs/videos/series-plans/competition-20261002/cost-ledger.csv` 那套欄位另外記。

內建瀏覽器的已知限制（2026-09 實測）：pane 隱藏時頁面是 `visibilityState: hidden`，`IntersectionObserver` 與 `requestAnimationFrame` 都不會觸發，懶載入的區塊看起來像「沒有」；pane 最多 9 個分頁；多代理同時操作會觸發站方的機器人牆，過一小時就好——那是工具故障，不是頁面的結論。2026-10-04 在這個表單上再量到三件：pane 隱藏時選單打不開、截圖逾時；沒有檔案上傳工具；頁面 fetch loopback 伺服器被擋。把檔案轉成 base64 分段貼進頁面、再用 `DataTransfer` 塞給檔案欄位，對幾 MB 的關鍵影格行不通，不要試。

### 1.3 Kling

**會員**（kling.ai 會員頁，2026-10-03 在內建瀏覽器讀，月繳視圖；WebFetch 同日只拿到殼）：

| 方案 | 標價／月 | 首月 | 之後每月（月繳 12% off） | 積分／月 | 頁面標的「每 100 積分」 |
| --- | --- | --- | --- | --- | --- |
| Standard | US$10 | US$6.99 | US$8.80 | 660 | US$1.06（是首月價算的） |
| Pro | US$37 | US$25.99 | US$32.56 | 3,000 | US$0.87 |
| Premier | US$92 | US$64.99 | US$80.96 | 8,000 | US$0.81 |
| Ultra | US$180 | US$127.99 | US$159.99 | 26,000 | US$0.49 |

年繳 34% off。每個付費方案：排隊不限、fast-track、1080p、圖片放大、去品牌浮水印、影片延長、商用；Pro 以上先用新功能；一次最多出 4 支（Basic 1）；高階有 4K。每段扣幾積分**未驗證**：第三方 2026 年的整理說 3.0 Omni 標準模式 5 秒約 35–45 積分、專業模式約 70；官方 CLI 的 `who_am_i` 列模型與參數、不給積分價，而 2026-10-04 授權進來的帳號是 NORMAL、0 積分，一支都沒生成（見下）。本文的 Kling 美元數全部建立在「標準 5 秒 40 積分、10 秒 80 積分」這個未驗證的假設上。第三方說的「Kling 只有 5 秒或 10 秒」對 3.0 不成立（`kling-video-v3_0` 是 3–15 秒整數，實測 2026-10-04），但 5、10 以外的秒數扣幾積分沒有任何來源。

**官方的兩條路**（指南 `kling.ai/app/mcp/guide`，登入後讀得到；實測 2026-10-04）。指南說同一個助理只裝其中一種：

- **MCP**：端點 `https://kling.ai/mcp`；在 Claude 是 Customize → Connectors → Add custom connector，用 Kling 帳號登入。
- **CLI**（站主 2026-10-04 選的）：npm 套件 `@klingai/cli-global`（2026-10-04 是 0.2.1，maintainer `klingai-fe`），執行檔 `kling`。`kling login` 開系統預設瀏覽器做 OAuth（PKCE；scope 是 `generation.create`、`generation.read`、`account.credit.read`），權杖存在 `~/.kling/.credentials`。同意由站主在瀏覽器裡按；代理不讀、不貼那個檔。

指令與 MCP 的工具一對一：`who_am_i`、`text_to_video`、`image_to_video`、`omni_ref_video`、`text_to_image`、`image_to_image`、`motion_control`、`motion_library_list`、`element_create`／`element_list`／`element_get`／`element_update`／`element_delete`、`query_tasks`、`file_upload`、`account`、`tool_list`、`feedback`、`logout`。

- `kling account` 回 `membershipType` 與 `availableRemainCredits`：讀起來是**會員積分**，不是開發者資源包；還沒有用一次付費生成確認（未驗證）。
- `kling who_am_i` 列模型與參數，不給積分價。

`image_to_video` 的模型（NORMAL 免費帳號列出的，**全部只有 720p**；實測 2026-10-04）：

- `kling-video-v3_0`：時長 3–15 秒整數；輸入 `first_image` 與 `tail_image`；elements；`enable_audio` 預設 true；`prefer_multi_shots` 預設 **true**。
- `kling-video-v3_0_omni` 與 `kling-video-o1`：輸入 `image_1`…`image_7`；`aspect_ratio` 16:9／9:16／1:1；`o1` 是 3–10 秒。
- `kling-video-v3_0_turbo`：只有 `first_image`。
- `kling-video-v2_5` 與 `kling-video-v2_6`：5 或 10 秒。

**進產線時 `enable_audio` 與 `prefer_multi_shots` 都要傳 false**：一鏡是一個連續鏡頭（模型自己切鏡是 `tools/video/media/qc.mjs` 會擋的那一類），片段的聲音成片不用。

**還沒驗的**：授權進來的帳號顯示 `membershipType` NORMAL、0 積分，所以沒有生成任何東西。每支扣幾積分、付費方案在 CLI 上有沒有 1080p（會員頁寫付費方案有 1080p）、CLI 扣的是不是會員積分，都還是**未驗證**；先用 `kling account` 看到付費方案與積分，生成一支、記前後差額，再改本文。CLI 做的片段匯入時用 `--provider kling-mcp`（`clips import` 只有 `hailuo-web`、`kling-mcp`、`external` 三個值），是 CLI 做的就寫進 `--note`。

**社群 MCP**（github.com/199-mcp/mcp-kling，2026-10-03 讀 README）：用開發者 API 的 access key 與 secret key 自動簽 JWT，扣的是**資源包**，不是會員積分；工具有 `generate_video`（5 或 10 秒、標準／專業、cfg_scale、鏡頭控制）、`generate_image_to_video`（圖生影片，鏡頭控制 `static`／`zoom`／`pan`／`auto` 加一段 motion prompt）、`extend_video`、`create_lipsync`、`generate_image`（KOLORS）、`get_account_balance`、`get_resource_packages`、`list_tasks`；結果下載到本機 `./downloads/` 底下分類資料夾。對應我們的運鏡字（詳見 animation-camera skill）：`locked`→`static`，`push-in`／`pull-out`→`zoom`（方向寫進 prompt），`pan-left`／`pan-right`→`pan`，`drift` 沒有對應，用 `static` 加 motion prompt。它的 `generate_video` 只給 5 或 10 秒，是這個社群工具的限制，不是 Kling 3.0 的。

**開發者 API**（kling.ai/dev；頁面是殼，數字是第三方整理，**未驗證**）：試用 US$9.80／100 units（30 天）、US$98／1,000；Standard US$700／5,000、US$2,100／15,000、US$4,200／30,000、US$7,560／60,000，180 天有效、20 併發；3.0 Omni 標準 5 秒約 US$0.42、10 秒約 US$0.84、專業 5 秒約 US$0.56；1080p 無音訊約 US$0.112／秒、有原生音訊 US$0.168／秒、4K 約 US$0.42／秒。會員方案沒有 API 權限，API 的額度也不會進網頁生成器。

### 1.4 MiniMax 預付套餐

platform.minimax.io 的 Video Packages（2026-10-03 讀）：Standard US$1,000／3,760 video points／1 個月／RPM 20／省 5%；Pro US$2,500／9,920／RPM 30／10%；Scale US$4,500／18,900／RPM 40／15%；Business US$6,000／26,780／RPM 50／20%。頁面明寫「MiniMax H3 is not supported yet」，H3 走 pay-as-you-go 或聯絡業務。我們的 adapter 只送 H3，所以套餐今天對產線沒有用；points 換秒的匯率沒讀。

## 2. 一鏡與一集的錢

**一段 8 秒、1080p 等級的片段，一次成功**（美元；伺服器路線另加 judge US$0.01）：

| 路線 | 一段 8 秒 | 依據 |
| --- | --- | --- |
| 伺服器 Veo 3.1 Lite 1080p | 0.64 | 價目 0.08／秒（目錄；profile 2026-10-01 核實） |
| 伺服器 Veo 3.1 Fast | 0.96 | 價目 0.12／秒 |
| 伺服器 Omni 1.1 Flash | 1.20 | 價目 0.15／秒 |
| 伺服器 Veo 3.1 | 3.20 | 價目 0.40／秒 |
| 伺服器 MiniMax-H3 2K | 1.04（帳本）；官方 768P 0.64、2K 1.04 | 價目 0.13／秒；`meter.usd_for` 不分解析度 |
| Hailuo H3 2K，96 積分 | 月繳 Standard 1.44、Pro 1.17、Master 1.10、Max 0.71；年繳 0.81／0.65／0.65／0.65；加購 1.37 | 12 積分／秒實測 2026-10-04（§1.2）；美元是月費 ÷ 積分的換算；輸出 2560×1440，不是 1080p |
| Hailuo H3 768P，56 積分 | 月繳 0.84／0.68／0.64／0.41；年繳 0.47／0.38／0.38／0.38 | 推算（768P 沒量）；低於 1080p |
| Hailuo 2.3 1080p 10 秒（Max 無限） | 月費之外 0；積分內的價未讀 | 訂閱頁 |
| Kling 標準 10 秒（第三方的兩個檔位之一；80 積分） | 標價 Standard 1.21、Pro 0.99、Premier 0.92、Ultra 0.55；之後月價 1.07／0.87／0.81／0.49；年繳 0.80／0.65／0.61／0.37 | 未驗證（積分假設）。`kling-video-v3_0` 可以直接要 8 秒（3–15 秒整數，實測 2026-10-04），但 8 秒扣幾積分沒有來源，所以這裡仍列 10 秒 |
| Kling 標準 5 秒（`episode_estimate.mjs` 的預設單位；40 積分） | 上列的一半：標價 0.61／0.49／0.46／0.28 | 未驗證（積分假設） |
| Kling 開發者 API 10 秒 1080p | 0.84–1.12 | 未驗證（兩個第三方數字） |

**一集 60 鏡，一次成功**（假設：全部是 clip、每鏡買 8 秒＝480 秒；關鍵影格 60 × 0.134 ＝ 8.04；設定圖 3 角色 × 3 候選 × 0.134 ＝ 1.21；judge 9 ＋ 60 ＋ 60 ＝ 1.29，外部路線沒有片段 judge 是 0.69；音樂 0.08。照 `drama-craft.md` 的節奏，60 鏡大約是 3 分鐘、每鏡需求 2.5–3.5 秒，所以 480 秒是**買到的**，不是片長——利用率約四成；Omni／H3 上短鏡只買 4 秒，片段那欄可以減半）：

| 路線 | 片段 | 圖＋judge＋音樂 | 合計 | 備註 |
| --- | --- | --- | --- | --- |
| 伺服器 Lite | 38.40 | 10.62 | 49.02 | profile 的指定模型 |
| 伺服器 Fast | 57.60 | 10.62 | 68.22 | |
| 伺服器 Omni | 72.00 | 10.62 | 82.62 | 預設模型；短鏡買 4 秒則 36.00 |
| 伺服器 Veo 3.1 | 192.00 | 10.62 | 202.62 | 超過單支上限 200，最後幾鏡結束碼 3 |
| 伺服器 H3 2K | 62.40 | 10.62 | 73.02 | 帳本價；短鏡買 4 秒則 31.20 |
| Hailuo H3 2K（5,760 積分＝480 秒 × 12，12 是實測 2026-10-04） | Master 月繳 65.82、年繳 39.06；Max 月繳 42.66、年繳 39.25 | 10.02 | 49–76 | Pro 的 4,500 不夠一集，要兩個月或加購 1,260 積分（US$18）；輸出 2560×1440，profile 不收 |
| Hailuo H3 768P（3,360 積分，推算） | Pro 月繳 41.06、年繳 22.70；Max 月繳 24.89 | 10.02 | 33–51 | 低於 1080p，profile 不收 |
| Kling 標準每鏡一支 10 秒（4,800 積分） | Premier 標價 55.20、之後月價 48.58、年繳 36.43；Ultra 33.23／29.54／21.93 | 10.02 | 32–65 | 未驗證；Pro 的 3,000 不夠一集 |
| Kling 標準每鏡一支 5 秒（2,400 積分＝Pro 的 80%，`SKILL.md` 三條路線表與 `episode_estimate.mjs` 用這個） | Pro 標價 29.60、之後月價 26.05、年繳 19.54 | 10.02 | 30–40 | 未驗證；一集 60 鏡 Pro 剛好夠一次 take，兩次不夠。`kling-video-v3_0` 能照鏡長要 3–15 秒整數（實測 2026-10-04），那樣扣幾積分沒有來源 |
| Kling 開發者 API | 50.40–67.20 | 10.02 | 60–77 | 未驗證 |

重拍不在表裡：伺服器路線每鏡最多 2 次（工具規定）；試作實際是 S01 送 4 次、S03 送 2 次、0 段被接受（量到的，`production-run-20261003.md`），而 `budget-and-launch.md` 的規矩是三份成功素材都不合格就重新設計鏡頭，不靠重抽。外部路線的重拍上限只有你自己的紀律，先在紀錄 JSON 裡寫下這一鏡允許幾次。操作時間也不在表裡：每段上傳、設定、等隊列、下載、`clips import`。量過的只有一支：Hailuo H3 2K 5 秒、沒有別的在排隊，送出到完成約 4 分 40 秒（實測 2026-10-04）；60 鏡的人工時數沒有量過。

**訂閱什麼時候贏過每秒計價**：只有一個條件——這個月**真的用掉的秒數** ≥ 月費 ÷ 伺服器的每秒價。沒用完的積分月底歸零，所以分母是用掉的，不是方案給的。下表 Hailuo 的方案秒數是積分 ÷ 12（H3 2K 每秒 12 積分，實測 2026-10-04）；Kling 兩列仍建立在未驗證的積分假設上。

| 方案（H3 2K） | 月費 | 方案秒數 | 換算每秒 | 要用到幾秒才贏 Lite 0.08 | 贏 H3 API 0.13 | 贏 Omni 0.15 |
| --- | --- | --- | --- | --- | --- | --- |
| Hailuo Pro 月繳 | 54.99 | 375 | 0.147 | 687（不可能） | 423（不可能） | 367（幾乎全用） |
| Hailuo Pro 年繳 | 30.40 | 375 | 0.081 | 380（差一點，不可能） | 234 | 203 |
| Hailuo Master 月繳 | 119.99 | 875 | 0.137 | 1,500（不可能） | 923（不可能） | 800 |
| Hailuo Master 年繳 | 71.20 | 875 | 0.081 | 890（不可能） | 548 | 475 |
| Hailuo Max 月繳 | 199.99 | 2,250 | 0.089 | 2,500（積分內不可能；之後 Hailuo 2.3 無限） | 1,538 | 1,333 |
| Kling Pro 標價（未驗證） | 37 | 375 | 0.099 | 不可能 | 285 | 247 |
| Kling Ultra 標價（未驗證） | 180 | 3,250 | 0.055 | 2,250 | 1,385 | 1,200 |

結論（編輯判斷，建立在上面的數字）：在產線現在的 Lite 價（0.08／秒 1080p）之下，**沒有任何訂閱靠積分贏**；訂閱贏的是（a）對 Omni 或 H3 API 的價，且每個月把積分用到八九成；（b）Max 積分用完後 Hailuo 2.3 1080p 的無限生成，量大且等得起隊列時；（c）Pro 以上無限的圖片生成，前提是關鍵影格能進 `keyframes/manifest.json`——今天沒有 import，storyboard 關卡綁的是工具畫的那份；（d）伺服器沒有 adapter（Kling）或主機地區被擋（`docs/videos/DRAMA.md` 的地區一節）。代價在 §3：沒有快取與自動 retake、judge 要另外問，每一段都要自己下載再 `clips import`。

## 3. 外部素材怎麼進產線

用 `clips import`（2026-10-04 落地，PR #1183；同一天用真的 ffmpeg 在下載的那支 Hailuo 片段上跑過，實測 2026-10-04。程序**只寫在 `stage-preconditions.md` 最後一節**，設計在 `docs/videos/DRAMA.md`「外面做的片段」）：

`node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"] [--judge] [--force]`

它查 `clips` 的前提（timeline 與 keyframes 是現在的、這一鏡的關鍵影格通過、storyboard 核准），把檔案複製成 `clips/<shot>-import-<n>.mp4`，跑買來的 take 同一組 ffmpeg 檢查（`tools/video/media/qc.mjs` 的 `clipVerdict`），寫 `clips`（`tools/video/media/clips.mjs`）自己寫的那種 manifest 條目加 `provider`、`plan`、`credits`、`imported_at`，在帳本記一筆 `status: "imported"`；`assemble`（`tools/video/assemble/cli.mjs`）與 `status`（`tools/video/core/state.mjs` `pipelineStatus`）照常讀那份 manifest。要記得的兩句沒變：外部素材的首格要用通過 judge 的那張關鍵影格，不然第 0 格 PSNR 會讓它 `needs_review`（`--force` 才留下）；judge 預設不問，`--judge` 才上傳媒體庫問 `clipRubric`（US$0.01）。實測（2026-10-04）多出兩句：**ffmpeg 檢查看不出浮水印**，Hailuo 下載錯版本（§1.2 第 6 步）匯入照樣通過，只有 `--judge` 的 `no_text` 題可能抓到；外面做的片段可能帶生成的音軌（Hailuo H3 帶 AAC；Kling 的 `enable_audio` 預設 true），成片不用它。用產線關鍵影格當首格的圖生影片還沒有匯入過。

**有 production profile 的作品進不去**：`clips import` 以結束碼 3 拒絕。`productionClipProblems`（`tools/video/core/lint.mjs`）要求 manifest 頂層 `clip.provider/model/resolution` 等於 profile 的（十部動畫是 gemini／veo-3.1-lite-generate-preview／1080p，`docs/videos/series-plans/production-20261001/profile.json`），每鏡要 `qc.ok === true` 且 `qc.metrics.duration` 蓋過整段台詞，`productionClipSizeProblem` 要求量到的 1920×1080（H3 的 2K 是 2560×1440，實測 2026-10-04，不是 1920×1080；要先縮成 1920×1080 再 probe；profile 收不收縮過的 2K，站主沒決定過）。`status` 與 `assemble` 都呼叫它。把 Hailuo 的素材標成 Veo Lite 是作假，不做；所以外部路線只用於沒有 profile 的漫劇，或等站主改 profile（那會換掉核准的設計雜湊）；讓 profile 能點名外部路線是第二張票，站主決定。

**匯入之後，產線知道與還不知道的事**：

| 哪裡 | 知道 | 還不知道 |
| --- | --- | --- |
| `media/ledger.json` | 一筆 `status: "imported"`：路線、方案、點數、秒數；`totals.clip_seconds` 與 `capProblem` 的單支上限都算它，`importedTotals` 另外加總 | 沒給 `--usd` 就是 US$0：`media-status --slug` 與 `clips` 的「this video has spent」少算點數的錢；廠商的實際帳單 |
| `clips/manifest.json` | `provider`、`plan`、`credits`、`imported_at`、量到的 `qc`、問過才有的 `judge` | 站方的任務 id、提示詞、送出與完成時間（要留就寫 `--note`） |
| `status`、`clips --dry-run`、`run_report.mjs`、`drama_preflight.mjs` | 把匯入的與買的分開列 | — |
| `media/cache.json` | — | 沒有這一段的請求鍵：`clips --force` 會在伺服器重買這一鏡 |
| 伺服器 | `--judge` 時片段進媒體庫、那一次 judge 進每月預算 | 沒有 job；片段秒數沒進每月預算；後台的 `media_usd`／`clip_seconds` 少算 |
| manifest 頂層 `clip` | — | 仍是伺服器的選擇（下一次 `clips` 會寫）；匯入的鏡頭看自己條目的 `provider` |

`--usd` 沒給時工具不替你把點數換成美元：點數對美元在 §1.2、§1.3 的表與 `episode_estimate.mjs` 的 PRICES，報帳時自己乘。指令落地前手放的片段（manifest 條目 `provider: "external"`，或帳本沒有它的 job）`run_report.mjs` 與 `drama_preflight.mjs` 仍認得，列成「手放」；用 `clips import` 重新帶進來一次，它們才有 QC 與帳本。

## 4. 權利與安全

- **帳號是站主的**。Hailuo 與 Kling 的登入、訂閱、加購都由站主做；代理不建帳號、不輸入密碼、不用自己的帳號、不把 cookie 或權杖寫進對話、檔案與指令參數（`youtube-video` skill 規矩 9）。MCP 連接器也是站主在自己的 Claude Desktop／claude.ai 加的；Kling CLI 的 `kling login` 由站主在瀏覽器裡同意 OAuth，權杖檔 `~/.kling/.credentials` 不讀、不貼、不進 repo。
- **商用與浮水印**：Hailuo 免費方案的下載有浮水印，不能上架；Standard 以上無浮水印且條款寫明保留 IP 含商用，但付費帳號的結果卡 `<video>` src 仍是有浮水印的檔，要走「無水印下載」（實測 2026-10-04，§1.2 第 6 步）。Kling 每個付費方案去品牌浮水印、商用；免費層沒讀到條款，當作不能用。產線自己的 Lyria 音樂帶 SynthID 浮水印（目錄註解），是允許的。
- **內容規則**：Hailuo 有內容審查，審查不過退積分；MiniMax API 的 1026／1027／2013 是內容被拒（`apps/api/app/video_media/providers/minimax.py`）；Kling 的內容政策沒有逐條讀，當作一樣有。被拒的題材先回報，不換字繞。
- **提示詞不帶個資**：不寫真人姓名、照片、聲音、站主的資料、金鑰；不用真人臉與聲音；這跟產線的規矩一樣（`docs/videos/DRAMA.md` 的 YouTube 一節）。
- **上架揭露**：3D 寫實 AI 畫面與 AI 配樂都勾「變造或合成內容」，不分哪一條路線買的。
- **檔案不進 git**：下載的 mp4、紀錄 JSON 都在 `<VIDEO_WORKDIR>` 底下；repo 是公開的。
- **價目會變**：本文的方案價 2026-10-03 讀、目錄價 2026-09-26／28 讀、profile 2026-10-01 核實；Hailuo H3 2K 的每秒積分、生成時間與輸出規格、Kling CLI 的指令與模型表是 2026-10-04 實測；Kling 積分與 API 價未驗證。定一場戲的錢之前先讀 §5 的頁面，改日期；頁面讀不到（SPA、登入牆）就寫「未驗證」，不要補一個數字。

## 5. 來源

| 事實 | 來源 | 讀取日 |
| --- | --- | --- |
| 伺服器目錄價、秒數表、參考圖數 | `apps/api/app/video_media/catalog.py`、`apps/api/app/video_media/schemas.py` | 2026-09-26、2026-09-28（圖片） |
| 每秒計價、每月預算、單支上限、judge 門檻、每小時上限 | `apps/api/app/video_media/meter.py`、`apps/api/app/video_automation/models.py`、`apps/api/app/video_media/admin_api.py` | 程式碼 |
| 買幾秒、take 上限、judge 單價、manifest 形狀 | `tools/video/media/clips.mjs`、`tools/video/media/stages.mjs`、`tools/video/media/ledger.mjs` | 程式碼 |
| assemble 的檢查 | `tools/video/assemble/cli.mjs`、`tools/video/assemble/drama.mjs`、`tools/video/media/qc.mjs`、`tools/video/core/lint.mjs` | 程式碼 |
| MiniMax API 價、時長、套餐 | platform.minimax.io 的 pricing-paygo、video-generation、pricing-video 三頁 | 2026-10-03 |
| Hailuo 方案、積分、模型、隊列 | hailuoai.video 的訂閱頁（內建瀏覽器） | 2026-10-03 |
| Hailuo 條款 | hailuoai.video/doc/payment-policy.html | 2026-10-03 |
| Hailuo H3 2K 每秒 12 積分、生成時間、輸出規格、設定面板的選項、浮水印與無水印下載 | 站主的 Max 帳號在 hailuoai.video 送的一支文生影片（H3、2K、5 秒、16:9）與下載的檔 | 實測 2026-10-04 |
| 內建瀏覽器傳不了本機檔案、表單怎麼點 | Claude 桌面版的內建瀏覽器，同一次操作 | 實測 2026-10-04 |
| Kling 會員方案 | kling.ai 會員頁（內建瀏覽器） | 2026-10-03 |
| Kling 官方 MCP 與 CLI：端點、套件、登入、指令、`image_to_video` 的模型與參數 | kling.ai/app/mcp/guide（登入後）、npm `@klingai/cli-global` 0.2.1、`kling who_am_i` 與 `kling account` 的輸出（NORMAL 帳號、0 積分） | 實測 2026-10-04 |
| `clips import` | PR #1183（`tools/video/media/clips.mjs`）；真的 ffmpeg 跑在下載的 Hailuo 片段上 | 實測 2026-10-04 |
| Kling 社群 MCP | github.com/199-mcp/mcp-kling README | 2026-10-03 |
| Kling 積分／段、API 價 | 第三方整理，未驗證 | 2026 |
| 試作的花費與重拍 | `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`、`docs/videos/series-plans/competition-20261002/budget-and-launch.md`、`docs/videos/series-plans/competition-20261002/cost-ledger.csv` | 2026-10-03 |
