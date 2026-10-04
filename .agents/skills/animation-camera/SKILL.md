---
name: animation-camera
description: 寫 AI 漫劇分鏡時怎麼把一場戲放進攝影機：軸線與視線、鏡位、camera／prompt／motion 的程式與模型讀法、運鏡字與 pan 方向、靜圖／片段／切素材的選法，以及同鏡的 Hailuo／Kling 網頁改寫。使用者指定「布袋喵參考風格」或真一隻布袋喵頻道時，讀可選的畫風、表演與鏡頭手冊。寫有角色的漫劇鏡頭、改被 judge 或站主退回的鏡頭、首格不像關鍵影格、或花錢前要確認鏡頭讀法時，先讀此 skill，寫完跑 shot_reading。Write, read and translate AI drama camera lines and an optional Budaimiao reference style for Hailuo or Kling browser production.
metadata:
  short-description: 動畫視角：一場戲怎麼寫進 camera、prompt、motion
---

# 動畫視角（animation-camera）

一場戲怎麼被攝影機看見，寫成 `video.json` 的 `camera`、`prompt`、`motion` 之後，三個程式讀者、兩個生成模型和 judge 各讀出什麼。三個程式讀者是：**craft**（`tools/video/core/craft.mjs`，`drama_craft_check.mjs` 與 lint 的 `craft …` 警告用它量景別、運鏡與動作比例）、**slides**（`tools/video/core/drama.mjs` 的 `cameraMove`，插畫投影片的變化規則；漫劇不跑它，但字表跟 assemble 逐字相同，下面合併寫）、**assemble**（`tools/video/assemble/drama.mjs` 的 `motionMove`，決定 `visual: "still"` 的靜圖實際怎麼動、第 0 格要不要驗 PSNR）。這裡只管「鏡頭怎麼寫」：手藝規格（開場、鏡位與剪點、鏡頭與台詞長度）在 `drama-craft.md`，階段順序、每一關的前提與錢在 `.agents/skills/animation-production/SKILL.md`，兩邊都不重複。數字分五種標：**量到的**、**編輯判斷**、**工具規定**（程式常數，附檔名）、**模型限制**、**價目**（附來源與查閱日）。工人不讀 skill：工人要守的都在 `tools/video`，這份是給親手寫、親手導、親手跑的代理。

下文的 `drama.md`、`drama-craft.md`、`visual-quality.md`、`animation-production.md`、`story.md`、`visuals.md` 都在 `.agents/skills/youtube-video/references/`；`DRAMA.md`（大寫）是 `docs/videos/DRAMA.md` 的設計文件，與程式不一致時以程式為準。

## 什麼時候用、什麼時候不用

- 用：寫或改任何有角色的漫劇分鏡（每一個 `template` 是 `shot` 的場景）；鏡頭被 judge、`assemble` 或站主退回要改；把同一鏡拿到 Hailuo／Kling 網頁或另外選定的 CLI／MCP 做；使用者指定「布袋喵參考風格」；花錢前要知道一場戲會被程式讀成什麼、要花多少。
- 不用：沒有角色的解說與品牌故事、插畫投影片（它們的畫面規則在 `story.md` 與 `visuals.md`，景別字表不同）；改 `look`、角色外觀、聲音（`drama.md`）；判斷畫面好不好看（`visual-quality.md`）；手藝規格沒過要改結構（`drama-craft.md`）。

## 先讀

| 寫第一場戲之前 | 讀 |
| --- | --- |
| 一場戲的鏡位、剪點、長度目標；檢查腳本 | `drama-craft.md` 第一到五節 |
| `video.json` 鏡頭欄位的定義、still 的運鏡表、`source`、`action_seconds` | `drama.md` 的「video.json 的重點」 |

| 遇到 | 再讀 |
| --- | --- |
| 寫 `camera`，想知道某個字三個讀者各讀成什麼 | `.agents/skills/animation-camera/references/camera-keywords.md`（正則逐字表、分家的字、35 行例子） |
| 寫一場戲：軸線、視線、進出、連戲帳；一場 12 鏡的戲寫兩次（可接受版附腳本輸出、craft 列與估價；試拍式每鏡標錯） | `.agents/skills/animation-camera/references/scene-coverage.md` |
| 被 judge、`assemble` 或站主退回 | `.agents/skills/animation-camera/references/model-misreads.md`（逐 take 的證據、提示怎麼組、Lite 的歷史參數失敗與此版本相容處理、judge 的題、Hailuo 與 Kling 的字彙來源）與 `visual-quality.md`（診斷、小卡、冷看） |
| 付費之前把整集排好：分鏡表、鏡位、每鏡路線與買幾秒、風險分級、動態分鏡、開拍鎖定 | `.agents/skills/animation-preproduction/SKILL.md`（鏡位設計是它的 P3） |
| 要算錢、選路線、看每個付費階段的前提 | `.agents/skills/animation-production/SKILL.md`；這批動畫的 Lite 契約（8 秒、首尾格、無參考圖、CC）在 `animation-production.md` |
| 使用者指定「布袋喵參考風格」或真一隻布袋喵頻道 | [references/budaimiao-style.md](../../../.agents/skills/animation-camera/references/budaimiao-style.md)：三支原片抽樣、可選美術與導演規格、原創八鏡與同鏡的 Hailuo／Kling 網頁提示；只在點名時套用，其他作品保留原風格 |
| 要透過內建瀏覽器製作 Hailuo／Kling 片段 | [.agents/skills/animation-production/references/browser-production.md](../../../.agents/skills/animation-production/references/browser-production.md)：依本次工具能力上傳、選設定、記帳與下載；先檢查 production profile 的匯入限制 |

