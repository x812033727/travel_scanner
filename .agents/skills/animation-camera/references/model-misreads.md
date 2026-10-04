# 模型畫錯過的事：試拍證據、提示怎麼組、judge 拒絕什麼

證據全部來自一次試拍：《喜宴未散》E1 2026-10-02／03 的 10 張圖與 6 次片段提交（`docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`、`visual-revision-20261003.md`），模型是 `gemini-3-pro-image` 與 `veo-3.1-lite-generate-preview` 1080p 8 秒。一次試拍的證據寫成規則是為了下一次少犯同樣的錯，不是跨模型定律（`.agents/skills/youtube-video/references/visual-quality.md` 的「證據與分歧」）；每條規則後面標它驗過沒有。

## 一、逐 take 的證據與對策

| 鏡／take | 寫了什麼 | 畫出或動出什麼 | 誰抓到、花了多少 | 規則（驗證狀態） |
| --- | --- | --- | --- | --- |
| 設定圖 zhitang A | appearance 寫 `small silver rectangular watch` | 錶畫成圓的 | 人看圖退回；重畫一張 US$0.134 | 招牌道具寫形狀＋位置＋數量，而且三視圖要求裡再寫一次；第二張用 `retake_of` 寫明原因才過（一次成功） |
| S01 首格 R01 | prompt 寫 `already closed south main door`、`no locking operation` | 人物背後畫成開著的門與通道 | 人看圖退回；US$0.134 | 狀態寫成畫面裡看得到的東西（`a continuous steel door, its seam sealed`），少用否定句；圖片模型把「不要 X」當題目畫 X 的風險，一次證據 |
| S01 首格 R02 | 寫 `medium close-up` | 畫到腰、錶在跟設定圖 B 不同的手腕 | 人看圖「可接受」放行 | **採用格連戲帳**：首格一通過，就把真圖裡的腕側、袖長、髮長、道具數抄進後面每一鏡的 prompt；S04 R02 後來就是因為錶換了手被退回，而來源從沒寫過左右腕 |
| S03 首格 R01 | `look.style` 裡有 `dusty grey warehouse with reflected warm firelight` | 婚禮桌上出現火光與餘燼；筆的顏色也錯 | 人看圖退回；US$0.134 | 場景的光寫在那一鏡的 `prompt`，不寫進 `look.style`（look 是整部片共用的）；一次證據 |
| S03 首格 R02 | 要原件「未簽」 | 原件上出現簽名筆畫、紙上出現英文標籤 | 獨立 QC 退回；US$0.134 | 紙面寫 `blank`、`no writing on the page`；任何要看的字另外合成（`animation-production.md` 的 text 規則）；judge 的 `no_text` 題也會扣 |
| S03 首格 R03 | `complete unsigned original`、`silver pen clearly suspended`、`one rectangular watch` | 通過 | — | 把要被對照的狀態逐件寫成「有什麼」：這一張是後面每一鏡要連戲的來源 |
| S04 首格 R01 | 手部插鏡，`characters` 列了新娘 | 畫成上半身廣鏡、盤髮不像設定圖的及肩髮 | 人看圖退回；US$0.134 | 插鏡的 prompt 只寫手、袖口、錶、道具，不寫臉與髮；列了角色就會把整段 appearance 接進提示（`shotAppearancePrompt`）並要 judge 問 identity，一張沒有臉的圖答不了這題。要不要列角色，兩種都沒驗穩 |
| S04 首格 R02 | 景別改對 | 錶跑到翻頁的那隻手，與 S03 持筆手戴錶不連戲 | 人比對兩張圖退回；US$0.134 | 同上一條的連戲帳；沒有任何程式比對相鄰兩張圖的道具（`JudgeKind` 有 `continuity`，沒有工具呼叫它） |
| S01 片段 R01／R02 | 送了 `look.negative` | HTTP 400 `INVALID_ARGUMENT: negativePrompt is not supported`，app 只回 `Gemini refused the request` | 診斷 transport 才看到原因；兩次預留各 US$0.64 | 第三節 |
| S01 片段 R03 | `Her fingers tighten once around the pen.` | 0.5 秒起多一只圓錶，左臂抬起加入持筆 | root 與獨立 QA 看聯絡表退回；US$0.64 | 小反應寫**數量與結束狀態**：`one hand in frame, the other hand stays out of frame`、`the pen does not move`、`one watch on the right wrist`；一次證據 |
| S01 片段 R04 | 同上 | 可用，但 judge 6.72 失敗，問題「片頭眼睛張開的額外動作」；逐格看是第 0 格已睜眼，0.375–0.583 秒一次自然眨眼 | judge US$0.01；owner 待決後被 60 分回饋取代 | judge 把小動作讀成「沒要求的動作」。`motion` 可以寫 `eyes open throughout, one natural blink is fine`；沒驗這句會不會改變分數。分數不改、門檻不降（visual-quality.md） |
| S03 片段 R01 | `Her pen-holding hand trembles briefly and steadies without touching the paper.` | 多一隻手、第二支筆、第二只錶，矩形錶變圓 | root 看聯絡表退回；US$0.64 | 「微顫」是 `isLookOnly` 的反應鏡：片段模型會把它放大。反應停留改用 `visual: "still"`（0.134，畫面不動）；一定要動就寫幅度：`the pen tip moves less than a finger's width and returns` |
| S03 片段 R02 | 同上 | 0.75–1.75 秒筆從斜抬到水平再轉回 | root 與獨立 QA 退回；US$0.64 | 同上；兩次重拍上限（`MAX_CLIP_TAKES = 2`）用完，這一鏡 0 支可用，US$1.28 |
| E2 S34（只改文字） | 首格 prompt 寫信封「已在袋裡」，`motion` 寫「放進袋裡」 | 還沒花錢，讀稿時發現 | 0 | `prompt` 是動作開始**之前**那一格；程式不檢查這件事，`shot_reading` 也只能提醒看 |

