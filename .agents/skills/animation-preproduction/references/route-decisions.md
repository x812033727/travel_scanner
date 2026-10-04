# 每鏡走哪條路、買幾秒、正文怎麼寫：伺服器、Hailuo、Kling

開拍鎖定包裡每一鏡的「路線、模型、解析度、買幾秒、首尾格、定稿正文」照這篇定。數字分四種標：**官方**（官方頁、官方指南或官方 UI 字串，附讀取日）、**實測**（站主帳號上真的扣過、量過）、**推算**、**編輯判斷**。2026-10-04 的官方規格是研究代理逐頁讀的（MiniMax 平台文件、hailuoai.video、Hugging Face 上的 MiniMax-H3 官方提示指南、kling.ai quickstart 與 API 文件）；價目會變，送出前以生成頁「創建／Generate」旁顯示的點數為準。伺服器路線的價與規則在 `.agents/skills/animation-production/references/cost-model.md`，這裡只放比較需要的。

## 1. 能力表

| 路線與模型 | 一支幾秒 | 解析度與實際輸出 | 首格／末格 | 參考與身份 | 音訊 | 價 | 依據 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 伺服器 Veo 3.1 Lite | 1080p 固定 8 | 1920×1080 | 首格（關鍵影格）＋選用末格 | 不送參考圖 | 不要 | US$0.08/s | 工具規定（`clipSeconds`、catalog） |
| 伺服器 Gemini Omni 1.1 Flash | 4–10 | 1080p | 首格 | ≤ 4 張參考 | 不要 | US$0.15/s | 工具規定 |
| Hailuo 網頁 H3 | 4–15 整數 | 2K＝2560×1440、768P＝1344×768；24 fps；帶立體聲 | 首格、末格、首尾格 | 有首格時**不能**再帶參考圖（API 的 v2 規則：圖生影片與參考生影片互斥） | 一定有（沒有關的開關），產線丟掉 | 2K 12 點／秒（實測 5 秒扣 60）、768P 7 點／秒（官方：UI 的 Video 12 Credits/s 與方案頁的每月秒數） | 實測 2026-10-04；官方 2026-10-04 |
| Hailuo 網頁 H3 Max | 5–15 | 480P／768P | 首尾格 | 參考影片只有 H3 能用 | 有 | 768P 7、480P 4 點／秒（官方換算） | 官方 2026-10-04 |
| Hailuo 網頁 2.3 | 6 或 10（1080p 只有 6） | 1080p（API 回 1920×1080）／768p | **只有首格**（首尾格是 Hailuo 2.0／02） | — | 無 | 768p 6 秒 25 點、10 秒 50 點；1080p 6 秒 80 點；**Max 方案點數用完後在 relax 佇列無限** | 官方訂閱頁 FAQ 與 tooltip 2026-10-04 |
| Kling 網頁 VIDEO 3.0 | 3–15 整數 | 720p、1080p、4K | 首格、首尾格（不能只有末格） | 首格＋綁最多 3 個元素（主體一致性；元素 2–4 張圖、建立免費） | 原生音訊可關 | 不開音訊 1080p 8、720p 6 點／秒；開音訊 12／9；4K 30 | 官方 user guide 2026-10-04；**還沒在站主帳號實扣** |
| Kling 網頁 VIDEO 3.0 Omni | 3–15 | 720p、1080p、4K | 首尾格 | 最多 7 張圖或元素（帶影片時 4），正文用 `@Image1`、`@元素名` | 帶參考影片時不支援音訊 | 同 3.0；帶影片 16／12 | 官方 2026-10-04 |
| Kling 3.0 Turbo | 3–15 | 720p、1080p | 只有首格 | 不能綁元素 | 官方只列有音訊的價 | 網頁點數沒公布 | 官方 2026-10-04 |

兩家的圖生影片比例都**跟著首格走**（Hailuo API 的 adaptive、Kling UI 字串）：關鍵影格本身就要是 16:9。Hailuo 的設定面板預設 21:9（實測），文生影片才吃它，但送出前照樣檢查。

官方另說：Kling 的 CLI／MCP 用的是同一套會員點數（Kling 網頁 UI 的 MCP/CLI FAQ 字串）；Kling 失敗的生成退點，但「批次生成」標不退；Hailuo 失敗或審核沒過自動退點。Kling 4.0（3–30 秒、10 張關鍵影格）官方說 10 月正式上線，價目頁還沒有，出了再重估。

## 2. 每鏡怎麼選

照順序問，第一個「是」就停：

