---
name: animation-preproduction
description: AI 動畫開拍前的企劃與鎖定：在付 Hailuo、Kling 或伺服器任何點數之前，先把分場與節拍、鏡位與剪點、每鏡做法（clip、still、切素材）、路線與買幾秒、首尾格、AI 風險分級與重設計、預算的期望與上限、動態分鏡、三鏡小樣、批次順序與備料清單一次排好，交站主確認一次後鎖定；鎖定後的改動一律走變更單。使用者說先規劃、分鏡表、鏡位表、動態分鏡、animatic、開拍前確認、估一集、怎麼省成本、照真一隻布袋喵的做法，或要改已鎖定的鏡頭時先讀，再交給 animation-production 批量製作。Plan, risk-grade, price and lock an AI animated episode before paying for any clip, then hold every later change to a change order.
metadata:
  short-description: 動畫前期：分鏡表、風險、動態分鏡、開拍鎖定、變更單
---

# 動畫前期（animation-preproduction）

動畫業的老規矩：「真人電影是先拍再剪；動畫是先剪好再拍。」（Pixar 剪接師 Ken Schretzmann 的話，業界訪談）AI 動畫更是這樣：每一支素材都要付錢、模型不會回頭問你哪裡不清楚，**邊做邊改是最貴的做法**。這個 skill 把一集從「劇本核准」帶到「站主確認一次的開拍鎖定包」，之後才交給 `.agents/skills/animation-production/SKILL.md` 批量製作。三個 animation skill 的分工：

- **animation-preproduction（這篇）**：決定與鎖定——每一鏡做不做、怎麼做、走哪條路、花多少、照什麼順序。
- **animation-camera**：一鏡怎麼寫——`camera`、`prompt`、`motion` 三欄被程式與模型怎麼讀。
- **animation-production**：花錢與收據——每個付費階段的前提、結束碼、帳本、錯誤目錄、檢討。

數字一律標來源：**官方**（官方頁或官方指南，附讀取日）、**實測**（站主帳號上真的扣過、量過）、**量到的**（參考片量測）、**工具規定**（程式常數，附檔名）、**推算**、**編輯判斷**。路徑相對 repo 根目錄；一集的工作目錄在 repo 外（`<VIDEO_WORKDIR>/<SLUG>/`）。

## 什麼時候用、什麼時候不用

- 用：任何會花錢做動畫片段之前（伺服器 `clips`、Hailuo 網頁、Kling 網頁或 CLI）；站主說「先規劃」「先確認再做」「分鏡表」「動態分鏡」「這集要多少錢」；鎖定之後有人要改鏡頭、台詞、look 或路線。
- 不用：主機工人自動跑的集（它照 `tools/video/automation/flow.mjs`）；沒有片段的插畫投影片與品牌故事；只是寫一鏡的欄位（`animation-camera`）；已經在批量製作、要查結束碼或報帳（`animation-production`）。

## 先讀

| 要做的 | 讀 |
| --- | --- |
| 九步的範本（條件卡、分場表、鏡位表、分鏡表欄位、鎖定包、變更單）與一個做完的例子 | `.agents/skills/animation-preproduction/references/preproduction-flow.md` |
| 每鏡走哪條路、買幾秒、哪個解析度、母鏡頭、正文怎麼寫（Hailuo H3／2.3、Kling 3.0 的官方格式）、送出前的表單清單 | `.agents/skills/animation-preproduction/references/route-decisions.md` |
| AI 鏡頭風險分級的表、重設計的招式 | `.agents/skills/animation-preproduction/references/shot-risk.md` |
| 參考風格：真一隻布袋喵的製作文法（量到的數字） | `.agents/skills/animation-camera/references/budaimiao-style.md` |
| 一場戲的鏡位、軸線、連戲帳 | `.agents/skills/animation-camera/references/scene-coverage.md` |
| 開場、鏡長、台詞的規格與檢查腳本 | `.agents/skills/youtube-video/references/drama-craft.md` |
| 小樣怎麼看、冷看、何時才放量 | `.agents/skills/youtube-video/references/visual-quality.md` |

## 成本階梯：每個決定最晚在哪一層之前定

改一個決定的代價，取決於它已經被哪些付費產物「綁」住。產線用雜湊綁（`tools/video/core/drama.mjs` 的 `lookHash`、`tools/video/core/timeline.mjs` 的 `visualHash` 與 `speechHash`），所以這張表是工具規定，不是建議：