兩集 81 行 `camera` 全部以 `Locked` 開頭、E1 前三鏡全是反應、整集沒有全景（量到的，`drama-craft.md` 第一張表）：這是站主「不會想繼續看」在分鏡上對得到的地方，鏡頭怎麼寫才是這份 skill 的主題，試拍退回的多半不是模型的錯。

## 二、片段提示怎麼組；`look.motion` 跟鎖定打架

`tools/video/media/clips.mjs` 的 `clipPrompt`（2026-10-03）：

```
[ data.motion, data.camera, look.motion, 有命名造型的角色外觀 ].join(". ").slice(0, 4000)
```

- 片段模型看到的順序是「動作、鏡頭、風格句、造型」；它看不到 `data.prompt`（那是給圖片模型的，片段模型拿到的是通過的關鍵影格當 `first_frame`）。
- 每個 preset 的 `look.motion`（`tools/video/core/drama.mjs` 的 `PRESETS`）都含一個運鏡：`cinematic-3d` 是 `slow cinematic camera move, subtle natural motion, …`，`anime-2d` 是 `gentle camera move, limited animation, …`，`ink-wash` 是 `slow drifting camera, …`，`flat-explainer` 與 `tech-story` 是 `slow push in or gentle drift, …`。寫 `camera: "Medium close-up, locked"` 的鏡頭，模型會收到「locked」接著「gentle camera move」兩個指令。試拍自己覆寫了 `look.motion`（`One clearly motivated character or prop action per clip, consistent adult identity, no morphing, …`）；沒有文件說要這樣做，這裡說：鎖定機位為主的作品，`look.motion` 寫一句沒有運鏡的話。
- `look.motion` 與 `look.negative` 都在 `lookHash` 裡（`resolveLook` 的結果整個進雜湊，2026-10-03 實測改 `negative` 雜湊就變）：改了就是設定圖、關鍵影格、片段全部過期、look 關卡失效。所以這兩個欄位在 `look` 跑之前定好。
- `motion` 與 `camera` 結尾的句點會跟 join 的 `". "` 疊成 `..`；關鍵影格提示的 `<prompt>. Style:` 也一樣。不以句點收尾。
- 片段永遠 `native_audio: false`；Lite 沒有這個開關、永遠產音軌，成片丟棄（profile 的 `native_clip_audio: discard`）。`motion` 不寫聲音。
- `data.negative` 是 lint 收的每鏡欄位，但 `look.mjs`、`keyframes.mjs`、`clips.mjs` 都只送 `look.negative`（2026-10-03 grep）：每鏡想少畫什麼，寫成 prompt 裡「有什麼」。

關鍵影格提示（`tools/video/media/keyframes.mjs` 的 `shotPrompt`）：`<prompt>. Style: <look.style>. Camera: <camera>. Characters: <name>: <appearance>; …`，切到 4000 字；`look.negative` 另送，Gemini 圖片 adapter 接在提示後面成 `\n\nAvoid: <negative>`，有參考圖再加一句 `Keep every character exactly as in the reference images.`（`apps/api/app/video_media/providers/gemini_images.py`）；MiniMax 接成 `. Avoid: …`（`apps/api/app/video_media/providers/minimax.py`）。圖片請求不帶 seed（兩個 adapter 都沒送；`keyframes` 的「換 seed」只改快取鍵）；參考圖最多 4 張（`apps/api/app/video_media/schemas.py` 的 `MAX_REFERENCES`，catalog 寫的 14 張是供應商的上限，工具用不到）。景別在提示裡出現兩次（prompt 開頭與 `Camera:` 子句），兩處要同一家族。

