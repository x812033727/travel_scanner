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
| 長度 | 單支至少 8 分鐘（漫劇以外每集都是，站主 2026-10-01 定）；預設目標 8–12 分鐘，上緣是撰稿瞄準的長度、不是上限，超過沒關係（站主 2026-10-04 定） |
| 試作 | 〈AI 模型怎麼挑〉，由 `ai-workflow-cost-quality-latency` 改寫 |

五類知識與非虛構長片使用[新版有效企劃](long-form/README.md)：科普／AI名詞目標10分鐘，品牌13分鐘；QA要求當前旁白正文及成片各480秒，片頭尾不計正文，不能以估計秒數替代。

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

核准綁雜湊：大綱綁 `brief.md`、試聽綁 `timeline.json`、成片綁 `final.mp4`；漫劇另有角色設定圖綁 `characters/manifest.json`、分鏡綁 `keyframes/manifest.json`；長篇作品的每一集（`video.json` 有 `series`，見 `SERIES.md`）另有劇本關卡綁 `script.md`（`node tools/video/cli.mjs script` 由 `video.json` 寫出，只含場景、台詞、說話者與情緒，不含鏡頭提示詞，所以媒體階段自動修提示詞不會讓核准失效）。檔案變了，舊的核准就不算，後面的指令會拒絕執行（結束碼 3）。

## 資料

文字進 repo、可以用 PR 審：`docs/videos/<slug>/`（`brief.md`、`video.json`、`claims.md`、`verify-*.md`、`i18n/<locale>.json`）與共用發音字典 `docs/videos/lexicon.json`。二進位產物（音檔、畫面、mp4）只放 `<VIDEO_WORKDIR>`，不進 repo（repo 是公開的）。

`video.json` 是單一真相，格式由 `tools/video/core/schema.mjs` 定義，範例在 `tools/video/core/fixtures/minimal/video.json`。重點：

- 句子 id 是 4–8 個小寫英數的穩定短碼（`node tools/video/cli.mjs ids --count 20` 產生），插句不重新編號，翻譯與快取都靠它對齊。
- `text` 是字幕與 CC 顯示的字；`say` 只在唸法必須不同時才寫，並記 `say_for`（`text` 的雜湊）。`text` 改了而 `say` 沒跟著改，lint 會擋。
- `reveal` 表示這句開始時畫面多亮出一個元素。
- 有 `chapter` 的場景開始一個 YouTube 章節；章節時間由時間軸算，不手寫。
- 翻譯一語系一檔，每句帶 `source_hash`；zh-TW 改了哪句，只重翻那句。標題、說明、標籤與各章節（以場景 id 為鍵）的雜湊放在 `source_hashes`，改名的章節、改過的說明、換了順序的標籤也一樣會被標成要重翻。各語系在該句的時間窗內自己分段，不要求段數相同（英文語序做不到自然的一對一）。

發音字典 `docs/videos/lexicon.json`：`{ "schema_version": 1, "terms": { "LLM": "L L M", "Claude": null } }`。值是唸法（組 SSML 時換成 `<sub alias>`），`null` 表示「照寫法唸，已經聽過沒問題」。旁白裡每個拉丁字詞都要在字典裡，lint 才會過：中文 TTS 最常唸錯的就是英文縮寫。

## 工作區檔案約定

每個階段把產物寫在 `<VIDEO_WORKDIR>/<slug>/`，並記下「用哪一版輸入做的」。`status` 靠比對這些雜湊判斷每一步做完了沒：腳本改過之後，舊的時間軸就不算數。約定的正本是 `tools/video/core/state.mjs` 的 `ARTIFACTS`。

| 檔案 | 誰寫 | 必帶欄位 |
| --- | --- | --- |
| `timeline.json` | `tts` | `buildTimeline()` 的內容＋`speech_hash`（`speechHash(doc, lexicon)`：聲音、每句說出的字與停頓，加上這些句子用到的字典條目；別支影片加的詞不算） |
| `narration.wav`、`audio/<line id>.wav` | `tts` | 48 kHz 16-bit mono；每句補靜音到整格 |
| `frames/manifest.json`、`contact-sheet.png` | `render` | `visual_hash`（`visualHash(doc)`） |
| `final.mp4`、`checks.json` | `assemble` | `checks.json` 帶 `ok`、`speech_hash`、`visual_hash`、`problems` |
| `captions/<locale>.srt`／`.vtt`、`captions/manifest.json` | `captions` | `speech_hash`、各語系段數與問題、沒寫出的語系與原因 |
| `upload/metadata.json` | `package` | `final_sha256`（必須等於成片核准的雜湊） |
| `approvals.json` | `approve` | 每筆：關卡、檔名、SHA-256、時間、備註 |
| `state.json` | 每個階段 | 執行紀錄，給交接用；判斷進度不看它 |

