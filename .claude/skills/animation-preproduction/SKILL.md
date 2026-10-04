---
name: animation-preproduction
description: AI 動畫開拍前的企劃與鎖定：在付 Hailuo、Kling 或伺服器任何點數之前，先把分場與節拍、鏡位與剪點、每鏡做法（clip、still、切素材）、路線與買幾秒、首尾格、AI 風險分級與重設計、預算的期望與上限、文字卡動態分鏡、小樣計畫、批次順序與備料清單一次排好，交站主確認一次後鎖定；之後的設定圖、配音、關鍵影格、小樣與批量照包做，改動一律走變更單。使用者說先規劃、分鏡表、鏡位表、動態分鏡、animatic、開拍前確認、估一集、怎麼省成本、照真一隻布袋喵的做法，或要改已鎖定的鏡頭時先讀，再交給 animation-production 製作。Plan, risk-grade, price and lock an AI animated episode before paying for anything, then hold every later change to a change order.
metadata:
  short-description: 動畫前期：分鏡表、風險、動態分鏡、開拍鎖定、變更單
---

# 動畫前期（animation-preproduction）

動畫業的老規矩：「真人電影是先拍再剪；動畫是先剪好再拍。」（Pixar 剪接師 Ken Schretzmann 的話，業界訪談）AI 動畫更是這樣：每一支素材都要付錢、模型不會回頭問你哪裡不清楚，**邊做邊改是最貴的做法**。這個 skill 把一集從「劇本核准」帶到「站主在花錢之前確認一次的開拍鎖定包」，之後照包交給 `.agents/skills/animation-production/SKILL.md` 製作。三個 animation skill 的分工：

- **animation-preproduction（這篇）**：決定與鎖定——每一鏡做不做、怎麼做、走哪條路、花多少、照什麼順序；鎖定後的變更單。
- **animation-camera**：一鏡怎麼寫——`camera`、`prompt`、`motion` 三欄被程式與模型怎麼讀。
- **animation-production**：花錢與收據——每個付費階段的前提、結束碼、帳本、錯誤目錄、檢討。

數字一律標來源：**官方**（官方頁或官方指南，附讀取日）、**實測**（站主帳號上真的扣過、量過）、**量到的**（參考片量測）、**工具規定**（程式常數，附檔名）、**推算**、**編輯判斷**。路徑相對 repo 根目錄；一集的工作目錄在 repo 外（`<VIDEO_WORKDIR>/<SLUG>/`）。

## 什麼時候用、什麼時候不用

- 用：任何會花錢做動畫之前（設定圖、配音、關鍵影格、伺服器 `clips`、Hailuo 網頁、Kling 網頁或 CLI）；站主說「先規劃」「先確認再做」「分鏡表」「動態分鏡」「這集要多少錢」；鎖定之後有人要改鏡頭、台詞、look、聲音或路線。
- 不用：主機工人自動跑的集（它照 `tools/video/automation/flow.mjs`）；沒有片段的插畫投影片與品牌故事；只是寫一鏡的欄位（`animation-camera`）；已經在照包製作、要查結束碼或報帳（`animation-production`）。

## 先讀

| 要做的 | 讀 |
| --- | --- |
| 各步的範本（條件卡、分場表、鏡位表、分鏡表欄位、鎖定包、變更單）與一個做完的例子 | `.agents/skills/animation-preproduction/references/preproduction-flow.md` |
| 每鏡走哪條路、買幾秒、哪個解析度、母鏡頭、正文怎麼寫（Hailuo H3／2.3、Kling 3.0 的官方格式）、送出前的表單清單 | `.agents/skills/animation-preproduction/references/route-decisions.md` |
| AI 鏡頭風險分級的表、重設計的招式、參考片怎麼避開 | `.agents/skills/animation-preproduction/references/shot-risk.md` |
| 參考風格：真一隻布袋喵的量測（鏡長、景別、接觸與台詞怎麼處理） | `docs/videos/drama-craft/reference-study-20261004-budaimiao.md`；畫風與表演的創作建議在 `.agents/skills/animation-camera/references/budaimiao-style.md` |
| 一場戲的鏡位、軸線、連戲帳 | `.agents/skills/animation-camera/references/scene-coverage.md` |
| 對話戲的開場、鏡長、台詞規格與檢查腳本 | `.agents/skills/youtube-video/references/drama-craft.md` |
| 小樣怎麼看、冷看、何時才放量 | `.agents/skills/youtube-video/references/visual-quality.md` |

