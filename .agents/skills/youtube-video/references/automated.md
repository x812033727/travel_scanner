# 全自動路線：AI 撰稿、台灣口音旁白、自動做成片

這條路線的成品是一支投影片加旁白的影片。旁白由伺服器代為合成（頻道聲音是 Gemini 的 Sulafat；Azure 是另一個供應商，站主覺得它的聲音太平），畫面由 HTML 版型截圖，合成用 ffmpeg。每支先只出繁體中文（CC 與標題說明）；其他語言（en、ja、ko、zh-CN 的標題說明、CC、配音）由站主在成片核准後為每支影片勾選才做（`docs/videos/LANGUAGES.md`，下面第 13 步）。關卡有四個（`docs/videos/HANDS-OFF.md`），前三個由 AI 決定，站主決定的是語言與上架時間：

| 關卡 | 誰決定 | 什麼時候才輪到站主 |
| --- | --- | --- |
| 選大綱 | Jev 依設定分頁的「頻道立場」挑（`POST /video/automation/judge/outline`）；選中的選項要符合立場 ≥ 0.6、有示範 ≥ 0.6、整份企劃的建議 ≤ 0.3 | 頻道立場還是空白或開關關著（伺服器回 409）；Jev 沒挑出過關的大綱、企劃模型重寫 `MAX_REPLANS`（2）次仍不過，這時審核卡片附上 Jev 的表 |
| 聽旁白 | Jev 每一句都唸對就核准 | 有句子被標記 |
| 看成片 | 自動品管（`qa` 的 11 項）全過、雜湊等於這份成片就核准 | 有項目沒過：卡片最上面列出沒過的項目與細節 |
| 確認上架 | 上傳包檢查（`files`、`descriptions`、`captions`、`disclosure`）全過就核准，影片進「可以上架」 | 有項目沒過 |

都在網站後台的「影片審核」頁（`/admin/videos`）：工具用 `review-push` 把該關的東西送上去（企劃、選項與 Jev 的 pick；旁白與 Jev 檢查；720p 成片、標題說明與 `qa` 的報告；完整上傳包與它的檢查；做好的語言批次），伺服器收到時照規則核准或留給站主，工具再用 `review-pull` 讀回。核准綁定檔案雜湊，檔案改過就要重新送審；同一份檔案還在等站主時再送一次，會換上新的 payload 重新判斷（字幕或連結修好後再 `review-push --gate final` 就會重判）。站主在 Studio 上傳成私人之後，在「可以上架」卡片貼上網址，工人下一輪把影片 id 寫進 `video.json`，影片就算完成。對話裡的提問只在後台頁用不了時當備援。

為什麼這樣設計、YouTube 與 Azure 的規則，寫在 `docs/videos/DESIGN.md`；頻道的版型、配色與聲音寫在 `docs/videos/README.md`。這份只寫**怎麼做**。

路徑寫法：`<ROOT>` 是 repo 根目錄；`<VIDEO_WORKDIR>` 是影片的工作資料夾，預設在使用者家目錄下，可以用 `--workdir` 或環境變數 `VIDEO_WORKDIR` 改；`<SLUG>` 是影片代號；`<VIDEO_DOCS>` 是這支影片在 repo 裡的資料夾 `docs/videos/<SLUG>/`，只放文字檔。音檔、畫面、mp4 只放在 `<VIDEO_WORKDIR>/<SLUG>/`，絕不進 git（repo 是公開的）。

## 一次性設定（站主做，代理不經手任何金鑰）

| 項目 | 怎麼做 | 沒做會怎樣 |
| --- | --- | --- |
| Gemini 語音（頻道聲音） | 不用新金鑰：伺服器用網站既有的 Gemini 金鑰（`hotspot_guide_gemini_api_key`，在「AI 供應商與金鑰」）。`video.json` 寫 `"voice": {"provider": "gemini", "name": "Sulafat", "style": "…"}`，模型預設 `gemini-3.8-flash-tts`。每月字數上限另計（預設 300,000 字），設在「Azure 語音（影片旁白）」卡片上 | `tts` 結束碼 3 |
| Azure 語音 | 只有選 Azure 聲音時才需要。Azure 入口網站建 Speech 資源（F0 免費層），金鑰與區域填在同一張「Azure 語音（影片旁白）」卡，按連線測試 | `tts` 結束碼 3 |
| 影片工具權杖 | 配對，不貼權杖（RFC 8628 裝置流程）：代理在背景跑 `node tools/video/cli.mjs login`，把它印出的連結（`/zh-TW/admin/settings?provider=azure_speech&video_pairing=…`，開到卡片的「配對本機工具」）交給站主；站主核對驗證碼和終端機上一樣，按「允許」。權杖直接寫進 `~/.mokaair/video-tool.json`，不會印出來。配對在 Redis 只活 10 分鐘，權杖在領取時才產生、只能領一次 | `tts` 結束碼 3，提示去 login |
| ffmpeg | Windows 執行 `winget install BtbN.FFmpeg.GPL`；Ubuntu 執行 `apt-get install ffmpeg`；也可以設 `FFMPEG_PATH` 指定位置 | `assemble` 結束碼 5 |
| 瀏覽器 | `npx playwright install chromium`；Windows ARM64 上建議用原生的 Edge：`render --channel msedge`，或設 `VIDEO_BROWSER_CHANNEL=msedge` | `render` 結束碼 5 |