## 三個欄位各給誰讀

| 欄位（上限是工具規定，`tools/video/core/drama.mjs` 的 `LIMITS`） | 程式讀者 | 進哪個模型 | judge 看得到 |
| --- | --- | --- | --- |
| `camera` ≤ 120 字 | craft `shotSize`、`cameraMove`（`tools/video/core/craft.mjs`）；slides `cameraMove`（`tools/video/core/drama.mjs`）；assemble `motionMove`（`tools/video/assemble/drama.mjs`） | 關鍵影格提示的 `Camera:` 子句；片段提示的第二段 | 兩種 judge 的 `context.shot.camera` |
| `prompt` ≤ 1000 字 | craft 只在 `camera` 沒寫景別時讀明寫的景別；`sizesDisagree`；`setupKey` 讀第一個子句；lint 的 `promptSimilarity`（相鄰 ≥ 0.8 警告） | 關鍵影格提示的開頭；**片段模型看不到它**（片段拿的是通過的關鍵影格） | keyframe 與 clip judge 的 `context.shot.prompt` |
| `motion` ≤ 300 字 | craft `isLookOnly`（第一個子句）、`motion.double`（info） | 片段提示的第一段；圖片模型看不到 | clip judge 的 `context.shot.motion` |
| `characters` ≤ 3 個 id | craft `size.stall`、`size.listeners` | 決定參考圖與接進提示的外觀標籤 | 每人一題 `identity_<id>`（權重 2） |

提示的組法（2026-10-03 逐字讀程式）：

- 關鍵影格（`tools/video/media/keyframes.mjs` 的 `shotPrompt`）：`<prompt>. Style: <look.style>. Camera: <camera>. Characters: <name>: <appearance>; …`，切到 4000 字。`look.negative` 另送，Gemini 圖片 adapter 接在後面成 `Avoid: …` 段。參考圖最多 4 張（`apps/api/app/video_media/schemas.py` 的 `MAX_REFERENCES`；catalog 寫的 14 張用不到）。圖片不帶 seed，「換 seed」只是換快取鍵。`end_frame` 同樣組法，畫了不 judge。
- 片段（`tools/video/media/clips.mjs` 的 `clipPrompt`）：`<motion>. <camera>. <look.motion>. <命名造型的外觀>`，切到 4000；`negative_prompt` 是 `look.negative`；Gemini adapter 對 Lite 省略不支援的 `parameters.negativePrompt`，把完整限制接成 `Avoid: …` 放進主提示，非 Lite 保留原參數；`first_frame` 是通過的關鍵影格；`native_audio` 永遠 false；Veo Lite 不帶參考圖。
- `data.negative` 每鏡欄位 lint 收，但 look、keyframes、clips 都只送 `look.negative`（2026-10-03 grep）：每鏡想少畫什麼，寫成 prompt 裡「有什麼」。
- `motion`、`camera`、`prompt` 不以句點收尾：組合時會疊成 `..`。
- judge 的 context 另帶每個角色的完整姓名、`appearance` 與 `look.style`；每一題 ≤ 400 字（`apps/api/app/video_media/schemas.py` 的 `JudgeCriterion`）。clip 的命名造型／長姓名識別題已使用有界文字，參考圖標籤 ≤ 80 字，完整姓名與造型留在 context（`tasks/done/2026-10-02-keep-named-look-clip-judge-questions.md`）；keyframe 題仍直接帶 appearance，須以 preflight 檢查實際題長，不能沿用 clip 的結論。

## 一場戲先定空間

全是人的事，沒有任何程式或 judge 檢查（`JudgeKind` 有 `continuity`，沒有工具呼叫它）。一句話：兩人之間畫一條軸線、攝影機整場留同一側、畫面側與視線寫進每一鏡的 `prompt`、進出同側、移動與新節拍之後給約兩秒的全景重新交代（編輯判斷）。八條規則、過肩與進場的寫法、採用格連戲帳的樣子都在 `scene-coverage.md` 第一節；五種鏡位的用途在 `drama-craft.md` 第二節。五種鏡位各自怎麼落到三個欄位：

| 鏡位 | `camera` 的寫法 | `prompt` 第一個子句 | `characters` | `motion` 的性質 |
| --- | --- | --- | --- | --- |
| 全景或多人鏡 | `Wide shot, locked`、`Two-shot, locked` | 空間：櫃檯怎麼橫過畫面、誰在左誰在右、門在哪 | 畫面裡的每個人 | 一個看得到的動作，交代誰在做什麼 |
| 說話者的中近景 | `Medium close-up, locked`（或 `slow push in`） | `Medium close-up of Chen behind the counter on screen right` | 他一個 | 對人或對物的動作；純說話也要有手上的事 |
| 聽者反應 | `Close-up, slow push in` | 臉在哪一側、眼睛看畫外哪一邊 | 聽的人 | 眼神、下顎、呼吸（look-only，占比有上限） |
| 過肩 | `Over-the-shoulder from behind Ayu on Chen, locked` | 肩在畫框哪邊、對面是誰、桌上有什麼在兩人之間 | 兩個人（近側的 identity 題見「寫 prompt」） | 對峙、遞交、推回 |
| 插鏡 | `Insert of the note on the scale pan, locked`、`Overhead insert of the hands, locked` | 東西在哪、哪隻手、袖口與腕上的東西；`Chen speaks off screen` | 見「寫 prompt」的插鏡條 | 東西的動作：盤子下沉、硬幣倒出 |

