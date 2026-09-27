# AI 漫劇路線（drama）：設計

2026-09-26 定案。這是既有全自動影片產線（[`DESIGN.md`](DESIGN.md)、[`AUTOMATION.md`](AUTOMATION.md)）的第二種格式：畫面不是投影片，而是 AI 生成的鏡頭片段；一支影片有旁白與多個角色；字幕燒進畫面；有背景音樂。這份只寫**為什麼這樣做**與各部分怎麼接起來；操作步驟在 skill `youtube-video` 的 `references/drama.md`（票 `2026-09-26-video-drama-skill-docs`）。工作分成 16 張票，id 都是 `2026-09-26-video-drama-*`。

## 目標與已定的選擇

站主給的參考是《山海经之万兽图鉴》（YouTube `qbyEeolMKDk`，#AI漫剧）：電影感 3D 寫實國風，每鏡 5–8 秒硬切，旁白加角色對白，底部燒錄字幕，有配樂。要求「品質在這以上」。

| 項目 | 決定（2026-09-26 站主） |
| --- | --- |
| 題材 | 原創連載故事（玄幻、古風等）與 Mokaair 內容改編都要；第一支先做原創故事 |
| 畫風 | 電影感 3D 寫實（同參考影片）；2D 日系之後以風格預設加入 |
| 預算 | 先不設上限，第一支用最好的模型做，看實際花費再設；設定欄位仍有數字，預設開大 |
| 格式 | 16:9、每集 2–4 分鐘、燒錄繁中字幕＋五語 CC；之後可合集 |
| 供應商 | 只用站上已有金鑰的 Gemini 與 MiniMax；Kling 第二期 |

「在參考影片之上」的可量化目標：角色跨鏡頭一致（有選定的設定圖當參考）、1080p 30 fps、每段片段過自動品檢（時長、黑格、凍格、切鏡、第 0 格對關鍵影格、視覺模型評分）不合格就重做、多角色配音、字幕排版乾淨、音樂在對白下自動壓低、名詞用發音字典與故事聖經統一。

## 為什麼是一條新路線，不是新工具

現有產線已經有：句子為時鐘的 30 fps／48 kHz 格線時間軸、經伺服器代呼叫的 TTS（金鑰不出 API 容器）、Gemini 轉寫＋Jev 判斷的旁白檢查、五語 CC、ffmpeg 合成與自動檢查、`/admin/videos` 的雜湊綁定審核關卡、主機上的 `video-worker` 容器。漫劇只需要四類新東西：

1. 故事聖經與分鏡的資料模型（`format: "drama"`）。
2. 圖片、片段、音樂的生成，經伺服器（`apps/api/app/video_media/`）。
3. 多角色配音（伺服器零改動：`/video/speech` 每次請求本來就帶 `voice`）。
4. 含動態片段、音樂、燒錄字幕的合成。

企劃→撰稿→審稿的模型階段、審核頁、字幕翻譯、上架包、主機工人全部沿用。

## 供應商（2026-09-26 查官方頁；模型 id 與單價只寫在 `apps/api/app/video_media/catalog.py`，實作時再核對一次）

| 用途 | 第一版 | 備援／第二期 | 單價（1080p） |
| --- | --- | --- | --- |
| 角色設定圖、關鍵影格 | Gemini 3 Pro Image（最多 14 張參考圖） | Gemini 3.1 Flash Image、MiniMax image-01 | 約 US$0.134／張 |
| 圖生影片 | Gemini Omni 1.1 Flash（3–10 秒、首尾影格、角色參考圖） | Veo 3.1 只給主鏡頭；MiniMax H3 2K 當第二個 adapter；Kling 3.0 第二期 | Omni US$0.15／秒、Veo US$0.40／秒、H3 US$0.13／秒 |
| 旁白 | 現有 Gemini 3.8 Flash TTS（Sulafat＋台灣腔 style） | — | 約 US$0.81／小時 |
| 角色配音 | Gemini TTS：30 個內建聲音配 style；之後用聲音設計拿持久的 `voice_…` id | MiniMax speech-2.8（情緒參數、聲音複製，沒有台灣腔）；Azure zh-TW 三個聲音沒有語氣 | 同旁白 |
| 品檢（judge） | Gemini 視覺模型看圖與片段打分 | — | 依 token |
| 背景音樂 | Gemini API 的 Lyria 3.5 | ElevenLabs Music（要新金鑰）、YouTube 音效庫（人工） | US$0.08／首 |
| 對嘴 | 第一版不做：旁白主導，對白用中景與反應鏡頭 | H3 音訊參考或 Kling lip-sync，只用在特寫 | — |