## 主幹

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 0 | 認領票、開工作區 | 協調者 | — | 票已認領 |
| 1 | 企劃（提示 `.agents/skills/youtube-video/references/prompts/planner.md`；有頻道立場時，站主觀點第一行寫「套用立場：N、M」） | 企劃代理（sonnet） | `<VIDEO_DOCS>/brief.md` | `review-push --gate outline` 先問 Jev 挑哪一個，過關就附上 pick 送審、伺服器直接核准；Jev 關著（409）才由站主在 `/admin/videos` 選；`review-pull` 記下核准 |
| 2 | 撰稿（提示 `.agents/skills/youtube-video/references/prompts/writer-video.md`） | 撰稿代理（sonnet） | `video.json`、`claims.md`、發音字典新增的詞 | `lint` 零錯誤 |
| 3 | 查核（提示 `.agents/skills/youtube-video/references/prompts/verifier-video.md`） | **另一個**代理（opus） | `verify-1.md` | 改超過 3 個事實，就換人再查一輪，寫 `verify-2.md` |
| 4 | 聽眾優先審稿：口語、句長、術語唸法、開場鉤子 | 審稿代理 | 修正清單 | 協調者套用後再跑 `lint` |
| 5 | `tts` | 工具 | 每句的音檔、`narration.wav`、`timeline.json` | 先跑 `--dry-run` 看字數與額度 |
| 6 | `check-audio`（Gemini 轉寫、Jev 判斷），再 `review-push` 送旁白 | 工具、站主 | `review/check-flags.json`、`review/rewrites.json` | 被標的句子補字典或改措辭，`tts --redo review/check-flags.json` 只重錄那幾句；重錄到上限仍被標的句子，工人交給聽眾審稿模型改寫措辭（提示 `.agents/skills/youtube-video/references/prompts/listener-rewrite.md`；數字、拉丁字詞、字典詞變了就退回這句），再 `tts --redo` 重錄、再檢查，最多兩輪，改了什麼寫在 `review/rewrites.json`、送審時附在 `payload.rewrites`；Jev 全過就自動核准，否則站主在 `/admin/videos` 核准旁白，`review-pull` 記下 |
| 6b | 插圖投影片才有：`keyframes`（每個 `shot` 一張圖，judge 評分、最多 3 次換 seed；先 `--dry-run` 看提示詞與最多幾塊錢）→ `review-push --gate storyboard`（伺服器依 judge 分數自動核准）→ `review-pull` | 工具 | `keyframes/manifest.json`、`keyframes/contact-sheet*.png` | 沒有 `needs_review` 的 shot；分鏡核准綁 manifest（改卡片文字不會失效，改 camera 或 prompt 才會） |
| 7 | `render` | 工具 | `frames/`、`contact-sheet.png`、`thumbnail.jpg` | 看聯絡表；版面錯誤就縮短文字 |
| 7b | 有 `music` 才有：`music`（`music.track` 只核對 `_music/` 裡的檔案與 sha） | 工具 | `music/manifest.json` | 檔案在、雜湊對 |
| 8 | `assemble` | 工具 | `final.mp4`、`checks.json` | 自動檢查全過 |
| 9 | `captions`：只有繁體中文的 CC（成片前不翻譯；其他語言在第 13 步） | 工具 | `captions/zh-TW.srt` | `captions/manifest.json` 的雜湊等於這份旁白 |
| 10 | `review-push --gate final`：先跑 `qa`（11 項，寫到 `review/qa.json`；字幕與標題說明兩項只看 zh-TW 加已選的語言），再送成片（720p 預覽、聯絡表、縮圖、標題說明、`payload.qa`） | 工具 | `review/qa.json` | 11 項全過、`final_sha256` 等於這份 `final.mp4`，伺服器就核准；沒過的才由站主在 `/admin/videos` 看；`review-pull` 記下。`qa` 結束碼 4（Jev 或連結檢查連不上）就不送，下一輪再試 |
| 11 | `package`（寫完就跑上傳包檢查、揭露答案寫進 `metadata.json`），再 `review-push --gate publish` 送上架確認：完整上傳包（`final`、`thumbnail`、`captions_<語系>`、`description_<語系>`、`metadata`）加 `payload.package` | 工具 | `upload/`（含只剩操作步驟的 `UPLOAD.md`） | 4 項全過、雜湊等於 `upload/metadata.json`，伺服器就核准；`review-pull` 記下。影片要等第 13 步的語言都做好才進「可以上架」，站主隨時可以先上傳 mp4 |
| 12 | 站主照 `UPLOAD.md` 在 Studio 上傳成私人，到 `/admin/videos` 的影片頁貼上網址、選上架時間 | 站主 | YouTube 影片 | 工人下一輪把影片 ID 寫回 `video.json` 的 `youtube.video_id`，影片標成完成；公開由站主選的時間決定，語言還在做時排程等語言做好才送出 |
| 13 | 語言（`docs/videos/LANGUAGES.md`），**成片核准後、站主在 `/admin/videos` 的影片頁「這支影片的語言」勾了才做**（四語 × 標題說明、CC、配音，或「只出繁體中文」）。工人把選擇抄成 `<VIDEO_WORKDIR>/<SLUG>/languages.json`，然後每個語言：`i18n-sheet --locale <語系> --parts <勾了的 metadata,captions>`（勾配音時每句帶 `max_chars`）→ 翻譯代理（`prompts/caption-translate.md`）→ `i18n-merge` → 審稿代理（`prompts/caption-review.md`）→ 再 merge；勾配音的再 `dub --locale <語系>` → 塞不下的句子走翻譯代理的縮短模式（`caption-translate.md` 最後一節）→ `i18n-merge` → 再 `dub`（最多 2 輪）→ `check-audio --locale <語系>` → `dub --redo`（最多 2 輪）；全部做好 `captions`（有配音的語系跟配音的時間）→ `package` → `review-push --gate languages` | 工具、翻譯與審稿代理、站主 | `<VIDEO_DOCS>/i18n/<語系>.json`、`captions/<語系>.srt`、`dubs/<語系>.m4a`、`upload/` 裡對應的檔 | 沒有配音的批次伺服器直接核准；有配音的，站主照 `UPLOAD.md` 的「配音音軌」在 Studio「語言」上傳後按「已在 Studio 上傳配音」。做不出來的配音寫進 `dubs/<語系>/skipped.json`，不擋影片。規則在 `publish.md` 的「語言」與 `docs/videos/DUBS.md` |