指令：`node tools/video/cli.mjs <status|lint|ids|approve|captions|tts|audition|review|render|assemble|package|youtube-sync>`，`--help` 有完整說明。

結束碼：0 成功；1 lint 或檢查沒過；2 用法錯誤；3 需要站主；4 外部服務或額度問題；5 工具還沒做或沒裝；6 被 `STOP` 檔停下、還沒做完（`tts`、`check-audio`）。在工作區（或它的上一層）放一個 `STOP` 檔，長時間執行的階段做完手上那一段就會停。工人（`auto`）跳過自己工作區裡有 `STOP` 檔的影片，這一輪接著做下一支；站主的放棄照樣處理這支影片，重試則等檔案拿掉後才做。`tts` 的章節不合 YouTube 的規則（少於 3 章、第一章不在 00:00、某章不到 10 秒；量的是成片會加上的片頭片尾之後）時，檔案照寫，結束碼 1。

## 技術做法

**影音同步靠構造保證，不靠抽查。**48,000 Hz ÷ 30 fps = 每格 1,600 個取樣。每句音檔加上句後停頓，一起補靜音到整格，所以每一句都從某一格的開頭開始，整條旁白與畫面沒有任何捨入誤差可以累積。字幕（毫秒精度）在句子的語音範圍內分段：有量到的字時就從唸到的字開始，否則依「唸出來的長度」分攤（見下方**字幕**）。

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
- 2026-09-24 在 AI Studio 的聲音庫篩選「Chinese」，找不到任何聲音；口音選單也沒有台灣。口音只能靠 `style`，或之後用「聲音設計」造一個。2026-10-03 起 style 不寫「台灣國語」「台灣腔」：在台灣那指的是重台語腔，模型照字面演，站主試聽後選了「標準國語，咬字清楚，台北人平常說話的語調」；寫法與送合成時的改寫見 [README.md](README.md) §頻道規格的「口音」列。

每個場景送一次請求，句間固定停頓，再在 Node 裡找靜音切段。逐句分開合成會讓每句語調重新起頭，聽起來像在念清單；切段對不上時，該場景退回逐句合成。一次最多 1,500 字，更長的場景由工具拆開。發音一律用 `<sub alias>`（也就是 part 的 `alias`）；zh-TW 的 `<phoneme>` 音標集沒有官方文件，不用。

**畫面**：HTML 版型，由 Playwright 截 1920×1080 PNG。repo 已有這個做法（`tools/claude-code-series/render-art.mjs`）。一個投影片狀態一張，逐條出現的轉場用 Web Animations 固定時間點截短影格。字型用根目錄 devDependencies 的 `@fontsource-variable/noto-sans-tc`、`@fontsource-variable/jetbrains-mono`（OFL），由 `page.route` 從本機提供，所有網路請求都擋掉。不用 Remotion：它不支援 Windows ARM64（arm64 Node 會直接拒絕），公司規模大了還要授權費。

**合成**：ffmpeg（Windows ARM64 用 `winget install BtbN.FFmpeg.GPL`，含 libx264；路徑由 `FFMPEG_PATH` 指定）。

- 每場景編一段，設定完全相同，再用 `-c copy` 串接；改一個場景只重編那一段。
- H.264 High、`-bf 2`、closed GOP、`yuv420p`、BT.709 轉換與標記（沒有的話 Chromium 截圖的顏色會偏）、`+faststart`。
- 音訊用 `loudnorm` 兩段式到 −14 LUFS／−1 dBTP，輸出 AAC-LC 立體聲 48 kHz 384 kbps。
- 自動檢查四項：總格數、音軌與影片差 ≤ 1 格、每章開頭抽格比對來源 PNG、響度。

