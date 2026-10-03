# 供應商與方案：伺服器 API、Hailuo 網頁訂閱、Kling MCP

給用手寫、用手導、用手跑漫劇的代理：同一個鏡頭的素材今天有三條路可以買，這一篇把三條並排、算一鏡與一集各要多少錢、說外部素材現在怎麼進產線（以及產線會不知道什麼）、最後是權利與安全。它不重複別處已經寫好的事：產線的步驟、指令與結束碼在 `.agents/skills/youtube-video/references/drama.md`；第一版的供應商決定與設計在 `docs/videos/DRAMA.md`；Veo 3.1 Lite 的鏡頭契約與十部動畫的製作規格在 `.agents/skills/youtube-video/references/animation-production.md`；一個鏡頭的 `camera`／`motion`／`prompt` 怎麼寫、同一鏡怎麼改寫給 Hailuo 的表單與 Kling 的鏡頭控制，在 animation-camera skill。

每個數字都標來源：**價目**是官方頁或目錄檔讀到的（附日期）；**工具規定**是 `tools/video` 或 `apps/api` 裡的常數（附檔名）；**模型限制**是供應商文件寫的；**推算**是本文從前兩者算出來、沒有在生成器裡核對過的；**未驗證**是第三方整理或根本讀不到的。價目與積分會不預告就改：定一場戲的錢之前，先把本文 §5 的頁面再讀一遍，把日期更新。

## 1. 三條路線並排

| | 伺服器 API（產線本來的路） | Hailuo 網頁訂閱（hailuoai.video） | Kling（官方 MCP；社群 MCP＋開發者 API） |
| --- | --- | --- | --- |
| 誰在呼叫 | `node tools/video/cli.mjs clips` 經網站的媒體端點叫 Gemini／MiniMax；金鑰只在站上 | 代理在內建瀏覽器或 Playwright 裡操作 SPA，用**站主的登入** | 官方 MCP：Claude Desktop／claude.ai 的自訂連接器，登入**站主的 Kling 帳號**；社群 MCP：開發者 API 的 access key／secret key |
| 計價 | 每秒：`usd_per_second × seconds`，解析度不改價（工具規定，`apps/api/app/video_media/meter.py` `usd_for`） | 月費換積分，積分月底歸零；用完可加購 | 會員月費換積分；開發者 API 另賣資源包，兩邊不互通 |
| 片段模型 | `apps/api/app/video_media/catalog.py` 列的：Omni 1.1 Flash、Veo 3.1／Fast／Lite、MiniMax-H3 | H3、H3 Max、Hailuo 2.0／2.3／1.0、Sora 2、Veo 3.1 | Kling 3.0／3.0 Omni、Motion Control |
| 首尾格與參考圖 | 首格必帶；參考圖最多 4（`MAX_REFERENCES`，`apps/api/app/video_media/schemas.py`；目錄寫 H3 9 張、Pro Image 14 張是供應商上限，不是我們送得出的）；Lite 不收參考圖 | 首格與末格；參考上傳區「參考 (0/12)」 | 首尾格；元素參考（Omni） |
| 品檢 | ffmpeg（`tools/video/media/qc.mjs`）＋ judge 自動跑，不過換 seed，最多 2 次（`MAX_CLIP_TAKES`，`tools/video/media/clips.mjs`） | 沒有：你自己看 | 沒有：你自己看 |
| 快取、帳本、預算 | `media/cache.json`（同一請求不付兩次）、`media/ledger.json`（每筆花費）、伺服器的每月預算與單支上限 | 都沒有：自己記（§1.2 的紀錄欄） | 都沒有：自己記 |
| 進產線 | 直接 | 下載後手工寫 `clips/manifest.json`（§3） | 同左 |
| 浮水印、商用 | 無浮水印；依各供應商條款 | 免費下載有浮水印；Standard 以上沒有，且保留 IP 含商用（條款，2026-10-03 讀） | 付費方案去浮水印、「Generated content is for commercial use」（會員頁，2026-10-03 讀） |
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