## 成本階梯：每個決定最晚在哪一層之前定

改一個決定的代價，取決於它已經被哪些付費產物「綁」住。產線用雜湊綁（`tools/video/core/drama.mjs` 的 `lookHash`、`tools/video/core/timeline.mjs` 的 `visualHash` 與 `speechHash`、`script` 關卡綁的 `script.md`），所以這張表是工具規定，不是建議：

| 決定 | 最晚在 | 過了再改要付 |
| --- | --- | --- |
| look（style、negative、motion、candidates）、角色 appearance、sheet_prompt | `look` 之前 | **全部**：設定圖、每張關鍵影格、每支素材 |
| 台詞文字、speaker、emotion、停頓、`action_seconds`、角色的名字與聲音 | `tts` 之前 | 那幾句的 TTS（聲音或詞庫改了是整個角色）；script 與 audio 核准；買的秒數可能跟著變 |
| 每一鏡的 `prompt`、`camera`、`characters`、`character_looks`、末格 | `keyframes` 之前 | 那一鏡的關鍵影格重畫重 judge（最多 3 take）＋下一列的全部 |
| 每一鏡的 `motion`、`source`、`chapter`、縮圖 | `keyframes` 之前 | 關鍵影格不重畫（#1193 起只有畫面請求或 judge 題目變了的那一鏡才重畫），但 keyframes manifest 改寫 → storyboard 核准失效；伺服器買的每一支素材再 judge 一次（從快取拿回）；已匯入的外部片段全部重匯（clips manifest 從空的重建） |
| 路線、模型、解析度、買幾秒、首尾格、網頁的定稿正文 | 送出第一支之前 | 已買的那幾支 |

所以**動作與運鏡要在畫關鍵影格之前定稿**：`motion` 圖片模型不讀，但它在 `scene.data` 裡、`visualHash` 綁整個 `data`，改一個字就要重送 storyboard、重 judge 素材、重匯外部片段。

另一條動畫業的規矩是**先錄音、後動畫**：每一鏡要買幾秒，等 `tts` 錄完、用實際的 `timeline.json` 量，不靠 lint 的估法（實測過偏差 7%，`.agents/skills/youtube-video/references/automated.md`）。鎖定時用估的秒數，錄完配音後 `--check` 看買的秒數有沒有變。

## 前期與製作的順序

站主要的是「開拍前整個確認」，所以**唯一一次整體確認在花任何錢之前**（P7）。之後的設定圖、配音、關鍵影格、小樣都照鎖定包做；它們各自原本就有的關卡（look、audio、storyboard）與小樣後的檢查點照常看，不是新的逐鏡核准。