| 決定 | 最晚在 | 過了再改要付 |
| --- | --- | --- |
| look（style、negative、motion、candidates）、角色 appearance、sheet_prompt | `look` 之前 | **全部**：設定圖、每張關鍵影格、每支素材 |
| 台詞文字、speaker、emotion、停頓、`action_seconds`、角色聲音 | `tts` 之前 | 那幾句的 TTS、audio 核准；買的秒數可能跟著變 |
| 每一鏡的 `prompt`、`camera`、**`motion`**、`characters`、`source`、`chapter`、縮圖 | `keyframes` 之前 | 那一鏡的圖與素材；**其他每一鏡的 judge 再付一次**、storyboard 核准失效、已匯入的外部片段要重匯 |
| 路線、模型、解析度、買幾秒、首尾格、網頁的定稿正文 | 送出第一支之前 | 已買的那幾支 |

最容易踩的是第三列：`motion` 圖片模型根本不讀，但它在 `scene.data` 裡、`visualHash` 綁整個 `data`，所以在關鍵影格畫完之後改一個字，manifest 就重建、全部重新 judge。**動作與運鏡要在畫關鍵影格之前定稿**。

另一條動畫業的規矩是**先錄音、後動畫**：每一鏡要買幾秒，等 `tts` 錄完、用實際的 `timeline.json` 量，不靠 lint 的估法（實測過偏差 7%，`.agents/skills/youtube-video/references/automated.md`）。

## 前期九步

| 步 | 產出 | 工具 | 過關條件 | 誰點頭 |
| --- | --- | --- | --- | --- |
| P0 製作條件卡 | 作品、路線、有沒有 production profile（決定外部片段收不收得進來）、交片規格、預算上限與預留、take 上限、期限 | 人；`episode_estimate.mjs --plan …` 粗估 | 每格有值；profile 作品不寫網頁路線 | 站主 |
| P1 劇本鎖定 | 核准的 `script` 關卡 | `tools/video/cli.mjs lint`、`drama_craft_check.mjs` | lint 零錯、craft 列過或逐列回答 | 站主（既有關卡） |
| P2 分場與節拍 | 每場：目的、轉折、地點、時間、光與色（整集的色彩腳本）、出場角色與道具 | 人 | 每場一句「觀眾在這場新知道什麼」 | — |
| P3 鏡位設計 | 每場的軸線、鏡位 A/B/C…、哪個是母鏡頭、哪幾鏡切素材、全景什麼時候回來 | `scene-coverage.md`；`shot_plan.mjs` 的鏡位代號 | 每場 3–6 個鏡位；回到同鏡位的寫 `source` | — |
| P4 分鏡表與製作規格 | 每鏡：類型、路線、買幾秒、首尾格、定稿正文、點數 | `shot_plan.mjs` | `--strict` 沒有問題；`shot_reading.mjs --strict` 沒有陷阱 | — |
| P5 風險分級與重設計 | 每鏡 A／B／C 與原因；C 級改掉或放進小樣 | `shot_plan.mjs`、`shot-risk.md` | C 級只剩劇情非要不可的，且在小樣裡 | — |
| P6 動態分鏡 | 文字卡版（免費）→ 定 look、錄配音、畫關鍵影格 → 關鍵影格版＋冷看 | `animatic.mjs` | 實速看過；開場 10／30 秒、節奏、空間與視線沒問題；冷看的人看得懂 | 站主看關鍵影格版（storyboard 關卡） |
| P7 三鏡小樣 | 同一場連續三鏡（含最難的那種）在選定路線上做出來、匯入、實速看 | `animation-production` 的 `browser-production.md`；`clips import` | 身份、動作、剪接、匯入都過；記下實際點數、時間、take | 站主 |
| P8 開拍鎖定包 | 上面全部＋預算期望與上限、批次順序、停損規則、備料清單、未驗事項 | `plan_lock.mjs --write`、`--ready` | 站主一次確認；`--ready` 程式項全過、人工項打勾 | **站主（唯一一次的整體確認）** |

P6 的文字卡版可以在 P3 之後就做（不用錢），節奏與資訊順序的問題在這裡改只要改字；關鍵影格版在 storyboard 關卡前做，改的是 `prompt` 與構圖。P7 之後如果改了 P4 的東西，回到 P4 重出表，不要邊做邊改。

## 專業判斷

**鏡位先於鏡頭。** 一場戲先決定攝影機站在哪幾個位置（全景／主鏡、每個說話者的中近景、反應、過肩、插鏡），再決定每句台詞剪到哪個位置。業界的精簡拍法一場對話 4–6 個鏡位；參考片一場三、四個鏡位但兩秒換一次畫面（`drama-craft.md` 第二節）。每場先定全景（主鏡）的關鍵影格、從它寫連戲帳，其他鏡位照它畫。

**每一鏡的做法依序問**（細節在 `route-decisions.md` 第二節）：profile 有沒有 → 需不需要模型做動作（不需要就 still＋運鏡）→ 是不是回到同鏡位（`source` 切）→ 無聲動作拍（`action_seconds`）→ 剩下的才買素材，再選路線。