訂閱頁 `/zh-Hant/subscribe` 是 React SPA，WebFetch 只拿得到殼；下面的數字是 2026-10-03 在內建瀏覽器讀到的，條款來自 `hailuoai.video/doc/payment-policy.html`（同日 WebFetch 再讀一次，一致）。

| 方案 | 月繳 | 年繳（換算每月） | 積分／月 | 排隊／執行 | 圖片 | 無限生成 |
| --- | --- | --- | --- | --- | --- | --- |
| Free | US$0 | — | 一次性試用積分，只有 Hailuo 系列 | 4／1 | — | — |
| Standard | US$14.99 | US$8.40（US$100.80／年） | 1,000 | 8／1 | — | — |
| Pro | US$54.99 | US$30.40 | 4,500 | 8／2 | 1K 無限（Nano Banana Pro／2、Seedream 4.5、GPT Image 1.5） | — |
| Master | US$119.99 | US$71.20 | 10,500 | 12／2 | 2K 無限 | — |
| Max | US$199.99 | US$184.00（US$2,208／年） | 27,000 | 12／2 | 4K 無限 | 積分用完後無限生成、進較慢的隊列。**哪些模型，兩個來源說法不同**（2026-10-03 同日讀）：方案表寫「海螺 2.0／2.3 模型 無限制」，FAQ 寫「MAX 會員可以使用海螺 1.0 和 2.0 系列模型無限制生成」；H3 兩邊都不在。`SKILL.md`、`cost-model.md` 與 `episode_estimate.mjs` 的 PLANS 都指這一格 |

條款（價目，2026-10-03）：會員積分一個月到期；加購 US$1 換 70 積分，有效到購買後第二個日曆年的 12 月 31 日；付費方案「retain any and all intellectual property rights to such content, including the right to use it for commercial purposes」；免費下載有浮水印、Standard 以上沒有；取消不退款；生成失敗或**內容審查不過**自動退積分（所以有內容審查）。條款頁還列著舊方案 Unlimited US$94.99 與 Ultra US$124.99，訂閱頁沒有。

**積分怎麼換秒**（推算：用訂閱頁每方案「約可做幾秒」反推，四個方案都對得上）：H3 2K 每秒 12 積分，H3／H3 Max 768P 每秒 7 積分，H3 Max 480P 每秒 4 積分。所以一段 8 秒 2K 是 96 積分、8 秒 768P 是 56 積分。訂閱頁自己標的「每秒美元」（Standard：2K US$0.101、768P US$0.059；Pro 以上：2K US$0.081、768P US$0.047、480P US$0.027）**只在年繳價成立**（375 秒 × 0.081 ≈ US$30.40，就是 Pro 的年繳月價）；月繳要用下表。

| 每秒 | Standard | Pro | Master | Max | 加購積分 |
| --- | --- | --- | --- | --- | --- |
| 美元／積分 | 月繳 0.0150；年繳 0.0084 | 0.0122；0.0068 | 0.0114；0.0068 | 0.0074；0.0068 | 0.0143 |
| H3 2K（12 積分） | 0.180；0.101 | 0.147；0.081 | 0.137；0.081 | 0.089；0.082 | 0.171 |
| H3 768P（7 積分） | 0.105；0.059 | 0.086；0.047 | 0.080；0.047 | 0.052；0.048 | 0.100 |
| 每月 2K 秒數 | 84 | 375 | 875 | 2,250 | — |
| 每月 768P 秒數 | 143 | 643 | 1,500 | 3,857 | — |

模型與方案（訂閱頁）：H3 4–15 秒 768p／2K；H3 Max 5–15 秒 480p／768p；Hailuo 2.3 6 秒 768p／1080p（Pro 以上 10 秒）；Hailuo 2.0（首尾格）6 秒 512p／768p／1080p（Pro 以上 10 秒）；Sora 2 4／8／12 秒 720p；Veo 3.1 8 秒 720p／1080p；Hailuo 1.0 6 秒 720p。各模型每段扣幾積分只有生成器裡看得到，本文只推算了 H3 系列；Hailuo 2.3、Sora 2、Veo 3.1 在這裡的積分**未驗證**。注意 H3 沒有 1080p：2K 在 1080p 之上，768P 在之下；production profile 要求原生 1920×1080（§3）。