## 寫 camera

順序固定：**景別 → 角度或高度 → 一種運鏡，或 `locked`**。craft 只在去掉修飾詞後的行首找景別（`LEADING_SIZE`），運鏡則整行找，所以景別放前、運鏡放後兩邊都讀得到；角度放中間是因為沒有讀者讀它，只有圖片模型看。例：`Medium close-up, low angle, slow push in`、`Overhead insert of the hands, locked`、`Wide shot, pan left`。

- 第一個詞是景別。craft 只跳過 `locked`、`static`、`fixed`、`handheld`、`slow`、`oblique`、`overhead`、`low-angle`、`high-angle`、`table-level` 這些修飾詞（`LEADING_QUALIFIER`）；整行沒有任何景別片語才算沒寫（`size.named`）：`view`、`over-table`、`table-height`、`framing` 都不是景別片語，試拍 E2 S09 的「Locked view through the door gap」就是這樣算進去的。接受的景別字與家族在 `camera-keywords.md` 第一節：`Medium close-up`、`Close-up`、`Extreme close-up`、`Over-the-shoulder` 是臉；`Wide`、`Two-shot`、`Group shot` 是全景；`Insert` 或拍東西的近景是插鏡；`Medium shot` 與 `POV` 讀得出來，但不屬於臉、全景、插鏡任何一個家族，craft 的 `size.face`／`size.wide`／`size.insert` 三列都不計它們。
- 角度與高度寫在景別之後：craft 不讀它們，圖片模型在 `Camera:` 子句讀得到；沒有任何讀者量它，連戲靠人。
  - `overhead`、`top-down`：桌面與手的插鏡；craft 把「overhead … close-up」算插鏡。
  - `low angle`：被逼近、被俯視的那個人看對方的角度；`high angle`：弱勢、被看著。
  - `table-level`：桌沿齊高的過肩或雙人鏡，桌上的東西在前景。
  - `from behind`、`in profile`、`silhouette`：只有插畫投影片的景別字表認（`tools/video/core/drama.mjs` 的 `SHOT_SIZE`），漫劇的讀者不讀，圖片模型讀得到。
- 一種運鏡。三個讀者都懂的只有八組字（工具規定）：`locked`（static、tripod、no camera move）、`push in`（dolly in、zoom in、closer）、`pull out`（pull back、zoom out、widen）、`pan left`、`pan right`、`tilt up`（crane up、rise）、`tilt down`（crane down、descend）、`drift`。靜圖的幅度與常數（放大 1.10 倍、1.08 倍滑窗、4% 漂移）在 `drama.md` 的運鏡表；三份正則與 PSNR 的規則在 `camera-keywords.md` 第二節。
- 運鏡的名字是觀眾看到畫面怎麼動，所以 pan 跟攝影機用語相反：`pan left` 是攝影機往左搖，畫面往右跑，assemble 叫它 `pan-right`（`tools/video/assemble/drama.mjs` 的 `MOVES` 註解與 `zoompanExpr`）。想要畫面往左跑，寫 `pan right` 或 `right to left`。tilt 保留攝影機的字。
- `locked` 的靜圖整格不動，而且跟 `push-in`、`drift` 一樣第 0 格要對關鍵影格算 PSNR ≥ 22（`IDENTITY_START`、`KEYFRAME_MIN_PSNR`）；`pull-out`、pan、tilt 一開始就裁掉邊緣，只驗格數。
- 寫了 `drift` 又寫 `static`：assemble 先試 drift，畫面會漂；craft 先試 locked，報表說它鎖定（`shot_reading` 的 `move.disagree`）。
- 會分家的字不要用（整表在 `camera-keywords.md` 第二節末）：`handheld`、`track`、`orbit`、`truck`、`steadicam`（craft 算跟拍，靜圖漂移）、`dolly out`、單獨的 `zoom`（craft 算推拉，靜圖漂移）、單獨的 `fixed`（craft 不算，靜圖鎖定）；`left to right`／`right to left` 在 slides 與 assemble 是 pan，craft 只認 `pan …`，讀成 `none`（`motion.repeat` 不算它一種運鏡）——要三個都讀到就寫 `pan left`／`pan right`。
- 人的動詞不進 `camera`：`she pushes the box`、`the paper rises` 在 slides 與 assemble 眼裡是推近與上搖，整行任何位置都算（`shot_reading` 的 `camera.person`）。
- 片段模型收到的是這一行原文，接在 `motion` 之後。Veo 文件（2026-10-03 讀）建議的字是 `aerial view, eye-level, top-down shot, dolly shot, worms eye` 與 `wide shot, close-up, single-shot or two-shot`；`locked`、`pan left` 這些字 Veo 與 Omni 怎麼理解沒有驗過。
- 鎖定機位不是預設值，但量到的參考片沒量運鏡（`drama-craft.md` 最後一節）；「同一種運鏡最多連 3」是編輯判斷。試拍兩集 81 行 `camera` 全寫 `Locked`（量到的，`model-misreads.md` 第一節）；站主說「不會想繼續看」，在分鏡上找得到的原因之一就是這個。