一集 3 分鐘、30 鏡 × 6 秒、重做係數 1.5：Omni 約 US$40，Veo 全用約 US$108，H3 約 US$35；圖片約 US$12，配音與音樂不到 US$1。OpenAI Sora API 已於 2026-09-24 下架；MiniMax 的音樂 API 對新用戶停售。

**地區**：Gemini Omni 的影片編輯／延長在歐洲經濟區與英國不開放，Veo 在歐盟只允許 `allow_adult` 的人物生成；基本圖生影片是否依呼叫端 IP 擋，沒查到明確答案。試作的第一個片段先在正式主機單獨跑一鏡；被擋就把 `clip_provider` 改成 minimax，或評估把工人搬到新加坡機房。

## 品質目標與業界慣例

- 流程：劇本 → 角色與場景設定圖 → 分鏡表 → 每鏡一張關鍵影格 → 圖生影片 → 配音 → 字幕 → 配樂 → 剪輯。每鏡 3–8 秒、每分鐘 5–8 張關鍵影格、八成硬切；每個角色鎖定基準圖；一部戲只用同一個影片模型。
- 觀眾最在意的缺陷（自動品檢要抓的）：臉在鏡頭之間變形、六指、手臂扭曲、人物飄浮、群像比例錯、背景色偏、表情僵硬、名詞不一致、節奏拖沓。
- 字幕：Noto Sans TC 白字深色描邊、離底邊約 14%、每行最多 16 字兩行；多人對白可加「【角色名】」。
- YouTube：3D 寫實畫面與 AI 音樂都勾「合成內容揭露」（官方明說不影響觸及與營利）；每集有獨立的劇情與構圖；站主關卡與製作紀錄（提示詞、參考圖）是作者證據；不轉載別人的漫劇；不用真人聲音或臉；音樂用有授權的來源。

## 資料模型：`format: "drama"`

規則在 `tools/video/core/drama.mjs`，`schema.mjs` 只多呼叫 `validateDrama`。範例：`tools/video/core/fixtures/drama/video.json`。

| 欄位 | 內容 |
| --- | --- |
| `look` | `{ preset?: cinematic-3d\|anime-2d\|ink-wash\|custom, style (≤600), negative?, motion?, candidates?: 2–4（預設 3）, style_frames?: string[] }`：全影片共用的風格提示詞 |
| `characters[]` | `{ id（小寫，不可是 narrator）, name, appearance（≤800，英文，給圖片模型）, voice（同 doc.voice 的物件）, sheet_prompt? }` |
| 鏡頭場景 | `template: "shot"`，`data: { prompt (≤1000), camera?, motion?, negative?, characters?: [id]（≤3）, fit?: auto\|freeze\|slow\|trim, seed?, transition?: cut\|dissolve, start_frame?: { shot, at: "last" }, end_frame?: { prompt } }`；句子不能有 `reveal`。`title`／`chapter`／`outro` 卡片仍可用 |
| 句子 | 多 `speaker?: narrator\|<角色 id>`（預設 narrator）與 `emotion?`（≤80，Gemini 併進 style；Azure 忽略並警告） |
| `music` | `{ prompt? , track?, sha256?, gain_db (-20), duck_db (-10), fade_in_ms (1500), fade_out_ms (3000) }`：有 `prompt` 由 `music` 階段經伺服器生成；有 `track` 用 `<VIDEO_WORKDIR>/_music/` 的檔案 |
| `subtitles` | `{ burn_in（drama 預設 true、slides 預設 false）, style: drama\|plain, speaker_prefix (false) }` |
| `thumbnail.data.shot?` | 用該鏡頭的關鍵影格當縮圖底圖 |

**句子仍是時鐘。** 鏡頭長度＝句子音檔＋停頓＋場景間隔，`buildTimeline` 不變。`clips` 在 `tts` 之後跑，所以知道每鏡精確格數，向供應商要 `duration_s = clamp(ceil(frames/30), 4, 10)`，再對齊伺服器回報的可用秒數。片段長短對不上由 assemble 的 `fitPlan` 決定：`auto` 太長從第 0 格截（第 0 格就是關鍵影格，檢查才成立），太短先慢放到 ≥0.85× 再 `tpad` 凍格；凍格超過 60 格算問題。lint 對估計超過 12 秒的鏡頭報錯、超過 10 秒警告：長旁白拆成更多鏡頭。要延續動作用 `start_frame: { shot, at: "last" }`。