**怎麼操作**（SPA 只能在內建瀏覽器或 Playwright 裡跑；內建瀏覽器的登入會留在 pane，Playwright 用 `launchPersistentContext` 指向站主自己登入過的 profile；代理不輸入密碼、不經手 cookie 與權杖、不建帳號、不用自己的帳號）：

1. 站主登入後，開 `/create/image-to-video`。
2. 把這一鏡通過 judge 的關鍵影格（`keyframes/manifest.json` 的 `file`，sha256 一起抄下來）上傳成首格；需要末格就上傳 `end_frame.file`。表單用檔案選擇器時，在頁面 JS 裡用 `DataTransfer` 塞 `File` 再觸發 `change` 可以免掉它；base64 分段貼、每段核 SHA-256，一次貼大段會悄悄錯字。
3. 選模型、解析度、時長（H3 整數 4–15；用 `clips --dry-run` 印的需求秒數，不要照 Lite 的固定 8）、比例 16:9；提示詞貼 `--dry-run` 印出的 clip prompt（`motion` ＋ `camera` ＋ `look.motion`，`tools/video/media/clips.mjs` `clipPrompt`）。表單有沒有負面提示欄位沒有核對；沒有就照 MiniMax adapter 的做法，在最後接 `Avoid: …`。
4. 送出前記積分餘額，送出後再記一次：扣了多少就是這一鏡的價。1–2 個執行、8–12 個排隊，一集 60 鏡要分批等；Max 用完積分後的無限生成不含 H3（哪些模型見上表 Max 列），進較慢的隊列，一支多久沒有量過。
5. 下載（付費無浮水印），之後照 `stage-preconditions.md` 最後一節（唯一的一份程序）：`ffprobe`、自己跑 `qc.mjs` 的黑格／凍格／切鏡／PSNR、寫 manifest 條目、記 `clips/<shot>-ext<n>.external.json`（欄位和試作的 `docs/videos/series-plans/competition-20261002/cost-ledger.csv` 同一套：`shot_id`、provider/model、`operation_id`、`input_sha256`、attempt、billed units、estimated/actual、accepted/rejected 原因；例子在那一節）。

內建瀏覽器的已知限制（2026-09 實測）：pane 隱藏時頁面是 `visibilityState: hidden`，`IntersectionObserver` 與 `requestAnimationFrame` 都不會觸發，懶載入的區塊看起來像「沒有」；pane 最多 9 個分頁；多代理同時操作會觸發站方的機器人牆，過一小時就好——那是工具故障，不是頁面的結論。

### 1.3 Kling

**會員**（kling.ai 會員頁，2026-10-03 在內建瀏覽器讀，月繳視圖；WebFetch 同日只拿到殼）：

| 方案 | 標價／月 | 首月 | 之後每月（月繳 12% off） | 積分／月 | 頁面標的「每 100 積分」 |
| --- | --- | --- | --- | --- | --- |
| Standard | US$10 | US$6.99 | US$8.80 | 660 | US$1.06（是首月價算的） |
| Pro | US$37 | US$25.99 | US$32.56 | 3,000 | US$0.87 |
| Premier | US$92 | US$64.99 | US$80.96 | 8,000 | US$0.81 |
| Ultra | US$180 | US$127.99 | US$159.99 | 26,000 | US$0.49 |

年繳 34% off。每個付費方案：排隊不限、fast-track、1080p、圖片放大、去品牌浮水印、影片延長、商用；Pro 以上先用新功能；一次最多出 4 支（Basic 1）；高階有 4K。每段扣幾積分只在登入後的生成器裡顯示；第三方 2026 年的整理說 3.0 Omni 標準模式 5 秒約 35–45 積分、專業模式約 70（**未驗證**，定價前先在站主帳號裡看一次）。本文的 Kling 美元數全部建立在「標準 5 秒 40 積分、10 秒 80 積分」這個未驗證的假設上。

