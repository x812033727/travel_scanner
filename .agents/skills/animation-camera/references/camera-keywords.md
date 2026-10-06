# 三個關鍵字讀者的表：逐字引自程式

讀 `camera`、`prompt`、`motion` 的程式有三處，各一份正則，用途不同。這份表 2026-10-03 逐字抄自下列檔案；程式改了，表就要跟著改，程式永遠為準。`tools/animation-camera.test.mjs` 把最後一節「例子」的每一列丟進同一組函式驗，所以表與程式分家時測試會紅。

| 讀者 | 檔案與函式 | 讀哪些欄位 | 結果用在哪 |
| --- | --- | --- | --- |
| craft（手藝檢查） | `tools/video/core/craft.mjs` 的 `shotSize`、`sizesDisagree`、`cameraMove`、`isLookOnly` | `camera`、`prompt`、`motion` | `lint` 的 `craft …` 警告、`.agents/skills/youtube-video/scripts/drama_craft_check.mjs` 的表、免關卡作品退稿的列（`CRAFT_GATE_ROWS`） |
| slides（插畫投影片的變化規則） | `tools/video/core/drama.mjs` 的 `cameraMove`（`CAMERA_MOVES`）與 `pictureVarietyProblems` | `camera` | 插畫投影片三張連用同一運鏡是錯誤（`SAME_MOVE_RUN_MAX = 2`）；漫劇不跑這條，但字表與 assemble 的相同 |
| assemble（靜圖的實際運鏡） | `tools/video/assemble/drama.mjs` 的 `motionMove`、`zoompanExpr`、`IDENTITY_START` | `camera` | `visual: "still"` 鏡頭與單態卡片的 zoompan；第 0 格要不要對關鍵影格算 PSNR |

三個讀者都把整行轉小寫再比對；沒有一個讀 `motion` 裡的攝影機字；沒有一個讀中文。

## 一、景別：只有 craft 讀（`shotSize`、`sizesDisagree`）

讀的順序（`sizeIn`）：`insert`／`detail shot`／`macro` 三個字出現就算插鏡 → 去掉開頭的修飾詞後，行首的景別（`LEADING_SIZE`）；行首若是一般 close-up，先問它是不是「拍東西的近景」（`isInsert`），是就算插鏡 → 行內任何位置第一個命中的景別（`CAMERA_SIZES`）→ 都沒有才讀 `prompt`，而且只認明寫的景別片語（`PROMPT_SIZES`，所以 "wide sleeves" 不是景別）→ 仍沒有就是 `null`，算進 `size.named`。

```js
const EXPLICIT_INSERT = /\binsert\b|detail shot|\bmacro\b/;
const LEADING_QUALIFIER = /^(?:(?:locked|static|fixed|handheld|slow|oblique|overhead|low[- ]angle|high[- ]angle|table[- ]level)[ ,]+)+/;
const LEADING_SIZE = [
  ["ecu", /^extreme close[- ]?up\b/],
  ["mcu", /^medium close[- ]?up\b/],
  ["cu", /^close[- ]?up\b/],
  ["ots", /^over[- ]the[- ]shoulder\b/],
  ["group", /^(?:two|three)[- ]shot\b|^group shot\b/],
  ["ms", /^(?:medium|mid) shot\b/],
  ["ws", /^(?:extreme )?wide\b|^establishing\b/],
  ["pov", /^pov\b|^point of view\b/],
];
const CAMERA_SIZES = [
  ["ecu", /extreme close[- ]?up|\becu\b/],
  ["mcu", /medium close[- ]?up|\bmcu\b|head[- ]and[- ]shoulders|chest[- ]up/],
  ["cu", /close[- ]?up|closeup/],
  ["ots", /over[- ]the[- ]shoulder|\bots\b/],
  ["group", /(?:two|three)[- ]shot|group shot|ensemble shot/],
  ["ms", /medium shot|mid shot|medium wide|waist[- ]up|cowboy shot/],
  ["ws", /wide[- ](?:shot|angle|view|establishing|frame|framing)|establishing|long shot|full shot|full-body shot|aerial|bird'?s[- ]eye/],
  ["pov", /\bpov\b|point of view/],
];
const PROMPT_SIZES = [
  ["ecu", /extreme close[- ]?up/],
  ["mcu", /medium close[- ]?up/],
  ["cu", /\bclose[- ]?up\b/],
  ["ots", /over[- ]the[- ]shoulder/],
  ["group", /(?:two|three)[- ]shot|group shot/],
  ["ms", /medium shot|mid shot|waist[- ]up/],
  ["ws", /wide (?:shot|angle|establishing)|establishing shot|long shot|full shot|aerial shot|bird'?s[- ]eye view/],
  ["pov", /\bpov\b|point of view/],
];
```