| 步 | 產出 | 工具 | 過關條件 |
| --- | --- | --- | --- |
| P0 製作條件卡 | 作品、路線、有沒有 production profile（決定外部片段收不收得進來）、交片規格、預算上限與預留、take 上限、AI 潤飾開或關、期限 | 人；`episode_estimate.mjs --plan …` 粗估（沒有尾巴把手，比 P4 少一點） | 每格有值；profile 作品不寫網頁路線 |
| P1 劇本鎖定 | 核准的 `script` 關卡 | `tools/video/cli.mjs lint`、`drama_craft_check.mjs` | lint 零錯、craft 列過或逐列回答 |
| P2 分場與節拍 | 每場：目的、轉折、地點、時間、光與色（整集的色彩腳本）、出場角色與道具 | 人 | 每場一句「觀眾在這場新知道什麼」 |
| P3 鏡位設計 | 每場的軸線、鏡位 A/B/C…、哪個是母鏡頭、哪幾鏡切素材、全景什麼時候回來 | `scene-coverage.md`；`shot_plan.mjs` 的鏡位代號 | 對話場 4–6 個鏡位、回到同鏡位的寫 `source`；打鬥場插鏡多，鏡位數不是目標 |
| P4 分鏡表與製作規格 | 每鏡：類型、路線、買幾秒、首尾格、定稿正文、點數 | `shot_plan.mjs`；`shot_reading.mjs --route <同一條>` | `shot_plan --strict` 沒有問題；`shot_reading --strict` 沒有陷阱 |
| P5 風險分級與重設計 | 每鏡 A／B／C 與原因；C 級改掉或放進小樣 | `shot_plan.mjs`、`shot-risk.md` | C 級只剩劇情非要不可的，且在小樣裡（`--strict` 會報不在小樣裡的 C） |
| P6 文字卡動態分鏡 | 實速可看的文字卡版 | `animatic.mjs` | 節奏、資訊順序、開場 10／30 秒、空間與視線沒問題；冷看的人看得懂 |
| **P7 開拍鎖定** | 鎖定包（下一節）＋`plan_lock.mjs --ready` 的「還要做的事」 | `plan_lock.mjs --ready`，站主點頭後 `--write` | **站主確認一次** |
| 製作 1 | 設定圖 → look 關卡；配音 → audio 關卡 | `animation-production` | 照包；改動走變更單 |
| 製作 2 | 關鍵影格 → 關鍵影格版動態分鏡 → storyboard 關卡 | `keyframes`、`animatic.mjs` | 站主看動態分鏡過 storyboard（既有關卡） |
| 製作 3 | 小樣（批次第一批）→ 檢查點 | `browser-production.md`、`clips import` | 身份、動作、剪接、匯入都過；站主看過才放量 |
| 製作 4 | 其餘批次 | 同上 | 每場一個檢查點 |

小樣的結果若要改鎖定的東西（換路線、改秒數、改正文），走變更單、重鎖；只是回填實際點數與時間，寫進 `route-decisions.md` 的表與回報。

## 專業判斷

**鏡位先於鏡頭。** 一場戲先決定攝影機站在哪幾個位置（全景／主鏡、每個說話者的中近景、反應、過肩、插鏡），再決定每句台詞剪到哪個位置。業界的精簡拍法一場對話 4–6 個鏡位；對話參考片一場三、四個鏡位但兩秒換一次畫面（`drama-craft.md` 第二節）。每場先定全景（主鏡）的關鍵影格、從它寫連戲帳，其他鏡位照它畫。

**每一鏡的做法依序問**（細節在 `route-decisions.md` 第二節）：profile 有沒有 → 需不需要模型做動作（不需要就 still＋運鏡）→ 是不是回到同鏡位（`source` 切）→ 無聲動作拍（`action_seconds`）→ 剩下的才買素材，再選路線。

**買幾秒**：需要的秒數（實際配音）＋0.5 秒尾巴把手；圖生影片沒有頭的把手（第 0 格是關鍵影格）。網頁照秒計價，所以一鏡一件事、鏡頭短，反而便宜；伺服器 Lite 永遠 8 秒，短鏡頭不省。

**母鏡頭**：一個鏡位會回來兩三次，就把第一次買長一點，後面切它。省下的不只是秒數，是少了要抽卡的鏡頭（`route-decisions.md` 第五節）。

