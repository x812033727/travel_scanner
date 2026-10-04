# 供應商與方案：伺服器 API、Hailuo／Kling 網頁、選用的 CLI／MCP

給用手寫、用手導、用手跑漫劇的代理：同一個鏡頭的素材今天有三條路可以買，這一篇把三條並排、算一鏡與一集各要多少錢、說外部素材現在怎麼進產線（以及產線會不知道什麼）、最後是權利與安全。它不重複別處已經寫好的事：產線的步驟、指令與結束碼在 `.agents/skills/youtube-video/references/drama.md`；第一版的供應商決定與設計在 `docs/videos/DRAMA.md`；Veo 3.1 Lite 的鏡頭契約與十部動畫的製作規格在 `.agents/skills/youtube-video/references/animation-production.md`；一個鏡頭的 `camera`／`motion`／`prompt` 怎麼寫、同一鏡怎麼改寫給 Hailuo 的表單與 Kling 的鏡頭控制，在 animation-camera skill。

每個數字都標來源：**價目**是官方頁或目錄檔讀到的（附日期）；**工具規定**是 `tools/video` 或 `apps/api` 裡的常數（附檔名）；**模型限制**是供應商文件寫的；**實測**是在站主的帳號上送出、下載或讀到的（附日期；2026-10-04 是 Hailuo 的一支片段與 Kling CLI 的輸出）；**推算**是本文從前兩者算出來、沒有在生成器裡核對過的；**未驗證**是第三方整理或根本讀不到的。價目與積分會不預告就改：定一場戲的錢之前，先把本文 §5 的頁面再讀一遍，把日期更新。

**開拍前先讀 `.agents/skills/animation-preproduction/references/route-decisions.md`**：每鏡走哪條路、買幾秒、哪個解析度、正文照哪家官方格式寫，都在那裡定，並寫進開拍鎖定包；這篇是方案、價目與帳的細節。2026-10-04 研究代理逐頁讀了官方頁（MiniMax 平台文件、hailuoai.video 訂閱頁與 UI 字串、Hugging Face 上的 MiniMax-H3 官方提示指南、kling.ai 的 quickstart、API 文件與價目頁），本文標「官方 2026-10-04」的都來自那次。

**本次 route 以使用者指定為準**：使用者提供內建瀏覽器並選 Hailuo／Kling 時，先讀 `browser-production.md`、依當次工具文件查 upload／download、做三鏡 pilot，再沿既有接受流程擴大。下面的價格與 Claude／Kling CLI 操作結果保留為歷史來源；它們不把本次 Kling 網頁換成 CLI，不代表今天的 UI、點數或 Codex 瀏覽器能力已驗。

## 1. 三條路線並排

