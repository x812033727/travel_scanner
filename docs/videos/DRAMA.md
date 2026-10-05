# AI 漫劇路線（drama）：設計

2026-09-26 起草，2026-10-01 更新字幕與動畫交付規格；2026-10-04 把鏡頭長度、片段買幾秒、參考圖上限與沒有人說話的鏡頭改成程式現在的行為（票 `2026-10-03-drama-design-documents-say-what-the`、`2026-10-04-anime-silent-action-guidance`）。這是既有全自動影片產線（[`DESIGN.md`](DESIGN.md)、[`AUTOMATION.md`](AUTOMATION.md)）的第二種格式：畫面是 AI 生成的鏡頭片段，一支影片有旁白、多個角色和背景音樂；新製作的對白與旁白字幕全為可開關 CC，`burn_in: false`。操作步驟在 skill `youtube-video` 的 `references/drama.md`。

**這次十部作品**依[動畫製作規格](series-plans/production-20261001/README.md)：先完成 zh-TW 台灣口音版，核准鎖定後才製作 ja／ko／en 配音及各語 CC。採 Veo Lite 的八秒 1080p 動態素材，正片不以靜圖縮放或尾格停格補時；同集造型由核定 `shot_looks`／`character_looks` 選擇。先試音、實測分鏡和代表小樣，再放量。多角色外語配音及自動對嘴尚未因這輪而實作，歷史文件／核准不能代替新製作驗收。

**2026-09-27 起**：單集與作品走同一條流程（單集是一部 `kind = one-off`、只有一集的作品，文件只有一份故事聖經 `bible`），漫劇不再用「選大綱」卡片，每支都有劇本關卡（`DRAMA_STEPS` 在 `fact-checked` 之後多了 `script approved`），站主可以在文件與劇本上跟模型討論（`video_drama_messages`）；設定分頁把漫劇與教學分開。設計在 [`DRAMA-FLOW.md`](DRAMA-FLOW.md)；下面「產線與關卡」改了第 1 步（站主核准故事聖經）、第 3 步（加聽眾審稿）、第 4 步（新的劇本關卡）、第 5 步（`auto_pick_look`）、第 12 步（只做繁中字幕）與第 13 步（成片自動品管），並加了第 15 步（語言）；其餘照舊。操作步驟在 skill 的 `references/drama.md`。

## 目標與已定的選擇

站主給的參考是《山海经之万兽图鉴》（YouTube `qbyEeolMKDk`，#AI漫剧）：電影感 3D 寫實國風，硬切（2026-10-03 量它的前 240 秒：鏡頭長度中位數 2.0 秒、最長 5.0 秒，見 `docs/videos/drama-craft/reference-study-20261003.md`；這裡原本寫的「每鏡 5–8 秒」是當時的印象），角色對白為主，底部燒錄字幕，有配樂。要求「品質在這以上」。

| 項目 | 決定（2026-09-26 站主） |
| --- | --- |
| 題材 | 原創連載故事（玄幻、古風等）與 Mokaair 內容改編都要；第一支先做原創故事 |
| 畫風 | 電影感 3D 寫實（同參考影片）；2D 日系之後以風格預設加入 |
| 預算 | 先不設上限，第一支用最好的模型做，看實際花費再設；設定欄位仍有數字，預設開大 |
| 格式 | 16:9、每集約 2–4 分鐘、可開關繁中 CC；日／韓／英版在繁中鎖定後；之後可合集 |
| 供應商 | 只用站上已有金鑰的 Gemini 與 MiniMax；Kling 第二期 |

「在參考影片之上」的可量化目標：角色跨鏡頭一致（有選定的設定圖當參考）、1080p 30 fps、每段片段過自動品檢（時長、黑格、凍格、切鏡、第 0 格對關鍵影格、視覺模型評分）不合格就重做、多角色配音、字幕排版乾淨、音樂在對白下自動壓低、名詞用發音字典與故事聖經統一。

## 為什麼是一條新路線，不是新工具

現有產線已經有：句子為時鐘的 30 fps／48 kHz 格線時間軸、經伺服器代呼叫的 TTS（金鑰不出 API 容器）、Gemini 轉寫＋Jev 判斷的旁白檢查、五語 CC、ffmpeg 合成與自動檢查、`/admin/videos` 的雜湊綁定審核關卡、主機上的 `video-worker` 容器。漫劇只需要四類新東西：

1. 故事聖經與分鏡的資料模型（`format: "drama"`）。
2. 圖片、片段、音樂的生成，經伺服器（`apps/api/app/video_media/`）。
3. 多角色配音（伺服器零改動：`/video/speech` 每次請求本來就帶 `voice`）。
4. 含動態片段與音樂的合成，對白字幕另外交付 CC。