**買幾秒**：需要的秒數（實際配音）＋0.5 秒尾巴把手；圖生影片沒有頭的把手（第 0 格是關鍵影格）。網頁照秒計價，所以一鏡一件事、鏡頭短，反而便宜；伺服器 Lite 永遠 8 秒，短鏡頭不省。

**母鏡頭**：一個鏡位會回來兩三次，就把第一次買長一點，後面切它。省下的不只是秒數，是少了要抽卡的鏡頭（`route-decisions.md` 第五節）。

**AI 風險**：手指拿小道具、兩人接觸、吃喝、變身、要讀的字，重拍不會收斂。在分鏡上用「騙鏡」改掉：切在動作兩端、反應替代動作、台詞放在聽者臉上、首尾格定住變化（`shot-risk.md`）。業界的抽卡率報告是一鏡可用 20–30%（第三方報導），而 take 上限是 2：只有把難鏡在前期改掉，兩次才夠。

**預算兩個數**：期望（每鏡一次的價 × 該級預期 take：A 1.2、B 1.5、C 2，編輯判斷；`--expected-takes` 可改）與上限（× take 上限）。鎖定包寫兩個數加一成預留（業界做法的常見值，第三方）；實際花到期望值就停下來看，碰到上限就停。

**參考風格**：站主指定「真一隻布袋喵」的做法時，鏡長、景別比例、開場、怎麼避開 AI 弱點照 `budaimiao-style.md` 的量測寫；那份是量過的數字，不是印象。

## 動態分鏡（animatic）

業界的「一支活的 animatic」：同一支片子從文字卡、關鍵影格一路換成買到的素材，節奏走樣馬上看得到。`animatic.mjs` 做的就是這件事：

- 時間照錄好的 `timeline.json`（沒有就 lint 估，頁面標「估計」），有 `narration.wav` 就同步播。
- 每鏡顯示：買到的素材（`clips/manifest.json` 沒標 needs_review 的）→ 關鍵影格（在圖上模擬推、拉、搖、俯仰）→ 文字卡（鏡號、景別、動作、台詞、類型、風險）。
- 頁面上方印鏡數、中位數、最長、前 10／30 秒開始幾鏡，對 `drama-craft.md` 的目標。
- 看什麼：先實速從頭看一次，不停；再逐鏡看。開場 10 秒內有沒有事、每鏡給不給新資訊、誰在哪一邊、視線接不接、全景多久回來一次、哪裡等太久。冷看照 `visual-quality.md` 第四節，請沒參與分鏡的人說他看懂了什麼。
- `--mp4` 在每鏡都有圖時接成一支 1080p 影片（站主不方便開本機 HTML 時用）。

## 三鏡小樣

`shot_plan.mjs` 的批次第一批就是小樣：同一場連續三鏡、風險分數最高的一段（切鏡的來源一起買）。目的與失敗條件寫在鎖定包裡再送（`visual-quality.md` 第三節）：要驗身份、主動作、兩鏡之間的剪接、首格 PSNR 與匯入、實際點數與時間。路線還沒定的那類鏡頭（例如 Hailuo 與 Kling 誰做大動作比較穩），小樣裡讓兩家各做同一鏡。小樣的結果寫回 `route-decisions.md` 的表與鎖定包，再寫鎖。

## 開拍鎖定包：站主確認一次

`animation-production` 與 `visual-quality.md` 都說「不逐鏡新增核准、不重問已有的授權」；站主要的是「開拍前整個確認」。兩件事不衝突：**整集只確認一次**，確認的是下面這一包，之後照包做，不再逐鏡問；包外的事（超預算、改鎖定的東西、未解的重大缺陷）才再問。

1. 製作條件卡（P0）。
2. 分鏡表（`shot_plan.mjs --markdown`）：每鏡的類型、路線、買幾秒、首尾格、風險、點數，與要貼的定稿正文。
3. 動態分鏡（`animatic.mjs`）的連結與冷看意見。
4. 小樣的結果（點數、時間、take、站主看過的那三鏡）。
5. 預算：期望、上限、預留；本月方案額度占多少。
6. 批次順序與每批之後的檢查點；停損規則（同一缺陷重複、到 take 上限、結果不明就停那一鏡）。
7. 備料清單（`plan_lock.mjs --ready`）。
8. 還沒驗的事與它們的風險。

站主點頭之後 `plan_lock.mjs --write --note "<站主的原話>"`，把雜湊、每鏡的定稿正文與 SHA-256、路線、預算寫進 `<workdir>/plan/lock.json`。

## 備料清單（開拍前到位）