| | 伺服器 API（產線本來的路） | Hailuo 網頁訂閱（hailuoai.video） | Kling 網頁；選用的官方 CLI／MCP、社群 MCP＋API |
| --- | --- | --- | --- |
| 誰在呼叫 | `node tools/video/cli.mjs clips` 經網站的媒體端點叫 Gemini／MiniMax；金鑰只在站上 | 本次代理用使用者提供的內建瀏覽器與**站主的登入**；檔案能力依 browser-production 查本次文件 | 本次同樣先用 Kling 網頁與站主登入；CLI／MCP 另選才用，開發者 API 的資源包與會員積分分開 |
| 計價 | 每秒：`usd_per_second × seconds`，解析度不改價（工具規定，`apps/api/app/video_media/meter.py` `usd_for`） | 月費換積分，積分月底歸零；用完可加購 | 會員月費換積分；開發者 API 另賣資源包，兩邊不互通 |
| 片段模型 | `apps/api/app/video_media/catalog.py` 列的：Omni 1.1 Flash、Veo 3.1／Fast／Lite、MiniMax-H3 | H3、H3 Max、Hailuo 2.0／2.3／1.0、Sora 2、Veo 3.1 | CLI 列的 `kling-video-v3_0`、`v3_0_omni`、`v3_0_turbo`、`o1`、`v2_5`、`v2_6`，另有 `motion_control`（實測 2026-10-04，§1.3） |
| 首尾格與參考圖 | 首格必帶；參考圖最多 4（`MAX_REFERENCES`，`apps/api/app/video_media/schemas.py`；目錄寫 H3 9 張、Pro Image 14 張是供應商上限，不是我們送得出的）；Lite 不收參考圖 | H3 首格、末格；參考上傳區「參考 (0/12)」，但**有首格時不能再帶參考圖**（官方 2026-10-04：H3 的 v2 API 圖生影片與參考生影片互斥）；Hailuo 2.3 只有首格 | `kling-video-v3_0`：`first_image`＋`tail_image`、elements；`v3_0_omni`／`o1`：`image_1`…`image_7`；`v3_0_turbo` 只有 `first_image`（實測 2026-10-04）。網頁 VIDEO 3.0 可首格＋綁最多 3 個元素（官方 2026-10-04） |
| 品檢 | ffmpeg（`tools/video/media/qc.mjs`）＋ judge 自動跑，不過換 seed，最多 2 次（`MAX_CLIP_TAKES`，`tools/video/media/clips.mjs`） | 站方沒有；`clips import` 匯入時跑同一組 ffmpeg 檢查，judge 要帶 `--judge` | 同左 |
| 快取、帳本、預算 | `media/cache.json`（同一請求不付兩次）、`media/ledger.json`（每筆花費）、伺服器的每月預算與單支上限 | 沒有快取與伺服器預算；`clips import` 把點數與秒數記進帳本（`status: "imported"`） | 同左 |
| 進產線 | 直接 | 下載後 `clips import`（§3） | 同左 |
| 浮水印、商用 | 無浮水印；依各供應商條款 | 免費下載有浮水印；Standard 以上沒有，且保留 IP 含商用（條款，2026-10-03 讀）。付費帳號也要走「無水印下載」：結果卡 `<video>` 的 src 是有浮水印的版本（實測 2026-10-04，§1.2） | 付費方案去浮水印、「Generated content is for commercial use」（會員頁，2026-10-03 讀） |
| 併發 | 伺服器每小時 240 次圖片送出、360 次 judge（`apps/api/app/video_media/admin_api.py`）；每月 3,000 片段秒、1,500 張圖、3,000 次 judge、60 首音樂（預設，`apps/api/app/video_automation/models.py`） | 方案表：排隊 Standard 8、Pro 8、Master 12、Max 12，同時跑 1／2／2／2（官方 2026-10-04 再讀）；條款（2025-07-14 版）的「排 5、跑 2」是舊的 | 付費方案：排隊不限、fast-track |
| 今天能用在 | 任何漫劇；有 production profile 的作品只能用 profile 指定的模型 | **沒有** production profile 的漫劇；import 對任何 profile 都拒絕，不只是不符 provider（§3） | 同左；repo 沒有 Kling adapter（`tasks/open/2026-09-26-video-drama-kling-provider-card.md`，P3） |

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
| Max | US$199.99 | US$184.00（US$2,208／年） | 27,000 | 12／2 | 4K 無限 | 積分用完後無限生成、進較慢的 relax 隊列。2026-10-04 的 tooltip 列 Hailuo 1.0、1.0-Director、1.0-Live、2.0、2.3、2.3-Fast，**H3 不在**（官方）；FAQ 還寫「20,000 積分」與「1.0 和 2.0」，是沒更新的舊答案。`SKILL.md`、`cost-model.md` 與 `episode_estimate.mjs` 的 PLANS 都指這一格 |

條款（價目，2026-10-03）：會員積分一個月到期；加購 US$1 換 70 積分，有效到購買後第二個日曆年的 12 月 31 日；付費方案「retain any and all intellectual property rights to such content, including the right to use it for commercial purposes」；免費下載有浮水印、Standard 以上沒有；取消不退款；生成失敗或**內容審查不過**自動退積分（所以有內容審查）。條款頁還列著舊方案 Unlimited US$94.99 與 Ultra US$124.99，訂閱頁沒有。