企劃→撰稿→審稿的模型階段、審核頁、字幕翻譯、上架包、主機工人全部沿用。

## 供應商（2026-09-26 查官方頁；模型 id 與單價只寫在 `apps/api/app/video_media/catalog.py`，實作時再核對一次）

| 用途 | 第一版 | 備援／第二期 | 單價（1080p） |
| --- | --- | --- | --- |
| 角色設定圖、關鍵影格 | Gemini 3 Pro Image（每次請求最多 4 張參考圖：伺服器 `apps/api/app/video_media/schemas.py` 的 `MAX_REFERENCES`，`tools/video/media/keyframes.mjs` 送最後 4 張；模型頁寫的上限 14 用不到） | Gemini 3.1 Flash Image、MiniMax image-01 | 約 US$0.134／張 |
| 圖生影片 | Gemini Omni 1.1 Flash（3–10 秒、首尾影格、角色參考圖） | Veo 3.1 只給主鏡頭；MiniMax H3 2K 當第二個 adapter；Kling 3.0 第二期 | Omni US$0.15／秒、Veo US$0.40／秒、H3 US$0.13／秒 |
| 旁白 | 現有 Gemini 3.8 Flash TTS（Sulafat＋頻道口音 style） | — | 約 US$0.81／小時 |
| 角色配音 | Gemini TTS：30 個內建聲音配 style；之後用聲音設計拿持久的 `voice_…` id | MiniMax speech-2.8（情緒參數、聲音複製，沒有台灣腔）；Azure zh-TW 三個聲音沒有語氣 | 同旁白 |
| 品檢（judge） | Gemini 視覺模型看圖與片段打分 | — | 依 token |
| 背景音樂 | Gemini API 的 Lyria 3.5 | ElevenLabs Music（要新金鑰）、YouTube 音效庫（人工） | US$0.08／首 |
| 對嘴 | 第一版不做：旁白主導，對白用中景與反應鏡頭 | H3 音訊參考或 Kling lip-sync，只用在特寫 | — |

一集 3 分鐘照 `.agents/skills/youtube-video/references/drama-craft.md` 的節奏（鏡頭長度中位數 2.5–3.5 秒）約 60 鏡。片段買的秒數不是鏡長，而是 `tools/video/media/clips.mjs` 的 `clipSeconds`：`veo-3.1*` 配 1080p 固定 8 秒；其他模型把鏡長進位成整秒、夾在 `MIN_CLIP_SECONDS` 4 與 `MAX_CLIP_SECONDS` 10 之間，再往上貼齊 `catalog.py` 該模型的 `durations`。60 鏡、每鏡 3 秒台詞、每鏡一次 take、每份素材一次 judge（US$0.01）：Veo 3.1 Lite 約 US$39（買 480 秒）、Omni 約 US$37（240 秒）、H3 約 US$32、Veo 3.1 全用約 US$193；關鍵影格含 judge 約 US$9；配音與音樂不到 US$1。重做到上限、每月額度與三條路線（伺服器 API、Hailuo 網頁、Kling）的比較在 `.agents/skills/animation-production/SKILL.md`「錢怎麼算」與 `.agents/skills/animation-production/references/cost-model.md`（2026-10-04 改；起草時的估算是 30 鏡、每鏡 6 秒、重做係數 1.5）。OpenAI Sora API 已於 2026-09-24 下架；MiniMax 的音樂 API 對新用戶停售。

**地區**：Gemini Omni 的影片編輯／延長在歐洲經濟區與英國不開放，Veo 在歐盟只允許 `allow_adult` 的人物生成；基本圖生影片是否依呼叫端 IP 擋，沒查到明確答案。試作的第一個片段先在正式主機單獨跑一鏡；被擋就把 `clip_provider` 改成 minimax，或評估把工人搬到新加坡機房。

## 品質目標與業界慣例