1. **這集有 `series.production.profile` 嗎？** 有就只能走伺服器（`clips import` 以 3 拒收外部片段），下面網頁的選項都不適用。
2. **這一鏡需要模型做動作嗎？** 沒有接觸、沒有身體位移的停留、建立鏡、反應：`visual: "still"`＋運鏡，只花一張圖（profile 不准）。
3. **它回到同一場更早的鏡位、而那支素材裡有這一刻嗎？** `data.source` 切素材，不買。要切兩三次的鏡位，把來源當**母鏡頭**買長一點（第 5 節）。
4. **沒有台詞的動作拍？** 場景層 `action_seconds`，照 clip 或 still 走。
5. **剩下的才買素材**。路線照下表的編輯判斷，最後以三鏡小樣的結果改：

| 情況 | 先選 | 理由 |
| --- | --- | --- |
| 一般對話、反應、單人動作（風險 A／B） | Kling 3.0 1080p、音訊關 | 原生 1080p、最短 3 秒、每秒 8 點；方案月費攤下來是網頁路線裡最便宜的原生 1080p（官方價，未實扣） |
| 動作重、物理多、站主要的「大場面」（風險 C 但非做不可） | Hailuo H3 2K 與 Kling 3.0 各試一支（小樣裡） | 誰比較穩沒有量過；先讓兩家做同一鏡，比完再定這類鏡頭的路線 |
| 不急的 A 級鏡頭，站主是 Max 方案 | Hailuo 2.3 1080p 6 秒 | 點數用完後在 relax 佇列無限；只有 6 秒、沒有末格，排多久沒量 |
| 有 production profile、或要從一支切多次而來源在 8 秒內 | 伺服器 Lite 1080p | profile 只收它；永遠買 8 秒 |
| 要首尾格定住結果（變身、開門、物件狀態變） | Kling 3.0 或 Hailuo H3 | 兩家都有首尾格；Hailuo 2.3 沒有 |

品質誰好**沒有量過**：上表的「先選」是價錢與規格的判斷。小樣（`preproduction-flow.md` P7）要讓同一鏡在選定的路線上做出來，必要時兩家各一支，結果寫回這張表。

## 3. 買幾秒

- 需要的秒數＝這一鏡在時間軸上的長度。**先錄配音再定**：lint 的估法跟合成的實際長度差得出來（一支說書口吻的影片實際長 7%，另一批偏短；`.agents/skills/youtube-video/references/automated.md`、`tools/video/qa/pace.mjs`），台詞改了就重量。`shot_plan.mjs` 讀錄好的 `timeline.json`，沒有就用 lint 的估法並標出來。
- 圖生影片**沒有頭的把手**：第 0 格必須是關鍵影格（`assemble` 對它算 PSNR ≥ 22），剪點只能往後移不能往前。尾巴留 0.5 秒（編輯判斷，`--handle`）：模型常在最後幾格才收勢，剪點落在收勢之後。
- 網頁路線買 `ceil(需要＋把手)`，夾在模型的範圍內：H3 4–15、Kling 3.0 3–15；Hailuo 2.3 只有 6／10。伺服器由 `clipSeconds` 決定，旗標改不了。
- 一個 3 秒鏡頭的價（月費攤：Kling Pro 37 美元／3,000 點、Hailuo Pro 54.99 美元／4,500 點；推算）：

| 路線 | 買 | 點數或價 | 約合 US$ |
| --- | --- | --- | --- |
| 伺服器 Lite 1080p | 8 s | US$0.64 | 0.64 |
| 伺服器 Omni | 4 s | US$0.60 | 0.60 |
| Kling 3.0 1080p、音訊關 | 4 s（3＋0.5 把手） | 32 點 | 0.39 |
| Hailuo H3 2K | 4 s | 48 點 | 0.59 |
| Hailuo H3 768P | 4 s | 28 點 | 0.34（要放大到 1080p，畫質沒驗） |
| Hailuo 2.3 1080p | 6 s | 80 點 | 0.98；Max 方案點數用完後 0 |

`shot_plan.mjs --route <r>` 對整集算一次、期望（乘預期 take）與上限各一個數，換路線重跑就能比。

## 4. 交片 1920×1080：解析度

`assemble` 把外部片段等比縮進 1920×1080 再補邊、轉 30 fps、丟音軌（`tools/video/assemble/drama.mjs`）。所以：

- Kling 1080p 是原生；Hailuo H3 2K（2560×1440）縮小，乾淨；H3 768P（1344×768）與 Kling 720p 要放大，畫質沒驗；比例不是 16:9 的片段會有黑邊。
- `clips import` 的下限是 1280×720、23 fps（`tools/video/media/qc.mjs`），Kling 720p 剛好過。
- 有 production profile 的作品要原生 1920×1080（`productionClipSizeProblem`），Hailuo 2K 也不收——而且 profile 作品根本匯入不了。