第 4 步聽眾審稿最常抓到的四種問題：代理替站主編經驗（「我都自己測過」）；台灣介面有中文名稱卻寫英文 UI 名；預測沒標成意見；引用站上已經過期的圖解。

隨時可以跑 `node tools/video/cli.mjs status --slug <SLUG>`，它會列出主幹做到哪裡（語言那一步不在清單上：它掛在影片頁的面板與 `languages.json`），並印出下一個該跑的指令。它判斷的依據是比對各檔案裡記下的雜湊，不看紀錄：腳本改過，舊的旁白就不算完成。

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
node tools/video/cli.mjs i18n-sheet --slug <SLUG> [--locale en,ja] [--parts metadata,captions]   # 翻譯底稿在 <VIDEO_WORKDIR>/<SLUG>/i18n/，只標出缺漏或過期的句子、章節、標題、說明與標籤；--parts 只出站主勾的部件，勾配音且有時間軸時每句帶 max_chars
node tools/video/cli.mjs i18n-merge --slug <SLUG> [--locale en,ja]   # 底稿寫回 i18n/<語系>.json，雜湊由工具算；底稿沒有的部件不動
node tools/video/cli.mjs captions --slug <SLUG>                 # zh-TW 加 languages.json 勾了 CC 的語系；沒有 languages.json 就每個有翻譯的語系
node tools/video/cli.mjs qa       --slug <SLUG>                 # 成片的 11 項自動品管，寫到 review/qa.json（結束碼 0 過、1 沒過、4 外部服務）
node tools/video/cli.mjs review-push --slug <SLUG> [--gate outline|audio|final|publish|languages]   # 送審到 /admin/videos；outline 先問 Jev，final 先跑 qa，publish 附完整上傳包，languages 送做好的語言批次（要先 package）
node tools/video/cli.mjs review-pull --slug <SLUG>              # 讀回決定（站主的或伺服器自動核准的），核准才寫進 approvals.json
node tools/video/cli.mjs approve  --slug <SLUG> --gate outline|audio|final|publish --note "<站主怎麼回答的>"   # 後台頁不能用時的備援
node tools/video/cli.mjs package  --slug <SLUG>
node tools/video/cli.mjs dub      --slug <SLUG> --locale en,ja [--dry-run] [--format m4a|mp3|wav] [--redo review/check-flags.en.json]   # 配音音軌：先 --dry-run 看字數、額度與塞得下幾個視窗；工人只做 languages.json 勾了配音的語系
node tools/video/assemble/smoke.mjs --workdir <DIR> [--channel msedge]   # 整條流程的冒煙測試
```

結束碼：0 成功；1 lint 或檢查沒過；2 用法錯誤或順序不對（例如還沒 tts 就 assemble）；3 需要站主（權杖、後台設定、核准）；4 外部服務或額度；5 工具沒裝。要中途停下來，在工作區或它的上一層放一個 `STOP` 檔：長的階段做完手上那一段就會停，下次從快取接著做。

## video.json 的重點

- 格式定義在 `tools/video/core/schema.mjs`。
- 最小範例：`tools/video/core/fixtures/minimal/video.json`。
- 每種版型各用一次的範例：`tools/video/templates/fixtures/showcase/video.json`。
- 英文旁白的範例：`tools/video/core/fixtures/en/video.json`。

寫作重點：

- **旁白語言**：預設 zh-TW。英文影片在 `video.json` 頂層寫 `"narration_locale": "en"`（2026-09-28 起，英文第一季 `docs/ai-video-en-season-01/`），`youtube.default_language` 也要是 `en`。這時：lint 只要求全大寫的縮寫（SEC、GPT、API）進字典，一般英文字照寫；字典裡含中文的唸法（`p95 → P 九十五`）自動不套用，跟配音一樣；`voice.style` 寫英文版的語氣（`tools/video/dubs/plan.mjs` 的 `DUB_STYLES.en` 可以直接抄）；`check-audio` 以 `en` 轉寫與判斷，同音字與語助詞規則不用；`i18n-sheet` 以英文為原文翻成 zh-TW、ja、ko、zh-CN，配音也可以做 zh-TW；說明欄的標籤文字用英文版。長度估算沿用每分鐘 250 個「單位」（一個英文字算兩單位，約 125 字／分），Gemini 實唸約 150 字／分，所以估計偏長兩成，跟中文一樣。
- **分類**（`category`，可省略；2026-10 起）：`/admin/videos` 篩選用，代碼與站上的 `VIDEO_CATEGORIES`（`tools/video/core/schema.mjs`，同 `apps/api/app/models.py`）一致，共十個：`ai-terms`（AI 名詞解釋）、`ai-news`（AI／科技時事）、`tutorial`（教學實作）、`comparison`（比較評測）、`explainer`（觀念解說）、`story`（品牌故事）、`drama`（漫劇）、`long-drama`（長篇劇）、`travel`（旅遊）、`other`（其他）；寫別的 lint 會擋。worker 的每次回報（`flow.mjs` 的 `report()`，狀態檔的 `category` 優先，其次 `video.json`）與 `review-push` 都會帶上它；站上只替還沒分類的影片填，站主在頁面上改過的分類不會被回報蓋掉，所以每個階段都送是安全的。品牌故事由 story 流程自動寫 `"story"`，第一次回報就帶；其他影片沒寫就是「未分類」，等站主在頁面上歸類。
- **句子 id**：用 `ids` 產生，是穩定的短碼。插入新句子時不要重新編號，翻譯、快取和站主的唸錯標記都靠它對齊。
- **章節**：有 `chapter` 的場景會開一個 YouTube 章節，也就是進度條上可以點選的段落。
  - 章節至少 3 個，每個至少 10 秒；lint 先用估計值檢查，`tts` 之後再用實際時間檢查一次。
  - 名稱寫內容，要是觀眾會搜尋的說法，例如「它能回答的三種題型」。第一個（00:00）和最後一個也一樣，不用「開場」「結論」。
  - 畫面左上會顯示「02 / 06 章節名」，頂部有一條分段進度條，都由工具自動畫。
- **版型**：共 16 種，資料欄位與可以逐條出現的數量定義在 `tools/video/templates/templates.mjs` 的 `TEMPLATE_SPECS`。`**文字**` 會變成強調色，`\n` 是手動斷行。放具體例子的四種：
  - `chat`：對話泡泡，例如提問與回答、客戶來信；
  - `quote`：官方原文加翻譯與來源；
  - `stats`：2–4 格大數字；
  - `cta`：影片中段一張卡，指向說明欄第一行的文章。
  - `terminal`（2026-10-01 加入，第 16 種）：模擬終端機，提示字元只能是 `$` 或 `>`，指令逐字打出、`output` 一段一段出現；指令與輸出必須照抄真的執行結果，並附 `ran_on`（執行日期）與 `tool_version`（工具自報的版本），缺一 lint 就擋，家目錄、user@host、email 也擋；範例 `tools/video/templates/terminal/fixtures/claude-code/video.json`。
- **畫面節奏**：純投影片同一個畫面最好不要停超過 15 秒左右。長段說明拆成幾個場景，或一句帶出一個項目；具體例子優先用 `chat`、`quote`、`stats`，不要一張條列從頭講到尾。
- **插圖投影片**（2026-09-29 定案，設計在 `docs/videos/ILLUSTRATED.md`；範例 `tools/video/core/fixtures/illustrated/video.json`）：卡片之間放 `shot` 場景——一張 AI 插圖加運鏡，`data.prompt`（英文 ≤1000 字，依序寫景別、地點與時間、一個人在做的一件事（有簡單的臉或背影，不是無臉人偶）、視線落點的物件與材質、光從哪來；不寫風格與顏色；不畫字、表面是字的東西、logo、真人）、`data.camera`（push in／pull out／pan left／pan right／tilt up／tilt down／drift）、`data.visual: "still"`、可選 `data.transition`（cut／dissolve，通常不寫）。要有 `look`（沒寫時工人依 slug 從五個版畫預設裡輪流挑，每支先畫一張畫風樣張當每張圖的參考圖；`docs/videos/ILLUSTRATED.md` §第二輪），可帶 `music.track`（站主放在 `<VIDEO_WORKDIR>/_music/` 的授權檔）與 `sfx.set`（`_sfx/<set>/` 的授權音效組）。節奏：每 5–8 秒換一張畫面、卡片狀態 ≤8 秒、插圖至少佔一半時間、開場 20 秒內落鉤；一個 shot 帶一到兩句；相鄰的 shot 提示詞不能相似、運鏡不跟上一張一樣（連三張同運鏡是 lint 錯誤）、每章一個自己的地點；主體放在畫面中間三分之一（Shorts 從 16:9 蓋滿 9:16 只留中間約 32% 寬）。節奏的 lint 先當警告，最終 QA 的 `pace` 項在真實時間軸上擋。主幹在「旁白核准」後多 `keyframes`（生圖，judge 自動核准分鏡）、在 `render` 後多 `music`；`assemble` 自動把單狀態卡片做成漂移、畫面間預設硬切（前一句有 ≥600 ms 停頓節拍或撰稿寫 dissolve 才溶接）、章節卡硬切、配樂壓在旁白下、音效放在章節卡、溶接與逐條出現上。
- **螢幕操作場景**（`template: "screencast"`，2026-10-01；程式在 `tools/video/screencast/`，範例 `tools/video/screencast/fixtures/tutorial/video.json`）：`data.steps` 是宣告式步驟，`render` 照著用 Playwright 操作公開網頁並截靜態圖（1280×720 版面、1.5 倍＝1920×1080；User-Agent 是規矩 5 那串；不登入、不用 `recordVideo`），游標滑過去、框選、點擊波紋與放大由版型畫。步驟有六種：`goto`（只收公開的 https 頁，網址不能帶帳密或 token、code、session 類參數）、`wait`（`selector` 或 `ms`）、`click`、`fill`（只打 `video.json` 寫好的字；密碼、驗證碼、信用卡、email、電話欄位一律拒絕，值像 email、電話、卡號、金鑰也拒絕）、`capture`（可帶 `focus` 與 `zoom` 1–2.5；沒有 `focus` 時游標指向它之後的下一個 `click`）、`mask`（`selector` 或 `rect`，之後每張截圖拍之前都先蓋上；selector 對不到任何元素就整個停下，頁面不一定有的加 `optional: true`）。每次 `capture` 是場景的一個狀態：N 張截圖的場景，台詞的 `reveal` 合計剛好 N−1、第一句不 reveal。選擇器只算看得見的元素，`click`、`fill` 要剛好對到一個（網站常藏一份手機版的同名按鈕；要等用戶端才畫出來的元素，先 `wait` 它再 `mask`）。截圖依步驟的雜湊快取在工作區的 `screencast/` 底下，重跑不再開網頁（`render --recapture` 才重拍）。`render --profile <目錄>`（或 `VIDEO_SCREENCAST_PROFILE`）指向站主自己登入過的瀏覽器設定檔，代理永遠不用；站主用的時候，畫面上的帳號、email 一律 `mask`。
- **圖片與圖解**：只能用 `apps/web/public/` 或 `docs/videos/` 底下的檔案，並列在 `assets`，寫清楚來源與授權。
- **說明欄**：`youtube.description` 只寫本文，開頭兩句說這支影片會帶觀眾看什麼。其餘由工具組進去，依序是：
  - 第一行的站內文章連結（依 `source_guide` 自動加 UTM）；
  - 本文；
  - 📌 章節時間戳；
  - 📚 參考資料（`sources`）；
  - 最後一行是前三個標籤變成的 #標籤。

## 發音與試聽

- 中文 TTS 最常唸錯英文縮寫和破音字。發音字典是 `docs/videos/` 底下的 `lexicon.json`，所有影片共用，第一支影片建立它。每個英文詞都要在字典裡，lint 才會過。
- 格式是 `{ "schema_version": 1, "terms": { … } }`。`terms` 的值有兩種：唸法（例如 `"LLM": "L L M"`，送出時變成 `<sub alias>`），或 `null`（表示照原字唸就對，要等試聽確認過）。
- zh-TW 的 `<phoneme>` 音標沒有官方文件，不要用。
- **Gemini 沒有 SSML**：字典的唸法直接換進文字裡送出（不是 `<sub alias>`），停頓換成 Gemini 的 `<long pause>`／`<short pause>` 標籤，但長度不像 Azure 的 break 那樣精準。語氣靠 `voice.style`，Gemini 聲音不能寫 `rate`。伺服器回 24 kHz，本機工具用視窗化 sinc 內插升到 48 kHz。
- **試聽只能經伺服器**：`audition --voices gemini:<聲音>`。站主的 Gemini 金鑰限了伺服器 IP，在 AI Studio 會 403；Cloud 的 Gemini-TTS 只收服務帳號。
- 內建瀏覽器放不了 repo 外 `file://` 路徑的音檔：試聽檔用 SendUserFile 直接給站主。試聽檔不要放在 scratchpad（代理會清掉）。
- **收斂旁白**：`check-audio` 先在本機比對，只差同音字（拼音連聲調相同）或語氣詞的句子不送 Jev；Jev 仍然懷疑的句子，可以再交給不看稿的第二個轉寫（`--second-opinion` 或 `VIDEO_SECOND_OPINION`，參考 `tools/video/tts/whisper_second_opinion.py`），它聽對的就排除並寫進旁白審核卡，兩個轉寫都聽錯同一處的才是聲音唸錯（`docs/videos/DUBS.md`）。第二個轉寫整批共用一個時限，預設 10 分鐘加每句 2 分鐘，`VIDEO_SECOND_OPINION_TIMEOUT_MS`（毫秒）可以整個改掉；逾時會印出「timed out after … on N clips」。慢的機器（例如 Windows ARM64 跑 Whisper `medium` 約一分鐘一句）用 `WHISPER_MODEL=small`，而且一次只跑一個 `check-audio`，兩個同時跑會互搶 CPU 而一起逾時；Jev 的每日次數在「AI 供應商與金鑰」卡片，和自動新聞、景點介紹共用。被標的句子 `tts --redo` 只重錄那幾句（快取按句）。一直被聽錯的句子就改措辭，例如句尾「答」→「回答」、「旗艦」→「旗艦模型」、「分三步走」→「分三個步驟」；工人在重錄到上限後自己做這一步（`prompts/listener-rewrite.md`，`tools/video/automation/rewrite.mjs` 比對改寫前後的數字、拉丁字詞與字典詞，變了就退回），本機也可以照同一份提示請代理改。`check-audio` 遇到轉寫失敗的句子會跳過，連續 3 句失敗才停；工具這邊的修改不用部署就生效。