**積分怎麼換秒**：H3 2K 每秒 12 積分是**實測 2026-10-04**——建立列「創建」旁邊顯示這次送出要扣的積分，H3 2K 5 秒顯示 60，送出後餘額 27,150 → 27,090；跟先前用訂閱頁每方案「約可做幾秒」反推的數字一致。量的是 Max 帳號；其他方案也是 12，仍是那個反推（四個方案的每月秒數都對得上）。H3／H3 Max 768P 每秒 7 積分、H3 Max 480P 每秒 4 積分：2026-10-04 官方頁有了依據（UI 的價錢提示字串寫「Video: 12 Credits/s」，方案表的每月秒數 1,000 積分＝768P 143 秒、H3 Max 480P 250 秒，正好是 7 與 4）；仍沒有在帳號上實扣 768P。頁面程式包裡另有每月繳的每秒美元標籤（H3 2K：Standard 0.126、Pro／Master 0.102、Max 0.096），跟標價月費 ÷ 秒數（Pro 0.147）對不上，可能是促銷價，送出前以頁面為準。所以一段 8 秒 2K 是 96 積分（12 × 8），8 秒 768P 是 56 積分（推算）。訂閱頁自己標的「每秒美元」（Standard：2K US$0.101、768P US$0.059；Pro 以上：2K US$0.081、768P US$0.047、480P US$0.027）**只在年繳價成立**（375 秒 × 0.081 ≈ US$30.40，就是 Pro 的年繳月價）；月繳要用下表。

| 每秒 | Standard | Pro | Master | Max | 加購積分 |
| --- | --- | --- | --- | --- | --- |
| 美元／積分 | 月繳 0.0150；年繳 0.0084 | 0.0122；0.0068 | 0.0114；0.0068 | 0.0074；0.0068 | 0.0143 |
| H3 2K（12 積分，實測 2026-10-04） | 0.180；0.101 | 0.147；0.081 | 0.137；0.081 | 0.089；0.082 | 0.171 |
| H3 768P（7 積分，推算） | 0.105；0.059 | 0.086；0.047 | 0.080；0.047 | 0.052；0.048 | 0.100 |
| 每月 2K 秒數 | 84 | 375 | 875 | 2,250 | — |
| 每月 768P 秒數 | 143 | 643 | 1,500 | 3,857 | — |

模型與方案（訂閱頁）：H3 4–15 秒 768p／2K；H3 Max 5–15 秒 480p／768p；Hailuo 2.3 6 秒 768p／1080p（Pro 以上 10 秒）；Hailuo 2.0（首尾格）6 秒 512p／768p／1080p（Pro 以上 10 秒）；Sora 2 4／8／12 秒 720p；Veo 3.1 8 秒 720p／1080p；Hailuo 1.0 6 秒 720p。各模型每段扣幾積分在生成器的建立列（「創建」旁）看得到：H3 2K 實測過（上段），H3 768P 與 H3 Max 有官方依據（上段）；其他模型訂閱頁 FAQ 有寫（官方 2026-10-04）：Hailuo 2.3／2.0 768p 6 秒 25、1080p 6 秒 80、768p 10 秒 50；2.3-Fast 15／50／30；Sora 2 4／8／12 秒 40／80／120；Veo 3.1 8 秒 120（促銷，原價 320）、3.1-Fast 60（原價 120）。首尾格只有 Hailuo 2.0（API 的 fl2v 是 02）；2.3 與 2.3-Fast 沒有首尾格。注意 H3 沒有 1080p：2K 的輸出是 2560×1440（實測 2026-10-04），768P 在 1080p 之下（輸出尺寸沒量）；production profile 要求原生 1920×1080（§3）。

**實測的一支**（2026-10-04，站主的 Max 帳號，文生影片，MiniMax H3、2K、5 秒、16:9；只有這一支，768P 與圖生影片都沒量）：

- 積分：扣 60（12／秒），餘額 27,150 → 27,090。
- 時間：送出到完成約 4 分 40 秒，當時沒有別的在排隊。
- 輸出：2560×1440、24 fps、124 格、5.167 秒、h264 約 6 Mbps，帶一條 AAC 音軌。所以 2K 不是 1920×1080，production profile 的原生 1080p 檢查不收（§3）；尺寸與 fps 都在 `tools/video/media/qc.mjs` 的下限（1280×720、23 fps）之上。音軌是模型生成的，成片不能用：`assemble` 的畫面段落只取影像、帶 `-an`（`tools/video/assemble/drama.mjs` 的 `encodeArgs`），在別處用這個檔要自己去掉。
- 設定面板的選項：比例 自動／21:9／16:9／4:3／1:1／3:4／9:16，解析度 768p／2K，時長 4–15 秒整數。**比例預設是 21:9，要改。**
- 浮水印：結果卡 `<video>` 的 src 是有浮水印的版本；當時乾淨的檔走「全部下載 → 無水印下載」，本次按官方 UI 與工具文件核對。