## 5. 母鏡頭＋切素材

一個鏡位拍一支長的，後面回到這個鏡位的鏡頭用 `data.source: { shot, from_s }` 切，不畫圖、不買素材、不 judge。網頁可以自己選秒數，這招在網頁上比伺服器好用：

- 母鏡頭要買到 `max(每個切鏡的 from_s＋鏡長)＋把手`；`shot_plan.mjs` 自動把它加上去，超過路線上限就報。
- 切出來的鏡第 0 格要對來源那一秒（`assemble` 算 PSNR），所以母鏡頭的那幾秒裡**要真的有**這一鏡要的表情或動作。母鏡頭的 `motion` 寫成「同一個主動作，前段與後段的狀態」，不要塞第二件事（一支一件事的規則不變）。
- 適合：說—聽—說回到同一個說話者、同一個反應鏡位拿兩次。不適合：每次回來表情都要不同、或鏡位已經換了光。
- 一支素材裡模型自己切了鏡，QC 會退（`qc.mjs` 在 0.1 秒後有切點就退）：Kling 的 Multi-Shot、H3 正文裡的 `[Shot 2]` 都不能用。
- 省多少：三次 3 秒的台詞，Kling 分三支是 3 × 4 秒 ＝ 96 點，一支 10 秒母鏡頭是 80 點，還少畫兩張關鍵影格、少兩次 judge；真正省的是**少兩個要抽卡的鏡頭**。這是編輯判斷，還沒實拍驗證（`shot_plan.mjs` 的槓桿會列出可切的鏡頭）。

## 6. 正文怎麼寫

共同的：

- **寫動作，不重講畫面**。首格已經決定了誰在哪、穿什麼；正文寫誰＋動詞＋對象＋幅度＋結束狀態，一件事（Runway 與 Kling 的官方圖生影片建議都這麼說；`animation-camera` 的「寫 motion」）。
- **正面寫**：否定句會被畫成正向（試拍把 already closed 畫成開著的門）。`look.negative` 只放進網頁真的有的負面欄。
- **同樣的東西用同樣的字**，每鏡照抄（Kling 官方工作流程文章的「固定字典」）。
- 名字對影片模型沒有意義：同框兩人時寫畫面位置或外觀（the woman on screen left）。
- 網頁的「AI 潤飾／AI Polish／Auto Refine」（Hailuo）與「AI Prompter」（Kling；關掉時嚴格照你的字）：**鎖定包裡寫明開或關，收據記下來**。開著時實際送出的不是你鎖的字。哪個比較好沒驗，小樣決定。

### Hailuo H3（官方圖生影片格式）

