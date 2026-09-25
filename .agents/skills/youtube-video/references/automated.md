# 全自動路線：AI 撰稿、台灣口音旁白、自動做成片

這條路線的成品是一支投影片加旁白的影片。旁白由伺服器用 Azure 語音合成，畫面由 HTML 版型截圖，合成用 ffmpeg，CC 字幕五語系。站主只要在四個地方把關：

1. 選大綱
2. 聽旁白
3. 看成片、確認可以上架
4. 在 YouTube Studio 按公開

前三個都在網站後台的「影片審核」頁（`/admin/videos`）做：工具用 `review-push` 把該關的東西送上去（企劃與選項、旁白與 Jev 檢查、720p 成片與五語系標題、上傳檢查表），站主在頁面上核准或退回，工具再用 `review-pull` 讀回。核准綁定檔案雜湊，檔案改過就要重新送審。對話裡的提問只在後台頁用不了時當備援。

為什麼這樣設計、YouTube 與 Azure 的規則，寫在 `docs/videos/DESIGN.md`；頻道的版型、配色與聲音寫在 `docs/videos/README.md`。這份只寫**怎麼做**。

路徑寫法：`<ROOT>` 是 repo 根目錄；`<VIDEO_WORKDIR>` 是影片的工作資料夾，預設在使用者家目錄下，可以用 `--workdir` 或環境變數 `VIDEO_WORKDIR` 改；`<SLUG>` 是影片代號；`<VIDEO_DOCS>` 是這支影片在 repo 裡的資料夾 `docs/videos/<SLUG>/`，只放文字檔。音檔、畫面、mp4 只放在 `<VIDEO_WORKDIR>/<SLUG>/`，絕不進 git（repo 是公開的）。

## 一次性設定（站主做，代理不經手任何金鑰）

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| Azure 語音 | Azure 入口網站建 Speech 資源（F0 免費層）。金鑰與區域填在正式站後台：「API 與供應商設定 → AI 服務 → Azure 語音（影片旁白）」，然後按連線測試 | `tts` 結束碼 3 |
| 影片工具權杖 | 在同一張卡按「建立權杖」→ 複製。站主**自己**在終端機執行 `node tools/video/cli.mjs login` 貼上（輸入會隱藏） | `tts` 結束碼 3，提示去 login |
| ffmpeg | Windows 執行 `winget install BtbN.FFmpeg.GPL`；Ubuntu 執行 `apt-get install ffmpeg`；也可以設 `FFMPEG_PATH` 指定位置 | `assemble` 結束碼 5 |
| 瀏覽器 | `npx playwright install chromium`；Windows ARM64 上建議用原生的 Edge：`render --channel msedge`，或設 `VIDEO_BROWSER_CHANNEL=msedge` | `render` 結束碼 5 |