插鏡的判定（`isInsert`）：行裡有 `face`、`medium close-up`、`reaction shot`、`over-the-shoulder` 任一（`FACE_IN_FRAME`）就不是插鏡；否則「close-up／shot／view／framing of／on ＋最多三個修飾詞＋一個東西」是插鏡（修飾詞不能是 -ing 字或介系詞，`NOT_A_MODIFIER`），「東西 close-up／shot」（`hand shot`、`prop close-up`）是插鏡，「overhead／top-down … close-up」是插鏡。東西的清單：

```js
const OBJECT = "(?:hands?|fingers?|fist|palm|thumb|pen|papers?|documents?|copy|copies|pages?|phone|ring|cup|bowl|keys?|letter|screen|ticket|seal|stamp|blade|sword|foot|feet|props?|objects?|original|contract|envelope|receipt|box|bag|tray|table)";
const OF_OBJECT = new RegExp(`(?:close[- ]?up|shot|view|framing) (?:of|on) ((?:[\\w'’-]+ ){0,3}?)${OBJECT}\\b`);
const NOT_A_MODIFIER = /ing$|^(?:at|around|with|near|behind|beside|by|in|from|over|under|across)$/;
const OBJECT_SHOT = new RegExp(`\\b${OBJECT}(?:-[\\w-]+)? (?:close[- ]?up|shot)`);
const OVERHEAD_CLOSE = /(?:overhead|top-down)[\w ,-]{0,24}close[- ]?up/;
const FACE_IN_FRAME = /\bface\b|medium close[- ]?up|reaction shot|over[- ]the[- ]shoulder/;
```

景別的家族（`family`）：`ecu`、`cu`、`mcu`、`ots` 是臉（`size.face`）；`ws`、`group` 是全景（`size.wide`、`size.reestablish`）；`insert` 是插鏡（`size.insert`）；`ms` 與 `pov` 三列都不算。`sizesDisagree` 是 `camera` 與 `prompt` 各讀出一個景別而家族不同（`cu` 對 `mcu` 不算不同）。鏡位（`setupKey`）是 `camera` 整行小寫加 `prompt` 到第一個逗號、句號或分號為止的小寫，逐字相同才算同一鏡位；`size.stall` 的「同一批人」是 `data.characters` 排序後相同，兩個都沒有人的鏡頭（插鏡）要鏡位相同才算同一批人。

## 二、運鏡：三個讀者，三份字表

### craft 的 `cameraMove`（`motion.repeat`、`motion.locked`）

只有行首、子句開頭（逗號、分號、句號、冒號之後）或攝影機修飾詞之後的字才算運鏡（`AT_CLAUSE`）；「she pushes the box」裡的 pushes 不算。`locked` 的字不受這個位置條件限制。依序試，第一個命中的贏，都沒有是 `none`。

```js
const AT_CLAUSE = "(?:^|[,;.:] ?|\\b(?:and|then|slow|slowly|gentle|gently|subtle|quick|fast|smooth|steady|camera|handheld|low|high) )";
const MOVES = [
  ["locked", /\blocked\b|\bstatic\b|fixed (?:camera|frame|shot)|tripod|no camera move|still camera/],
  ["pull", move("pull(?:s|ing)?[- ](?:back|out)|pull-?back|dolly(?:ing)? out|zoom(?:s|ing)? out|widen(?:s|ing)?|back(?:s|ing)? away")],
  ["push", move("push(?:es|ing)?[- ]?in|dolly(?:ing)? in|zoom(?:s|ing)?(?: in)?|mov(?:e|es|ing) in|closer")],
  ["pan", move("pan(?:s|ning)?")],
  ["tilt", move("tilt(?:s|ing)?|crane(?:s|ing)?|pedestal|rises?|descend(?:s|ing)?")],
  ["track", move("track(?:s|ing)?|truck(?:s|ing)?|follow(?:s|ing)?|handheld|orbit(?:s|ing)?|arc(?:s|ing)? (?:left|right|around)|steadicam")],
];
```

### slides 的 `CAMERA_MOVES`（`tools/video/core/drama.mjs`）與 assemble 的 `MOVES`（`tools/video/assemble/drama.mjs`）

兩份正則逐字相同，只有名稱寫法不同（`push in` 對 `push-in`）。整字比對、行內任何位置都算、`drift` 先於 `locked` 試、都沒有就漂移（slides 回 `"drift"`，assemble 回 `{ name: "drift", direction: 由鏡頭 id 的字元碼和決定 right 或 left }`）。沒有 track、orbit、handheld、truck、dolly out、pedestal：這些字在這兩個讀者眼裡等於沒寫。

```js
const MOVES = [
  ["drift", /\bdrift(?:s|ing)?\b/],
  ["locked", /\blocked\b|\bstatic\b|\bfixed\b|\btripod\b|\bno camera move\b|\bstill camera\b/],
  ["push-in", /\bpush(?:es|ing)?\b|\bdolly(?:ing)? in\b|\bzoom(?:s|ing)? in\b|\bcloser\b|\bmov(?:e|es|ing) in\b/],
  ["pull-out", /\bpull(?:s|ing)?\b|\bzoom(?:s|ing)? out\b|\bwiden(?:s|ing)?\b|\bback(?:s|ing)? away\b/],
  ["pan-right", /\bpan(?:s|ning)? (?:to the )?left\b|\bleft to right\b/],
  ["pan-left", /\bpan(?:s|ning)? (?:to the )?right\b|\bright to left\b/],
  ["tilt-up", /\btilt(?:s|ing)? up\b|\bcrane(?:s|ing)? up\b|\brises?\b|\brising\b/],
  ["tilt-down", /\btilt(?:s|ing)? down\b|\bcrane(?:s|ing)? down\b|\bdescend(?:s|ing)?\b/],
];
const IDENTITY_START = new Set(["push-in", "drift", "locked"]);
```

運鏡的名字是**觀眾看到畫面怎麼動**，所以 pan 跟攝影機用語相反：`zoompanExpr` 的 `pan-right` 把裁切窗從右邊緣滑到左邊緣，窗往左滑、窗裡的畫面往右跑；寫 `pan left`（攝影機往左搖）或 `left to right`（畫面自己的方向）都得到它。tilt 保留攝影機的字：`tilt up`、`crane up`、`rise` 都是 `tilt-up`，窗從下滑到上。幅度是工具規定（`tools/video/assemble/drama.mjs`）：`MOTION_ZOOM = 0.10`（push-in 從 1.0 放大到 1.10，pull-out 相反）、`MOTION_PAN_ZOOM = 1.08`（pan 與 tilt 固定 1.08 倍滑窗）、`MOTION_DRIFT_ZOOM = 0.04`（drift 放大 4% 並往一側移 15% 的可移距離）、`MOTION_SOURCE_SCALE = 1.25`（先放大 1.25 倍再裁，裁切窗永遠不小於輸出）、`MOTION_TRAVEL_SECONDS = 6`（6 秒以上走完整段，短鏡至少走 `MOTION_TRAVEL_MIN = 0.5`）、長片的靜圖用 smoothstep 緩入緩出。`IDENTITY_START` 裡的三種第 0 格是整張關鍵影格，`assemble` 對它們算 PSNR（`KEYFRAME_MIN_PSNR = 22`）；pull-out、pan、tilt 一開始就裁掉邊緣，只驗格數，`checks.json` 的 `metrics.shots[]` 記 `kind: "motion"`、`move`、`keyframe_psnr`（沒驗的是 `null`）。

### 三個讀者分家的字

| 寫在 `camera` 的字 | craft | slides／assemble | 後果 |
| --- | --- | --- | --- |
| `handheld`、`track`、`truck`、`follow`、`orbit`、`arc left`、`steadicam` | `track` | 沒這些字 → `drift` | 片段模型收到的是原文；靜圖會漂移而不是跟拍；`motion.repeat` 把它們算一種運鏡 |
| `dolly out`、`pull back`（沒有 pull 開頭之外的字時） | `pull` | `dolly out` 沒有 → `drift`；`pull back` 有 pull → `pull-out` | 靜圖想拉遠要寫 `pull out`、`zoom out`、`widen` |
| `slow zoom`、`zoom`（沒有 in） | `push` | 要 `zoom in` 才算 → `drift` | 靜圖想推近寫 `push in`、`zoom in`、`closer` |
| 人的動詞：`she pushes the box`、`the paper rises` | 不算（不在子句開頭）→ `none` | `\bpush…\b`、`\brises?\b` 整行都算 → `push-in`、`tilt-up` | 靜圖會動；人的動作寫在 `motion`，不寫在 `camera` |
| `static, slight handheld drift` | `locked`（static 先試） | `drift`（drift 先試） | `motion.locked` 說它鎖定，畫面卻在漂 |
| 單獨的 `fixed` | 不算（craft 要 `fixed camera／frame／shot`）→ `none` | `locked` | 寫 `locked` 兩邊都懂 |
| `left to right`、`right to left`（沒有 pan 字） | 不算（craft 只認 `pan…`）→ `none` | `pan-right`／`pan-left` | 靜圖照搖，但 `motion.repeat` 不算它一種運鏡；要三個都讀到寫 `pan left`／`pan right` |
| `pedestal` | `tilt` | 沒有 → `drift` | 寫 `tilt up`／`tilt down` |

## 三、只有眼神（`isLookOnly`）

讀 `motion` 的第一個子句（在逗號、分號、句號、` and `、` while `、` without `、` as `、` then ` 之前切開），命中下列任一就是「只有眼神」；空的 `motion` 也是。「抬頭去看」（`lifts her head to look at …`）整行先判為眼神。這些是反應，不是動作：一場戲需要，所以 craft 量的是比例與連續（`motion.look ≤ 1/3`、`motion.run ≤ 2`、`motion.opening` 開場三鏡不能全是；都是編輯判斷）。加一個運鏡不改變判定。

```js
const FACE_PART = "(?:gaze|eyes?|eyelids?|expression|smile|brows?|lips?|jaw|mouth|breath|breathing)";
const SMALL = [
  new RegExp(`^(?:[\\w'’-]+ ){0,6}?${FACE_PART} \\w+`),
  new RegExp(`\\b(?:turns?|lifts?|raises?|lowers?|drops?|shifts?|moves?|holds?|keeps?|fixes|narrows?|closes?|shuts?|squeezes?|opens?|widens?) (?:his|her|their|the) (?:[\\w-]+ )?${FACE_PART}\\b`),
  /\b(?:his|her|their) face (?:falls|hardens|softens|tightens|pales|flushes|darkens|stills|freezes|crumples)\b/,
  /^(?:[\w'’-]+ ){0,4}?(?:stands?|sits?|kneels?|lies|waits?|pauses?|hesitates?|faces|remains?|stays?|holds?)\b(?! (?:up|down|out|back|away|off)\b)/,
  /^(?:[\w'’-]+ ){0,4}?(?:looks?|glances?|stares?|gazes?|studies|watches|blinks?|breathes?|swallows?|frowns?|smiles?|smirks?|squints?|waits?|listens?|reads?)\b/,
  /(?:^|\b(?:a|her|his|their|the) )(?:single |lone )?tears? (?:falls?|wells?|rolls?|streams?|runs?|slides?)\b/,
  /\b(?:hands?|fingers?|fist|grip|knuckles?) (?:\w+ly )?(?:tightens?|trembles?|quivers?|twitch(?:es)?|shakes?|clench(?:es)?|whitens?|curls?)\b/,
  /\b(?:tightens?|clench(?:es)?|closes?|curls?) (?:his|her|their) (?:fingers?|fist|grip|hand)\b/,
  /\b(?:stands?|sits?|remains?|stays?|holds?) (?:very |perfectly |completely )?(?:still|motionless|frozen)\b/,
  /^(?:[\w'’-]+ ){0,3}?(?:trembles?|shivers?|sways?|flickers?)\b/,
];
```

試拍的 81 句 motion 與人工逐句判讀 81 句一致、景別 80 句一致（量到的，`drama-craft.md` 第七節）；換一種寫法仍可能誤判，覺得不對就用 `drama_craft_check.mjs --json` 或 `shot_reading.mjs` 看那一鏡被讀成什麼。

## 四、其他讀 `camera` 的地方

- 關鍵影格提示把整行接成 `Camera: <camera>` 放在 `Style:` 之後（`tools/video/media/keyframes.mjs` 的 `shotPrompt`）；片段提示把整行接在 `motion` 之後、`look.motion` 之前（`tools/video/media/clips.mjs` 的 `clipPrompt`）。兩個模型讀到的是原文，不是上面任何一個讀者的結果。
- 兩種 judge 的 `context.shot.camera` 是原文；clip judge 的 `prompt` 題問「有沒有做出要求的 motion 與 camera move」（權重 1）。
- `camera` 上限 120 字、`prompt` 1000、`motion` 300（工具規定，`tools/video/core/drama.mjs` 的 `LIMITS`）。
- 插畫投影片另有一份景別字表（`tools/video/core/drama.mjs` 的 `SHOT_SIZE`）讀的是 `prompt`，不是 `camera`；那條路線不在這份 skill 裡。

## 五、各模型的提示長度與「疊加物不是景深」

2026-10-05 讀的官方頁面；官方沒給數字的寫「無」，再列社群的數字與出處（次級，標名）。單位分清楚：words 是英文字、characters 是字元（API 的上限幾乎都算字元）、tokens 只有 Google 用。產線自己的上限在第四節（`camera` 120、`prompt` 1000、`motion` 300；組好的提示切 4000）。

| 模型（路線） | 官方的規定（頁面、讀取日） | 官方沒說的：社群甜蜜點（來源） | 量到的 |
| --- | --- | --- | --- |
| Hailuo H3 ／ MiniMax-H3（API v2、網頁 H3） | API 每個 `text` ≤ 7,000 字元（platform.minimax.io/docs/api-reference/video-generation-v2-create；platform.minimax.io/docs/guides/video-generation 也寫「Prompt length limit ≤ 7000 characters」；頁面無日期，2026-10-05 讀）。官方提示指南（huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md，模型卡最後更新 2026-08-13，2026-10-05 讀）對 T2VA／I2VA 沒有字數；全參考指南（同目錄的 `…_ref_en.md`）說生成任務的 `detailed_description` 通常 350–500 英文字，對白多的以塞下完整台詞為準。GitHub 的官方 skill（github.com/MiniMax-AI/MiniMax-H3 的 `skills/h3-prompt-writing/SKILL.md`，2026-10-05 讀）只說描述的總時長要對齊 4–15 秒 | `ayase0307/h3-video-prompting`（MIT；整理官方飛書手冊與社群實測）：純文字 prompt 300–700 英文字，「太短＝沒東西可參考」；有參考素材（首格）時字數要縮、只寫新變化；每個 shot 一個主動作、一個運鏡；對白 15 秒約 20 英文字 | 官方 I2VA 範例的 `integrated_multimodal_description` 82 字、T2VA 範例 86 字；GitHub README 的 T2VA 範例 379 字、I2VA 範例 724 字（2026-10-05 數的） |
| Hailuo 2.3（API i2v、網頁 2.3） | `prompt` ≤ 2,000 字元；15 個方括號運鏡指令，一個括號內同時生效、建議最多 3 個；`prompt_optimizer` 預設 true（platform.minimax.io/docs/api-reference/video-generation-i2v，無日期，2026-10-05 讀）。沒有甜蜜點 | 無專屬數字；產線的寫法是一個方括號加一句動作，6 秒一個運鏡（`.agents/skills/animation-preproduction/references/route-decisions.md` 第六節） | — |
| Kling 2.x ／ 3.0（API、網頁） | VIDEO 3.0 user guide（kling.ai/quickstart/klingai-video-3-model-user-guide，2026-02-06，2026-10-05 讀）沒有字數，只有範例。API 的 `prompt` 與 `negative_prompt` 各 ≤ 2,500 字元：現行 kling.ai/document-api 的頁面是 SPA，2026-10-05 抓到的只有標題；數字來自已停更的官方文件（docs.qingque.cn「可靈AI API 接口文档」，2024-09-19 的變更紀錄「不超過2500個字符」，文件最後更新 2025-06-19） | `smixs/visual-skills` 的 `video/references/kling.md`（CC BY 4.0，Serge Shima）：2.5 Turbo Pro 3–4 個元素、50–80 字；2.6 Pro 5–7 個元素、50–80 字；3.0 歡迎長一點，多鏡要明寫結構、每個 shot 約 30–60 字；圖生影片不分版本 20–40 字、只寫動作，「Long prompts on 1.x – 2.x = melted outputs」 | 官方 3.0 指南的範例：圖生影片短例 31 字、辦公室一鏡到底 220 字、兩個 15 秒範例 216 與 317 字 |
| Veo 3.1 ／ 3.1 Fast ／ 3.1 Lite（產線 Lite） | 三個模型的 Text input 都是 1,024 tokens（ai.google.dev/gemini-api/docs/veo 的模型表，頁面 2026-09-17 更新，2026-10-05 讀）。Veo 提示指南（docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide；舊址 cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide 轉址過去，頁面 2026-10-01 更新，2026-10-05 讀）沒有字數；給的是結構：subject、action、scene／context、camera angles、camera movements、lens、visual style、temporal、audio；negative prompt 不寫 no／don't，寫名詞清單（「wall, frame」） | smixs 的 `video/references/veo.md`：「Sweet spot. 50-200 words」，短＝創作空間大、長＝控制緊但易自相矛盾；「Prompt too long, model cherry-picks」的修法是壓到 50–100 字或改 JSON。2026-10-05 的研究另記 Veo 3.1／Sora 2 100–250 字，今天沒有在列名的來源裡找到原句，當次級 | — |
| Gemini Omni 1.1 Flash（產線預設片段模型） | 無字數；模型表（ai.google.dev/gemini-api/docs/models，2026-10-05 讀）只列端點。提示指南（ai.google.dev/gemini-api/docs/omni，2026-09-23 更新，2026-10-05 讀）：**預設會自己切成幾個鏡頭**，要單鏡得寫「In a single unbroken scene」「In a single continuous shot」「No scene cuts」；編輯用簡單句，「Overly descriptive prompts can lead to unintended changes」；時間可寫 `[0-3s]`；上面那份 Veo 指南同時涵蓋 Omni | 無專屬數字 | 產線 `look.motion` 的預設句寫 `no cuts`（否定句），不是官方建議的正向句（`tools/video/core/drama.mjs` 的 `PRESETS`）；錯誤目錄 #65 |
| 其他（產線不用） | — | 2026-10-05 的研究記的次級數字：Seedance 2.x hero shot 200–400 字、LTX-2 ≤ 80、Runway Gen-4 ≤ 60，今天沒有重新找到出處。`A-cat-with-carrots/OnlyShot`（MIT）對即夢（Seedance）CLI 的實測：字元 ≤ 1,500（1,200–1,400 理想），超過回 `ret=1046 InvalidNode`，作者自己標明不是官方常數 | — |

讀法：官方只給上限，沒有一家給甜蜜點；甜蜜點全是社群的，而且算的是英文字。產線的 `prompt` 1000 字元（約 150 英文字，估）落在每一家的甜蜜點裡；H3 網頁正文由 `shot_plan.mjs` 組，它的 `chars` 欄看一眼就知道離 7,000 多遠。

### 疊加物不是景深

標題、字卡、HUD、箭頭、字幕、浮水印、AIGC 標示都是後製：字幕由 `assemble` 燒（`subtitles.burn_in`），要看的字另外合成（`.agents/skills/youtube-video/references/animation-production.md` 的 text 規則）。它們**不向影片模型要，也不寫進 prompt 的前景／中景／背景**：模型會把它們畫成場景裡的物件（試拍 S03 R02 的英文標籤與簽名筆畫，`model-misreads.md` 第一節；judge 的 `no_text` 題扣分），而且畫出來的字對不上後製的字型與位置。佐證（除 H3 官方指南外都是社群，標名）：

- H3 官方指南把「真的在畫面裡的字」（banner、sign、label、subtitle、neon）寫成英文雙引號逐字——那是場景物件的規則，不是疊加物的；`ayase0307/h3-video-prompting` 的失敗分診：「HUD elements」「some labels」沒逐字打出就變噪音；字幕跑出來時「不要在 prompt 寫『不要字幕』」（否定句被畫出來），修法是減少台詞、後期。
- `A-cat-with-carrots/OnlyShot` 的即夢 case G：寫「彈幕刷屏」三次被畫成三個相同字標；它的字幕與 AIGC 標示都在剪映後製。
- `smixs/visual-skills` 的 Kling 負面欄範例列 `watermark, subtitles, logo, text overlay`——Kling 有獨立負面欄才這樣寫，寫進正文就是否定句。
- `LearnPrompt/awesome-seedance` 有「HUD 與直播疊層」模板：疊層本身就是畫面的類型，釘在固定位置、數字跟著動作變；那是另一種片，不是漫劇。

例外只有劇情裡實體存在的字（招牌、信封上的字）：它是場景物件，要可讀就另外合成，prompt 寫 `blank`、`no writing on the page`。

## 例子

每列是一行 `camera`，後面是四個函式讀出的結果：`shotSize`（只給 `camera`，沒有 `prompt`）、craft 的 `cameraMove`（`none` 寫 `-`）、slides 的 `cameraMove`、assemble 的 `motionMove().name`，以及 assemble 會不會對第 0 格算 PSNR（`startsAtIdentity`）。前 23 列是寫法示範與陷阱，接著是試拍的原句，最後兩列是靜圖常見的寫法。`tools/animation-camera.test.mjs` 逐列驗。

```
| camera line | craft size | craft move | slides move | assemble move | PSNR-checked |
| --- | --- | --- | --- | --- | --- |
| `Wide shot, locked` | `ws` | `locked` | `locked` | `locked` | `yes` |
| `Medium shot, slow push in` | `ms` | `push` | `push in` | `push-in` | `yes` |
| `Medium close-up` | `mcu` | `-` | `drift` | `drift` | `yes` |
| `Close-up, slow pull back` | `cu` | `pull` | `pull out` | `pull-out` | `no` |
| `Insert, locked` | `insert` | `locked` | `locked` | `locked` | `yes` |
| `Close-up of the pen hand` | `insert` | `-` | `drift` | `drift` | `yes` |
| `Close-up of his face, slow push in` | `cu` | `push` | `push in` | `push-in` | `yes` |
| `Over-the-shoulder on Chen, locked` | `ots` | `locked` | `locked` | `locked` | `yes` |
| `Two-shot, static` | `group` | `locked` | `locked` | `locked` | `yes` |
| `Extreme close-up of her eyes` | `ecu` | `-` | `drift` | `drift` | `yes` |
| `Wide shot, pan left along the counter` | `ws` | `pan` | `pan left` | `pan-right` | `no` |
| `Wide shot, pan right` | `ws` | `pan` | `pan right` | `pan-left` | `no` |
| `Wide, left to right` | `ws` | `-` | `pan left` | `pan-right` | `no` |
| `Medium shot, tilt up to his face` | `ms` | `tilt` | `tilt up` | `tilt-up` | `no` |
| `Wide shot, crane down` | `ws` | `tilt` | `tilt down` | `tilt-down` | `no` |
| `Medium shot, handheld` | `ms` | `track` | `drift` | `drift` | `yes` |
| `Static, slight handheld drift` | `-` | `locked` | `drift` | `drift` | `yes` |
| `Slow orbit around the table` | `-` | `track` | `drift` | `drift` | `yes` |
| `Medium close-up, slow zoom` | `mcu` | `push` | `drift` | `drift` | `yes` |
| `Medium close-up, zoom in` | `mcu` | `push` | `push in` | `push-in` | `yes` |
| `Wide shot, dolly out` | `ws` | `pull` | `drift` | `drift` | `yes` |
| `Medium shot as she pushes the box back` | `ms` | `-` | `push in` | `push-in` | `yes` |
| `Close-up; the paper rises in frame` | `cu` | `-` | `tilt up` | `tilt-up` | `no` |
| `Medium close-up, fixed` | `mcu` | `-` | `locked` | `locked` | `yes` |
| `Medium shot, fixed camera, she rises from the chair` | `ms` | `locked` | `locked` | `locked` | `yes` |
| `Wide shot, truck right along the table` | `ws` | `track` | `drift` | `drift` | `yes` |
| `Medium close-up, no camera move` | `mcu` | `locked` | `locked` | `locked` | `yes` |
| `POV from the doorway, slow push in` | `pov` | `push` | `push in` | `push-in` | `yes` |
| `Overhead insert of the hands, tripod` | `insert` | `locked` | `locked` | `locked` | `yes` |
| `Overhead close-up of the hands, locked` | `insert` | `locked` | `locked` | `locked` | `yes` |
| `Locked medium close-up; full face, suit and pen-holding hand remain visible.` | `mcu` | `locked` | `locked` | `locked` | `yes` |
| `Locked view through the door gap.` | `-` | `locked` | `locked` | `locked` | `yes` |
| `Locked wide enough to separate original and retained copy.` | `ws` | `locked` | `locked` | `locked` | `yes` |
| `Locked table-height two-position framing; only bride identifiable.` | `-` | `locked` | `locked` | `locked` | `yes` |
| `Medium close-up, drift` | `mcu` | `-` | `drift` | `drift` | `yes` |
```

讀法：`Locked view through the door gap.` 與 `Locked table-height two-position framing` 都沒有景別（view、table-height 不在 `LEADING_QUALIFIER`，後面也沒有景別片語），算進 `size.named`；`Static, slight handheld drift` 三個讀者各讀各的；`Medium shot as she pushes the box back` 在 craft 眼裡沒有運鏡，在 assemble 眼裡是推近。