MiniMax-H3 官方提示指南（`huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`，2026-10-04 讀）的圖生影片版是固定第一行、空一行、三個欄位；運鏡寫成「種類＋幅度＋速度」的句子，不堆標籤；單鏡就只寫 `[Shot 1]`：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] <motion>. The camera pushes in with small amplitude at slow speed. <look.motion>. Keep the supplied first frame's composition, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.
overall_soundscape: N/A
non_diegetic_music: N/A
```

`shot_plan.mjs --route hailuo` 照這個格式產生。官方的運鏡種類：Zoom In／Out、Push In／Pull Out、Pan、Truck、Tilt、Pedestal、Arc Shot、Tracking Shot、Static Shot、Shake、POV、Roll；幅度 `with small／large amplitude`，速度 `at slow／fast speed`。H3 的台詞與畫外音另有格式（`<d>…</d>`、`says in an off-screen voiceover … lips remain completely closed`），產線的配音另外合成，所以正文不寫台詞。

### Hailuo 2.3（方括號指令）

官方的方括號指令只寫給 2.3／2.3-Fast／02／Director（MiniMax 平台 i2v 文件、hailuoai.video 運鏡小抄，2026-10-04 讀）：`[Push in] [Pull out] [Zoom in] [Zoom out] [Pan left] [Pan right] [Tilt up] [Tilt down] [Truck left] [Truck right] [Pedestal up] [Pedestal down] [Tracking shot] [Shake] [Static shot]`。同一個括號逗號隔開＝同時（建議最多 3 個），分開的括號＝依序；括號放在動作發生的那句；`[Static shot]` 再補一句 the camera stays completely still；一支 6 秒一個運鏡最穩。`--hailuo-model 2.3` 用這個寫法。

### Kling 3.0

官方圖生影片的公式是「主體＋動作，再加背景＋動作」，用簡單的字、動作合乎物理，正文離首格太遠會讓模型切鏡（kling.ai quickstart 的 image-to-video guide）。Multi-Shot 關著時預設產生單鏡（3.0 user guide）。`shot_plan.mjs --route kling` 寫成：

```text
Single continuous shot, the camera slowly pushes in. <motion>. <look.motion>. Keep the supplied first frame's composition, character identities, costumes and props; one continuous shot with no cuts and no on-screen text.
```

送出前：Multi-Shot 關、原生音訊關、輸出數 1（UI 有「Number of Outputs」，2.6 指南寫一次最多 4 支；點數是不是照支數乘官方沒寫，送出前看 Generate 旁的點數）、1080p、AI Prompter 照鎖定包。身份要穩就把首格裡的角色做成元素綁上（最多 3 個，建立免費）。

### 運鏡字對照

我們的 `camera` 用攝影機的字（`animation-camera`）：`pan left` 是攝影機往左搖、畫面往右跑；Hailuo 的 Pan left 與 Kling 的 pans left 也是攝影機的方向。

| `camera` 寫 | 三個讀者讀成（group） | H3 句子 | Hailuo 2.3 | Kling 3.0 |
| --- | --- | --- | --- | --- |
| `locked`、`static` | locked | The camera is a static shot and stays completely still | `[Static shot]`＋stays completely still | locked-off camera, no camera movement |
| `slow push in` | push in | The camera pushes in with small amplitude at slow speed | `[Push in]` | the camera slowly pushes in |
| `pull out` | pull out | The camera pulls out | `[Pull out]` | the camera pulls back |
| `pan left`／`pan right` | pan left／pan right | The camera pans left／right | `[Pan left]`／`[Pan right]` | the camera pans left／right |
| `tilt up`／`tilt down` | tilt up／tilt down | The camera tilts up／down | `[Tilt up]`／`[Tilt down]` | the camera tilts up／down |
| `tracking`、`follow` | track（craft 也讀成跟拍） | The camera is a tracking shot that follows the subject | `[Tracking shot]` | the camera tracks alongside the subject |
| `drift` | drift | The camera trucks right with small amplitude at slow speed | 自然語言 | the camera drifts very slightly |

## 7. 送出前的表單清單

| | Hailuo 網頁 | Kling 網頁 |
| --- | --- | --- |
| 帳號 | 站主登入、方案對、餘額 ≥ 這一批的期望＋預留 | 同 |
| 模式 | 圖生影片；上傳這一鏡核准的關鍵影格（首格），計畫有末格才放末格 | 同；Add End Frame 才是首尾格 |
| 模型、解析度、秒數 | 照鎖定包（H3 2K／768P；秒數 4–15） | VIDEO 3.0、1080p、秒數照鎖定包 |
| 比例 | 16:9（設定面板預設 21:9） | 跟首格走 |
| 單鏡 | 正文只有 `[Shot 1]` | Multi-Shot 關 |
| 音訊 | 關不掉，正文寫 N/A，產線丟掉 | 原生音訊關 |
| 份數 | — | 輸出數 1 |
| 潤飾 | AI Polish 照鎖定包 | AI Prompter 照鎖定包 |
| 正文 | 照貼鎖定包的定稿（sha256 對得上） | 同 |
| 送出 | 記「創建」旁的點數與送出前餘額；只按一次 | 同（Generate） |
| 下載 | 全部下載 → 無水印下載（結果卡的 `<video>` 是有浮水印的版本） | 會員的無浮水印下載 |

## 8. 還沒驗、不能宣稱的事

- Kling 的點數是官方價目，站主帳號上還沒實扣過一支；輸出數是不是照支數乘、網頁 3.0 有沒有負面欄、AI Prompter 預設、實際 fps 與輸出尺寸，都要第一支下載後量。
- Hailuo H3 768P 的實際輸出尺寸（官方自架指南是 1344×768）、網頁有沒有負面欄、AI Polish 預設開不開、H3 網頁的末格、2.3 relax 佇列要等多久。
- 兩家誰比較穩：一支都沒比過。用產線關鍵影格當首格的圖生影片在兩家都還沒送過。
- 母鏡頭切三次在網頁素材上可不可用、0.5 秒尾巴把手夠不夠：編輯判斷。
- Hailuo 的無浮水印下載有一段提示說「僅供個人學習與收藏」並要求發布時標示 AI 生成；條款（2026-08-19）也禁止移除 AI 標示或 metadata。產線重新編碼會不會去掉檔案裡的 AIGC metadata、要不要保留，是站主的決定；YouTube 上傳包已經標 `contains_synthetic_media`。
