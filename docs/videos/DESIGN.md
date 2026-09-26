# 全自動 YouTube 教學影片產線：設計

2026-09-24 定案。操作步驟在 skill `youtube-video`（`.agents/skills/youtube-video/SKILL.md`），這份只寫**為什麼這樣做**與各部分怎麼接起來。工作分成 11 張票，id 都是 `2026-09-24-video-*`。第二種格式 AI 漫劇（`format: "drama"`，2026-09-26 定案）沿用這裡的產線、時間軸、關卡與主機工人，只加自己的部分，寫在 [`DRAMA.md`](DRAMA.md)。

## 目標與已定的選擇

站主要一條「AI 撰稿 → 查核 → 合成語音 → 自動做畫面 → 合成影片 → 五語系 CC → 上架」的產線，做 AI／科技資訊與 AI 工具教學影片。

| 項目 | 決定 |
| --- | --- |
| 形式 | 第一版：深色投影片＋旁白（參考 Gary Chen〈一部影片看完 Stanford AI 系統課程〉）。第三期：螢幕操作手把手 |
| 聲音 | 雲端 TTS、台灣口音、固定一個頻道聲音（Azure AI Speech，試聽後決定） |
| 字幕 | **不燒錄**；上傳五條 CC：zh-TW、en、ja、ko、zh-CN（同 `apps/api/app/i18n.py`） |
| 中繼資料 | 標題、說明、標籤五語系；說明欄有章節、參考資料、站內文章連結 |
| 頻道 | Mokaair 品牌：片頭片尾、縮圖用 Mokaair 字樣 |
| 長度 | 單支 8–12 分鐘 |
| 試作 | 〈AI 模型怎麼挑〉，由 `ai-workflow-cost-quality-latency` 改寫 |

`youtube-video` skill 原本是人工錄製路線（代理交稿子、分鏡、字卡、上架文字，站主錄音剪輯）。全自動路線加進同一個 skill，兩條路線共用選題、格式、口播稿寫法與上架檢查。

## 產線與關卡

| # | 階段 | 誰 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 0 | 認領票，開持久工作區 `<VIDEO_WORKDIR>/<slug>/`（repo 外） | 協調者 | `state.json` | 工作區不在 repo 內 |
| 1 | 企劃：觀眾、看完能做到什麼、**站主觀點**、至少一段實際示範或實算、章節大綱 | 企劃代理 | `docs/videos/<slug>/brief.md` | 站主選大綱 → `approve --gate outline` |
| 2 | 撰稿 | 撰稿代理 | `video.json`、`claims.md` | `lint` 零錯誤 |
| 3 | 查核（換人；改超過 3 個事實就第二輪再換人） | 查核代理 | `verify-1.md` | 完成 |
| 4 | 聽眾優先審稿 | 審稿代理 | 修正清單 | 協調者套用 |
| 5 | 語音 | `tts` | `audio/`、`narration.wav`、`timeline.json` | 每段長度與估計相符 |
| 6 | 試聽，標出唸錯的句子，補發音字典，只重做那幾句 | 站主 | `review/audio.html` | `approve --gate audio` |
| 7 | 畫面 | `render` | `frames/`、`contact-sheet.png` | 超框、缺字檢查 |
| 8 | 合成 | `assemble` | `final.mp4` | 影音自動檢查 |
| 9 | CC 與中繼資料翻譯 | 翻譯與逐語審稿代理、`captions` | `i18n/<locale>.json`、`captions/*.srt` | 過期翻譯、行長、每秒字數 |
| 10 | 打包 | `package` | `upload/`、`UPLOAD.md` | 站主看完全片 → `approve --gate final` |
| 11 | 站主在 Studio 上傳成私人 → `youtube-sync` 補五語系中繼資料與 CC → 站主自己按公開 | 站主＋工具 | YouTube 影片 | 公開一律站主按 |

核准綁雜湊：大綱綁 `brief.md`、試聽綁 `timeline.json`、成片綁 `final.mp4`；漫劇另有角色設定圖綁 `characters/manifest.json`、分鏡綁 `keyframes/manifest.json`。檔案變了，舊的核准就不算，後面的指令會拒絕執行（結束碼 3）。