- 流程：劇本 → 角色與場景設定圖 → 分鏡表 → 每鏡一張關鍵影格 → 圖生影片 → 配音 → 字幕 → 配樂 → 剪輯。鏡頭長度照 2026-10-03 量過參考片後定的規格（`.agents/skills/youtube-video/references/drama-craft.md`）：中位數 2.5–3.5 秒，九成不超過 6 秒，最長 8 秒，溶接不超過一成；檢查腳本的門檻是 `tools/video/core/craft.mjs` 的 `TARGETS`（`medianShotSeconds` 2–4、`p90ShotSeconds` 6、`longestShotSeconds` 8、`dissolveShare` 0.1）。每個要畫的鏡頭一張關鍵影格，從別鏡素材切來的（`source`）不畫（`tools/video/core/drama.mjs` 的 `drawnShotScenes`）。lint 對估計超過 12 秒的鏡頭報錯、超過 10 秒警告，有角色的漫劇中位數低於 2 秒也警告（同檔的 `MAX_SHOT_SECONDS`、`WARN_SHOT_SECONDS`、`MIN_MEDIAN_SHOT_SECONDS`）。每個角色鎖定基準圖；一部戲只用同一個影片模型。（2026-10-04 改；起草時這裡寫的是 2026-09-26 查到的業界慣例，比量到的參考片慢。）
- 觀眾最在意的缺陷（自動品檢要抓的）：臉在鏡頭之間變形、六指、手臂扭曲、人物飄浮、群像比例錯、背景色偏、表情僵硬、名詞不一致、節奏拖沓。
- 字幕：Noto Sans TC 白字深色描邊、離底邊約 14%、每行最多 16 字兩行；多人對白可加「【角色名】」。
- YouTube：3D 寫實畫面與 AI 音樂都勾「合成內容揭露」（官方明說不影響觸及與營利）；每集有獨立的劇情與構圖；站主關卡與製作紀錄（提示詞、參考圖）是作者證據；不轉載別人的漫劇；不用真人聲音或臉；音樂用有授權的來源。

## 資料模型：`format: "drama"`

規則在 `tools/video/core/drama.mjs`，`schema.mjs` 只多呼叫 `validateDrama`。範例：`tools/video/core/fixtures/drama/video.json`。

| 欄位 | 內容 |
| --- | --- |
| `look` | `{ preset?: cinematic-3d\|anime-2d\|ink-wash\|flat-explainer\|custom, style (≤600), negative?, motion?, candidates?: 2–4（預設 3）, style_frames?: string[] }`：全影片共用的風格提示詞 |
| `characters[]` | `{ id（小寫，不可是 narrator）, name, appearance（≤800，英文，給圖片模型）, voice（同 doc.voice 的物件）, sheet_prompt? }` |
| 鏡頭場景 | `template: "shot"`，`data: { prompt (≤1000), camera?, motion?, negative?, characters?: [id]（≤3）, fit?: auto\|freeze\|slow\|trim, seed?, transition?: cut\|dissolve, start_frame?: { shot, at: "last" }, end_frame?: { prompt }, visual?: clip\|still, source?: { shot, from_s } }`；`visual` 預設 `clip`，`still` 不買片段，由 `assemble` 用關鍵影格加運鏡（下面「畫面等級與運鏡」）；`source` 從更早一個 clip 鏡頭的素材第 `from_s` 秒切進來，不畫關鍵影格、不買素材（下面「同一份素材切幾次」）；有角色、沒有時長下限、`category` 不是 anime 的漫劇，與政策有效的 `long-anime-v1` 長篇動畫，可用場景層的 `action_seconds`（1–8）加空 `lines` 寫沒有人說話的鏡頭（下面「沒有人說話的鏡頭」）；句子不能有 `reveal`。`title`／`chapter`／`outro` 卡片仍可用 |
| 句子 | 多 `speaker?: narrator\|<角色 id>`（預設 narrator）與 `emotion?`（≤80，Gemini 併進 style；Azure 忽略並警告） |
| `music` | `{ prompt? , track?, sha256?, gain_db (-20), duck_db (-10), fade_in_ms (1500), fade_out_ms (3000) }`：有 `prompt` 由 `music` 階段經伺服器生成；有 `track` 用 `<VIDEO_WORKDIR>/_music/` 的檔案 |
| `subtitles` | `{ burn_in（預設 false；新自動製作固定 false）, style: drama\|plain, speaker_prefix (false) }`；舊手動影片仍可讀取其明確的燒錄設定 |
| `thumbnail.data.shot?` | 用該鏡頭的關鍵影格當縮圖底圖 |

**句子仍是時鐘。** 鏡頭長度＝句子音檔＋停頓＋場景間隔，`buildTimeline` 不變。`clips` 在 `tts` 之後跑，所以知道每鏡精確格數，買幾秒由 `tools/video/media/clips.mjs` 的 `clipSeconds` 決定：`veo-3.1*` 模型配 1080p 一律 8 秒（Veo 3.1 的 1080p 只有 8 秒，Lite 也是）；其他模型是格數 ÷ 30 進位成整秒、夾在 `MIN_CLIP_SECONDS` 4 與 `MAX_CLIP_SECONDS` 10 之間，再取伺服器回報的該模型可用秒數（`catalog.py` 的 `durations`）裡第一個不短於它的，都短就取最長的。片段長短對不上由 assemble 的 `fitPlan` 決定：`auto` 太長從第 0 格截（第 0 格就是關鍵影格，檢查才成立），太短先慢放到 ≥0.85× 再 `tpad` 凍格；凍格超過 60 格算問題。lint 對估計超過 12 秒的鏡頭報錯、超過 10 秒警告：長旁白拆成更多鏡頭。要延續動作用 `start_frame: { shot, at: "last" }`。