**AI 風險**：手指拿小道具、兩人接觸、吃喝、變身、要讀的字最容易壞。在分鏡上用「騙鏡」改掉：切在動作兩端、反應替代動作、台詞放在聽者臉上、首尾格定住變化（`shot-risk.md`）。業界報導的一鏡可用率是 20–30%（第三方），而 take 上限是 2：只有把難鏡在前期改掉，兩次才夠。

**預算兩個數**：期望（每鏡一次的價 × 該級預期 take：A 1.2、B 1.5、C 2，編輯判斷，不超過 take 上限；`--expected-takes` 可改）與上限（× take 上限）。鎖定包寫兩個數加一成預留（業界常見的風險預留，第三方）；實際花到期望值就停下來看，碰到上限就停。拿 `--expected-takes 2,3,4` 跑一次看最壞情況要多少。

**參考風格**：站主指定「真一隻布袋喵」的做法時，先讀它的量測（`docs/videos/drama-craft/reference-study-20261004-budaimiao.md`）：那個頻道把接觸、說話的嘴、細手部動作幾乎都設計掉了，打鬥靠插鏡、閃光、特效與反應鏡剪出來（`shot-risk.md` 的最後一節）。它的極快剪接（中位數不到 1 秒）產線還做不到（`tasks/open/2026-10-04-drama-montage-beats-flash-cuts.md`）；對話戲照 `drama-craft.md` 的目標。

## 動態分鏡（animatic）

業界的「一支活的 animatic」：同一支片子從文字卡、關鍵影格一路換成買到的素材，節奏走樣馬上看得到。`animatic.mjs` 做的就是這件事：

- 時間照錄好的 `timeline.json`（沒有就 lint 估，頁面標「估計」），有 `narration.wav` 就同步播。
- 每鏡顯示：買到的素材（`clips/manifest.json` 沒標 needs_review 的）→ 關鍵影格（在圖上模擬推、拉、搖、俯仰，方向照攝影機：pan left 畫面往右跑）→ 文字卡（鏡號、景別、動作、台詞、類型、風險）。
- 頁面上方印鏡數、中位數、最長、前 10／30 秒開始幾鏡，對 `drama-craft.md` 的目標。
- 看什麼：先實速從頭看一次，不停；再逐鏡看。開場 10 秒內有沒有事、每鏡給不給新資訊、誰在哪一邊、視線接不接、全景多久回來一次、哪裡等太久。冷看照 `visual-quality.md` 第四節，請沒參與分鏡的人說他看懂了什麼。
- `--mp4` 在每鏡都有圖時接成一支 1080p 影片（站主不方便開本機 HTML 時用）。

## 小樣

`shot_plan.mjs` 的批次第一批就是小樣：同一場連續三鏡，買素材的鏡頭裡有台詞鏡與無聲動作拍、風險分數最高的一段（切鏡的來源一起買）；`--pilot s04,s05,s06` 指定。小樣是**一條路線、一個模型、一個檔位**的三鏡；想比另一家，最多另選一鏡，在鎖定包裡另列一行（路線、這一鏡的點數與上限、`shot_plan.mjs --route <另一家>` 的正文與 SHA-256、take 上限 1），站主點頭才做，它不剪進小樣、只決定 `route-decisions.md` 那一列。目的與失敗條件寫在鎖定包裡（`visual-quality.md` 第三節）：身份、主動作、兩鏡之間的剪接、首格 PSNR 與匯入、實際點數與時間。

## 開拍鎖定包：站主在花錢之前確認一次

`animation-production` 與 `visual-quality.md` 都說「不逐鏡新增核准、不重問已有的授權」；站主要的是「開拍前整個確認」。兩件事不衝突：**整集只在花錢之前確認一次**，確認的是下面這一包，之後照包做，不再逐鏡問；包外的事（超預算、改鎖定的東西、未解的重大缺陷）才再問。