## 成本

- Azure 每個中文字算兩個計費字元，SSML 標記也計費。一支 10 分鐘的影片約 8,000–9,000 計費字元，免費額度每月 50 萬，大約可以做 50 支。
- `tts --dry-run` 會印出這支影片的估計字數，以及伺服器回報的本月用量。
- 每月上限由站主在後台卡片設定。超過時伺服器以 429 拒絕，請求不會送到 Azure，所以不會產生費用。
- Gemini 以送出的文字字數計，和 Azure 分開算，預設每月 300,000 字（約一百支 10 分鐘影片）。
- 實測合成語速約每分鐘 300 字（48 kHz 單聲道），工具估計用 250，所以 `lint` 估的長度偏長。2026-10-04 一支說書口吻的插圖投影片量到相反的結果：`lint` 估 12.2 分鐘，合成旁白實際 13.07 分鐘（約長 7%）；每個狀態的估計秒數也偏短，估計時過關的狀態到真實時間軸上超過 8 秒，要到 QA 的 `pace` 項才量得到。所以估計偏長或偏短要看口吻，長度與每個狀態的秒數都以 `tts` 之後的實際時間軸為準，接近 8 秒的狀態撰稿時就先拆。長度規則只有 8 分鐘以上（站主 2026-10-04 定）：`target_minutes` 的上緣是撰稿瞄準的長度，不是上限，估計超過上緣 `lint` 不再警告；不為了壓進目標刪事實，也不灌水。每集至少 8 分鐘（普通漫劇除外）：`lint` 估計不足 8 分鐘、`target_minutes` 下限低於 8 都是錯誤；成片品管的 `assemble` 項量到成片不足 8 分鐘就不過，要加寫旁白後重跑 `tts` 與 `assemble`。知識科普／AI名詞用10分鐘製作目標，品牌故事保留13分鐘；五類長片另外核對當前正文及成片各480秒、speech hash與影格綁定，片頭片尾不計正文。普通工人／CLI會忽略 `VIDEO_MIN_EPISODE_MINUTES=0`；只有 Node test runner 及 repository 的 `assemble/smoke.mjs` 短範例入口可放寬估算／通用成片門檻，五類長片的實測正文門檻始終不受該變數影響。
- 配音音軌（`dub`）以送出的翻譯字數計：一支 10 分鐘的影片，en 約 10,000、ja 約 6,000、ko 約 6,500、zh-CN 約 5,000 個 Gemini 字元，四條約 28,000（含場景切分的標記）。額度不夠時把 `video_speech_gemini_monthly_character_limit` 調高。翻譯與審稿的模型呼叫只花在站主勾了的語言上（每語一次翻譯加一次審稿）。