**字幕**：每句先切段（優先句末、其次逗號，數字不離單位），再決定每段何時出現（2026-10-06 起，票 `2026-10-05-long-video-cc-from-aligned-times`）。Azure 聲音一句話大小的請求，在 `tts` 時先送 `POST /api/video/speech/align`：同一次付費合成順便帶回 Azure 的 WordBoundary，伺服器換成每個書寫單位（一個中文字、一個英文字或數字、一個標點）在音檔裡的毫秒數；工具依文字順序把單位分給同一請求裡的各句，換算到各句自己的音檔，寫進 `timeline.json` 該句的 `timing`（另存在 `audio/<id>.timing.json`，綁住那個 WAV 的 SHA-256：重用音檔時照寫，重錄就丟掉）。「一句話大小」是最多 59 字（`tts/cli.mjs` 的 `ALIGNED_MAX_CHARACTERS`，句間停頓也折成字數）：這條路由把 WAV 用 base64 包在 JSON 裡回傳，是為 Shorts 的一句話設計的，一整個場景該走會串流的 `speech`；59 字讓 WAV 留在路由自己的 2 MB 音檔上限內（每秒 96,000 位元組，2 MB 約 20.8 秒，扣 1 秒前後靜音，以每秒 3 字的慢速估）。長片一個場景一個請求，多半超過，照舊走 `speech`、不帶 `timing`：伺服器的 CPU 對齊器（不付費，可以逐句對音檔）上線以前，長片有實測字時的只有單獨重錄的句子、切段對不上而逐句重合成的句子，和很短的場景。有 `timing` 的句子，每段從它第一個唸出來的字開始、到下一段開始為止；最後一段照舊停到語音後 400 ms，短於 900 ms 的段照樣併到鄰段。文字跟量到的字對不上（`say` 改了字、翻譯）時，該句退回依「唸出來的長度」分攤；翻譯語系目前都是如此，因為 `buildCues` 只拿到該語系的文字與時間軸，拿不到旁白原文，沒辦法沿用 zh-TW 的實測切點。Gemini 聲音沒有字時（伺服器的 CPU 對齊器還沒上線），不會去問；舊站回 404、或答案來自語音日誌（speech journal），都照常合成、不帶 `timing`。`timing` 是從音檔量出來的，不是輸入：請求、音檔快取鍵與 `speech_hash` 都不含它，沒有 `timing` 的時間軸做出的 SRT／VTT 與以前逐位元組相同。

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
| AI 揭露 | 只有擬真到會被誤認為真人、真實事件、真實場景時要揭露；AI 寫稿、資訊圖不用。通用 TTS 旁白官方沒點名，依規則推論不需要。插圖投影片的風格化插圖（`tech-story`、`flat-explainer`）加授權配樂不需揭露；`cinematic-3d` 或生成配樂則勾（`qa/checks.mjs`；[`SHORTS.md`](SHORTS.md) 對 AI 音樂的說法較嚴，工具採嚴的一邊） | support.google.com/youtube/answer/14328491 |
| Azure 語音 | zh-TW：HsiaoChen（女）、YunJhe（男）、HsiaoYu（女），沒有 HD 版；多語 Ava／Andrew／Brian／Emma 可用 `<lang xml:lang="zh-TW">`。每百萬計費字元 15 美元，免費層每月 50 萬。**每個中文字算 2 個計費字元**，SSML 標記（`<speak>`、`<voice>` 以外）也計費：一支 10 分鐘約 3,000 字，連標記約 8,000–9,000 計費字元，免費額度每月約 50 支。即時 REST 單次上限 10 分鐘、只回音檔 | learn.microsoft.com（speech-service 的 text-to-speech §Billable characters、language-support、rest-text-to-speech） |

## 營利政策的對策（寫成關卡，不只是建議）

這條產線的形式正是政策點名的類型，所以：

- `brief.md` 必須有「站主觀點」與「觀眾看完能做到的事」兩節，而且不能空白。lint 會擋，站主選大綱時一併確認。
- 每支至少一段實際示範或實算，不只是念重點。
- 場景版型的順序和其他支太像時，lint 會警告（只比卡片；插圖不算）。
- 插圖投影片（[`ILLUSTRATED.md`](ILLUSTRATED.md)）：每 5–8 秒一張原創插圖加運鏡、卡片漂移、溶接、配樂與音效、說書式旁白——這是對「AI 旁白配幻燈片」這一類的回答：有觀點、有實料、畫面不重複。字幕只做 CC，畫面不燒錄字。
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