## 資料

文字進 repo、可以用 PR 審：`docs/videos/<slug>/`（`brief.md`、`video.json`、`claims.md`、`verify-*.md`、`i18n/<locale>.json`）與共用發音字典 `docs/videos/lexicon.json`。二進位產物（音檔、畫面、mp4）只放 `<VIDEO_WORKDIR>`，不進 repo（repo 是公開的）。

`video.json` 是單一真相，格式由 `tools/video/core/schema.mjs` 定義，範例在 `tools/video/core/fixtures/minimal/video.json`。重點：

- 句子 id 是 4–8 個小寫英數的穩定短碼（`node tools/video/cli.mjs ids --count 20` 產生），插句不重新編號，翻譯與快取都靠它對齊。
- `text` 是字幕與 CC 顯示的字；`say` 只在唸法必須不同時才寫，並記 `say_for`（`text` 的雜湊）。`text` 改了而 `say` 沒跟著改，lint 會擋。
- `reveal` 表示這句開始時畫面多亮出一個元素。
- 有 `chapter` 的場景開始一個 YouTube 章節；章節時間由時間軸算，不手寫。
- 翻譯一語系一檔，每句帶 `source_hash`；zh-TW 改了哪句，只重翻那句。各語系在該句的時間窗內自己分段，不要求段數相同（英文語序做不到自然的一對一）。

發音字典 `docs/videos/lexicon.json`：`{ "schema_version": 1, "terms": { "LLM": "L L M", "Claude": null } }`。值是唸法（組 SSML 時換成 `<sub alias>`），`null` 表示「照寫法唸，已經聽過沒問題」。旁白裡每個拉丁字詞都要在字典裡，lint 才會過：中文 TTS 最常唸錯的就是英文縮寫。

## 工作區檔案約定

每個階段把產物寫在 `<VIDEO_WORKDIR>/<slug>/`，並記下「用哪一版輸入做的」。`status` 靠比對這些雜湊判斷每一步做完了沒：腳本改過之後，舊的時間軸就不算數。約定的正本是 `tools/video/core/state.mjs` 的 `ARTIFACTS`。

| 檔案 | 誰寫 | 必帶欄位 |
| --- | --- | --- |
| `timeline.json` | `tts` | `buildTimeline()` 的內容＋`speech_hash`（`speechHash(doc, lexicon)`） |
| `narration.wav`、`audio/<line id>.wav` | `tts` | 48 kHz 16-bit mono；每句補靜音到整格 |
| `frames/manifest.json`、`contact-sheet.png` | `render` | `visual_hash`（`visualHash(doc)`） |
| `final.mp4`、`checks.json` | `assemble` | `checks.json` 帶 `ok`、`speech_hash`、`visual_hash`、`problems` |
| `captions/<locale>.srt`／`.vtt`、`captions/manifest.json` | `captions` | `speech_hash`、各語系段數與問題、沒寫出的語系與原因 |
| `upload/metadata.json` | `package` | `final_sha256`（必須等於成片核准的雜湊） |
| `approvals.json` | `approve` | 每筆：關卡、檔名、SHA-256、時間、備註 |
| `state.json` | 每個階段 | 執行紀錄，給交接用；判斷進度不看它 |

指令：`node tools/video/cli.mjs <status|lint|ids|approve|captions|tts|audition|review|render|assemble|package|youtube-sync>`，`--help` 有完整說明。

結束碼：0 成功；1 lint 或檢查沒過；2 用法錯誤；3 需要站主；4 外部服務或額度問題；5 工具還沒做或沒裝。在工作區（或它的上一層）放一個 `STOP` 檔，長時間執行的階段做完手上那一段就會停。

## 技術做法

**影音同步靠構造保證，不靠抽查。**48,000 Hz ÷ 30 fps = 每格 1,600 個取樣。每句音檔加上句後停頓，一起補靜音到整格，所以每一句都從某一格的開頭開始，整條旁白與畫面沒有任何捨入誤差可以累積。字幕（毫秒精度）在句子的語音範圍內依「唸出來的長度」分段。