**id 與雜湊。** 鏡頭 id 就是場景 id、角色 id 穩定、句子 id 不變，快取都以 id＋內容雜湊為鍵。`speechHash` 納入每句的說話者、情緒與角色聲音；`visualHash` 已含 `scene.data`；新增 `lookHash`（look＋角色外觀）、`keyframeKey`、`clipKey`、`subtitlesHash`、`mixHash`（改音樂增益不會讓片段失效）。`checks.json` 記六個雜湊，`pipelineStatus` 全對才算成片完成。

drama 的 `brief.md` 必要章節：「故事前提」「角色」「站主觀點」。

## 產線與關卡

| # | 階段 | 誰 | 產出（`<VIDEO_WORKDIR>/<slug>/`） | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 企劃：故事前提、角色、看點、2–3 個大綱 | 企劃代理 | `brief.md` | 站主選大綱 |
| 2 | 撰稿：劇本＋分鏡（`video.json`）、`claims.md`（設定與名詞表） | 撰稿代理 | | `lint` 零錯誤 |
| 3 | 連貫性查核：角色設定、名詞、時間線 | 查核代理 | `verify-1.md` | |
| 4 | `look`：每角色數張設定圖、judge 評分、聯絡表 | 工具 | `characters/` | **站主在 `/admin/videos` 為每個角色選一張（`look` 關卡，每角色一張審核）** |
| 5 | `tts`（依說話者分批）→ `check-audio` | 工具 | `audio/`、`narration.wav`、`timeline.json` | 旁白核准（Jev 全過自動核准，照舊） |
| 6 | `keyframes`：每鏡一張關鍵影格，以選定設定圖當參考；judge 不過換 seed 重做（≤3 次） | 工具 | `keyframes/` | 分鏡關卡 `storyboard`（可選；`auto_approve_storyboard` 開且 judge 過就自動核准） |
| 7 | `render`：卡片、字幕條、縮圖 | 工具 | `frames/` | 缺字、超框 |
| 8 | `clips`：每鏡圖生影片、QC、重做（≤2 次）、預算把關 | 工具 | `clips/` | `needs_review` 為空 |
| 9 | `music`：Lyria 生成或核對站主的檔 | 工具 | `music/` | |
| 10 | `assemble`：片段對齊、字幕疊圖、音樂壓低、串接、檢查 | 工具 | `final.mp4`、`checks.json` | 六個雜湊全對、檢查全過 |
| 11 | CC 翻譯與 `captions` | 翻譯與審稿代理、工具 | `captions/` | |
| 12 | 720p 送審 | 站主 | | 成片核准 |
| 13 | `package` → 上架確認 → 站主在 Studio 上傳成私人、勾合成內容揭露 | 站主 | `upload/` | 上架核准 |

look 排在旁白之前，讓站主在花任何錢之前就能砍掉不對的概念；render 便宜且會先擋缺字，排在最貴的 clips 之前。

## 工具端的階段（`tools/video/media/`）

| 階段 | 做法 | 上限 |
| --- | --- | --- |
| `look` | 每角色用 `sheet_prompt ?? 預設（正面、四分之三、全身、灰底）` 生 `candidates` 張，judge rubric `sheet`（辨識度、符合外觀、風格、乾淨、無文字），最好的當 `suggested`；全部不及格補一輪 | `MAX_LOOK_ROUNDS = 2` |
| `keyframes` | 提示詞＝`data.prompt + look.style`＋角色短標籤；參考圖＝選定設定圖（＋風格圖）；1920×1080；rubric `keyframe`：每角色 `identity_<id>`、符合提示、風格、瑕疵、無文字、主體避開字幕帶；相鄰鏡頭 dHash 太近警告 | `MAX_KEYFRAME_TAKES = 3` |
| `clips` | 依 `start_frame.shot` 拓撲排序；`start_frame`＝關鍵影格、`end_frame` 可選、參考圖給支援的供應商；提示詞＝`motion + camera + look.motion`；輪詢可續跑；QC：`ffprobe` 時長／解析度／fps、`blackdetect`、`freezedetect`、`select='gt(scene,0.5)'`、第 0 格對關鍵影格 PSNR ≥22 且比相鄰鏡頭高 3 dB、judge rubric `clip` | `MAX_CLIP_TAKES = 2`；送出前 `ledger` 對 `max_usd_per_video` |
| `music` | `music.prompt` → 伺服器生成 ≥ 影片長度的曲子；`music.track` → sha256 核對 | |
| `media-status` | 印伺服器預算與本支總計 | |