## 主幹

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 0 | 認領票、開工作區 | 協調者 | — | 票已認領 |
| 1 | 企劃（提示 `.agents/skills/youtube-video/references/prompts/planner.md`） | 企劃代理（sonnet） | `<VIDEO_DOCS>/brief.md` | `review-push` 送企劃；站主在 `/admin/videos` 從 2–3 個大綱選一個；`review-pull` 記下核准 |
| 2 | 撰稿（提示 `.agents/skills/youtube-video/references/prompts/writer-video.md`） | 撰稿代理（sonnet） | `video.json`、`claims.md`、發音字典新增的詞 | `lint` 零錯誤 |
| 3 | 查核（提示 `.agents/skills/youtube-video/references/prompts/verifier-video.md`） | **另一個**代理（opus） | `verify-1.md` | 改超過 3 個事實，就換人再查一輪，寫 `verify-2.md` |
| 4 | 聽眾優先審稿：口語、句長、術語唸法、開場鉤子 | 審稿代理 | 修正清單 | 協調者套用後再跑 `lint` |
| 5 | `tts` | 工具 | 每句的音檔、`narration.wav`、`timeline.json` | 先跑 `--dry-run` 看字數與額度 |
| 6 | `check-audio`（Gemini 轉寫、Jev 判斷），再 `review-push` 送旁白 | 工具、站主 | `review/check-flags.json` | 被標的句子補字典或改措辭，`tts --redo review/check-flags.json` 只重錄那幾句；站主在 `/admin/videos` 核准旁白，`review-pull` 記下 |
| 7 | `render` | 工具 | `frames/`、`contact-sheet.png`、`thumbnail.jpg` | 看聯絡表；版面錯誤就縮短文字 |
| 8 | `assemble` | 工具 | `final.mp4`、`checks.json` | 自動檢查全過 |
| 9 | CC 翻譯：`i18n-sheet` 出底稿 → 每個語系一個翻譯代理（`prompts/caption-translate.md`，sonnet）填 → `i18n-merge` → 另一個審稿代理（`prompts/caption-review.md`，opus）只交修正清單 → 協調者改底稿再 merge → `captions` | 翻譯與審稿代理、工具 | `<VIDEO_DOCS>/i18n/<語系>.json`、`captions/*.srt` | `i18n-merge` 沒有列出問題；lint 沒有過期或缺漏的翻譯 |
| 10 | `review-push` 送成片（720p 預覽、聯絡表、縮圖、五語系標題說明） | 站主 | — | 站主在 `/admin/videos` 看完核准，`review-pull` 記下 |
| 11 | `package`，再 `review-push` 送上架確認 | 工具、站主 | `upload/`（含 `UPLOAD.md`） | 核准的成片必須和目前的 `final.mp4` 一致；站主按「確認可以上架」，`review-pull` 記下 |
| 12 | 站主照 `UPLOAD.md` 在 Studio 上傳成私人，檢查後自己按公開 | 站主 | YouTube 影片 | 影片 ID 寫回 `video.json` 的 `youtube.video_id` |

隨時可以跑 `node tools/video/cli.mjs status --slug <SLUG>`，它會列出 12 步做到哪裡，並印出下一個該跑的指令。它判斷的依據是比對各檔案裡記下的雜湊，不看紀錄：腳本改過，舊的旁白就不算完成。

## 指令

```bash
node tools/video/cli.mjs status   --slug <SLUG>
node tools/video/cli.mjs lint     --slug <SLUG>              # 或 --file 指向範例
node tools/video/cli.mjs ids      --count 20 --slug <SLUG>   # 新句子的穩定 id
node tools/video/cli.mjs audition --text-file <FILE> [--voices a,b]   # 中文一律走檔案
node tools/video/cli.mjs tts      --slug <SLUG> [--dry-run] [--redo flags.json]
node tools/video/cli.mjs review   --slug <SLUG>
node tools/video/cli.mjs render   --slug <SLUG> [--channel msedge]
node tools/video/cli.mjs assemble --slug <SLUG>
node tools/video/cli.mjs i18n-sheet --slug <SLUG> [--locale en,ja]   # 翻譯底稿在 <VIDEO_WORKDIR>/<SLUG>/i18n/，只標出缺漏或過期的句子
node tools/video/cli.mjs i18n-merge --slug <SLUG> [--locale en,ja]   # 底稿寫回 i18n/<語系>.json，雜湊由工具算
node tools/video/cli.mjs captions --slug <SLUG>
node tools/video/cli.mjs review-push --slug <SLUG> [--gate outline|audio|final|publish]   # 送審到 /admin/videos
node tools/video/cli.mjs review-pull --slug <SLUG>              # 讀回站主的決定，核准才寫進 approvals.json
node tools/video/cli.mjs approve  --slug <SLUG> --gate outline|audio|final|publish --note "<站主怎麼回答的>"   # 後台頁不能用時的備援
node tools/video/cli.mjs package  --slug <SLUG>
node tools/video/assemble/smoke.mjs --workdir <DIR> [--channel msedge]   # 整條流程的冒煙測試
```