1. 製作條件卡（P0），含 AI 潤飾開或關。
2. 分鏡表（`shot_plan.mjs --markdown`）：每鏡的類型、路線、買幾秒、首尾格、風險、點數，與要貼的定稿正文；負面欄的處理（網頁真的有才貼 `look.negative`，不寫進正文）。
3. 文字卡動態分鏡（`animatic.mjs`）的連結與冷看意見。
4. 小樣計畫：哪三鏡、目的與失敗條件、take 上限、點數上限；另一家比較（如果要）另列一行。
5. 預算：設定圖、配音、關鍵影格（伺服器端）與片段的期望、上限、預留；本月方案額度占多少。
6. 批次順序與每批之後的檢查點；停損規則（同一缺陷重複、到 take 上限、結果不明、花到期望值就停那一鏡）。
7. `plan_lock.mjs --ready` 的結果：程式查得到、現在還沒做到的（關卡、配音、關鍵影格）列成「製作中要完成的」；人工項目（帳號、餘額、上傳的路、表單設定）列成送第一支之前的清單。
8. 還沒驗的事與它們的風險。

站主點頭之後 `plan_lock.mjs --write --note "<站主的原話>" --assist on|off`（加上跟 `shot_plan.mjs` 同一組規劃旗標），把雜湊、每鏡的定稿正文與 SHA-256、路線與設定、小樣、預算寫進 `<workdir>/plan/lock.json`。送出第一支素材之前再跑一次 `--ready`，程式項要全過。

## 備料清單（送第一支之前到位）

`plan_lock.mjs --ready` 查程式查得到的：鎖定與現況一致、script／look／audio／storyboard 關卡、配音 timeline 綁著現在的台詞、keyframes manifest 綁著現在的 look 與畫面、每個要買素材的鏡頭都有通過的首格（計畫的末格也畫了）、profile 收不收外部片段。人工打勾的：帳號與方案、餘額 ≥ 期望＋預留、首格上傳的路（依當次瀏覽器工具確認；2026-10-04 Claude 桌面版內建瀏覽器傳不了本機圖，當時的替代是站主同意後用 Claude in Chrome 的 `file_upload`，或站主手動）、表單設定（`route-decisions.md` 第七節）、AI 潤飾照鎖定、無浮水印下載、收據檔、`drama_preflight.mjs --stage clips` 沒有 refuse。

## 批次順序與停損

1. 小樣三鏡 → 站主看過才往下。
2. 依場：每場先母鏡頭（切鏡等它）、再 C、B、A（早失敗、早改設計）；切鏡與 still 不買素材。
3. 第一場做完是檢查點：用 `animatic.mjs` 把買到的素材換進去實速看，查漂移與連戲，再開下一場。
4. 照併發送：Hailuo Pro 以上 2 支同時、排隊 8–12（官方方案表）；Kling 排隊不限、輸出數 1。每支一筆收據（`animation-production` 的 `browser-production.md` 第四節），收據的正文 SHA-256 要等於鎖定檔的（這一項人工對，`--check` 不讀收據）。
5. 停：同一鏡同一缺陷出現兩次、到 take 上限、結果不明（先查任務紀錄與餘額，不重按）、花到期望值。停的是那一鏡，不是整批；其他鏡照做。網頁上被退掉、沒匯入的 take 不在 `run_report.mjs` 裡，回填預期 take 時從收據數。

## 變更控制

鎖定之後任何人要改東西，先 `plan_lock.mjs --check`：它對照鎖定檔印出變更單——哪幾鏡的畫面欄位、台詞或定稿正文變了、哪個雜湊動了（look、visual、speech、script）、哪幾張關鍵影格要重畫、要重付幾次 judge、哪個**已核准**的關卡失效、哪些外部片段要重匯；給了規劃旗標就也比路線與設定（換路線、換解析度也是變更）。做法：