`plan_lock.mjs --ready` 查程式查得到的：鎖定與現況一致、script／look／audio／storyboard 關卡、配音 timeline 綁著現在的台詞、keyframes manifest 綁著現在的 look 與畫面、每個要買素材的鏡頭都有通過的首格（計畫的末格也畫了）、profile 收不收外部片段。人工打勾的：帳號與方案、餘額 ≥ 期望＋預留、首格上傳的路（內建瀏覽器傳不了本機圖，用 Claude in Chrome 的 `file_upload` 或站主手動）、表單設定（`route-decisions.md` 第七節）、無浮水印下載、收據檔、`drama_preflight.mjs --stage clips` 沒有 refuse。

## 批次順序與停損

1. 小樣三鏡 → 站主看過才往下。
2. 依場：每場先母鏡頭（切鏡等它）、再 C、B、A（早失敗、早改設計）；切鏡與 still 不買素材。
3. 第一場做完是檢查點：用 `animatic.mjs` 把買到的素材換進去實速看，查漂移與連戲，再開下一場。
4. 照併發送：Hailuo Pro 以上 2 支同時、排隊 8–12；Kling 排隊不限但一次一份輸出。每支一筆收據（`animation-production` 的 `browser-production.md` 第四節）。
5. 停：同一鏡同一缺陷出現兩次、到 take 上限、結果不明（先查任務紀錄與餘額，不重按）、花到期望值。停的是那一鏡，不是整批；其他鏡照做。

## 變更控制

鎖定之後任何人要改東西，先 `plan_lock.mjs --check`：它對照鎖定檔印出變更單——哪幾鏡的畫面欄位、台詞或定稿正文變了、哪個雜湊、會重買哪些已畫已買的東西、要重付幾次 judge、哪個核准失效、哪些外部片段要重匯。做法：

- 改動先攢齊，給站主看變更單、點頭，一次改完，再 `--write --force` 重鎖（舊的鎖定檔留在旁邊，變更記在 `plan/changes.jsonl`）。
- 批次進行中不為單鏡改字：那一鏡停下、記下問題，這一批其他鏡做完再一起改。
- 業界的區分：還沒鎖的階段裡修改是正常工作；改**已鎖**的東西才是變更，要記錄誰要求、動到什麼、花多少、誰決定。

## 腳本

三支都離線、不花錢、不碰伺服器，從 `tools/video` 與 `animation-production` 的估價腳本匯入（不重寫價目）；argv 只用 ASCII；結束碼 0、1（有問題或有變更）、2（讀不到或參數錯）。

```bash
# 分鏡表與製作規格：每鏡類型、鏡位代號、路線、買幾秒、首尾格、風險、點數，定稿正文，批次順序與槓桿
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs <VIDEO_DOCS>/video.json | --slug <SLUG> [--route server|hailuo|kling] [--plan hailuo:pro|kling:pro|...] [--hailuo-model h3|2.3] [--resolution 1080p|720p|768p|2k] [--timeline <timeline.json>] [--workdir <dir>] [--handle 0.5] [--clip-takes 2] [--expected-takes 1.2,1.5,2] [--markdown|--csv|--json] [--strict]
# 動態分鏡：HTML（文字卡→關鍵影格→買到的素材），--mp4 在每鏡都有圖時接成影片
node .agents/skills/animation-preproduction/scripts/animatic.mjs --slug <SLUG> | --file <video.json> [--workdir <dir>] [--out <animatic.html>] [--mp4 <animatic.mp4>] [--route ...]
# 開拍鎖定、變更單、備料清單
node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>  --write [--note "..."] [--force] | --check | --ready  [--route ...] [--plan ...]
```

`--slug` 時工作目錄照 `tools/video` 的規則（`VIDEO_WORKDIR`），`--workdir` 是放所有影片的目錄；給檔案時 `--workdir` 是這一支影片自己的工作目錄。`tools/animation-preproduction.test.mjs` 盯著：`shot-risk.md` 的表等於 `RISK_RULES`、每條風險的對例與反例、各路線買幾秒、H3／2.3／Kling 正文格式、profile 擋網頁路線、鎖定抓得到 `motion` 改一個字、animatic 的長度與跳脫。

## 還沒驗、不能宣稱的事

- 預期 take（A 1.2、B 1.5、C 2）是編輯判斷；第一集做完用 `run_report.mjs` 的每鏡 take 回填。
- 風險級只讀文字：模型可能一次過一個 C，也可能在 A 上抽到六根手指；過了也要實速看。
- Kling 的點數是官方價目、Hailuo 2.3 的價是官方 FAQ，都還沒在站主帳號實扣；兩家誰做動作比較穩沒比過；用產線關鍵影格當首格的圖生影片在兩家都還沒送過（實拍驗證另有一張票）。
- 母鏡頭切三次、0.5 秒尾巴把手、動態分鏡在圖上模擬的運鏡，都是編輯判斷，沒有實拍對照。
- 有 production profile 的作品（十部動畫）走 Hailuo／Kling 還不行：`clips import` 拒收，要另一張票改產線與契約。
