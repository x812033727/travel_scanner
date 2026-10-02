# Mokaair 影片頻道規格

這份是頻道的「長相」：每支全自動影片都照這裡做，改這裡等於改整個頻道。產線怎麼跑寫在 skill `youtube-video`（`.agents/skills/youtube-video/references/automated.md`），為什麼這樣設計、YouTube 與 Azure 的官方規則寫在 [`DESIGN.md`](DESIGN.md)。AI 漫劇（`format: "drama"`：AI 生成的鏡頭片段、多角色配音、燒錄字幕、配樂）是第二種格式，設計在 [`DRAMA.md`](DRAMA.md)；下面沒有另外說的地方，漫劇都照這份。投影片影片可以帶插圖、配樂與音效（**插圖投影片**，2026-09-29 定案，設計在 [`ILLUSTRATED.md`](ILLUSTRATED.md)）：卡片之間放 AI 插圖加運鏡，單狀態卡片漂移、畫面間溶接。

## 資料夾

| 路徑 | 放什麼 |
| --- | --- |
| `docs/videos/DESIGN.md` | 產線設計與官方規則 |
| `docs/videos/README.md` | 這份頻道規格 |
| `docs/videos/lexicon.json` | 所有影片共用的發音字典（第一支影片建立） |
| `docs/videos/<slug>/` | 一支影片的文字檔：`brief.md`、`video.json`、`claims.md`、`verify-*.md`、`i18n/<語系>.json` |

音檔、畫面、mp4 與站主的核准紀錄 `approvals.json` 只放在 repo 外的工作區（`VIDEO_WORKDIR`），不進 git。

## 成品規格

| 項目 | 規格 | 在哪裡定 |
| --- | --- | --- |
| 畫面 | 1920×1080、30 fps | `tools/video/core/timeline.mjs` |
| 影像編碼 | H.264 High、CRF 18、`stillimage`、2 個 B 幀、2 秒一個 closed GOP、4:2:0、BT.709 標記 | `tools/video/assemble/plan.mjs` |
| 聲音 | AAC-LC 立體聲 48 kHz 384 kbps；兩段式 loudnorm 到 −14 LUFS、峰值 −1 dBTP | 同上 |
| 容器 | MP4，faststart | 同上 |
| 縮圖 | 1280×720 JPEG | `tools/video/render/` |
| 長度 | **每集至少 8 分鐘，漫劇除外**（站主 2026-10-01 定；原來如此事務所也算在內）：投影片 8–12 分鐘（`video.json` 的 `target_minutes` 可以改，但下限不得低於 8），原來如此事務所 8–12 分鐘；`lint` 估計不足 8 分鐘是錯誤，成片品管（`qa` 的 `assemble` 項）量到不足 8 分鐘不給過。漫劇一集 2–4 分鐘；一鍵合集把一部作品的每集接成一支，30–480 分鐘可設、預設 120（設計在 [`BINGE.md`](BINGE.md)） | `tools/video/core/schema.mjs`（`MIN_EPISODE_MINUTES`）、`tools/video/core/drama.mjs` 的 `needsMinimumLength`、`apps/api/app/video_automation/schemas.py`（`EPISODE_MIN_MINUTES`）、`apps/api/app/video_automation/series.py` 的 `binge_shape` |
| 合集 | 每集成片 `-c copy` 串接、音訊重編一次；集間 2 秒章節卡、片尾 4 秒卡；章節＝每集；五語字幕合併。審核頁只放 720p 預覽（`-crf 26 -maxrate 2M`，兩小時約 ≤ 2 GB）；1080p 成片從後台的作品頁或「可以上架」卡下載（`GET /admin/videos/{slug}/download`，API 唯讀掛載工人的 `video_work`）再上傳。合集的 `category_id` 是 24（娛樂） | `tools/video/core/compilation.mjs`、`tools/video/compile/cli.mjs` |
| 字幕 | zh-TW 的 CC 一定有。en、ja、ko、zh-CN 的 CC 與標題說明是每支影片的選擇：成片核准後站主在 `/admin/videos` 那支影片的「這支影片的語言」面板勾了才做，工人只做勾了的、做好才排上架（[`LANGUAGES.md`](LANGUAGES.md)；設定分頁的 `caption_locales` 只是面板的預先勾選）。投影片影片**不燒錄**；漫劇預設把繁中字幕燒進畫面（漫劇頻道的慣例），由 `video.json` 的 `subtitles.burn_in` 決定 | `tools/video/core/captions.mjs`、`tools/video/core/stages.mjs`、`tools/video/core/drama.mjs` |
| 配音音軌 | 語言的第三個部件：投影片影片可以多掛 en、ja、ko、zh-CN 四條 YouTube 多語言音軌，同一個頻道聲音唸字幕的翻譯，塞在 zh-TW 的畫面時間軸裡。站主在同一個面板勾了配音才做（勾配音會一起勾 CC），做好後由站主在 Studio「語言」上傳、在「語言」卡片按「已在 Studio 上傳配音」；做不出來的語系跳過並寫原因，不擋上架。漫劇第一期不做。音軌怎麼做在 [`DUBS.md`](DUBS.md) | `tools/video/dubs`、`tools/video/automation/flow.mjs` |
| 配樂與音效 | 任何格式都可以帶 `music`（站主提供有授權的檔案放 `<VIDEO_WORKDIR>/_music/`，或由 Lyria 生成），在旁白下自動壓低到 ≤ −24 LUFS；插圖投影片另可帶 `sfx`（授權音效組放 `_sfx/<set>/`：章節卡蓋章、溶接 whoosh、逐條出現 pop）。純投影片預設兩者都沒有 | `tools/video/core/drama.mjs`、`tools/video/assemble/sfx.mjs` |