**官方 MCP**：`kling.ai/mcp`，加進 Claude Desktop／claude.ai／Cursor 的自訂連接器，「sign in with your Kling account」，用的是站主的帳號；指南 `kling.ai/app/mcp/guide` 要登入才看得到（WebFetch 與未登入的 pane 都是空的，2026-10-03），所以**它暴露哪些工具、從會員積分還是資源包扣、能不能帶首尾格，都要在站主帳號裡讀**，本文沒有驗證。

**社群 MCP**（github.com/199-mcp/mcp-kling，2026-10-03 讀 README）：用開發者 API 的 access key 與 secret key 自動簽 JWT，扣的是**資源包**，不是會員積分；工具有 `generate_video`（5 或 10 秒、標準／專業、cfg_scale、鏡頭控制）、`generate_image_to_video`（圖生影片，鏡頭控制 `static`／`zoom`／`pan`／`auto` 加一段 motion prompt）、`extend_video`、`create_lipsync`、`generate_image`（KOLORS）、`get_account_balance`、`get_resource_packages`、`list_tasks`；結果下載到本機 `./downloads/` 底下分類資料夾。對應我們的運鏡字（詳見 animation-camera skill）：`locked`→`static`，`push-in`／`pull-out`→`zoom`（方向寫進 prompt），`pan-left`／`pan-right`→`pan`，`drift` 沒有對應，用 `static` 加 motion prompt。

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
| Hailuo H3 2K，96 積分 | 月繳 Standard 1.44、Pro 1.17、Master 1.10、Max 0.71；年繳 0.81／0.65／0.65／0.65；加購 1.37 | 推算（§1.2） |
| Hailuo H3 768P，56 積分 | 月繳 0.84／0.68／0.64／0.41；年繳 0.47／0.38／0.38／0.38 | 推算；低於 1080p |
| Hailuo 2.3 1080p 10 秒（Max 無限） | 月費之外 0；積分內的價未讀 | 訂閱頁 |
| Kling 標準 10 秒（> 5 s 的鏡；沒有 8 秒；80 積分） | 標價 Standard 1.21、Pro 0.99、Premier 0.92、Ultra 0.55；之後月價 1.07／0.87／0.81／0.49；年繳 0.80／0.65／0.61／0.37 | 未驗證（積分假設） |
| Kling 標準 5 秒（≤ 5 s 的鏡，`episode_estimate.mjs` 的預設單位；40 積分） | 上列的一半：標價 0.61／0.49／0.46／0.28 | 未驗證（積分假設） |
| Kling 開發者 API 10 秒 1080p | 0.84–1.12 | 未驗證（兩個第三方數字） |

**一集 60 鏡，一次成功**（假設：全部是 clip、每鏡買 8 秒＝480 秒；關鍵影格 60 × 0.134 ＝ 8.04；設定圖 3 角色 × 3 候選 × 0.134 ＝ 1.21；judge 9 ＋ 60 ＋ 60 ＝ 1.29，外部路線沒有片段 judge 是 0.69；音樂 0.08。照 `drama-craft.md` 的節奏，60 鏡大約是 3 分鐘、每鏡需求 2.5–3.5 秒，所以 480 秒是**買到的**，不是片長——利用率約四成；Omni／H3 上短鏡只買 4 秒，片段那欄可以減半）：

| 路線 | 片段 | 圖＋judge＋音樂 | 合計 | 備註 |
| --- | --- | --- | --- | --- |
| 伺服器 Lite | 38.40 | 10.62 | 49.02 | profile 的指定模型 |
| 伺服器 Fast | 57.60 | 10.62 | 68.22 | |
| 伺服器 Omni | 72.00 | 10.62 | 82.62 | 預設模型；短鏡買 4 秒則 36.00 |
| 伺服器 Veo 3.1 | 192.00 | 10.62 | 202.62 | 超過單支上限 200，最後幾鏡結束碼 3 |
| 伺服器 H3 2K | 62.40 | 10.62 | 73.02 | 帳本價；短鏡買 4 秒則 31.20 |
| Hailuo H3 2K（5,760 積分） | Master 月繳 65.82、年繳 39.06；Max 月繳 42.66、年繳 39.25 | 10.02 | 49–76 | Pro 的 4,500 不夠一集，要兩個月或加購 1,260 積分（US$18） |
| Hailuo H3 768P（3,360 積分） | Pro 月繳 41.06、年繳 22.70；Max 月繳 24.89 | 10.02 | 33–51 | 低於 1080p，profile 不收 |
| Kling 標準每鏡一支 10 秒（> 5 s 的鏡；4,800 積分） | Premier 標價 55.20、之後月價 48.58、年繳 36.43；Ultra 33.23／29.54／21.93 | 10.02 | 32–65 | 未驗證；Pro 的 3,000 不夠一集 |
| Kling 標準每鏡一支 5 秒（≤ 5 s 的鏡；2,400 積分＝Pro 的 80%，`SKILL.md` 三條路線表與 `episode_estimate.mjs` 用這個） | Pro 標價 29.60、之後月價 26.05、年繳 19.54 | 10.02 | 30–40 | 未驗證；一集 60 鏡 Pro 剛好夠一次 take，兩次不夠 |
| Kling 開發者 API | 50.40–67.20 | 10.02 | 60–77 | 未驗證 |