**id 與雜湊。** 鏡頭 id 就是場景 id、角色 id 穩定、句子 id 不變，快取都以 id＋內容雜湊為鍵。`speechHash` 納入每句的說話者、情緒與角色聲音；`visualHash` 已含 `scene.data`；新增 `lookHash`（look＋角色外觀）、`keyframeKey`、`clipKey`、`subtitlesHash`、`mixHash`（改音樂增益不會讓片段失效）。`checks.json` 記六個雜湊，`pipelineStatus` 全對才算成片完成。

drama 的 `brief.md` 必要章節：「故事前提」「角色」「站主觀點」。

### 畫面等級與運鏡（2026-09-27 加，設計在 [`BINGE.md`](BINGE.md)）

長篇作品可以選每集有多少鏡頭買片段（`visual_tier`；單集漫劇沒有這個設定，全部是 clip）：

| 等級 | 片段比例上限（`TIER_CLIP_SHARE_MAX`） | 30 鏡一集最多幾個 clip |
| --- | --- | --- |
| `clips` | 1 | 30（still 只警告） |
| `hybrid` | 0.4 | 12 |
| `stills` | 0.1 | 3 |

- 鏡頭的 `data.visual` ∈ `VISUAL_MODES = ["clip", "still"]`。lint 從 `docs/videos/<slug>/series.json` 的 `visual_tier` 讀等級（工人從作品寫進去；沒有就不檢查），超過上限是錯誤（`visualTierProblems`）。`clipsHash` 只算 clip 鏡頭。
- `clips` 只為 clip 鏡頭生成；still 鏡頭在 `clips/manifest.json` 記 `{ still: true, file, sha256 }` 指向它通過 judge 的關鍵影格。
- `assemble`：`layoutDrama` 對 still 鏡頭回 `kind: "motion"`；`motionSegmentArgs` 把關鍵影格 `-loop 1` 成該鏡的格數、放大 1.25 倍（`MOTION_SOURCE_SCALE`）、`zoompan`（`d=1`、以輸出格號 `on` 寫表達式、最後一格剛好到位）、`trim`，然後字幕條、溶接、色彩標記與編碼參數都與片段段相同，只多一個位元率上限（`-maxrate 8M -bufsize 16M`：CRF 18，但不超過 YouTube 對 1080p30 上傳建議的 8 Mbit/s；2026-10-04 起，量測在 `ILLUSTRATED.md` §成片大小），`-c copy` 串接不變；獨立 `MOTION_ENCODER_VERSION`。幅度小：push／pull 10%、pan／tilt 固定 1.08 倍、drift 4%。
- 運鏡由 `motionMove(data)` 只從 `camera` 的關鍵字決定（整字比對；`motion` 是畫面裡發生的事，不讀，2026-10-03 起）：`push-in`（push、dolly in、zoom in、closer、move in）、`pull-out`（pull、zoom out、widen、back away）、`pan-right`（pan left、left to right：以畫面的移動方向命名，攝影機向左搖畫面往右跑）、`pan-left`（pan right、right to left）、`tilt-up`（tilt up、crane up、rise）、`tilt-down`（tilt down、crane down、descend）、`locked`（locked、static、fixed、tripod：整格不動）、其他 `drift`（寫 drift 也是）。
- 檢查：`push-in`、`drift` 與 `locked` 的第 0 格是整張關鍵影格，對它算 PSNR（≥ 22）；其他運鏡只驗格數；`checks.json.metrics.shots` 記 `kind: "motion"` 與 `move`。

### 同一份素材切幾次（2026-10-03 加，票 `2026-10-03-drama-craft-in-video-tools`）

量過的漫劇一場戲只有三、四個鏡位，卻每兩秒換一次畫面（`.agents/skills/youtube-video/references/drama-craft.md`）；每個鏡頭各買一份素材，切得密就是一刀一份。回到同一鏡位的鏡頭寫 `data.source: { shot, from_s }`：

- lint（`validateDrama`）：`shot` 是更早的一個 clip 鏡頭，本身不能再是 `source`、不能是 still；這個鏡頭不能有 `start_frame`／`end_frame`、不能是 still、不能當 `thumbnail.data.shot`；`from_s` 加估計鏡長超過 10 秒（片段模型的上限）是錯誤，production profile 下超過 8 秒也是。
- `keyframes` 不畫它（`drawnShotScenes`），storyboard 關卡沒有它的圖；`clips` 不買（`sourcedShotScenes`），在來源素材通過品檢後於 manifest 記 `{ source: { shot, from_s, from_frame }, file, sha256, frames, seconds, needed_s }` 指向來源素材；來源沒過或太短就 `needs_review`。`--dry-run` 印出不用買的秒數；帳本（`media/ledger.json`）記一筆 `kind: "clip"`、`status: "cut"`、`cost_usd: 0`，帶 `saved_seconds`／`saved_usd`（`savedTotals`），重跑只換不重複記。`clips_hash` 用來源素材的雜湊，來源重做它就跟著重組。
- `assemble`：`layoutDrama` 給它 `from_frame` 與 `source`，片段鏈前面加 `trim=start_frame=<from_frame>`；可用格數是來源素材扣掉起點；第 0 格不比關鍵影格，改比來源素材在 `from_frame` 那一格（`frameArgs` 抽出 PNG，PSNR ≥ 22；`checks.json.metrics.shots[].source_frame_psnr`）。
- 還沒做：同一份素材放大成較近的景別（punch-in，最多 1.5 倍）。要拿一場試拍的 1080p 素材量過裁切後的畫質才決定，不先假設。