**歷史 Claude 瀏覽器能力**（實測 2026-10-04；不當作 Codex 本次操作指令）：

- **文生影片**在 Claude 桌面版的內建瀏覽器裡做得完；站主的登入會留在 pane。
- **當時的 Claude 桌面版圖生影片沒有本機 upload 工具**；頁面讀 loopback 也被擋（`net::ERR_BLOCKED_BY_CLIENT`）。沒有送出圖生影片，換瀏覽器的 upload 方案亦未驗；不能推論現在的 Codex 同樣做不到。
- 當時隱藏 pane 的選單／截圖失敗，窄視窗的設定鈕難操作，提示框是 Slate 編輯器。這些是當時 UI 的觀察，現行表單先讀新狀態，不沿用舊選擇器、頁面 action JS 或讀取 browser profile 的做法。

**本次操作**照 `browser-production.md`：使用者登入與提供分頁 → 查工具能力與匯入目的地 → 上傳核准首格 → 核對 16:9、模型、解析度、單鏡與秒數 → 記完整提示、首格 hash、job 與點數 → 一次送出 → 查同一 job → 官方無浮水印下載 → 三鏡實速小樣 → 匯入。無負面欄位時，把已核准的限制清楚接入正文並記輸入方式；不以未核對的舊 UI 細節作為操作依據。

浮水印歷史實測：卡片播放檔右下角有「MINIMAX | Hailuo AI」，官方「無水印下載」取得另一份乾淨檔。`clips import` 的 ffmpeg 檢查看不出浮水印，下載錯版本仍可能通過；`--judge` 的 `no_text` 題也只可能抓到，所以下載後實看。送出到完成約 4 分 40 秒與 60 點只是當時那一支的結果，不給本次隊列或價錢保證。

### 1.3 Kling

**本次網頁路線**：使用者提供內建瀏覽器時，照 `browser-production.md` 查當次 upload、download、首格／參考圖、單鏡、音訊、模型與價錢。CLI 的 model id、參數名與 NORMAL 帳號結果不替代網頁欄位，網頁的控制語法仍待 pilot 驗。匯入用 `--provider external --note "route=kling-web …"`，如實留 job 與提示收據。

**會員**（kling.ai 會員頁，2026-10-03 在內建瀏覽器讀，月繳視圖；WebFetch 同日只拿到殼）：

| 方案 | 標價／月 | 首月 | 之後每月（月繳 12% off） | 積分／月 | 頁面標的「每 100 積分」 |
| --- | --- | --- | --- | --- | --- |
| Standard | US$10 | US$6.99 | US$8.80 | 660 | US$1.06（是首月價算的） |
| Pro | US$37 | US$25.99 | US$32.56 | 3,000 | US$0.87 |
| Premier | US$92 | US$64.99 | US$80.96 | 8,000 | US$0.81 |
| Ultra | US$180 | US$127.99 | US$159.99 | 26,000 | US$0.49 |

年繳 34% off。每個付費方案：排隊不限、fast-track、1080p、圖片放大、去品牌浮水印、影片延長、商用；Pro 以上先用新功能；高階有 4K。官方的「每 100 積分」以續訂價算是 Standard US$1.33、Pro 1.09、Premier 1.01、Ultra 0.62（kling.ai 積分花費部落格，2026-07-28；上表的頁面數字是首月價算的）。

**每秒扣幾積分（官方 2026-10-04，還沒在站主帳號實扣）**：VIDEO 3.0 與 3.0 Omni 不開原生音訊 1080p 8、720p 6；開音訊 12／9；語音控制再加 2；4K 30；Omni 帶參考影片 16／12（不支援音訊）；O1 1080p 8、720p 6；2.6 不開音訊專業 5、標準 3（kling.ai quickstart 的各模型 user guide 與積分花費部落格）。所以 1080p 不開音訊的 5 秒是 40——先前第三方的「5 秒 40」只對這一種成立。秒數：3.0／Omni 3–15 整數，O1 3–10，2.6 只有 5 或 10。網頁有「輸出數」設定（2.6 指南寫一次最多 4 支）：要設 1；積分是不是照支數乘官方沒寫，送出前看 Generate 旁的數字。失敗的生成退積分，「批次生成」標不退（UI 字串）。Multi-Shot 關著時 3.0 預設產生單鏡；正文寫 single continuous shot。Kling 4.0 官方說 10 月上線（3–30 秒、10 張關鍵影格），價目頁還沒有。