## 寫 prompt

- 寫**動作開始之前那一格**：手舉在秤盤上方，不是紙已經放平；信封在袋口外，不是已經在袋裡（試拍 E2 S34 讀稿才抓到的錯）。剪進成片的只有素材前幾秒，`motion` 要在這幾秒裡做完。
- 第一個子句＝景別＋誰在畫面哪一側、面朝哪裡：`Medium close-up of Chen behind the counter on screen right`。景別在提示裡出現兩次（這裡與 `Camera:` 子句），要同一家族，`size.agree` 量它。
- 回到同一鏡位時 `camera` 整行與第一個子句逐字照抄（`setupKey`），其餘只改表情與動作；第二、三次回去的鏡頭寫 `source`，不畫圖不買素材：

```json
{ "id": "s04", "template": "shot",
  "data": { "camera": "Medium close-up, locked",
            "prompt": "Medium close-up of Chen behind the counter on screen right, facing left toward Ayu off screen left, his right hand reaching down toward the scale pan at the bottom frame edge, lamp light from the right",
            "motion": "Chen lifts the folded note off the pan.", "characters": ["chen"] },
  "lines": [{ "id": "sa04", "speaker": "chen", "text": "三萬，一毛都不能少。" }] },
{ "id": "s08", "template": "shot",
  "data": { "camera": "Medium close-up, locked",
            "prompt": "Medium close-up of Chen behind the counter on screen right, the folded note in his raised right hand, his eyes lifting to Ayu off screen left",
            "motion": "He looks up from the note at Ayu.", "characters": ["chen"],
            "source": { "shot": "s04", "from_s": 1.5 } },
  "lines": [{ "id": "sa09", "speaker": "chen", "text": "叫我也沒用。" }] }
```

  `from_s` 看來源**實際買到**的秒數，不看 lint 的上限：s04 約 2.93 s、s08 約 2.2 s（lint 對 `scene-coverage.md` 示範場的估計），伺服器預設的 Omni（與 H3）照 `clipSeconds` 只買 4 s，1.5 ＋ 2.2 ＝ 3.7 放得下，代價是重播 s04 的 1.5–2.93 s；想從尾巴之後切（`from_s: 4`）只有 Lite 1080p 固定 8 s 時成立，Omni 下得把 s04 寫長（多買秒數）。細節在下一節的 `source` 條。
- 不要把 `camera` 整行貼在 prompt 開頭再加一段每鏡共用的狀態段（試拍 E2 的寫法）：`promptSimilarity` 警告、`setupKey` 把不同鏡位黏成一個、`shot_reading` 的 `prompt.camera`、模型多看一遍沒有新資訊。
- 畫外說話者寫 `Chen speaks off screen`，不列進 `characters`：列了他就占一張參考圖（上限 4）、多一題 `identity_chen`，而圖裡沒有他的臉，judge 答不了。`speaker` 仍是他（`shot_reading` 的 `cast.offscreen`、`cast.speaker`）。
- 目光或動作指向畫外的人時，畫外片語要緊接那個人：`Shen off screen left at his eyeline`、`toward Wei off screen right`。`cast.offscreen` 只把畫外片語緊接（或只隔 speaks、stands 這類字）的那個名字算成畫外；動手的人隔著 toward／at 這類方向字，算在畫面裡。讀不出片語在說誰時它報一次、問你，修法不叫你刪入鏡的角色。
- 數量與狀態寫成看得到的東西：`one folded note`、`one watch on the right wrist`、`a continuous steel door with its seam sealed`、`blank paper, no writing`。否定句少用：試拍把「already closed」「no locking operation」畫成開著的門。紙上任何字 judge 的 `no_text` 都扣，要讀的字另外合成。
- 場景的光寫在這一鏡（`lamp light from the right`），不寫進 `look.style`（試拍倉庫火光漏進婚禮）。
- 手部插鏡只寫手、袖口、腕上的東西、道具，不寫臉與髮型。`characters` 列不列：`visual-quality.md` 第二節要留資料綁定（只精簡 prompt）；這裡建議留空，理由是列了角色就把整段 appearance 接進提示（`shotAppearancePrompt`），而 identity 題（`keyframeRubric` 權重 2、單題 ≥ 4.0 才過，`apps/api/app/video_media/judge.py` 的 `MIN_CRITERION`）在沒有臉的圖上答不了（試拍 S04 R01 畫成上半身廣鏡）。哪種更穩沒驗，兩種別在同一場裡混用。範本：`Insert of <東西> on <哪裡>, <哪隻手> with <腕上的東西> at frame <left／right>; <誰> speaks off screen`。
- 過肩的近側只有肩膀與後腦，兩個 id 都列時近側那題 identity 只能靠髮型、衣服與體型答：試拍沒有一張過肩的關鍵影格進過 judge，過不過**未驗**。預設做法：對面的人一定列；近側的人列進去，identity 題被扣就改成只列對面、近側寫成 prompt 裡的肩膀（`the back of Ayu's right shoulder at frame left`，不點名就不占參考圖）。只有一隻手入鏡的人跟插鏡同一條：不列，手寫在 prompt。
- **採用格連戲帳**：一張關鍵影格通過後，把真圖裡的腕側、袖長、髮長、道具數、門的狀態抄進後面每一鏡的 prompt；規則與樣子在 `scene-coverage.md` 第一節第 8 條，寫在這一集的回報裡。
- 1000 字是欄位上限；組合後的關鍵影格提示（prompt ＋ `look.style` ＋ 外觀標籤）切在 4000，`shot_reading` 的 `prompt.length` 會算。