共用：`media/client.mjs`（比照 `tts/client.mjs`：重試分類、`Retry-After`、預算耗盡不重試）、`media/cache.json`（同一請求不付兩次）、`media/jobs.json`（中斷後接著輪詢）、`media/ledger.json`（花費帳）；每次遠端呼叫之間看 `STOP` 檔。

`tts`：`voiceFor(doc, line)` 決定每句聲音，場景內 `(speaker, emotion)` 改變就切一個請求。`render`：鏡頭場景不畫；字幕條用 `buildCues`（與 CC 同一套斷句計時）每個不同的字幕文字出一張 1920×260 透明 PNG，樣式 `drama`（Noto Sans TC 600 56px、4px 黑描邊、置中、離底 56px）。不用 libass：內建字型只有 woff2，fontconfig 會悄悄換系統字型，三個環境會不一樣。

`assemble`：`layoutDrama` 每場景給 `stills`（卡片，走原路）或 `clip`；`clipSegmentArgs`＝scale/pad → `setpts` → `fps=30` → `tpad` → `trim` → `overlay` 字幕條，編碼參數與投影片段相同但 `-tune film`、獨立 `CLIP_ENCODER_VERSION`，所以 `-c copy` 串接照舊；`dissolve` 在段內用上一鏡最後一格做。音訊：旁白 `asplit` 一路當側鏈，音樂 `stream_loop`＋淡入淡出＋`volume`，`sidechaincompress`，`amix=duration=first`（長度精確等於旁白），再兩段式 loudnorm；沒有 `music` 走原路。檢查：片段格數、第 0 格 PSNR、凍格 >60、音樂床 ≤ −24 LUFS、既有探測與響度。煙霧測試用 `lavfi testsrc2` 與 `sine` 造替身，不碰任何服務。

## 伺服器：`apps/api/app/video_media/`

比照 `video_speech`／`video_reviews`：`admin_api.py` 集中所有 `AppError`（後台路徑不需要四語訊息）、`schemas.py`、`models.py`（`video_media_jobs`，migration `0096`）、`jobs.py`、`storage.py`（`MediaStore(ReviewStore)`）、`meter.py`（包 `usage_meter` 的月計數器）、`catalog.py`、`settings.py`（`VIDEO_MEDIA_*` 環境變數）、`judge.py`、`providers/`。驗證沿用影片工具權杖。

| 端點（`/api/v1/video/media`） | 內容 |
| --- | --- |
| `GET /status` | 供應商、模型選項、drama 設定快照、預算與用量、本月美元估計、`max_usd_per_video`、儲存空間、限制 |
| `POST /images` | `{slug, purpose, prompt, negative_prompt?, aspect, references: [{sha256, role}] ≤4, seed?, shot_id?}` → 202 `JobOut`（重複請求 200）。參考圖一律先在媒體庫，請求裡不放 base64 |
| `POST /clips` | 加 `shot_id`、`first_frame: {sha256}`、`last_frame?`、`seconds`、`resolution?`、`native_audio` |
| `POST /music` | `{slug, prompt, seconds}` → `JobOut` |
| `GET /jobs/{id}` | 回 `JobOut` 並推進一步（向廠商查一次；完成就串流下載入庫） |
| `PUT /files/{slug}/{sha256}?part&parts&size` | 分段上傳（同 `video_reviews`） |
| `GET /files/{slug}/{sha256}` | 串流、Range、`ETag` |
| `POST /judge` | `{slug, kind, files ≤6 圖或 1 片, rubric ≤12, context, min_score?}` → `{scores: {key: 0–10}, overall, pass, problems, notes, model}` |

**輪詢驅動的狀態機**：API 沒有背景執行程序，工作存 Postgres（`queued → submitted → ready | failed | expired`），`GET /jobs/{id}` 拿 Redis 鎖後推進一步；同 `(slug, request_hash)` 去重；`failed` 三次後 409；`submitted` 超過 24 小時 `expired`。預算（片段秒數、圖片、音樂、judge 次數）在呼叫廠商前預留，廠商拒收或判失敗才釋放。Gemini 的下載要帶金鑰，只在 URL 是 https 且主機正是釘住的 `generativelanguage.googleapis.com` 時附上。媒體庫 `/var/lib/mokaair/video-media/<slug>/<sha256>`，單檔 200 MB、總量 30 GB、保留 14 天，`prune` 刪過期、已放棄、已上架的專案。

網站轉送 `apps/web/app/api/video/media/*` 沿用 `forwardToSpeech`；`files` GET 串流 `upstream.body` 並傳 Range，絕不 `arrayBuffer()`。

## 設定（`video_automation_settings`，migration `0095`）