## 坑

- **中文參數一律寫進檔案**：PowerShell 5.1 會弄壞命令列上的非 ASCII 參數，所以 `audition` 只收 `--text-file`；`approve --note` 也盡量寫英文或短句。
- **`render` 回報版面錯誤**：代表縮小 40% 以後字還是放不下，或畫面裡有字型沒有的字（例如 emoji）。處理方式是縮短文字或換版型，不要改主題 CSS。
- **`assemble` 回報某一格「不像」預期的畫面**：代表畫面錯位了，先看 `checks.json` 是哪個場景的哪一格。門檻：44 dB 以上直接算對、35 以下算錯；中間（字很密的表格、比較卡，正確也只有 40 左右）要比同場景其他畫面高 3 dB，`checks.json` 會記下它和每個對手的分數。不要調低門檻。
- **`tts` 回報某一批改成逐句合成**：代表那一批的靜音切段和字數對不上。這通常不影響成品，只是多送幾次請求。如果同一批一直發生，把那個場景拆短一點。
- **`dub` 回報視窗塞不下（結束碼 1）**：那個投影片狀態裡的翻譯，就算整窗加速 1.15 倍也講不完。`dubs/<語系>/fit.json` 的 `over` 列出每句最多幾個字元：只縮那幾句（數字、專有名詞、說法不能改；字幕跟著用縮短後的句子），寫進 `i18n-sheet --parts captions` 的底稿、`i18n-merge` 之後再跑 `dub`，只重錄改過的句子（做法在 `prompts/caption-translate.md` 最後一節）。`i18n-sheet` 在有時間軸、且該語系勾了配音時會先給每句 `max_chars`，翻譯時照它寫就少一輪。英文最容易超，第二批實測一支有 7 個視窗要縮。工人縮短兩輪、重錄兩輪仍不行就寫 `dubs/<語系>/skipped.json`，語言卡片列出原因，影片照樣上架；要重試就刪掉那個檔再勾一次。
- **成片核准了，語言面板還沒出現**：面板靠影片清單的 checklist 有「成片核准」；工人核准那一輪會回報一次，最多等一輪（5 分鐘）。本機手動跑的影片用 `review-push --report-only` 登記。
- **手動跑語言時**：先把站主的選擇寫成 `<VIDEO_WORKDIR>/<SLUG>/languages.json`（`{"locales": {"en": {"metadata": true, "captions": true, "dub": false}}, "decided_at": "<ISO 時間>"}`），`captions`、`package`、`qa`、`review-push --gate languages` 才會只做那些；沒有這個檔就照舊做每個有翻譯的語系。
- **代理不能碰權杖**：用上面的配對流程，權杖不能出現在對話裡、檔案裡或指令參數裡。替站主開一個終端機分頁讓他打權杖，會被分類器擋成 Credential Leakage。
- **ffmpeg（除錯 `assemble` 時用得到）**：PNG 的 concat 預設時基是 1/25 秒，每個檔案要加 `option framerate 30`；PNG 沒有色彩資訊，要 `setparams` 加 `-x264-params colorprim/transfer/colormatrix`；單聲道先正規化再轉立體聲會大 3 LU；抽格用場景片段上的 `select=eq(n,N)`，不要對串好的 mp4 用 `-ss`；Noto Sans CJK 單行會「溢出」零點幾個行高，所以版面檢查容許到 0.4 em。
- **本機環境**：
  - `winget install BtbN.FFmpeg.GPL`（原生 ARM64）之後，舊的 shell 的 PATH 沒有它：用完整路徑或 `FFMPEG_PATH`。
  - Playwright 要的 `chromium_headless_shell` 在 Windows ARM64 是 x64 模擬，很慢：用 `--channel msedge`（17 個投影片狀態約 75–90 秒）。
  - 沒有 `node_modules` 的 worktree 會解析到主 checkout 的（沒有字型套件）：在 worktree 裡跑 `npm ci --ignore-scripts`。
  - `uv sync` 失敗留下的壞 venv（`apps/api` 底下的 `.venv`，沒有 fastapi、os error 183）：刪掉重來。
  - npm 11.6.2 的 `--package-lock-only` 會拿掉 `libc` 欄位：lockfile 的條目要手補。