## 寫 motion

`motion` 是片段模型唯一讀到的動作描述：它拿到的是通過的關鍵影格（圖）加 `<motion>. <camera>. <look.motion>`，從頭到尾看不到 `prompt`。prompt 寫的起點與對象在 motion 裡要再說一次：誰＋動詞＋對象＋幅度＋結束狀態。

- 一個動作：`Chen pushes the coin bag back across the counter toward Ayu`、`Ayu takes the note from his hand`。第二個動作用 `and`／`then` 接的，craft 的 `motion.double` 只報不扣，而且它讀的是整行任何位置的 and／then，名詞片語（`between the bowl and the far edge`）也算：確認不是兩個動作就不用改。8 秒素材通常只剪 2–5 秒進成片（編輯判斷，drama-craft 的中位數 2.5–3.5 秒），放不下兩件事：拆鏡。
- 模型會放大小反應（一次試拍的證據，`model-misreads.md` 第一節）。小反應要嘛寫成靜圖（畫面不動），要嘛寫幅度與結束狀態，要嘛換一個看得見的動作：

| 寫了 | 試拍動出來的 | 改寫 |
| --- | --- | --- |
| `Her fingers tighten once around the pen.` | 左臂抬起加入持筆、多一只錶 | `Her right hand tightens once on the pen; the pen does not move; her left hand stays out of frame; one watch on the right wrist` |
| `Her pen-holding hand trembles briefly and steadies without touching the paper.` | 筆抬到水平再轉回；另一版多一隻手、第二支筆 | `visual: "still"`，或 `the pen tip moves less than a finger's width and returns; one hand, one pen` |
| 無（第 0 格已睜眼，自然眨眼） | judge 6.72：「片頭眼睛張開的額外動作」 | `eyes open throughout, one natural blink is fine`（會不會改分數沒驗） |

- 反應不是動作：規則與比例（≤ 1/3、≤ 連 2、開場三鏡不能全是，編輯判斷）在 `drama-craft.md` 第三節，判定是 craft 的 `isLookOnly`（正則在 `camera-keywords.md` 第三節）。容易踩的一組：`stands`、`sits`、`kneels`、`lies`、`waits`、`pauses`、`hesitates`、`faces`、`remains`、`stays`、`holds` 在前五個字裡出現也算「站著不動」，整組只有緊接 `up`／`down`／`out`／`back`／`away`／`off` 才例外——`holds out the key` 是動作，`holds the key out across the table` 是看。遞東西寫 `lifts the key off the table toward Chunmei until her arm is straight`。非臉的景別只有眼神，`shot_reading` 報 `motion.look`；空的 `motion` 報 `motion.empty`。加一個推近不會讓反應變成動作。
- 不寫攝影機字（三個讀者都不讀 `motion` 裡的 push、pan；片段模型卻會當指令），不寫聲音（片段 `native_audio: false`，Lite 的音軌成片丟棄）。來源沒有的行為不加。
- 沒有台詞的動作拍：**場景層**的 `action_seconds`（1–8 整數）配空的 `lines`，不在 `data` 裡（放進 `data` 是 lint 的 unknown field）：

```json
{ "id": "s09", "template": "shot", "action_seconds": 2, "lines": [],
  "data": { "camera": "Two-shot, locked", "prompt": "Two-shot from the customer side: Ayu on screen left, the coin bag back in front of her, her right hand on the drawstring; Chen on screen right watching her",
            "motion": "Ayu pulls the drawstring of the coin bag open.", "characters": ["ayu", "chen"] } }
```

  普通漫劇須「有角色、沒有時長下限、不是知識長片、`category` 不是 anime」（`tools/video/core/drama.mjs` 的 `timesSilentShots`）；長篇動畫另由有效的 `long-anime-v1` production policy 接受動作拍（`tools/video/core/schema.mjs` 的 `validAnime`）。品牌故事與解說不適用。`motion` 寫完整的起手、接觸、收勢一件事，秒數照動作需要寫，不照台詞；長度估算就是這個數。

## 靜圖、片段、切素材、接續、fit

| 這一鏡要的 | 寫法 | 買什麼 |
| --- | --- | --- |
| 反應停留、沒有接觸的動作、建立鏡 | `visual: "still"`＋`camera` 寫表裡的運鏡或 `locked` | 1 張圖＋1 次 judge |
| 一個接觸動作 | clip（預設） | 圖＋judge＋素材＋judge。素材秒數是 `clipSeconds`（工具規定，`tools/video/media/clips.mjs`）：`veo-3.1*` 配 1080p 固定 8 秒；其他模型 `clamp(ceil(frames/30), 4, 10)` 再往上貼齊模型的秒數表（Omni 與 H3 在 catalog 都是 4–10）；H3 在 MiniMax 直打與 Hailuo 網頁是 4–15 整數，自己選 |
| 回到同一鏡位的第二、三次 | `source: { shot, from_s }` | 不畫圖、不買素材、不 judge（帳本記 `cut`） |
| 無聲的動作拍 | 場景層 `action_seconds`＋空 `lines`（上一節） | 同 clip 或 still |