**沒有人說話的鏡頭**：場景層寫 `action_seconds`（1–8 的整數）加空的 `lines`，鏡頭的 `prompt` 與 `motion` 寫看得到的動作，長度就是它。`tools/video/core/schema.mjs` 的 `validateScenes` 在兩種影片接受（`validAnime || timesSilentShots(doc)`；`tools/video/core/timeline.mjs` 排時間軸時同一條件）：有角色、沒有時長下限、不是知識長片、`category` 不是 anime 的漫劇（`drama.mjs` 的 `timesSilentShots`，2026-10-03 加）；與 `production_policy: "long-anime-v1"` 且 `tools/video/core/anime-policy.mjs` 的 `validateAnimePolicy` 沒有問題的長篇動畫（原本只有它，規則在 [`LONG-ANIME-PRODUCTION.md`](LONG-ANIME-PRODUCTION.md)）。旁白講述的影片、有 480 秒下限的知識長片（品牌故事、AI 名詞、解說，就算列了角色）都不行：它們的長度是在旁白上量的，靜默鏡會填掉下限。`category: "anime"` 而沒有有效長篇政策的集也不行：動畫類的靜默鏡只經由那份政策（2026-10-04 更正：這裡原本把動畫類整個列為不行）。

## 產線與關卡

| # | 階段 | 誰 | 產出（`<VIDEO_WORKDIR>/<slug>/`） | 關卡 |
| --- | --- | --- | --- | --- |
| 1 | 企劃：故事聖經（前提、角色、幕、一個大綱、素材、不做的事；作品是設定集、總綱、篇章細綱） | 企劃模型（variant `bible`） | 站上的文件版本；核准後工人寫 `brief.md`（`## 大綱` 只有選項 A，本機核准） | **站主核准故事聖經**（可先在討論串問或要求改） |
| 2 | 撰稿：劇本＋分鏡（`video.json`）、`claims.md`（設定與名詞表） | 撰稿代理 | | `lint` 零錯誤 |
| 3 | 連貫性查核：角色設定、名詞、時間線 → 聽眾審稿 | 查核代理 | `verify-1.md` | |
| 4 | 劇本：`script.md`（只含敘事） | 工具 | `docs/videos/<slug>/script.md` | **劇本關卡 `script`：站主讀、討論、核准；「劇本先給我看」（`series_script_gate`）關著就自動核准。在任何圖片或片段花錢之前** |
| 5 | `look`：每角色數張設定圖、judge 評分、聯絡表 | 工具 | `characters/` | `look` 關卡（每角色一張審核）：`auto_pick_look` 開著就核准 judge 建議的那張；沒過或關著才**站主在 `/admin/videos` 為每個角色選一張** |
| 6 | `tts`（依說話者分批）→ `check-audio` | 工具 | `audio/`、`narration.wav`、`timeline.json` | 旁白核准（Jev 全過自動核准，照舊） |
| 7 | `keyframes`：每鏡一張關鍵影格，以選定設定圖當參考；judge 不過換 seed 重做（≤3 次） | 工具 | `keyframes/` | 分鏡關卡 `storyboard`（可選；`auto_approve_storyboard` 開且 judge 過就自動核准） |
| 8 | `render`：卡片、字幕條、縮圖 | 工具 | `frames/` | 缺字、超框 |
| 9 | `clips`：每鏡圖生影片、QC、重做（≤2 次）、預算把關 | 工具 | `clips/` | `needs_review` 為空 |
| 10 | `music`：Lyria 生成或核對站主的檔 | 工具 | `music/` | |
| 11 | `assemble`：片段對齊、字幕疊圖、音樂壓低、串接、檢查 | 工具 | `final.mp4`、`checks.json` | 六個雜湊全對、檢查全過 |
| 12 | `captions`（只有繁中） | 工具 | `captions/` | |
| 13 | 720p 送審 | 工具、站主 | | 成片關卡 `final`：自動品管全過就核准（`drama_auto_approve_final`），沒過才站主看 |
| 14 | `package` → 上架確認 → 站主在 Studio 上傳成私人、勾合成內容揭露 | 站主 | `upload/` | 上架核准 |
| 15 | 語言（[`LANGUAGES.md`](LANGUAGES.md)）：成片核准後站主勾語言，工人只做勾了的 | 站主、工具、翻譯代理 | `captions/<語系>.srt`、`upload/` | `languages` 關卡 |