結束碼：0 成功；1 lint 或檢查沒過；2 用法錯誤或順序不對（例如還沒 tts 就 assemble）；3 需要站主（權杖、後台設定、核准）；4 外部服務或額度；5 工具沒裝。要中途停下來，在工作區或它的上一層放一個 `STOP` 檔：長的階段做完手上那一段就會停，下次從快取接著做。

## video.json 的重點

- 格式定義在 `tools/video/core/schema.mjs`。
- 最小範例：`tools/video/core/fixtures/minimal/video.json`。
- 每種版型各用一次的範例：`tools/video/templates/fixtures/showcase/video.json`。

寫作重點：

- **句子 id**：用 `ids` 產生，是穩定的短碼。插入新句子時不要重新編號，翻譯、快取和站主的唸錯標記都靠它對齊。
- **章節**：有 `chapter` 的場景會開一個 YouTube 章節。章節至少 3 個，每個至少 10 秒；lint 先用估計值檢查，`tts` 之後再用實際時間檢查一次。
- **版型**：共 11 種，資料欄位與可以逐條出現的數量定義在 `tools/video/templates/templates.mjs` 的 `TEMPLATE_SPECS`。`**文字**` 會變成強調色，`\n` 是手動斷行。
- **圖片與圖解**：只能用 `apps/web/public/` 或 `docs/videos/` 底下的檔案，並列在 `assets`，寫清楚來源與授權。
- **說明欄**：`youtube.description` 只寫本文。章節時間戳、站內文章連結（依 `source_guide` 自動加 UTM）、參考資料（`sources`），都由工具組進去。

## 發音與試聽

- 中文 TTS 最常唸錯英文縮寫和破音字。發音字典是 `docs/videos/` 底下的 `lexicon.json`，所有影片共用，第一支影片建立它。每個英文詞都要在字典裡，lint 才會過。
- 格式是 `{ "schema_version": 1, "terms": { … } }`。`terms` 的值有兩種：唸法（例如 `"LLM": "L L M"`，送出時變成 `<sub alias>`），或 `null`（表示照原字唸就對，要等試聽確認過）。
- zh-TW 的 `<phoneme>` 音標沒有官方文件，不要用。
- 第一次開頻道，先用 `audition` 產生幾個聲音給站主比較：曉臻、雲哲、曉雨，以及 Ava、Andrew 講台灣國語。站主選定之後寫進 `docs/videos/README.md`，之後每支影片都用同一個聲音。

## 成本

- Azure 每個中文字算兩個計費字元，SSML 標記也計費。一支 10 分鐘的影片約 8,000–9,000 計費字元，免費額度每月 50 萬，大約可以做 50 支。
- `tts --dry-run` 會印出這支影片的估計字數，以及伺服器回報的本月用量。
- 每月上限由站主在後台卡片設定。超過時伺服器以 429 拒絕，請求不會送到 Azure，所以不會產生費用。

## 坑

- **中文參數一律寫進檔案**：PowerShell 5.1 會弄壞命令列上的非 ASCII 參數，所以 `audition` 只收 `--text-file`；`approve --note` 也盡量寫英文或短句。
- **`render` 回報版面錯誤**：代表縮小 40% 以後字還是放不下，或畫面裡有字型沒有的字（例如 emoji）。處理方式是縮短文字或換版型，不要改主題 CSS。
- **`assemble` 回報某一格「不像」預期的畫面**：代表畫面錯位了，先看 `checks.json` 是哪個場景的哪一格。門檻：44 dB 以上直接算對、35 以下算錯；中間（字很密的表格、比較卡，正確也只有 40 左右）要比同場景其他畫面高 3 dB，`checks.json` 會記下它和每個對手的分數。不要調低門檻。
- **`tts` 回報某一批改成逐句合成**：代表那一批的靜音切段和字數對不上。這通常不影響成品，只是多送幾次請求。如果同一批一直發生，把那個場景拆短一點。
- **代理不能碰權杖**：`login` 要站主自己跑，權杖不能出現在對話裡、檔案裡或指令參數裡。