每一種的價錢在 `.agents/skills/animation-production/SKILL.md` 的「錢怎麼算」；三條路線的點數換算在它的 `references/cost-model.md`。

- 靜圖的運鏡：要驗第 0 格就寫 `push in`、`drift` 或 `locked`（`IDENTITY_START`：第 0 格是整張關鍵影格，`assemble` 算 PSNR ≥ 22）；`locked` 只給刻意的 hold（`shot_reading` 報 `still.locked` 問一次：是就留著並在回報說明，不是就給 `push in` 或 `drift`）；`pull out`、pan、tilt 一開始就裁掉邊緣，不驗第 0 格。`checks.json` 的 `metrics.shots[]` 記 `kind: "motion"`、`move` 與 `keyframe_psnr`，看到 `drift` 多半是 `camera` 沒寫或用了表外的字（`still.drift`）。靜圖不能有 `end_frame`（lint 錯誤）。
- `source` 的規矩（lint，`tools/video/core/drama.mjs` 的 `validateShotData`）：來源要是更早的 clip 鏡頭、自己有素材（不是 still、不是本身切來的）；不能同時有 `start_frame`／`end_frame`；不能當縮圖底圖；`from_s`＋鏡長在 lint 的上限內：沒有 production profile 10 秒（`MAX_SOURCE_CLIP_SECONDS`）、有 profile 8 秒（`tools/video/core/lint.mjs`）。但素材真正有幾秒是來源鏡頭**買到的**：Lite 1080p 永遠 8；Omni／H3 是 ceil(需要) 最少 4（`clipSeconds`），一個 3 秒的來源在伺服器預設的 Omni 下只有 4 秒可切，`clips.mjs` 在來源買下之後才把超出的切鏡標 `needs_review`。Omni／H3 下要嘛刻意把來源鏡頭寫長（多買秒數），要嘛接受重播來源的開頭；「說—聽—說回同一鏡位」切尾巴之後那段，只在 Lite 1080p 固定 8 秒時成立。`shot_reading` 分兩個陷阱：`source.length`（超過 lint 上限）、`source.bought`（在上限內但超過來源買到的秒數，以 Omni／H3 的 4–10 算）。`assemble` 拿第 0 格對來源素材第 `from_s` 秒那一格算 PSNR。
- 素材放大成較近的景別（punch-in）**沒有做**（`docs/videos/DRAMA.md`）：要更近的景別就是新的一鏡。
- `look.motion` 會接在每一支片段的 `camera` 後面，而 preset 的 `look.motion` 都含一個運鏡字（`gentle camera move`、`slow cinematic camera move`）：寫 `locked` 的鏡頭，模型同時收到「鎖定」與「緩慢運鏡」。以鎖定機位為主的作品，把 `look.motion` 設成空字串或一句沒有運鏡字的話，而且要在 `look` 跑之前定（它在 `lookHash` 裡，之後改會讓設定圖與關鍵影格全部過期）。`shot_reading` 只在 `camera` 鎖定且 `look.motion` 含 `LOOK_MOVE_WORDS` 的字（`camera move`、`drifting`、`push`、`pan`、`tilt`、`zoom`、`dolly`、`handheld`…，編輯判斷）時報 `look.motion`；試拍覆寫成的那句（`One clearly motivated character or prop action per clip, …`）沒有運鏡字，不算矛盾，只在第一行印出它仍會接上；`no morphing, no cuts` 這類穩定用語要留就放進 `motion` 句尾。
- `start_frame: { shot, at: "last" }` 目前只把上一鏡最後一格當參考圖，片段仍從自己的關鍵影格開始，所以兩張關鍵影格要自己在位置與接觸點上接得上。
- `fit`（`auto` 最多慢到 0.85 倍、`slow` 0.5 倍、`freeze`、`trim`；`tools/video/assemble/drama.mjs` 的 `fitPlan`）：素材比鏡頭長時四種都只是裁尾，Lite 固定 8 秒而鏡頭 ≤ 8 秒，所以 fit 幾乎永遠不生效。production profile 以 lint 禁 `fit: "freeze"`（`tools/video/core/lint.mjs` 的 `productionShotProblems`）；`slow` 不是 lint 錯誤，但 profile 下素材要蓋滿鏡長（`clips.mjs` 的「would need padding or slowing」），所以放慢補長度的 take 會被 QC 退回。
- 一鏡會被 lint 擋的：估計超過 12 秒（10 秒警告）、`characters` 超過 3（`shot_reading` 的 `cast.count`）、still 帶 `end_frame`、`source` 超出 lint 上限。

## 同一鏡在 Hailuo 與 Kling 怎麼寫

先沿**使用者本次指定的路線**：要求內建瀏覽器，就用 Hailuo／Kling 網頁；CLI／MCP 是另外選定的路線，不因歷史選擇自動取代網頁。產線的關鍵影格已定景別、構圖與軸線，兩家都用同一鏡核准首格；`camera` 仍照上面的工具讀法寫，網頁的動態正文由 `animation-preproduction` 的 `shot_plan.mjs --route hailuo|kling` 照各家官方格式組好（Hailuo H3 的固定第一行與三個欄位、運鏡寫成「種類＋幅度＋速度」；Hailuo 2.3 的方括號指令；Kling 3.0 的自然語言），運鏡字的對照表在它的 `references/route-decisions.md` 第六節。操作讀 [browser-production.md](../../../.agents/skills/animation-production/references/browser-production.md)，具體八鏡改寫讀 [budaimiao-style.md](../../../.agents/skills/animation-camera/references/budaimiao-style.md) 第四節。