劇本關卡在 look 之前，站主在花任何錢之前讀過整個故事；look 排在旁白之前，judge 選不出來時站主還能砍掉不對的概念；render 便宜且會先擋缺字，排在最貴的 clips 之前。

## 工具端的階段（`tools/video/media/`）

| 階段 | 做法 | 上限 |
| --- | --- | --- |
| `look` | 每角色用 `sheet_prompt ?? 預設（正面、四分之三、全身、灰底）` 生 `candidates` 張，judge rubric `sheet`（辨識度、符合外觀、風格、乾淨、無文字），最好的當 `suggested`；全部不及格補一輪 | `MAX_LOOK_ROUNDS = 2` |
| `keyframes` | 提示詞＝`data.prompt + look.style`＋角色短標籤；參考圖＝選定設定圖（＋風格圖）；1920×1080；rubric `keyframe`：每角色 `identity_<id>`、符合提示、風格、瑕疵、無文字、主體避開字幕帶；相鄰鏡頭 dHash 太近警告 | `MAX_KEYFRAME_TAKES = 3` |
| `clips` | 依 `start_frame.shot` 拓撲排序；`start_frame`＝關鍵影格、`end_frame` 可選、參考圖給支援的供應商；提示詞＝`motion + camera + look.motion`；輪詢可續跑；QC：`ffprobe` 時長／解析度／fps、`blackdetect`、`freezedetect`、`select='gt(scene,0.5)'`、第 0 格對關鍵影格 PSNR ≥22 且比相鄰鏡頭高 3 dB、judge rubric `clip` | `MAX_CLIP_TAKES = 2`；送出前 `ledger` 對 `max_usd_per_video`：先記一筆 `reserved`，job 回來才對帳成實價（見「成本與紀錄」）；judge 每次 US$0.01 也過同一道 |
| `music` | `music.prompt` → 伺服器生成 ≥ 影片長度的曲子；`music.track` → sha256 核對 | |
| `media-status` | 印伺服器預算與本支總計（`totals.usd` 含送出還沒對帳的 `reserved` 預留；`--json` 另列 `totals.reserved` 與 `reservations`） | |

共用：`media/client.mjs`（比照 `tts/client.mjs`：重試分類、`Retry-After`、預算耗盡不重試）、`media/cache.json`（同一請求不付兩次）、`media/jobs.json`（中斷後接著輪詢）、`media/ledger.json`（花費帳：送出前先記 `reserved`，job 回來再對帳）；每次遠端呼叫之間看 `STOP` 檔。

### 外面做的片段：`clips import`（2026-10-04 加，票 `2026-10-03-clips-import-bring-a-clip-made`）

站主的 Hailuo 網頁方案與 Kling MCP 做出的片段不經過伺服器，用這個指令進到一個鏡頭：

```bash
node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web|kling-mcp|external [--plan <方案>] [--credits N] [--usd N] [--note "…"] [--judge] [--force]
```