`drama_enabled`、`image_provider`／`image_model`、`clip_provider`／`clip_model`、`clip_resolution`（720p|1080p）、`clip_seconds_default`（4–10）、`clip_native_audio`、`drama_aspect`、`max_clips_per_video`、`max_retakes_per_shot`、`monthly_clip_seconds_budget`（預設 3000）、`monthly_images_budget`（1500）、`monthly_judge_calls_budget`（3000）、`monthly_music_budget`（60）、`max_usd_per_video`（200）、`judge_min_score`（7）、`auto_approve_storyboard`（關）、`character_voice_pool`、`music_enabled`、`subtitle_burn_in`、`style_preset`（cinematic-3d）、`drama_topic_scope`。旁白聲音沿用 `voice`。預算預設刻意開大（站主先不設上限），第一支做完再調。

文字階段不加新名字：drama 的提示詞送在 `planner`／`writer`／`verifier`／`translator`／`caption_reviewer` 底下，`shot_fixer` 用 `writer` 帶 fix payload。

## 審核關卡

`Gate` 加 `look`、`storyboard`；`video_reviews.subject` 讓每個角色一張審核，取代規則改成「同關卡同 subject」；`look` 必須 `choice`；`storyboard` 可自動核准。後台頁的 `LookBody` 是 radio 卡片，`StoryboardBody` 是聯絡表加關鍵影格格網與 judge 摘要。

## 成本與紀錄

| 項目 | 數字 | 來源 |
| --- | --- | --- |
| 一集 3 分鐘的片段（30 鏡 × 6 秒 × 1.5） | Omni 約 US$40、H3 約 US$35、Veo 約 US$108 | 官方單價，2026-09-26 |
| 圖片（約 90 張候選） | 約 US$12 | 同上 |
| 配音、音樂、judge | 不到 US$2 | 同上 |
| 磁碟：媒體庫每支 | 約 1 GB；14 天保留、3–4 支在做約 4–6 GB | 估計，試作後更新 |
| 磁碟：工人 `video_work` 每支 | 1.5–2 GB；發布後刪片段 | 估計 |
| 試作實際花費、每鏡秒數、重做率、地區測試 | （試作票 `2026-09-26-video-drama-pilot` 做完補） | |

## 分期與票

| 票 | 內容 | scope |
| --- | --- | --- |
| `video-drama-settings-and-look-gates` | 設定欄位（遷移）、look／storyboard 關卡 | `apps/api/app/video_automation`、`video_reviews`、`models.py` |
| `video-drama-media-api` | 媒體生成 API、adapter、預算、儲存 | `apps/api/app/video_media`、遷移 `0096` |
| `video-drama-media-web-routes` | 網站轉送路由 | `apps/web/app/api/video/media` |
| `video-drama-admin-settings-and-gates` | 後台設定區與審核卡片 | 影片審核元件、五語 `admin.json`（等衝突票） |
| `video-drama-media-volume` | `video_media` volume | `docker-compose.prod.yml`（等衝突票） |
| `video-drama-core` | 格式、雜湊、lint、狀態、關卡、這份文件 | `tools/video/core`、`cli.mjs`、`docs/videos` |
| `video-drama-media-client` | 用戶端、快取、帳本、QC 解析 | `tools/video/media/{client,cache,ledger,qc,cli}.mjs` |
| `video-drama-tts-voices` | 多聲 | `tools/video/tts` |
| `video-drama-look-keyframes` | look、keyframes、關卡送審 | `tools/video/media/{look,keyframes}.mjs`、`tools/video/review` |
| `video-drama-clips-music` | clips、music | `tools/video/media/{clips,music}.mjs` |
| `video-drama-render` | 字幕條、縮圖 | `tools/video/render`、`templates` |
| `video-drama-assemble` | 片段合成、混音、煙霧測試 | `tools/video/assemble`、`package`、CI |
| `video-drama-automation` | 主機自動流程 | `tools/video/automation`、`AUTOMATION.md` |
| `video-drama-skill-docs` | skill 的 drama 路線 | `.agents/skills/youtube-video`、`.claude/skills/youtube-video` |
| `video-drama-pilot` | 試作：精衛填海 | `docs/videos/jingwei-fills-the-sea`、`lexicon.json` |
| `video-drama-kling-provider-card` | 第二期：Kling | 供應商卡片與 adapter（等衝突票） |

順序：伺服器端 settings → media-api → volume，web-routes 平行；工具端 core → media-client／tts-voices／render 平行 → look-keyframes → clips-music、assemble → automation → skill-docs → pilot。第二期：對嘴、音效、2D 風格預設、Kling、MiniMax 語音、直式 Shorts。