- 改動先攢齊，給站主看變更單、點頭，一次改完，再 `--write --force` 重鎖（沒給旗標就沿用鎖定的設定；舊的鎖定檔留在旁邊，變更記在 `plan/changes.jsonl`）。
- 批次進行中不為單鏡改字：那一鏡停下、記下問題，這一批其他鏡做完再一起改。
- 業界的區分：還沒鎖的階段裡修改是正常工作；改**已鎖**的東西才是變更，要記錄誰要求、動到什麼、花多少、誰決定。

## 腳本

三支都離線、不花錢、不碰伺服器，從 `tools/video` 與 `animation-production` 的 `episode_estimate.mjs` 匯入（伺服器與方案的價目在那裡；Hailuo 網頁各模型的價在 `shot_plan.mjs` 的 `HAILUO_MODELS`）；argv 只用 ASCII。規劃旗標三支共用（`PLAN_FLAGS`），`plan_lock` 鎖的就是 `shot_plan` 算的那一份。

```bash
# 分鏡表與製作規格：每鏡類型、鏡位代號、路線、買幾秒、首尾格、風險、點數，定稿正文，批次順序與槓桿；--strict 有問題結束碼 1
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs <VIDEO_DOCS>/video.json | --slug <SLUG> [--workdir <dir>] [--route server|hailuo|kling] [--plan hailuo:pro|kling:pro|...] [--hailuo-model h3|2.3] [--resolution 1080p|720p|768p|2k] [--timeline <timeline.json>] [--handle 0.5] [--clip-takes 2] [--expected-takes 1.2,1.5,2] [--pilot s04,s05,s06] [--production] [--markdown|--csv|--json] [--strict]
# 動態分鏡：HTML（文字卡→關鍵影格→買到的素材），--mp4 在每鏡都有圖時接成影片（缺圖結束碼 1，沒有 ffmpeg 5）
node .agents/skills/animation-preproduction/scripts/animatic.mjs --slug <SLUG> | --file <video.json> [--workdir <dir>] [--out <animatic.html>] [--mp4 <animatic.mp4>] [規劃旗標]
# 開拍鎖定、變更單、備料清單：--check 有變更、--ready 有沒過、--write 的計畫做不進產線都是 1；鎖定檔讀不懂是 2
node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>  --write [--note "..."] [--assist on|off] [--force] | --check | --ready  [規劃旗標]
```

`--slug` 時工作目錄照 `tools/video` 的規則（`VIDEO_WORKDIR`），`--workdir` 是放所有影片的目錄；給檔案時 `--workdir` 是這一支影片自己的工作目錄。`tools/animation-preproduction.test.mjs` 盯著：`shot-risk.md` 的表等於 `RISK_RULES`、每條風險的對例與反例（含打鬥用字）、各路線買幾秒、H3／2.3／Kling 正文格式、profile 擋網頁路線、鎖定抓得到 `motion` 改一個字而不誤報重畫關鍵影格、換聲音也算變更、舊版鎖定檔讀不懂、animatic 的長度、跳脫與運鏡方向。

## 還沒驗、不能宣稱的事

- 預期 take（A 1.2、B 1.5、C 2）是編輯判斷；第一集做完用收據與 `run_report.mjs` 的每鏡 take 回填。
- 風險級只讀文字：模型可能一次過一個 C，也可能在 A 上抽到六根手指；過了也要實速看。
- Kling 的點數是官方價目、Hailuo 2.3 的價是官方 FAQ、H3 768P 的每秒點數是推算，都還沒在站主帳號實扣；兩家誰做動作比較穩沒比過；用產線關鍵影格當首格的圖生影片在兩家都還沒送過（`tasks/open/2026-10-04-paid-verification-hailuo-kling-web.md`）。
- 母鏡頭切三次、0.5 秒尾巴把手、動態分鏡在圖上模擬的運鏡，都是編輯判斷，沒有實拍對照。
- 有 production profile 的作品（十部動畫）走 Hailuo／Kling 還不行：`clips import` 拒收（`tasks/open/2026-10-04-profile-works-external-clip-route.md`）。