- **前提與 `clips` 一樣**：timeline 與 keyframes manifest 是現在的劇本（否則 2）、這一鏡有通過 judge 的關鍵影格（否則 2）、storyboard 已核准（否則 3）。鏡頭必須是 clip 鏡：still 與從別鏡切的（`source`）都是 2。**有 production profile 的作品一律 3**：profile 指定了買片段的模型，`productionClipProblems` 會拿 manifest 對它；要收別條路線的片段得先由站主改 profile，那是另一張票。
- **做什麼**：把檔案複製成 `clips/<shot>-import-<n>.mp4`（同一個檔再匯入一次沿用原編號），跑買來的 take 同一組 ffmpeg 檢查（`qc.mjs`：解析度、fps、黑格、旁白範圍內的凍格、模型自己切鏡、第 0 格對關鍵影格 PSNR ≥ 22 且比相鄰關鍵影格高 3 dB；沒有向伺服器要過秒數，所以不查「比要求的短」，比台詞短時只提醒，由 `assemble` 的 `fitPlan` 處理）。`--judge` 才把片段與角色設定圖上傳媒體庫、問 `clip` rubric，記一筆 US$0.01 的 judge，這一次也先過單支上限；不帶 `--judge`、`--usd` 也沒給（或給 0）就完全不碰網站，`--usd` 大於 0 要先讀一次 `status` 拿上限。
- **沒過**：跟失敗的 take 一樣 `needs_review: true` 帶原因，結束碼 1；`--force` 留下它（`needs_review: false`、`forced: true`，量到的問題仍在 `qc.problems`）。外部生成時用這一鏡的關鍵影格當首格，PSNR 才過得了。
- **manifest**：`clips` 寫的形狀（`file`、`sha256`、`seconds`、`frames`、`needed_s`、`first_frame`、`qc`、`judge`、`takes`、`needs_review`）加 `provider`、`plan`、`credits`、`imported_at`（與 `note`、`forced`）；原本買的 take 留在 `takes` 裡。從這一鏡切出去的鏡頭（`source`）跟著改指新檔，新檔不夠長的那個 `needs_review`、結束碼 1。`clips_hash` 重算，`state.json` 記一次 `clips`。
- **帳本**：一筆 `{ stage: "clips", kind: "clip", id, provider, plan, credits, seconds, cost_usd, file, sha256, status: "imported" }`（`bookImport`，同一鏡同一檔只記一筆）。`cost_usd` 是 `--usd` 給的數，沒給是 0：點數換美元由操作的人算，工具不代換。秒數算進 `totals.clip_seconds`；`--usd` 大於 0 先過單支上限（超過是結束碼 3，沒有 `--force` 可以越過），檢查期間在帳本記一筆 key 為 `import:<shot>:<sha256>` 的 `reserved`，`--judge` 的那一次 judge 看得到它，`bookImport` 用匯入列取代它，沒記成（STOP、ffmpeg 缺、檢查途中出錯）就放掉；`importedTotals` 把匯入的另外加總。
- **之後**：`clips` 把匯入的鏡頭當已完成留用（`kept (imported from …)`），`--dry-run` 不替它估價，`status` 的 `clips generated` 後面寫「N of M clips imported: …」。`clips --force` 仍會把它重買。

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
| `POST /locate` | `{slug, sha256, labels? ≤8}` → `{boxes: [{label, box: [ymin, xmin, ymax, xmax], score}], width, height, model}`：媒體庫裡一張 png／jpeg／webp 的主體在哪裡（`locate.py`，2026-10-05 加）。`box` 是 Gemini 的 `box_2d`，0–1000 等分圖高與圖寬，乘 `height/1000`、`width/1000` 得像素（工具端 `client.mjs` 的 `scaleBox`）；`labels` 用劇本的字眼說要找誰，不給就找每個角色（主角在前）與最明顯的主體；沒找到回空陣列。跟 judge 同一次「Gemini 看一眼」：記在 `judge_calls` 預算與每小時 judge 次數上、每次 US$0.01、同一把金鑰與模型、同 `inline_judge_bytes` 上限；片段回 422 `video_media_invalid`，工具先抽一格上傳再問。直式裁切、Shorts 智慧裁切與日後任何重新取景都從這裡拿座標。`GET /status` 的 `limits.locate_labels` 表示伺服器有這個端點 |

**輪詢驅動的狀態機**：API 沒有背景執行程序，工作存 Postgres（`queued → submitted → ready | failed | expired`），`GET /jobs/{id}` 拿 Redis 鎖後推進一步；同 `(slug, request_hash)` 去重；`failed` 三次後 409；`submitted` 超過 24 小時 `expired`。預算（片段秒數、圖片、音樂、judge 次數）在呼叫廠商前預留，廠商拒收或判失敗才釋放。Gemini 的下載要帶金鑰，只在 URL 是 https 且主機正是釘住的 `generativelanguage.googleapis.com` 時附上。媒體庫 `/var/lib/mokaair/video-media/<slug>/<sha256>`，單檔 200 MB、總量 30 GB、保留 14 天，`prune` 刪過期、已放棄、已上架的專案。

網站轉送 `apps/web/app/api/video/media/*` 沿用 `forwardToSpeech`；`files` GET 串流 `upstream.body` 並傳 Range，絕不 `arrayBuffer()`。

## 設定（`video_automation_settings`，migration `0095`）

`drama_enabled`、`image_provider`／`image_model`、`clip_provider`／`clip_model`、`clip_resolution`（720p|1080p）、`clip_seconds_default`（4–10）、`clip_native_audio`、`drama_aspect`、`max_clips_per_video`、`max_retakes_per_shot`、`monthly_clip_seconds_budget`（預設 3000）、`monthly_images_budget`（1500）、`monthly_judge_calls_budget`（3000）、`monthly_music_budget`（60）、`max_usd_per_video`（200）、`judge_min_score`（7）、`auto_approve_storyboard`（關）、`character_voice_pool`、`music_enabled`、`subtitle_burn_in`、`style_preset`（cinematic-3d）、`drama_topic_scope`。旁白聲音沿用 `voice`。預算預設刻意開大（站主先不設上限），第一支做完再調。