- **在過期的分支上跑新工具（toolrun）**：`git archive -o x.tar origin/main tools/video .agents/skills/youtube-video`，再**另一個指令** `tar -xf`（串在一起會被 worktree 守門擋）。在解開的目錄建一個指向 worktree `node_modules` 的 junction（它會消失，消失後 pinyin-pro 會失敗），並複製一份 docs；`--file`／`--slug` 相對於 toolrun 目錄。
- **worktree 隔離的 session**：含 `$(…)`、shell 迴圈、`MSYS_NO_PATHCONV=1 "/c/Program Files/…"`、jq 字串，甚至 `node -e` 裡出現「不進 git」字樣的指令，都可能被當成 git 操作擋下。改用 PowerShell、ccd_pr 工具、Edit，或 scratchpad 裡的 .mjs 腳本。`EnterWorktree` 也會把還在跑的背景代理鎖在外面（它們對舊 worktree 的寫檔、curl、node 都被拒）：等代理做完再切，或讓代理寫到 repo 外。
- **改工具或後台時的測試坑**：
  - `apps/api/tests/test_error_localization.py`：admin／deployments 以外的每個 `AppError(…, "code")` 都要四語系訊息，否則 CI 的 api 會紅（只跑單一檔案時看不到）。影片工具的錯誤在 `apps/api/app/video_speech/admin_api.py` 丟；其他模組丟自己的例外（例如 `checking.CheckUnavailable`）。
  - 新的後台頁要加進 `apps/web/e2e/admin-operations-full-stack.spec.ts` 寫死的導覽清單。
  - 改這個 skill：`tools/skills.test.mjs` 檢查路徑前會拿掉 `<X>/` 這種大寫佔位符，所以寫 `<VIDEO_DOCS>/brief.md`；還不存在的檔案要寫成「`docs/videos/` 底下的 `lexicon.json`」。