重拍不在表裡：伺服器路線每鏡最多 2 次（工具規定）；試作實際是 S01 送 4 次、S03 送 2 次、0 段被接受（量到的，`production-run-20261003.md`），而 `budget-and-launch.md` 的規矩是三份成功素材都不合格就重新設計鏡頭，不靠重抽。外部路線的重拍上限只有你自己的紀律，先在紀錄 JSON 裡寫下這一鏡允許幾次。操作時間也不在表裡：每段上傳、設定、等隊列、下載、記錄、手工 import，60 鏡的人工時數沒有量過。

**訂閱什麼時候贏過每秒計價**：只有一個條件——這個月**真的用掉的秒數** ≥ 月費 ÷ 伺服器的每秒價。沒用完的積分月底歸零，所以分母是用掉的，不是方案給的。

| 方案（H3 2K） | 月費 | 方案秒數 | 換算每秒 | 要用到幾秒才贏 Lite 0.08 | 贏 H3 API 0.13 | 贏 Omni 0.15 |
| --- | --- | --- | --- | --- | --- | --- |
| Hailuo Pro 月繳 | 54.99 | 375 | 0.147 | 687（不可能） | 423（不可能） | 367（幾乎全用） |
| Hailuo Pro 年繳 | 30.40 | 375 | 0.081 | 380（差一點，不可能） | 234 | 203 |
| Hailuo Master 月繳 | 119.99 | 875 | 0.137 | 1,500（不可能） | 923（不可能） | 800 |
| Hailuo Master 年繳 | 71.20 | 875 | 0.081 | 890（不可能） | 548 | 475 |
| Hailuo Max 月繳 | 199.99 | 2,250 | 0.089 | 2,500（積分內不可能；之後 Hailuo 2.3 無限） | 1,538 | 1,333 |
| Kling Pro 標價（未驗證） | 37 | 375 | 0.099 | 不可能 | 285 | 247 |
| Kling Ultra 標價（未驗證） | 180 | 3,250 | 0.055 | 2,250 | 1,385 | 1,200 |

結論（編輯判斷，建立在上面的數字）：在產線現在的 Lite 價（0.08／秒 1080p）之下，**沒有任何訂閱靠積分贏**；訂閱贏的是（a）對 Omni 或 H3 API 的價，且每個月把積分用到八九成；（b）Max 積分用完後 Hailuo 2.3 1080p 的無限生成，量大且等得起隊列時；（c）Pro 以上無限的圖片生成，前提是關鍵影格能進 `keyframes/manifest.json`——今天沒有 import，storyboard 關卡綁的是工具畫的那份；（d）伺服器沒有 adapter（Kling）或主機地區被擋（`docs/videos/DRAMA.md` 的地區一節）。代價在 §3：沒有快取、judge、帳本與 retake，每一段都要手工進產線。

## 3. 外部素材今天怎麼進產線