**另選 CLI／MCP 的歷史資料**（指南 `kling.ai/app/mcp/guide`，登入後讀得到；實測 2026-10-04）。指南說同一個助理只裝其中一種；先前 CLI 的選擇不覆蓋本次網頁指定：

- **MCP**：端點 `https://kling.ai/mcp`；在 Claude 是 Customize → Connectors → Add custom connector，用 Kling 帳號登入。
- **CLI**（站主 2026-10-04 選的）：npm 套件 `@klingai/cli-global`（2026-10-04 是 0.2.1，maintainer `klingai-fe`），執行檔 `kling`。`kling login` 開系統預設瀏覽器做 OAuth（PKCE；scope 是 `generation.create`、`generation.read`、`account.credit.read`），權杖存在 `~/.kling/.credentials`。同意由站主在瀏覽器裡按；代理不讀、不貼那個檔。

指令與 MCP 的工具一對一：`who_am_i`、`text_to_video`、`image_to_video`、`omni_ref_video`、`text_to_image`、`image_to_image`、`motion_control`、`motion_library_list`、`element_create`／`element_list`／`element_get`／`element_update`／`element_delete`、`query_tasks`、`file_upload`、`account`、`tool_list`、`feedback`、`logout`。

- `kling account` 回 `membershipType` 與 `availableRemainCredits`：是**會員積分**（官方 MCP／CLI 常見問題說跟網頁同一套，2026-10-04 讀），不是開發者資源包；還沒有用一次付費生成核對扣點。
- `kling who_am_i` 列模型與參數，不給積分價。

`image_to_video` 的模型（NORMAL 免費帳號列出的，**全部只有 720p**；實測 2026-10-04）：

- `kling-video-v3_0`：時長 3–15 秒整數；輸入 `first_image` 與 `tail_image`；elements；`enable_audio` 預設 true；`prefer_multi_shots` 預設 **true**。
- `kling-video-v3_0_omni` 與 `kling-video-o1`：輸入 `image_1`…`image_7`；`aspect_ratio` 16:9／9:16／1:1；`o1` 是 3–10 秒。
- `kling-video-v3_0_turbo`：只有 `first_image`。
- `kling-video-v2_5` 與 `kling-video-v2_6`：5 或 10 秒。

**進產線時 `enable_audio` 與 `prefer_multi_shots` 都要傳 false**：一鏡是一個連續鏡頭（模型自己切鏡是 `tools/video/media/qc.mjs` 會擋的那一類），片段的聲音成片不用。

**還沒驗的**：當時帳號顯示 `membershipType` NORMAL、0 積分，所以沒有生成任何東西。官方的 MCP／CLI 常見問題（kling.ai 網頁的 UI 字串，2026-10-04 讀）說 MCP 與 CLI 跟網頁用同一套積分、訂閱權益通用；每秒的價也有官方數字（上段）。還沒實際扣過一支、付費方案在 CLI 上有沒有 1080p 仍**未驗證**；另選 CLI 且有生成授權時，先讀帳號／模型資料並記一次生成前後差額，再改實測紀錄。CLI 做的片段匯入時用 `--provider kling-mcp`（`clips import` 只有 `hailuo-web`、`kling-mcp`、`external` 三個值），是 CLI 做的就寫進 `--note`；網頁用 external，兩者不混寫。