| 東西 | Hailuo 網頁 | Kling 網頁 |
| --- | --- | --- |
| 首格與參考 | 用當前瀏覽器有文件的上傳工具交同一張首格，確認預覽；參考欄另核對 | 同；CLI 的 image 欄位名不當成網頁欄位 |
| 運鏡與動作 | 一鏡一個主要可見動作、一個運鏡；H3 用官方的運鏡句子（種類＋幅度＋速度），方括號只給 2.3 | 一個連續鏡頭、一個運鏡寫在正文開頭；不把社群 MCP 的 camera control 當網頁選項 |
| 風格與否定 | 保留本集 `look.motion` 的穩定要求；H3 的 API 沒有負面欄（官方），網頁有沒有沒驗；正文只寫正面狀態，`look.negative` 只貼進真的有的負面欄 | 同：負面欄真的有才貼；字數上限按當前 UI 核對 |
| 秒數、比例、模型 | 由本鏡需求與當前 UI 決定，16:9；歷史 H3 2K 實測不是原生 1080p | 同；CLI 列出的秒數／解析度不代替網頁實測 |
| 聲音與分鏡 | 一個連續鏡頭；原生聲音按本案契約處理，既有配音／CC不改 | 同；多鏡／原生音訊開關只操作網頁實際提供的 |
| 下載與匯入 | 用網站下載按鈕取得正確版本；先檢查浮水印，再依 stage-preconditions 匯入 | 同；網頁來源以 `--provider external` 並在 `--note` 記 Kling web，CLI／MCP 的歷史標籤不冒充網頁 |

**能力的邊界**：2026-10-04 Claude 桌面內建瀏覽器曾無本機上傳工具，是那次環境的證據；不能推成 Codex 或所有內建瀏覽器都不能上傳。依當前工具文件與 UI 確認；做不到時交站主完成缺的一步，不抽 cookie、不換 profile、不注入 base64／DataTransfer。

CLI／MCP 的模型、字彙來源與已驗／未驗值仍在 `model-misreads.md` 第五節及 `.agents/skills/animation-production/references/providers-and-plans.md`；不是本次網頁路線的預設。外部片段沒有自動通過產線 judge；現行 `clips import` 無條件拒絕含 `series.production.profile` 的作品，改 provider 值也不會解除，付費前先查。

## 每寫完一場戲的檢查清單

craft 的列（景別有名、`camera` 與 `prompt` 同家族、全景占比與重新交代、同景別同人 ≤ 連 2、反應鏡的比例與開場、雙動作 info）照 `drama-craft.md` 第一張表跑 `drama_craft_check.mjs`，目標值在那張表，這裡不重抄；下面是它不量、`shot_reading` 與人才抓的：

| # | 看什麼 | 誰抓 |
| --- | --- | --- |
| 1 | 畫外說話者不在 `characters`，prompt 寫 off screen | `shot_reading` `cast.offscreen`、`cast.speaker`；craft `size.listeners` info |
| 2 | 每鏡 ≤ 3 人 | lint 錯誤 `must list at most 3 distinct character ids`；`shot_reading` `cast.count` |
| 3 | still 的 `camera` 照上一節「靜圖的運鏡」那一段；`drift`＋`static` 不並寫 | `shot_reading` `still.drift`、`still.locked`、`move.disagree`；`checks.json` `metrics.shots[].move`、`keyframe_psnr` |
| 4 | `source` 的 `from_s`＋鏡長在 lint 上限內，也在來源買到的秒數內（伺服器路線；網頁路線的母鏡頭由 `animation-preproduction` 的 `shot_plan.mjs` 買到蓋住切鏡，`shot_reading --route hailuo|kling` 不報 `source.bought`）；來源是有素材的 clip 鏡 | lint 錯誤；`shot_reading` `source.length`、`source.bought`、`source.shot` |
| 5 | 鎖定作品的 `look.motion` 是空字串；`look.negative` 保留所需限制，兩者在 `look` 之前定好；不為 Lite 清空已核准的 negative | `shot_reading` `look.motion`；`animation-production` 的 `drama_preflight.mjs` |
| 6 | `camera` ≤ 120、`prompt` ≤ 1000、`motion` ≤ 300；組合後的關鍵影格提示 ≤ 4000；人的動詞不在 `camera`；prompt 不抄 `camera` | lint；`shot_reading` `prompt.length`、`camera.person`、`prompt.camera` |
| 7 | 軸線、畫面側、視線、進出方向、採用格連戲帳 | 只有人；寫在這場戲的回報裡 |

順序：`lint` → `drama_craft_check.mjs` → `shot_reading.mjs` → `animation-production` 的 `episode_estimate.mjs`，四個都離線、不花錢；之後才 `keyframes --dry-run`。查核改了鏡頭、旁白量過之後，前三個再跑一次。寫單場戲時 `lint --file` 的 `brief.md is missing` 與「1 chapters; YouTube needs at least 3」屬整集，看 `scenes[n].data.*` 的錯誤與 `craft …` 警告就好。