`clips`（`tools/video/media/clips.mjs`）寫 `clips/manifest.json`，`assemble`（`tools/video/assemble/cli.mjs`、`tools/video/assemble/drama.mjs` `layoutDrama`）與 `status`（`tools/video/core/state.mjs` `pipelineStatus`）只讀這一份。沒有 `clips import` 指令；今天是手工，**程序只寫在 `stage-preconditions.md` 最後一節**（放檔、`ffprobe`、自己跑 `qc.mjs` 的黑格／凍格／切鏡／PSNR、manifest 條目的例子、`external.json` 的例子、`clipsHash` 重算、`assemble` 真正查什麼）。要記得的只有兩句：外部素材的首格要用通過 judge 的那張關鍵影格，不然 `assemble` 的第 0 格 PSNR 會擋；`assemble` 不跑 `clips` 階段的 `clipVerdict`（黑格、凍格、模型自己切鏡），那些要自己跑。

**有 production profile 的作品今天進不去**：`productionClipProblems`（`tools/video/core/lint.mjs`）要求 manifest 頂層 `clip.provider/model/resolution` 等於 profile 的（十部動畫是 gemini／veo-3.1-lite-generate-preview／1080p，`docs/videos/series-plans/production-20261001/profile.json`），每鏡要 `qc.ok === true` 且 `qc.metrics.duration` 蓋過整段台詞，`productionClipSizeProblem` 要求量到的 1920×1080（H3 的 2K 不是 1920×1080——實際像素沒有讀——要先縮成 1920×1080 再 probe；profile 收不收縮過的 2K，站主沒決定過）。`status` 與 `assemble` 都呼叫它。把 Hailuo 的素材標成 Veo Lite 是作假，不做；所以外部路線今天只用於沒有 profile 的漫劇，或等站主改 profile（那會換掉核准的設計雜湊）。

**產線不會知道的事**：

| 哪裡 | 不知道什麼 | 後果 |
| --- | --- | --- |
| `media/ledger.json` | 這一段的錢（`bookJob` 只為伺服器的 job 寫；`bookReuse` 只記 `source` 的切用） | `media-status --slug`、`clips` 的「this video has spent」、`capProblem` 的單支上限、本 skill 的 `run_report.mjs` 都少算它 |
| `media/cache.json` | 沒有這一段的請求鍵 | `--force` 或 manifest 的雜湊一變，`clips` 會在伺服器重買這一鏡；外部檔不會從快取回來 |
| 伺服器 | 沒有 job、沒進每月預算、媒體庫沒有這個檔 | judge 看不到它（`Stage.judge` 要媒體庫裡的 sha256）；後台的 `media_usd`／`clip_seconds` 少算 |
| `state.json` | `recordStage` 沒跑 | 階段牆鐘、`generated` 計數沒有它 |
| judge | 沒打分 | `needs_review: false` 是你的斷言；§1.3 的 Kling 與 Hailuo 都沒有自動品檢 |
| manifest 頂層 `clip` | 下一次 `clips` 會改成伺服器的選擇 | 有 profile 的作品把整份 manifest 當舊的丟掉重買（`modelCurrent`）；沒有 profile 的保留 |

**提議的工具**——票已開：`tasks/open/2026-10-03-clips-import-bring-a-clip-made.md`，契約以票的 Definition of done 為準，下面照抄，免得實作的人看到兩種：`node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"] [--judge] [--force]`。

- 前置同 `clips`：storyboard 沒核准就拒絕（3）；timeline 不現行 2；這一鏡必須是 clip 鏡（不是 still、不是 `source`）。
- 複製檔案到 `clips/<shot>-import-<n>.mp4`，`ffprobe`（時長、解析度、fps），跑買來的 take 同一組 QC（`qc.mjs`：黑格、凍格、切鏡、首格對這一鏡關鍵影格的 PSNR）；`--judge` 才上傳媒體庫叫 `clipRubric`（記 US$0.01 一筆 `kind: "judge"`）。
- 首格 PSNR 低於 `keyframe_min_psnr`（22，`qc.mjs`）的片段跟失敗的 take 一樣 `needs_review: true` 帶原因；`--force` 留下它並記 note。
- 寫 manifest 項目：`clips` 寫的形狀（`file`、`sha256`、`seconds`、`frames`、`needed_s`、`first_frame`、`qc`、`judge`、`takes`、`needs_review`）加平鋪的 `provider`、`plan`、`credits`、`imported_at`；重算 `clips_hash`，`recordStage(workdir, "clips", …)`。
- 帳本一筆：`{ stage: "clips", kind: "clip", id, provider, plan, credits, cost_usd: --usd 或 0, status: "imported" }`；票要 `ledgerTotals`（`tools/video/media/ledger.mjs`）算進它的秒數，`clips` 的 dry run 與本 skill 的 `run_report.mjs` 把匯入的跟買的分開列。`--usd` 沒給時票不替你把點數換成美元：點數對美元在 §1.2、§1.3 的表與 `episode_estimate.mjs` 的 PRICES，報帳時自己乘。
- 有 profile 的作品：票不改 profile；`productionClipProblems` 放行外部來源要 profile 先有欄位（站主決定），是第二張票。
- 結束碼：票只定了 storyboard 的 3；其餘照 `tools/video/cli.mjs` 的 `EXIT` 慣例（0 成功、1 品檢沒過、2 順序不對、3 要站主、5 ffmpeg 沒裝）。