## 三、Veo Lite 的 negativePrompt：歷史失敗與已完成的相容修正

第一節 S01 R01／R02 是修正前的真實結果：送出不支援的 `parameters.negativePrompt`，兩個 seed 都在 HTTP 400 停下，兩次各預留 US$0.64。原逐 take 表與試拍收據保留，不把後來修正寫成當時成功。

此程式版本的 `apps/api/app/video_media/providers/gemini_video.py` 對 `veo-3.1-lite-generate-preview` 省略該參數，把完整 negative 文字接成 `\n\nAvoid: …` 放進主提示；其他 Gemini 影片模型保留原 `parameters.negativePrompt`。修正與離線 request-body 證據在 `tasks/done/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md`。MiniMax 仍以自己的 adapter 把 negative 接進提示。實際後端須核對部署版本；本機 preflight 通過不證明正式服務已更新。

因此不必清空 `look.negative`，也不必為 Lite 更改已核准的 look：negative 仍進入 `lookHash`，更改會使設定圖、關鍵影格、片段與核准過期。保留既有預算、重拍上限與 owner 關卡；離線相容測試不代表新付費片段或視覺驗收已完成。

## 四、judge 怎麼讀、拒絕什麼

通過條件（`apps/api/app/video_media/judge.py`）：加權總分 ≥ `judge_min_score`（後台設定，預設 7）且每一題 ≥ `MIN_CRITERION = 4.0`；temperature 0；每次記 US$0.01（`JUDGE_USD_PER_CALL`）。題目每題 ≤ 400 字（`schemas.py` 的 `JudgeCriterion`）。歷史試拍的 zhitang 基底造型 422 字曾被驗證擋在 clip judge 之前；目前 clip 識別題已改成有界文字、參考圖標籤 ≤ 80 字，完整姓名與 appearance 保留在 context（`tasks/done/2026-10-02-keep-named-look-clip-judge-questions.md`）。keyframe 識別題仍直接帶 appearance，preflight 對本次要畫的鏡頭保留 400 字檢查。judge 的 context 另含 `shot.prompt`／`camera`／`motion` 原文與 `look.style`。

| judge | 題（key、權重） | 什麼時候出現 | 鏡頭寫法的含意 |
| --- | --- | --- | --- |
| keyframe（`keyframes.mjs` 的 `keyframeRubric`） | 每個列出的角色 `identity_<id>`（2）；`prompt`（2）：主體、場景、動作、構圖是否如 prompt；`style`（1）；`clean`（2）：手指、臉、漂浮或重複的部位、背景；`no_text`（1）；`subtitle_band`（1）只在 `subtitles.burn_in: true` 時問；`craft`（1）只給插畫投影片 | 每張關鍵影格；end_frame 不 judge（`keyframes --dry-run` 把它多算一次） | 景別寫錯會落在 `prompt` 題裡，權重 2 但只是其中一個子句；沒有臉的插鏡列了角色就答不了 identity；紙上任何字扣 `no_text` |
| clip（`clips.mjs` 的 `clipRubric`） | 每個角色 `identity_<id>`（2，問最後一格或整段）；`motion`（2）：自然連續、不變形、不閃；`prompt`（1）：有沒有做出要求的 motion 與 camera move；`clean`（2）：手臉身體正確、沒有東西出現或消失；`no_text`（1） | 每支片段，先過 ffmpeg（解析度、fps、時長、黑格、旁白範圍內凍格 ≥ 1 秒、模型自己切鏡、第 0 格 PSNR ≥ 22 且比相鄰關鍵影格高 3 dB；`tools/video/media/qc.mjs` 的 `THRESHOLDS`） | 「多出一隻手」落在 `clean`；眨眼落在 `motion` 或 `prompt`；運鏡字模型不理也只扣權重 1 的那題 |

judge 不看的：軸線與視線、相鄰鏡頭的道具連戲、景別是不是寫的那一種（S04 R01 是人抓到的）、動作幅度對不對。這些是人的事，寫在每場戲的回報裡。

## 五、Hailuo 與 Kling 的鏡頭字彙：知道什麼、從哪裡知道