**社群 MCP**（github.com/199-mcp/mcp-kling，2026-10-03 讀 README）：用開發者 API 的 access key 與 secret key 自動簽 JWT，扣的是**資源包**，不是會員積分；工具有 `generate_video`（5 或 10 秒、標準／專業、cfg_scale、鏡頭控制）、`generate_image_to_video`（圖生影片，鏡頭控制 `static`／`zoom`／`pan`／`auto` 加一段 motion prompt）、`extend_video`、`create_lipsync`、`generate_image`（KOLORS）、`get_account_balance`、`get_resource_packages`、`list_tasks`；結果下載到本機 `./downloads/` 底下分類資料夾。對應我們的運鏡字（詳見 animation-camera skill）：`locked`→`static`，`push-in`／`pull-out`→`zoom`（方向寫進 prompt），`pan-left`／`pan-right`→`pan`，`drift` 沒有對應，用 `static` 加 motion prompt。它的 `generate_video` 只給 5 或 10 秒，是這個社群工具的限制，不是 Kling 3.0 的。

**開發者 API**（kling.ai/dev/pricing 與 API 價目文件，官方 2026-10-04，從官方 JS 包讀；`docs/videos/why-openai-killed-sora/verify-1.md` 2026-09-28 讀的一致）：1 unit ＝ US$0.14；Kling 3.0 每秒 720P 0.6 u（US$0.084）、1080P 0.8 u（US$0.112），有音訊 0.9／1.2 u，4K 3.0 u；3.0 Omni 無影片無音訊 0.6／0.8 u；失敗不扣。先前第三方整理的資源包價（US$9.80／100 units 起、180 天、20 併發）在官方頁沒找到，**未驗證**。會員積分與 API units 分開賣，不互通。

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
| Kling 3.0 1080p 8 秒、音訊關（64 積分） | 標價 Standard 0.97、Pro 0.79、Premier 0.74、Ultra 0.44；續訂 0.85／0.69／0.65／0.39；年繳 0.64／0.52／0.49／0.29 | 官方每秒 8 積分（2026-10-04），未實扣；美元是月費 ÷ 積分的換算；原生 1920×1080（官方說 1080p，尺寸未量） |
| Kling 開發者 API 3.0 1080p 8 秒 | 0.90（0.8 u × 8 × 0.14） | 官方 2026-10-04 |

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
| Kling 3.0 1080p 每鏡 8 秒（3,840 積分） | Premier 標價 44.16、續訂 38.86、年繳 29.15；Ultra 26.58／23.63／17.60 | 10.02 | 28–54 | 官方每秒價，未實扣；Pro 的 3,000 不夠一集 |
| Kling 3.0 1080p 照鏡長買（每鏡約 4 秒＝1,920 積分，`shot_plan.mjs` 與 `episode_estimate.mjs` 的算法） | Pro 標價 23.68、續訂 20.84、年繳 15.63 | 10.02 | 26–34 | 官方每秒價，未實扣；Pro 一個月夠一次 take，兩次不夠 |
| Kling 開發者 API 1080p 8 秒 | 53.76 | 10.02 | 64 | 官方（0.8 u × 480 秒 × US$0.14） |

重拍不在表裡：伺服器路線每鏡最多 2 次（工具規定）；試作實際是 S01 送 4 次、S03 送 2 次、0 段被接受（量到的，`production-run-20261003.md`），而 `budget-and-launch.md` 的規矩是三份成功素材都不合格就重新設計鏡頭，不靠重抽。外部路線的重拍上限只有你自己的紀律，先在紀錄 JSON 裡寫下這一鏡允許幾次。操作時間也不在表裡：每段上傳、設定、等隊列、下載、`clips import`。量過的只有一支：Hailuo H3 2K 5 秒、沒有別的在排隊，送出到完成約 4 分 40 秒（實測 2026-10-04）；60 鏡的人工時數沒有量過。

**訂閱什麼時候贏過每秒計價**：只有一個條件——這個月**真的用掉的秒數** ≥ 月費 ÷ 伺服器的每秒價。沒用完的積分月底歸零，所以分母是用掉的，不是方案給的。下表 Hailuo 的方案秒數是積分 ÷ 12（H3 2K 每秒 12 積分，實測 2026-10-04）；Kling 兩列是積分 ÷ 8（官方每秒價，未實扣）。