今天本 skill 的腳本認外部片段的方法是 manifest 的 `provider: "external"`，或帳本沒有這一鏡的 job（`run_report.mjs`、`drama_preflight.mjs` 各自的 `external` 篩選），路線與點數從 `stage-preconditions.md` 那個例子的 `external` 區塊讀。指令落地後 `provider` 會是 `hailuo-web`／`kling-mcp`、帳本會有 `status: "imported"` 那一筆，兩支腳本要改成讀它——票的 Definition of done 點名 `run_report.mjs`，`drama_preflight.mjs` 一起改。

## 4. 權利與安全

- **帳號是站主的**。Hailuo 與 Kling 的登入、訂閱、加購都由站主做；代理不建帳號、不輸入密碼、不用自己的帳號、不把 cookie 或權杖寫進對話、檔案與指令參數（`youtube-video` skill 規矩 9）。MCP 連接器也是站主在自己的 Claude Desktop／claude.ai 加的。
- **商用與浮水印**：Hailuo 免費方案的下載有浮水印，不能上架；Standard 以上無浮水印且條款寫明保留 IP 含商用。Kling 每個付費方案去品牌浮水印、商用；免費層沒讀到條款，當作不能用。產線自己的 Lyria 音樂帶 SynthID 浮水印（目錄註解），是允許的。
- **內容規則**：Hailuo 有內容審查，審查不過退積分；MiniMax API 的 1026／1027／2013 是內容被拒（`apps/api/app/video_media/providers/minimax.py`）；Kling 的內容政策沒有逐條讀，當作一樣有。被拒的題材先回報，不換字繞。
- **提示詞不帶個資**：不寫真人姓名、照片、聲音、站主的資料、金鑰；不用真人臉與聲音；這跟產線的規矩一樣（`docs/videos/DRAMA.md` 的 YouTube 一節）。
- **上架揭露**：3D 寫實 AI 畫面與 AI 配樂都勾「變造或合成內容」，不分哪一條路線買的。
- **檔案不進 git**：下載的 mp4、紀錄 JSON 都在 `<VIDEO_WORKDIR>` 底下；repo 是公開的。
- **價目會變**：本文的方案價 2026-10-03 讀、目錄價 2026-09-26／28 讀、profile 2026-10-01 核實、Kling 積分與 API 價未驗證。定一場戲的錢之前先讀 §5 的頁面，改日期；頁面讀不到（SPA、登入牆）就寫「未驗證」，不要補一個數字。

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
| Kling 會員方案 | kling.ai 會員頁（內建瀏覽器） | 2026-10-03 |
| Kling 官方 MCP | kling.ai/mcp（WebFetch 回 401）、kling.ai/app/mcp/guide（登入牆） | 2026-10-03 |
| Kling 社群 MCP | github.com/199-mcp/mcp-kling README | 2026-10-03 |
| Kling 積分／段、API 價 | 第三方整理，未驗證 | 2026 |
| 試作的花費與重拍 | `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`、`docs/videos/series-plans/competition-20261002/budget-and-launch.md`、`docs/videos/series-plans/competition-20261002/cost-ledger.csv` | 2026-10-03 |