**語音**：Azure 即時 REST，輸出 `riff-48khz-16bit-mono-pcm`，但**不是本機直接呼叫**。

- 2026-09-24 站主決定：Azure 金鑰存在正式站後台的「Azure 語音（影片旁白）」卡，永遠不離開伺服器。
- 本機工具帶著「影片工具權杖」呼叫 `POST https://mokaair.com/api/video/speech`。
- 權杖靠**配對**取得，沒有人需要複製它（2026-09-24 站主決定）。流程仿 RFC 8628：
  1. `login` 開一個配對，印出驗證碼與後台卡片的連結。
  2. 站主在卡片上核對驗證碼、按「允許」。
  3. 工具用只有它知道的 device code 輪詢，只領一次權杖，直接寫進本機檔案，不印在畫面上，所以代理可以替站主跑。
  - 配對紀錄只放 Redis 10 分鐘。權杖在工具來領的那一刻才產生，所以明文權杖從來不落地。
  - 卡片上的「建立權杖」按鈕仍保留，給不能配對的場合（`login --paste`）。
- 送出的是結構化的句子：`{voice, rate, segments:[{parts:[{text, alias?}], break_after_ms}]}`。伺服器組 SSML、算計費字元、向每月預算預留字元，再呼叫 Azure，最後回傳 WAV。
- `GET /api/video/speech/status` 回傳允許的聲音、上限與本月用量。
- 程式在 `apps/api/app/video_speech/` 與 `apps/web/app/api/video/`（`speech/`、`pairings/`）。

**第二個聲音供應商：Gemini**（2026-09-24 加入）。站主試聽 Azure 七個聲音後，覺得最好的 Ava 仍然「語調太平、像在念稿」，所以加上 Gemini 的模型式語音來比較：
- 用網站已存的 Gemini 金鑰（`hotspot_guide_gemini_*`，AI 行程規劃與文章搜尋也用這把），站主不用新開帳號。這把金鑰限了伺服器的 IP，所以在 AI Studio 裡試不了，只能經伺服器。
- `video.json` 寫 `"voice": {"provider": "gemini", "name": "Sulafat", "style": "…"}`；送到伺服器的聲音名稱是 `gemini:Sulafat`。
  - `style` 是一句文字，描述要怎麼唸（例如「輕鬆、像跟朋友解釋」）。
  - 沒有 `rate`，語速寫在 `style` 裡。
  - `model` 可選 `gemini-3.8-flash-tts`（預設）或 `gemini-3.8-flash-lite-tts`。
- 沒有 SSML：術語的唸法直接換進文字裡；句間停頓寫成 Gemini 的 `<long pause>`／`<short pause>` 標籤；文字裡的角括號一律拿掉，避免被當成標籤。
- Gemini 回傳 24 kHz，本機工具用視窗化 sinc 內插升到 48 kHz，時間軸與後面的步驟都不用改。
- 每月用量以送出的文字字數計，和 Azure 分開算，預設上限 30 萬字（`VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT`）。後台卡片還沒有這一欄。
- 2026-09-24 在 AI Studio 的聲音庫篩選「Chinese」，找不到任何聲音；口音選單也沒有台灣。台灣腔只能靠 `style`，或之後用「聲音設計」造一個。

每個場景送一次請求，句間固定停頓，再在 Node 裡找靜音切段。逐句分開合成會讓每句語調重新起頭，聽起來像在念清單；切段對不上時，該場景退回逐句合成。一次最多 1,500 字，更長的場景由工具拆開。發音一律用 `<sub alias>`（也就是 part 的 `alias`）；zh-TW 的 `<phoneme>` 音標集沒有官方文件，不用。