| 方案（H3 2K） | 月費 | 方案秒數 | 換算每秒 | 要用到幾秒才贏 Lite 0.08 | 贏 H3 API 0.13 | 贏 Omni 0.15 |
| --- | --- | --- | --- | --- | --- | --- |
| Hailuo Pro 月繳 | 54.99 | 375 | 0.147 | 687（不可能） | 423（不可能） | 367（幾乎全用） |
| Hailuo Pro 年繳 | 30.40 | 375 | 0.081 | 380（差一點，不可能） | 234 | 203 |
| Hailuo Master 月繳 | 119.99 | 875 | 0.137 | 1,500（不可能） | 923（不可能） | 800 |
| Hailuo Master 年繳 | 71.20 | 875 | 0.081 | 890（不可能） | 548 | 475 |
| Hailuo Max 月繳 | 199.99 | 2,250 | 0.089 | 2,500（積分內不可能；之後 Hailuo 2.3 無限） | 1,538 | 1,333 |
| Kling Pro 標價（官方每秒價，未實扣） | 37 | 375 | 0.099 | 不可能 | 285 | 247 |
| Kling Ultra 標價（官方每秒價，未實扣） | 180 | 3,250 | 0.055 | 2,250 | 1,385 | 1,200 |

結論（編輯判斷，建立在上面的數字）：在產線現在的 Lite 價（0.08／秒 1080p）之下，**沒有任何訂閱靠每秒單價贏**；但網頁照鏡長買（3 秒的鏡頭 Kling 買 4 秒、Lite 永遠 8 秒），一鏡的錢網頁可能比較少（`animation-preproduction/references/route-decisions.md` 第三節的表），這要用 `shot_plan.mjs` 對整集各算一次。訂閱贏的是（a）對 Omni 或 H3 API 的價，且每個月把積分用到八九成；（b）Max 積分用完後 Hailuo 2.3 1080p 的無限生成，量大且等得起隊列時；（c）Pro 以上無限的圖片生成，前提是關鍵影格能進 `keyframes/manifest.json`——今天沒有 import，storyboard 關卡綁的是工具畫的那份；（d）伺服器沒有 adapter（Kling）或主機地區被擋（`docs/videos/DRAMA.md` 的地區一節）。代價在 §3：沒有快取與自動 retake、judge 要另外問，每一段都要自己下載再 `clips import`。

## 3. 外部素材怎麼進產線

用 `clips import`（2026-10-04 落地，PR #1183；同一天用真的 ffmpeg 在下載的那支 Hailuo 片段上跑過，實測 2026-10-04。程序**只寫在 `stage-preconditions.md` 最後一節**，設計在 `docs/videos/DRAMA.md`「外面做的片段」）：

`node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"] [--judge] [--force]`

它查 `clips` 的前提（timeline 與 keyframes 是現在的、這一鏡的關鍵影格通過、storyboard 核准），把檔案複製成 `clips/<shot>-import-<n>.mp4`，跑買來的 take 同一組 ffmpeg 檢查（`tools/video/media/qc.mjs` 的 `clipVerdict`），寫 `clips`（`tools/video/media/clips.mjs`）自己寫的那種 manifest 條目加 `provider`、`plan`、`credits`、`imported_at`，在帳本記一筆 `status: "imported"`；`assemble`（`tools/video/assemble/cli.mjs`）與 `status`（`tools/video/core/state.mjs` `pipelineStatus`）照常讀那份 manifest。要記得的兩句沒變：外部素材的首格要用通過 judge 的那張關鍵影格，不然第 0 格 PSNR 會讓它 `needs_review`（`--force` 才留下）；judge 預設不問，`--judge` 才上傳媒體庫問 `clipRubric`（US$0.01）。實測（2026-10-04）多出兩句：**ffmpeg 檢查看不出浮水印**，Hailuo 下載錯版本（§1.2）匯入照樣通過，只有 `--judge` 的 `no_text` 題可能抓到；外面做的片段可能帶生成音軌，成片不用它。用產線關鍵影格當首格的圖生影片還沒有匯入過。