craft 的列沒過，改到過或在回報裡逐列寫這一集為什麼不同（`drama-craft.md` 第七節）；`shot_reading` 的陷阱同樣。`still.locked` 與 `look.motion` 兩條只是問「這是不是故意的」：在回報裡答一句就算處理，不用改鏡頭。兩支腳本都不擋任何指令、不改目標；不靠換關鍵字騙過檢查。

## 腳本

```bash
node .agents/skills/animation-camera/scripts/shot_reading.mjs <VIDEO_DOCS>/video.json            # 每鏡一塊：visual、craft 景別與家族、三個讀者的運鏡與要不要驗 PSNR、look-only、台詞與說話者、characters、組合後的提示長度；陷阱與修法；最後一行計數
node .agents/skills/animation-camera/scripts/shot_reading.mjs <VIDEO_DOCS>/video.json --route kling   # 網頁路線：source.bought 不報（母鏡頭的秒數由 shot_plan 定）
node .agents/skills/animation-camera/scripts/shot_reading.mjs <VIDEO_DOCS>/video.json --shot a,b  # 只看這幾鏡（照文件順序）；旁邊有 series.json 的 production profile 時 source 以 8 秒算
node .agents/skills/animation-camera/scripts/shot_reading.mjs --file one-shot.json                 # 一個 { camera, prompt, motion, characters?, visual?, source?, lines?, look? } 物件
node .agents/skills/animation-camera/scripts/shot_reading.mjs <file> --json | --strict             # --json 的 summary 有 shots、traps、by_kind；--strict 有陷阱就結束碼 1；讀不到 2
```

最後一行是「讀了 N 個鏡頭，M 個陷阱：<id> 次數…」或「沒有陷阱：三個讀法讀到的就是寫的；畫面好不好仍要看小樣」；每個陷阱下面有一行修法。

陷阱的 id（`TRAP_IDS`）：`size.none`、`size.disagree`、`still.drift`、`still.locked`、`camera.person`、`move.disagree`、`motion.empty`、`motion.look`、`look.motion`、`cast.offscreen`、`cast.speaker`、`cast.count`、`prompt.camera`、`prompt.length`、`source.shot`、`source.length`、`source.bought`。它讀的是英文關鍵字，跟 `drama_craft_check.mjs` 用同一組函式（`tools/video/core/craft.mjs`、`tools/video/core/drama.mjs`、`tools/video/assemble/drama.mjs`；買到的秒數用 `tools/video/media/clips.mjs` 的 `clipSeconds`），不擋任何指令；`tools/animation-camera.test.mjs` 把 `camera-keywords.md` 的例子表逐行丟進同一組函式驗。

## 模型畫錯過的事

一次試拍的證據寫成規則，不是定律；逐 take 的表、提示的組法、Lite 的歷史參數失敗與現行相容處理、judge 的題目與通過條件在 `.agents/skills/animation-camera/references/model-misreads.md`。最常踩的五條：關門寫成否定句被畫成開門；場景光放在 `look.style` 漏到別的場景；手部插鏡列了角色被畫成上半身；「微顫」「收緊」被片段模型放大成抬筆、多一隻手；錶在兩張通過的圖之間換了手，來源從沒寫過左右腕。此程式版本已完成 Lite adapter 相容修正（`tasks/done/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md`）；保留 `look.negative`，不用為此改 look 或重做核准。實際後端須核對部署版本，本機 preflight 通過不代表正式服務已更新或付費片段已成功。原試拍結果仍是當時的歷史證據。

## 還沒驗、不能宣稱的事

- 片段模型對 `locked`、`pan left`、`push in` 原文的反應：沒有量過，`camera` 的字只保證三個讀者讀對。
- 參考片的運鏡：量到的只有鏡長與景別（`drama-craft.md` 最後一節），「鎖定不是預設」「同一運鏡 ≤ 連 3」是編輯判斷。
- 手部插鏡列不列角色哪種更穩、過肩近側的 identity 題過不過、`eyes open throughout, one natural blink is fine` 會不會改變 judge 分數：各一次證據或零次。
- H3 照不照方括號指令（官方只寫給 Hailuo 2.3／02）、H3 與 Kling 3.0 對官方運鏡句子的實際反應、Kling MCP 的 pan 方向與 zoom 正負：都沒有實拍（`model-misreads.md` 第五節）。2026-10-04 的實測沒有補上這幾項：Hailuo 那一支是文生影片，量的是點數、時間與輸出規格；Kling 官方 CLI 讀了指令、模型與參數，帳號 0 點、一支都沒生成。
- 這份 skill 讓一個沒看過產線的代理寫出可接受的一場戲（任務的驗收第五條）：一次前向測試（2026-10-03，12 鏡的兩人餐桌戲）三稿到可接受，但寫的人開了 `timeline.mjs`、`clips.mjs` 與 craft 的正則才過；`action_seconds` 的位置、`holds` 那組字、來源買到的秒數就是從那次來的。這個 12 鏡用例尚未重跑；2026-10-04 另做布袋喵風格的原創三鏡前向測試，讀法零陷阱並能寫出兩家網頁提示與 profile 匯入限制，但只完成離線分鏡，未驗模型、媒體或完整集。