文字階段不加新名字：drama 的提示詞送在 `planner`／`writer`／`verifier`／`translator`／`caption_reviewer` 底下，`shot_fixer` 用 `writer` 帶 fix payload。

## 審核關卡

`Gate` 加 `look`、`storyboard`（`script` 見 [`SERIES.md`](SERIES.md)，2026-09-27 起每支漫劇都有）；`video_reviews.subject` 讓每個角色一張審核，取代規則改成「同關卡同 subject」；`look` 必須 `choice`；`storyboard` 可自動核准。後台頁的 `LookBody` 是 radio 卡片，`StoryboardBody` 是聯絡表加關鍵影格格網與 judge 摘要。

## 成本與紀錄

| 項目 | 數字 | 來源 |
| --- | --- | --- |
| 一集 3 分鐘的片段（60 鏡、每鏡 3 秒台詞、一次 take，秒數照 `clipSeconds`；2026-10-04 改，原本是 30 鏡 × 6 秒 × 1.5） | Veo 3.1 Lite 約 US$39、Omni 約 US$37、H3 約 US$32、Veo 3.1 約 US$193（各含每份素材一次 judge） | `catalog.py` 單價（2026-09-26 查，Lite 2026-10-01）；算式在 `.agents/skills/animation-production/SKILL.md`「錢怎麼算」 |
| 圖片（60 張關鍵影格與 9 張設定圖，各一次，含 judge） | 約 US$10 | 同上 |
| 配音、音樂、judge | 不到 US$2 | 同上 |
| 磁碟：媒體庫每支 | 約 1 GB；14 天保留、3–4 支在做約 4–6 GB | 估計，試作後更新 |
| 磁碟：工人 `video_work` 每支 | 1.5–2 GB；發布後刪片段 | 估計 |
| 試作實際花費、每鏡秒數、重做率、地區測試 | （試作票 `2026-09-26-video-drama-pilot` 做完補） | |

### 先預留、後對帳（2026-10-05 加，票 `2026-10-05-media-budget-estimate-reserve-reconcile`）

錢在花掉之前先進帳本。`Stage.generate`（`tools/video/media/stages.mjs`）過了 `capProblem` 之後、送出之前，用 `reserve`（`ledger.mjs`）在 `media/ledger.json` 記一筆 `{ stage, kind, id, provider, model, key, seconds, cost_usd: 目錄價, status: "reserved" }`，`key` 是這個請求的快取 key；job 回來（ready、failed、`video_media_model_changed`）`bookJob` 以同一個 key 找到這筆，換成伺服器實際記的 `usd_estimate`，不多一列。伺服器拒收（有 HTTP 狀態：額度用完、同一請求失敗三次、參考圖缺）就 `release` 掉——沒有 job 就沒有錢；連不上（`code: "network"`）不放，因為伺服器可能已經收了請求，下次跑同一個 key 會把同一筆換掉（`reserve` 同 key 只留一筆）再對帳。程序在送出與對帳之間死掉或被 `STOP` 停下，帳本留著這筆 `reserved`、`media/jobs.json` 留著 job id：`media-status --slug` 的「this video」把它算進去（`--json` 的 `totals.reserved`／`reservations` 另列），`episode_estimate.mjs --workdir` 逐筆列出；再跑那個階段會接回 job 對帳。

- `totals.usd` 是這支影片已承諾的錢（伺服器記的 ＋ 還在預留的）；`capProblem` 比的就是它加上這一次，所以進行中與死掉留下的預留都擋得到，訊息會寫出其中多少是預留。`totals.reserved`／`reservations` 是其中預留的部分；舊帳本沒有 `reserved` 列，讀起來就是 0，其他欄位照舊。
- judge：`Stage.judge` 先 `spend(JUDGE_USD_PER_CALL)` 過上限才問，回來才記；一次 US$0.01 不另外預留，程序在問到一半死掉最多少記一筆。
- `clips import --usd N`（N > 0）：先讀 `status` 拿上限、過 `spend`，以 `import:<shot>:<sha256>` 為 key 預留，`--judge` 的那一次 judge 看得到這筆；`bookImport` 用匯入列取代預留，沒記成就放掉。沒有 `--force` 可以越過上限。
- 估價：`node .agents/skills/animation-production/scripts/episode_estimate.mjs <video.json> --workdir <VIDEO_WORKDIR>/<slug>`（或 `--ledger <檔>`）印「已花、預留、上限還剩」，裁定比的是最壞情況對剩餘；`--json` 多 `ledger` 與 `verdict.remaining_usd`。沒給就當還沒花錢。
- 不管的：伺服器的月額度照舊由 `meter.py` 預留與退回，這裡只是單支的視角；`run_report.mjs` 把留下來的 `reserved` 當花費列出（它讀 `cost_usd`），對帳後自然消失。

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