**任何 production profile 都不能匯入**：`importClip` 對存在的 `series.production.profile` 無條件以 3 拒絕，單改 provider／model 也不會解除。`productionClipProblems`（`tools/video/core/lint.mjs`）另要求 manifest 頂層 `clip.provider/model/resolution` 等於 profile（十部動畫的契約在 `docs/videos/series-plans/production-20261001/profile.json`）、QC 通過與素材蓋滿台詞；`productionClipSizeProblem` 另驗原生 1920×1080。縮放 H3 的 2K、手改 manifest 或刪 profile 都不能作為受核准的外部路線支援。既有正片要採用外部路線，須另做產線匯入／驗證支援與契約更新並重新綁核准；這次只改技能，不開放它。付費之前查目的地，避免做出不能使用的素材。

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
- **商用與浮水印**：Hailuo 免費方案的下載有浮水印，不能上架；Standard 以上無浮水印且條款寫明保留 IP 含商用，但歷史付費帳號的卡片播放檔仍有浮水印，要走官方無水印下載（§1.2）。Kling 付費方案的去浮水印與商用描述也是當時資料；本次核對實際方案、下載與條款。產線自己的 Lyria 音樂帶 SynthID 浮水印（目錄註解），是允許的。
- **內容規則**：Hailuo 有內容審查，審查不過退積分；MiniMax API 的 1026／1027 是內容被拒，2013 是參數錯（`apps/api/app/video_media/providers/minimax.py` 照官方文件這樣分）；Kling 的內容政策沒有逐條讀，當作一樣有。被拒的題材先回報，不換字繞。
- **提示詞不帶個資**：不寫真人姓名、照片、聲音、站主的資料、金鑰；不用真人臉與聲音；這跟產線的規矩一樣（`docs/videos/DRAMA.md` 的 YouTube 一節）。
- **上架揭露**：3D 寫實 AI 畫面與 AI 配樂都勾「變造或合成內容」，不分哪一條路線買的。
- **檔案不進 git**：下載的 mp4、紀錄 JSON 都在 `<VIDEO_WORKDIR>` 底下；repo 是公開的。
- **價目會變**：本文的方案價 2026-10-03 讀、目錄價 2026-09-26／28 讀、profile 2026-10-01 核實；Hailuo H3 2K 的每秒積分、生成時間與輸出規格、Kling CLI 的指令與模型表是 2026-10-04 實測；Kling 的每秒積分與 API 價、Hailuo 其他模型的積分是 2026-10-04 讀的官方頁，還沒實扣。定一場戲的錢之前先讀 §5 的頁面，改日期；頁面讀不到（SPA、登入牆）就寫「未驗證」，不要補一個數字。

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
| 當時缺本機 upload、pane 與表單操作限制 | Claude 桌面版的內建瀏覽器，同一次操作；不當作本次 Codex 的能力結論 | 實測 2026-10-04 |
| Kling 會員方案 | kling.ai 會員頁（內建瀏覽器） | 2026-10-03 |
| Kling 官方 MCP 與 CLI：端點、套件、登入、指令、`image_to_video` 的模型與參數 | kling.ai/app/mcp/guide（登入後）、npm `@klingai/cli-global` 0.2.1、`kling who_am_i` 與 `kling account` 的輸出（NORMAL 帳號、0 積分） | 實測 2026-10-04 |
| `clips import` | PR #1183（`tools/video/media/clips.mjs`）；真的 ffmpeg 跑在下載的 Hailuo 片段上 | 實測 2026-10-04 |
| Kling 社群 MCP | github.com/199-mcp/mcp-kling README | 2026-10-03 |
| Kling 每秒積分、輸出數、單鏡、元素、首尾格 | kling.ai/quickstart 的 VIDEO 3.0、3.0 Omni、O1、2.6 user guide；kling.ai/blog 的積分花費指南；kling.ai 網頁 UI 字串 | 官方 2026-10-04 |
| Kling API 價 | kling.ai/dev/pricing、API 價目文件 | 官方 2026-10-04 |
| Hailuo 其他模型的積分、Max 無限的模型、隊列 | hailuoai.video 訂閱頁的方案表、FAQ、tooltip 與 UI 字串 | 官方 2026-10-04 |
| H3 的首格與參考互斥、秒數、輸出、提示格式 | platform.minimax.io 的 v2 video generation 文件；Hugging Face 上 MiniMax-H3 的官方提示指南；hailuoai.video 的 H3 工具頁 | 官方 2026-10-04 |
| 試作的花費與重拍 | `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`、`docs/videos/series-plans/competition-20261002/budget-and-launch.md`、`docs/videos/series-plans/competition-20261002/cost-ledger.csv` | 2026-10-03 |