每句旁白和它後面的停頓，都補到整格（48,000 Hz ÷ 30 fps ＝ 每格 1,600 個取樣），所以十分鐘的影片不會有影音漂移。

## 版型

深色主題，由網站圖解的配色反轉而來（`docs/life-ai-series-brief.md` 第 6 節）：網站的文字色當底色、紙色當文字、青綠提亮成強調色，橘色只用在最重要的一個詞。定義在 `tools/video/templates/theme.css`。

| 用途 | 顏色 |
| --- | --- |
| 底色 | `#0e2627`，面板 `#173d3e` |
| 文字 | `#f7f1e8`，次要 `#a8bcb8` |
| 強調 | 青綠 `#4fc1b5`；`**文字**` 會變成這個顏色 |
| 重點 | 橘 `#f0a04b`，一張投影片最多用一次 |
| 程式碼底 | `#081819` |

字型只用 Noto Sans TC 與 JetBrains Mono，兩者都是開源字型，由 npm 套件提供，不讀系統字型。畫面下方 12% 不放重要內容，因為 YouTube 的控制列和 CC 字幕在那裡。

15 種投影片版型（每種的欄位與上限在 `tools/video/templates/templates.mjs` 的 `TEMPLATE_SPECS`，範例在 `tools/video/templates/fixtures/showcase/video.json`），加上不是 HTML 版型的 `shot`（一張 AI 插圖加運鏡，[`ILLUSTRATED.md`](ILLUSTRATED.md)；插圖投影片每 5–8 秒一張、至少佔一半時間）：

| 版型 | 用在 | 可以逐條出現 |
| --- | --- | --- |
| `title` | 開場：問題當標題、一句副標、一個標籤 | — |
| `chapter` | 章節開頭的大字 | — |
| `bullets` | 1–6 個重點 | 每一條 |
| `compare` | 左右兩欄比較 | 左、右 |
| `steps` | 2–5 個步驟 | 每一步 |
| `table` | 最多 5 欄 8 列的表，可以標出一列 | 每一列 |
| `code` | 最多 16 行、每行 64 字元的程式碼，可以標出幾行 | — |
| `big` | 一個關鍵數字或關鍵詞 | — |
| `diagram` | repo 裡的 SVG 圖解（沿用文章的圖） | — |
| `screenshot` | repo 裡的截圖，可以框出一塊 | 框 |
| `outro` | 結尾：回答、下一步、`mokaair.com` | — |

縮圖用 `thumb` 版型：一個標籤、一行大標、一行小字，左下角是 MOKAAIR 字樣。

## 片頭與片尾

- **頻道片頭／片尾**：站主選定 5 秒無標語片頭，以及 3 秒「按讚、分享、開啟小鈴鐺」片尾。安裝外部素材包後，新製長片在正文之外加入這兩段；字幕、章節及多語音軌一起調整。素材安裝、舊片採用及狀態邊界見 [`BRANDING.md`](BRANDING.md)。Shorts 不套用。
- **正文開場**仍是開場鉤子（`title` 版型）：第一句是觀眾的問題或一個反直覺的說法，30 秒內說完「為什麼該看、會得到什麼、怎麼進行」。正文 `outro` 版型負責回答與內容下一步；頻道片尾是正文後的獨立素材。合集有頻道片尾時省略原本額外的 4 秒結尾卡。
- 配樂：插圖投影片用站主的授權音樂床（`music.track`），純投影片不放；漫劇的配樂規則在 [`DRAMA.md`](DRAMA.md)。