**畫面**：HTML 版型，由 Playwright 截 1920×1080 PNG。repo 已有這個做法（`tools/claude-code-series/render-art.mjs`）。一個投影片狀態一張，逐條出現的轉場用 Web Animations 固定時間點截短影格。字型用根目錄 devDependencies 的 `@fontsource-variable/noto-sans-tc`、`@fontsource-variable/jetbrains-mono`（OFL），由 `page.route` 從本機提供，所有網路請求都擋掉。不用 Remotion：它不支援 Windows ARM64（arm64 Node 會直接拒絕），公司規模大了還要授權費。

**合成**：ffmpeg（Windows ARM64 用 `winget install BtbN.FFmpeg.GPL`，含 libx264；路徑由 `FFMPEG_PATH` 指定）。

- 每場景編一段，設定完全相同，再用 `-c copy` 串接；改一個場景只重編那一段。
- H.264 High、`-bf 2`、closed GOP、`yuv420p`、BT.709 轉換與標記（沒有的話 Chromium 截圖的顏色會偏）、`+faststart`。
- 音訊用 `loudnorm` 兩段式到 −14 LUFS／−1 dBTP，輸出 AAC-LC 立體聲 48 kHz 384 kbps。
- 自動檢查四項：總格數、音軌與影片差 ≤ 1 格、每章開頭抽格比對來源 PNG、響度。

**上架**：mp4 由站主在 Studio 上傳。`tools/video/youtube/` 只做 `videos.update`（先讀現值再合併整段送）、`captions.insert`×5、`thumbnails.set`。OAuth 用桌面應用程式、scope 只有 `youtube.force-ssl`，token 放工作區的 `.secrets/`。

## YouTube 與 Azure 的規則（2026-09-24 查官方文件）

| 規則 | 內容 | 來源 |
| --- | --- | --- |
| API 上傳鎖私人 | 未通過稽核的 API 專案用 `videos.insert` 上傳的影片會被鎖成私人，不能申訴，只能重新上傳 → mp4 一律 Studio 手動上傳 | developers.google.com/youtube/v3/docs/videos/insert、support.google.com/youtube/answer/7300965 |
| 配額 | `captions.insert` 400、`videos.update` 50、`thumbnails.set` 約 50；每日預設 10,000 → 一支約 2,100 | developers.google.com/youtube/v3/determine_quota_cost |
| `videos.update` | 送 `localizations` 必須帶 `snippet.defaultLanguage`；沒送的欄位會被清掉 | developers.google.com/youtube/v3/docs/videos/update |
| OAuth 測試中 | refresh token 7 天過期 | developers.google.com/identity/protocols/oauth2 |
| CC 格式 | SRT、WebVTT 都收；中文語言碼官方沒寫，第二期實測 | support.google.com/youtube/answer/2734698 |
| 中繼資料 | 標題 ≤100 字元、說明 ≤5,000 **位元組**（中文一字 3 位元組），兩者不可含 `<` `>`；標籤合計 ≤500 字元 | developers.google.com/youtube/v3/docs/videos |
| 章節 | 第一個 00:00、至少 3 個、遞增、每段 ≥10 秒 | support.google.com/youtube/answer/9884579 |
| 縮圖 | JPG／PNG，手機上傳上限 2 MB，帳號需驗證 | support.google.com/youtube/answer/72431 |
| 編碼 | MP4＋faststart、H.264 High、2 個連續 B 幀、closed GOP、4:2:0、BT.709；AAC-LC 立體聲 48 kHz 384 kbps。−14 LUFS 是業界常用值，官方沒公布 | support.google.com/youtube/answer/1722171 |
| 營利 | 「非原創內容」（2025-07 由「重複內容」改名）：缺乏教育價值的投影片、套模板、沒有創作者觀點的量產 AI 內容不能營利；另禁止 AI 角色給健康、法律、財務、政治建議 | support.google.com/youtube/answer/1311392 |
| AI 揭露 | 只有擬真到會被誤認為真人、真實事件、真實場景時要揭露；AI 寫稿、資訊圖不用。通用 TTS 旁白官方沒點名，依規則推論不需要 | support.google.com/youtube/answer/14328491 |
| Azure 語音 | zh-TW：HsiaoChen（女）、YunJhe（男）、HsiaoYu（女），沒有 HD 版；多語 Ava／Andrew／Brian／Emma 可用 `<lang xml:lang="zh-TW">`。每百萬計費字元 15 美元，免費層每月 50 萬。**每個中文字算 2 個計費字元**，SSML 標記（`<speak>`、`<voice>` 以外）也計費：一支 10 分鐘約 3,000 字，連標記約 8,000–9,000 計費字元，免費額度每月約 50 支。即時 REST 單次上限 10 分鐘、只回音檔 | learn.microsoft.com（speech-service 的 text-to-speech §Billable characters、language-support、rest-text-to-speech） |