| 路線 | 已知（來源、日期） | 未驗 |
| --- | --- | --- |
| MiniMax API（H3、H3 Max） | 官方影片生成文件（platform.minimax.io，2026-10-03 讀）：鏡頭指令用方括號接在描述後面，列出的字是 `[pan]`、`[zoom]`、`[static]`；首尾格用 `role: "first_frame"`／`"last_frame"`，0–2 張；prompt ≤ 7000 字。2026-10-04 再讀（官方）：H3 只在 v2 端點，**有首格時不能帶參考圖**；Hugging Face 上 MiniMax-H3 的官方提示指南要運鏡寫成「種類＋幅度＋速度」的句子（The camera pushes in with small amplitude at slow speed），圖生影片用固定第一行加三個欄位（格式在 `animation-preproduction/references/route-decisions.md` 第六節）；帶方向的十五個方括號指令（`[Pan left]`、`[Truck right]`…）官方只寫給 Hailuo 2.3／02／Director。產線的 adapter 不加這些字，送的是 `clipPrompt` 原文加 `. Avoid:`；它送的是 v1 欄位、同時帶首格與 subject_reference，跟官方 v2 規則不合（另有票） | H3 照不照方括號；H3 對原文 `locked` 的反應 |
| Hailuo 網頁 | 同一批模型（H3 4–15 秒 768p／2K；Hailuo 2.3 6 秒，768p 另有 10 秒，1080p 只有 6 秒），image-to-video 頁有首格與參考上傳；H3 2K 下載的 mp4 是 2560×1440、24 fps、帶 AAC 音軌（實測 2026-10-04，一支文生影片）；價目與方案在 `animation-production` 的 references | 網頁的 prompt 上限；768P 的實際輸出尺寸（官方自架指南的畫布是 1344×768）；AI Polish 開或關的差別；H3 照不照方括號（官方只寫給 2.3） |
| Veo 3.1 / Lite（產線） | 官方 Veo 文件（ai.google.dev，2026-10-03 讀）建議的字：`aerial view, eye-level, top-down shot, dolly shot, worms eye`、`wide shot, close-up, single-shot or two-shot`；頁面沒有列 `negativePrompt`；Lite 有首尾格、沒有延長 | 文件摘要說 Lite 有參考圖，但 adapter 對 Lite 的 referenceImages 回 422、catalog 寫 0 張：產線照程式走，哪邊對沒驗；`locked`、`pan left` 這些原文 Lite 怎麼理解沒驗 |
| Kling 社群 MCP（github.com/199-mcp/mcp-kling） | README（2026-10-03 讀）：`generate_image_to_video` 的 camera movement 是 `Static, zoom, pan, or auto`，motion prompt 可自動或自訂；`generate_video` 的 camera control 是 `type: "simple"` 加 `{ zoom: 5 }` 這類設定，只有 V1 模型；用 access key 與 secret key 簽 JWT（走開發者 API 的資源包，不是會員 credits） | pan 的方向、zoom 的正負怎麼給；`negative_prompt` 的上限；哪些模型版本吃 camera control |
| Kling 官方 API、官方 MCP 與 CLI | 官方 API 文件頁是 SPA，2026-10-03 抓到的是空殼。官方 MCP 與 CLI 的指南（kling.ai/app/mcp/guide）登入後讀得到（實測 2026-10-04）：CLI 的 `who_am_i` 列 `image_to_video` 的模型與參數，`kling-video-v3_0` 是 3–15 秒整數、`first_image`＋`tail_image`，`enable_audio` 與 `prefer_multi_shots` 預設 true（進產線都傳 false）；整份在 `.agents/skills/animation-production/references/providers-and-plans.md` §1.3 | 2026-10-04 從官方 API 文件讀到（官方）：舊的 image2video 端點的 `camera_control` 是預設型別或六軸（horizontal／vertical／pan／tilt／roll／zoom，-10 到 10、一次一軸），不能跟末格一起用；3.0 的官方建議是把運鏡寫進正文。官方 MCP／CLI 常見問題說跟網頁同一套積分。授權進來的帳號 NORMAL、0 credits，一支都沒生成；網頁 3.0 有沒有鏡頭控制 UI 未驗 |

三條路線共同的事：關鍵影格仍由產線畫（景別、構圖、軸線在圖裡已經定了）；`camera` 這一行照產線的讀者寫，再把運鏡翻成那家的字；外面做好的 mp4 用 `clips import` 回到產線（`.agents/skills/animation-production/references/stage-preconditions.md` 最後一節）。