## 聲音

| 項目 | 值 |
| --- | --- |
| 供應商 | Azure 語音，由正式站伺服器代為合成（金鑰在後台「API 與供應商設定 → AI 服務 → Azure 語音（影片旁白）」） |
| 頻道聲音 | **還沒選**。第一支影片開工前，用 `audition` 讓站主聽同一段旁白比較：曉臻、雲哲、曉雨，以及 Ava、Andrew 講台灣國語。選定後寫在這裡，之後每支影片都用同一個聲音 |
| 語速 | `+0%`；稿子的長度以每分鐘 250 字估計 |
| 口吻 | 2026-09-29 起是**說書式**（Gemini `voice.style`：有起伏、揭曉前停一拍、「你以為」放慢、「其實」亮起來；全文在 [`ILLUSTRATED.md`](ILLUSTRATED.md)），站主在 `/admin/videos` 設定分頁貼上；改了 style 全部重錄 |
| 停頓 | 句與句之間 0.3 秒，換場景多 0.7 秒；單句可以用 `pause_after_ms` 改 |

## 說明欄

站主或撰稿代理只寫 `youtube.description` 的本文。上架包裡的說明，由 `package` 依下面的順序組好：

1. 本文。前兩行說這支影片回答什麼、給誰看（搜尋結果只顯示這兩行）。
2. `章節`：由實際的時間軸算出，第一個是 0:00，至少 3 個，每個至少 10 秒。
3. `完整文章`：`source_guide` 指向的 Mokaair 文章，帶語系與追蹤參數。
4. `參考資料`：`sources` 裡的每個官方頁。

各語系的標籤文字（例如英文的 Chapters）定義在 `tools/video/core/metadata.mjs`。說明欄上限 5,000 位元組：中文一個字佔 3 位元組，所以大約是 1,666 個中文字，章節與連結也算在內。標題、說明都不能有角括號。

站內連結的格式：

    https://mokaair.com/<語系>/life/<slug>?utm_source=youtube&utm_medium=video&utm_campaign=<影片 slug>
    https://mokaair.com/<語系>/guides/<kind>/<slug>?utm_source=youtube&utm_medium=video&utm_campaign=<影片 slug>

生活與 AI 類文章用第一種，其他類用第二種。每個語系的說明都連到同語系的文章；文章沒有那個語系時，連到 zh-TW 版。

## 上架

- 分類 28（科學與技術），不是兒童專屬，預設語言 zh-TW。
- mp4 一律由站主在 YouTube Studio 上傳，先設成「私人」：沒通過稽核的 API 專案上傳的影片會被鎖成私人。
- 公開或排程，永遠由站主自己按。
- 上架前的檢查表在上架包的 `UPLOAD.md`；判斷標準在 `.agents/skills/youtube-video/references/publish.md`。

## 本機工具

| 工具 | 版本與來源 | 備註 |
| --- | --- | --- |
| Node | 22 以上（`package.json` 的 engines） | 和 repo 其他工具一樣 |
| ffmpeg（Windows ARM64） | BtbN 的 GPL 版 `N-125875-g5d4d3bdc61-20260731`，`winget install BtbN.FFmpeg.GPL` 安裝；`ffmpeg.exe` 的 SHA256 是 `4FBD8C3D57188AE4AB0F91D02883CE83F774AFB294D824E098A10C02AC6995AD` | 原生 ARM64，含 libx264、loudnorm、ebur128、psnr。不用 Playwright 附的 ffmpeg（只有 VP8），也不用 `ffmpeg-static` |
| ffmpeg（CI） | Ubuntu 的 `apt-get install ffmpeg` | `.github/workflows/video-tooling.yml` |
| 瀏覽器 | Playwright 的 Chromium；Windows ARM64 上用原生 Edge（`--channel msedge` 或 `VIDEO_BROWSER_CHANNEL=msedge`） | Playwright 附的 Chromium 在 ARM64 上是模擬執行，而且版本要對 |

換 ffmpeg 版本時，更新這一節，並跑一次 `node tools/video/assemble/smoke.mjs`：它會從範例影片一路做到上架包，檢查格數、色彩標記、響度與每個場景的抽樣格。

## 改規格的時候

- 改主題顏色或版型：先跑 `node tools/video/cli.mjs render --file tools/video/templates/fixtures/showcase/video.json`，看聯絡表上每種版型都還正常。
- 改編碼或響度：更新 `ENCODER_VERSION`，讓快取失效；同時更新 `DESIGN.md` 的規則表。
- 選定或更換頻道聲音：更新上面的聲音表，並在後台卡片的允許清單加上那個聲音。已經上架的影片不重做。