## 營利政策的對策（寫成關卡，不只是建議）

這條產線的形式正是政策點名的類型，所以：

- `brief.md` 必須有「站主觀點」與「觀眾看完能做到的事」兩節，而且不能空白。lint 會擋，站主選大綱時一併確認。
- 每支至少一段實際示範或實算，不只是念重點。
- 場景版型的順序和其他支太像時，lint 會警告。
- 一週 1–2 支，站主看完才上架。
- 題材不給財務建議：幣圈題材只做資訊與工具教學，不談投資。

## 本機與 CI

- 開發機是 Windows 11 ARM64：無 NVIDIA GPU，所以不跑本機 Whisper 或 TTS。Chromium 以 x64 模擬執行，截圖速度在試作時量。
- 中文參數一律走檔案（`--text-file`）：PowerShell 5.1 會弄壞非 ASCII 的命令列參數。
- `npm run test:tools` 會跑 `tools/video/**/*.test.mjs`，這些測試全是純函式，不需要 Chromium 或 ffmpeg。實際的 render＋assemble 煙霧測試放在另一個路徑過濾的 workflow（T4）。

## 分期與票

| 票 | 內容 | scope |
| --- | --- | --- |
| `video-tooling-core` | 格式、lint、時間軸、字幕、狀態、核准、CLI | `tools/video/cli.mjs`、`tools/video/core`、`package.json`、這份文件 |
| `video-speech-server` | 後台 Azure 語音卡、伺服器代為合成、影片工具權杖 | `apps/api/app/video_speech`、`apps/web/app/api/video`、後台設定面板 |
| `video-tts-azure` | 本機 TTS 用戶端（經伺服器）、選聲、靜音切段 | `tools/video/tts` |
| `video-render-slides` | 版型與截圖 | `tools/video/templates`、`tools/video/render` |
| `video-assemble-package` | ffmpeg、審看頁、上傳包、CI 煙霧測試 | `tools/video/assemble`、`review`、`package` |
| `video-skill-automated` | skill 加全自動路線、頻道規格 | `.agents/skills/youtube-video`、`docs/videos/README.md` |
| `video-pilot-ai-model-choice` | 試作影片 | `docs/videos/ai-model-choice`、`docs/videos/lexicon.json` |
| `video-tool-pairing` | 在後台按「允許」配對本機工具，不必複製權杖 | `apps/api/app/video_speech`、`apps/web/app/api/video/pairings`、權杖卡片、`tools/video/tts` |
| `video-captions-i18n` | 五語系 CC | `tools/video/i18n` |
| `video-youtube-sync` | API 同步 | `tools/video/youtube` |
| `video-screencast-steps`、`video-terminal-template`、`video-obs-import` | 第三期：螢幕操作、模擬終端機、OBS 匯入 | 各自的 `tools/video/<area>` |

## 站主要先準備的東西

1. Azure Speech 資源（免費層 F0）。金鑰與區域填在後台「API 與供應商設定 → AI 服務 → Azure 語音」，按連線測試。之後本機工具的 `login`（誰跑都可以）會印出一個連結與驗證碼，站主在卡片上核對後按「允許」一次即可。
2. 安裝 ffmpeg：`winget install BtbN.FFmpeg.GPL`。
3. 試聽後選定頻道聲音。
4. YouTube 頻道完成手機驗證（自訂縮圖需要）。
5. 第二期：Google Cloud 專案啟用 YouTube Data API v3，建立「桌面應用程式」OAuth 用戶端。