## 主機自動產線

設計在 `docs/videos/AUTOMATION.md`；這裡是維運。容器是 `docker-compose.prod.yml` 的 `video-worker`（compose profile `video`，部署腳本已帶 `--profile video`）。

- 看紀錄：`docker compose -f docker-compose.prod.yml logs --timestamps video-worker`；`top video-worker` 看它是不是在 `sleep 300`。
- 一輪同時推兩支影片（compose 的 `VIDEO_WORKER_LANES: "2"`，上限 3，設 1 回到一次一支）：第一條線照舊處理放棄、重試、貼網址、討論、作品與新稿，第二條只推已經在做的影片；兩條線不會拿同一支，紀錄裡第二條線的行前面有 `[lane 2]`。
- 緊急停止：`docker compose -f docker-compose.prod.yml exec -T video-worker touch /var/lib/mokaair/video-work/STOP`，做完手上那一段就停；要恢復時刪掉這個檔。Shorts 的敲門（`ops/video/worker.sh` 在 `auto` 旁邊另開的背景迴圈，每 `VIDEO_SHORTS_KNOCK_SECONDS`（預設 300）秒跑一次 `shorts/cli.mjs tick`）也看這個檔，有 STOP 就不敲門，網站也就不鎖定時段、不再開始送 Shorts，紀錄印一行 `video-worker: shorts: STOP found`。工人的 Shorts 單位在兩個單位之間也看這個檔。
- **Shorts 在一輪裡的位置**（`tools/video/automation/cli.mjs`、`tools/video/automation/shorts.mjs`）：每輪 `auto` 先讀 Shorts 設定；片庫少於 `stock_days` 天的量時，Shorts 的一個單位排在漫劇與教學之前，否則排在它們之後；教學的自動草稿關著也照做，只看 Shorts 設定的「讓主機工人自己做 Shorts」。一個單位是：先替成片已被站主核准的 Shorts 補送上傳包，再問 `GET /video/automation/shorts/next`，做 `report`（上週的每週報告）、`plan`（排到下週日的時段）、`brief`（補題）或 `make`（做一支實測）其中一件。實測的步驟、自動修與卡住的規則在 `.agents/skills/youtube-video/references/shorts.md` §工人怎麼做；產物在工作區的 `_shorts/`。紀錄裡這些行以 `shorts:` 或那支 Shorts 的代號開頭；Shorts 出錯只印一行，不會中斷這一輪。工人目前只做實測線，精華與漫劇直式短篇的題目先跳過。
- `video_docs` volume 只在第一次建立時從映像填入，之後映像裡的 `docs/videos` 更新不會進去。
- 工人只看得到自己的 volume，可能重做本機已經做過的題目：本機或分支上的影片用 `review-push --report-only` 登記到審核頁。
- 換新模型前先更新主機的 Claude CLI（`claude update`；2.1.259 對 Opus 5.5 回 400，要 2.1.280 以上）。
- 第一次配對碰上部署重啟的 502：重啟工人即可；驗證碼 10 分鐘過期，工人會自己重新要。
- 診斷時用 stdin 跑 `flow.mjs` 的 `step()` 會真的做一個單位的工作，不是唯讀。
