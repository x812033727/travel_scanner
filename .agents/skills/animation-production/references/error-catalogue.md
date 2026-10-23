# 錯誤目錄：錯誤 → 階段 → 誰抓 → 漏掉的代價 → 預防

按階段分組。「誰抓」寫程式碼裡真的擋的那一行，或「無」（花了錢才知道）；`preflight` 指 `.agents/skills/animation-production/scripts/drama_preflight.mjs`，`estimate` 指 `episode_estimate.mjs`。代價用 `cost-model.md` 的價：圖 US$0.134、judge 0.01、Lite 素材 8 秒 0.64、Omni 4 秒 0.60。標 **試拍** 的是 2026-10-03 《喜宴未散》E1 真的發生過的（`docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`）。

## 開拍前（劇本、分鏡、設定）

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 1 | 分鏡的鏡頭數照 DRAMA.md 的「30 鏡 × 6 秒」估價，實際照 drama-craft 寫成 60 鏡 | `estimate` | 預算少算一倍的圖與 judge；Lite 下素材也少算一倍（每鏡都是 8 秒） | 用 `estimate` 逐鏡算，不沿用 DRAMA.md 的例子 |
| 2 | 一鏡估計超過 12 秒 | lint 錯誤（`drama.mjs:740`）；10 秒警告 | 0 元；Omni 貼到 10 秒的鏡頭利用率最差 | 拆鏡；profile 下 8 秒是錯誤（`lint.mjs:400`） |
| 3 | 回到同一鏡位的鏡頭各寫一個全新 prompt | `drama_craft_check` 的鏡位數；lint 的 Jaccard ≥ 0.8 警告（反方向：太像） | 每個鏡位多買一張圖、一份素材 | 第二次回來寫 `data.source`；要重畫就照抄 camera 整行與 prompt 第一子句 |
| 4 | `data.source` 的 `from_s` 加鏡長超過來源素材 | lint（10 秒；profile 8 秒）；`clips` 來源太短 → `needs_review` | 一輪 | `estimate` 的「可切鏡」列 |
| 5 | keyframe 命名造型的 `appearance` 加進 identity 題後超過 400 字，伺服器 422（`schemas.py` 的 `JudgeCriterion`）；clip 題已改用有界文字與完整 context | `preflight` 查本次要畫的 keyframe 實際題長；lint 只擋 800 | 圖買了、judge 沒做、take 算失敗 | 修正真正超長的 keyframe 題；不能以舊 clip 模板推導統一的 appearance 160 字上限 |
| 6 | 角色超過 3 個、`characters` 列了畫外的說話者 | lint（`MAX_SHOT_CHARACTERS`）；craft 的 `size.*` | 多一道 identity 題、多一張參考圖（上限 4 張，style_frames 被擠掉） | 畫外的人只在 `speaker`，prompt 寫 off screen（animation-camera） |
| 7 | `look`／`keyframes` 之後更改或清空 `look.negative` | `status`、`preflight` | `lookHash` 變：設定圖、關鍵影格、素材全部重買，兩個關卡重審 | negative 在 `look` 之前定好；#23 已修正，不為 Lite 相容性清空已核准的限制 |
| 8 | `look.candidates` 一開始就開到 6 | — | 角色數 × 6 張；大多用不到 | 預設 3；不過再補一輪 |

## `look`

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 9 | 劇本還沒核准就跑 `look` | 無（`look.mjs` 不查 script 關卡） | 劇本退回改了角色就整套重買 | drama.md 的順序；手動也守 |
| 10 | 設定圖通過 judge 但道具錯（**試拍**：知棠 A 的錶是圓的，來源是矩形銀錶） | 無；站主或獨立看圖 | 一張 0.144 ＋ 之後每張關鍵影格都錯 | 看圖再核准；`sheet_prompt` 把識別道具寫進去 |
| 11 | `auto_pick_look` 關著，等站主選圖時改了 appearance | `approvalState` → stale | 整套重畫 | 改之前看 `status` |

## `tts`、`check-audio`

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 12 | ASR 把同音字當唸錯（Jev 標句） | `check-audio` | 站主一輪審旁白；重錄到上限再給聽眾審稿改句 | 發音字典、`claims.md` 的名字；一下「九嬰」一下「九影」 |
| 13 | 改了一句的 `emotion` 或 `speaker` 沒重跑 `tts` | `clips`／`assemble` 的 `speech_hash` → 2 | 0 元一輪；audio 核准 stale | `status` |
| 14 | 旁白核准後又改字 | `approvalState` → stale | 站主再審；clips manifest 重建、judge 全部重付 | 攢齊再改 |

## `keyframes`

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 15 | look 沒核准、或 stale、或有角色沒選圖就跑 | `keyframes.mjs:143-150` → **3** | 0 元一輪 | `preflight` |
| 16 | 一鏡的 prompt 改了就跑 `keyframes`（整個或 `--shot`） | 無；`preflight` 的 kept／new | 60 次 judge ＝ US$0.60；storyboard stale。`--shot` 救不了：`visualHash` 變了 manifest 從空的重建（`keyframes.mjs:197` 的 `shots: {}`），`--shot` 寫出來的 manifest 只有那一鏡，`clips` 對其他鏡回 2 | 攢齊再跑整個 `keyframes`；`--shot` 只在雜湊沒變時用（補 `needs_review` 的鏡） |
| 17 | 相鄰兩鏡畫得一樣（dHash < 8 位元） | `keyframes.mjs:287-291` 在**花錢之後**警告；lint 的 Jaccard 在前 | 兩張圖 ＋ 兩次 judge；之後素材第 0 格比鄰鏡高不到 3 dB 也不過 | 回同一鏡位用 `data.source`；不然改景別或 camera |
| 18 | 插鏡（手、道具）被畫成上半身廣鏡（**試拍** S04 R01） | judge 的 `prompt` 題有時抓不到；站主看 | 一張圖 ＋ judge；之後素材照這張做 | camera 第一個詞寫 `Insert`／`Close-up of the hand`；prompt 只寫袖口、錶、道具（visual-quality.md） |
| 19 | 兩張首格之間道具換了手（**試拍** S04 R02 的錶換到翻頁那隻手；原文沒指定左右腕） | 無；站主看 | 一張圖；連戲斷 | 識別道具寫明哪隻手；同一鏡位照抄 prompt 第一子句 |
| 20 | 畫面裡出現生成的英文標籤、簽名筆畫（**試拍** S03 R02） | judge `no_text`；`clean` | 一張圖 ＋ judge | prompt 寫 no text；劇情要的字另外合成（animation-production.md） |
| 21 | 第一次 `keyframes` 就 `--takes 1` 想省錢 | — | 省的是上限不是一次；沒過的鏡頭下次還是從 take 1 的快取開始 | 預設 3 |
| 22 | `end_frame.prompt` 寫了很多鏡 | `estimate` | 每鏡多一張 0.134；dry-run 還多算 0.01 judge | 只給真的要末格的鏡 |

## `clips`

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 23 | **歷史已修正：Veo Lite 的 negativePrompt 相容性**。試拍時 adapter 把不支援的 `parameters.negativePrompt` 送到 Lite，HTTP 400 `INVALID_ARGUMENT`，兩個 seed 都失敗；修正 `tasks/done/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md` 已使 Lite 省略參數，完整限制接成 `Avoid: …` 進主提示，非 Lite 保留原參數 | 現行 `apps/api/tests/test_video_media_providers.py` 的離線 request-body 回歸；原始試拍表與收據保留 | 當時每次 0.64 的預留（退）＋ 等待；兩次用完 `MAX_CLIP_TAKES`、`needs_review` | 保留 `look.negative` 與已核准 look，不沿用清空欄位的舊權宜；不自動重買。相容測試不等於新付費媒體已驗收 |
| 24 | storyboard 沒核准、或重畫過一鏡沒再 `review-push` | `clips.mjs:154-158` → **3** | 0 元一輪 | `preflight` |
| 25 | timeline 是舊劇本的 | `clips.mjs:131-134` → **2** | 0 元一輪 | `status` |
| 26 | profile 釘 Lite 1080p，伺服器設定是 Omni | `clips.mjs:222-225` → 3 | 0 元一輪 | `media-status` |
| 27 | 第一鏡沒單獨跑，主機地區被擋 | 無 | 整集排隊後全失敗（退款）；一輪 | `clips --shot <第一鏡>` |
| 28 | 素材裡多一隻手、第二支錶、第二支筆（**試拍** S01 R03、S03 R01） | judge `clean`、`identity`；試拍是 root QC | 一次 0.65；重拍同一 prompt 再中 | 內容問題：改 prompt／motion，不換 seed（SKILL.md 的分類表） |
| 29 | 「微顫後穩住」被做成抬筆到水平再轉回（**試拍** S03 R02） | judge `prompt`／`motion`；試拍是獨立 QA | 一次 0.65 | motion 寫可讀的幅度與既有的手／筆關係；不寫「微顫」（visual-quality.md） |
| 30 | 一次自然眨眼被 judge 讀成「開頭睜眼」，6.72 不過（**試拍** S01 R04） | judge | 一次 0.65 ＋ 一次 judge；人覺得能用也不能改分 | 逐幀看、記下差異；要重拍就重拍，不重判 |
| 31 | 片段送 judge 超過 20 MB → 413 | 自動：720p 代理（`clips.mjs:354-359`） | 多一次上傳 | 不用做 |
| 32 | 素材的第 0 格不是關鍵影格（PSNR < 22），或在灰區 22–30 比鄰鏡高不到 3 dB | `qc.mjs:136-137` | 一次素材 | 首格就是關鍵影格；相鄰鏡別畫一樣 |
| 33 | 模型在素材裡自己切鏡（0.1 秒後 scene > 0.5） | `qc.mjs` | 一次素材 | 一鏡一事；motion 不寫兩個動作 |
| 34 | 旁白窗內凍格 ≥ 1 秒 | `qc.mjs` | 一次素材 | motion 寫看得見的動作；look-only 的鏡少 |
| 35 | profile 下素材不是原生 1920×1080，或格數蓋不滿鏡長 | `clips.mjs:367-375` | 一次素材 | 1080p；鏡長 ≤ 8 秒含停頓 |
| 36 | 中途放 `STOP`，忘了拿掉 | `preflight` | 下一階段立刻停；`incomplete` 的鏡頭留著 | 跑前看工作區與上一層 |
| 37 | 單支上限到了（Veo 3.1 一次 60 鏡 US$192.6 ＋ 圖） | `stages.mjs:148-151` → 3 | 前面已買的留著；後面停 | `estimate --cap` |
| 38 | 月額度到了（伺服器 429 `video_media_budget_exhausted`） | 伺服器；工具 → 3（owner code） | 請求不會送到廠商 | `media-status` 的剩餘 |
| 39 | 同一請求失敗 3 次（409 `video_media_job_exhausted`） | 伺服器 | 換 seed 就是新 key | 改提示詞 |

## `assemble` 與外部片段

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 40 | 外部片段的首格不是這一鏡的關鍵影格；或有黑格、凍格、模型自己切鏡 | `clips import`：`clipVerdict`（PSNR < 22、黑格、凍格、切鏡）→ `needs_review`，**1**；`--force` 留下的由 `assemble` 再比一次第 0 格 | 那一支白做；點數不退 | Hailuo／Kling 生成時用關鍵影格當首格；不要用 `--force` 蓋過量到的問題 |
| 41 | 外部片段放進有 production profile 的集 | `clips import` → **3**；手放的由 `productionClipProblems`／`productionClipSizeProblem`（`lint.mjs:408-434`）→ `assemble` 2，`status` 不算完成 | 白做 | 只用在沒 profile 的集 |
| 42 | Hailuo relax 隊列的片段回來時 timeline 已改（台詞改了、重跑 `tts`） | `clips import` 的雜湊檢查 → 2 | 關鍵影格重畫之後這一支多半要重做 | 送出前 `status`；台詞定了再排隊 |
| 43 | 手寫 manifest 漏了 `frames` 或 `clips_hash` 沒重算（指令落地前的手放） | `assemble` 的 fit 算錯；`status` 的「video assembled」永遠不完成 | 一輪 | 不手寫：用 `clips import` 重新帶進來 |
| 44 | 片段比句子短，`fit: "auto"` 慢到 0.85 倍還不夠、尾格超過 60 格 | `assemble`：`freezeProblem` → 1 | 一輪；profile 下不准 `freeze` | 拆句或要更長的素材；`estimate` 的「超過 8 秒」列 |
| 45 | 匯入的片段後來跑 `clips --force` | 無（`clips --dry-run --force` 會把它列成要買的） | 那一鏡在伺服器重買（key 不在快取），匯入的條目被換掉 | 不要 `--force`；用 `--shot` 指定別的鏡 |

## 收工與回報

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 46 | 把 job `ready` 當通過：**試拍** 16 jobs、14 ready、2 failed、站主接受 0 | `run_report.mjs` 五欄 | 誤報進度、放量 | 五個數字分開 |
| 47 | 把保守預留當花費、或把 judge 的 0.01 跟 manual reserve 重複加（**試拍** US$15.18 含 reserve 10，judge 0.02 已在 reserve 內） | — | 報錯帳 | 預留、估價、實際帳單三欄 |
| 48 | 改分、降 `judge_min_score`、重判到過 | visual-quality.md 的規矩 | 品質紀錄作廢 | 不過就記不過 |
| 49 | PowerShell 5.1 把非 ASCII 的 `--shot` 或路徑弄壞 | 無 | 跑錯鏡或找不到檔 | argv 只用 ASCII；鏡頭 id 本來就是 |
| 50 | 公開文件放了機器路徑或憑證 | `tools/skills.test.mjs`、`repo-hygiene` | 撤文 | 素材與收據留 repo 外 |

## 規劃與網頁路線（2026-10-04 補）

`plan_lock.mjs`、`shot_plan.mjs`、`animatic.mjs` 是 `.agents/skills/animation-preproduction/scripts/` 的三支；規劃的做法在那個 skill。

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 51 | 關鍵影格畫完（或 storyboard 核准後）才改某一鏡 `motion` 的一個字；圖片模型不讀 `motion`，但 `visualHash` 綁整個 `scene.data` | `plan_lock.mjs --check`；`status` 的 stale | 關鍵影格不重畫（#1193 起只有畫面請求或 judge 題目變了的鏡頭才重畫；改 `prompt`／`camera` 的那一鏡會重畫重 judge），但 keyframes manifest 改寫 → storyboard 重審；伺服器買的素材每支再 judge（60 支 US$0.60）；已匯入的外部片段全部重匯 | 動作與運鏡在 `keyframes` 之前定稿；鎖定後的改動攢齊走變更單 |
| 52 | 小樣或批次中途為一鏡改 `video.json` 或網頁正文 | 改 `video.json`：`plan_lock.mjs --check`；只改網頁正文：人工對收據的正文 SHA-256 與 `plan/lock.json` 的 `shots[id].prompt.sha256`（`--check` 不讀收據） | 同 51，加上收據重現不了 | 記下問題，這一批做完一起改、重鎖 |
| 53 | Kling 的「輸出數」沒設 1、或開了原生音訊 | 無（Generate 旁的點數） | 多份輸出照支數扣（推算）；音訊 1080p 每秒多 4 點（官方） | 送出前清單（`animation-preproduction/references/route-decisions.md` 第七節） |
| 54 | Kling Multi-Shot 開著，或 H3 正文寫了 `[Shot 2]`，模型在一支裡切鏡 | `clips import` 的切點檢查 → `needs_review`，1 | 那一支白做 | Multi-Shot 關；H3 只寫 `[Shot 1]`（`shot_plan.mjs` 的正文） |
| 55 | 網頁正文把 `look.negative` 的否定句照抄進去 | 無 | 否定的東西被畫出來（**試拍**：already closed 畫成開著的門） | 負面欄真的有才貼；正文寫看得到的正面狀態 |
| 56 | 網頁買的秒數剛好等於需要的秒數 | `assemble` 的 fit／freeze | 收勢被切掉、或要放慢補長度 | 尾巴留 0.5 秒（`shot_plan.mjs --handle`）；圖生影片沒有頭的把手 |
| 57 | 沒做動態分鏡，節奏與資訊順序在素材買完才看出來 | 無 | 重剪不夠就重買 | `animatic.mjs` 文字卡版在 P3 之後就看；關鍵影格版在 storyboard 關卡前看 |
| 58 | C 級鏡頭（手指拿小道具、兩人接觸、吃喝、變身、要讀的字）照原樣排進批次 | `shot_plan.mjs` 的風險級；`--strict` 報不在小樣裡的 C | **試拍**：生成出來的 4 個 take 有 3 個在手與道具上出錯，S03 兩次上限用完；到 take 上限就停 | 前期重設計（`shot-risk.md` 的招式），非做不可就放進小樣 |
| 59 | Hailuo 的 AI Polish、Kling 的 AI Prompter 開著卻沒記 | 無 | 實際送出的不是鎖定的字，下一次重現不了 | 鎖定包寫明開或關；收據記 |
| 60 | 用有 production profile 的集規劃網頁路線 | `shot_plan.mjs`（refuse）；`clips import` → 3 | 做出來進不了產線 | P0 條件卡先查 profile |
| 66 | 鎖定包的 `buy_s` 沒量這一鏡的台詞；或寫「買 N 秒」前沒看這一鏡的 `visual_kind` | 無：要人量 | 片子收不下台詞就重買；`visual_kind` 是 cut 或 still 的鏡頭根本不用買（偶的江湖：站主差點為兩個這種鏡頭付點數） | 建包前量每鏡的台詞需求（錄好的 WAV ＋ 每段間隔 300 ms ＋ 尾巴 1 秒），`buy_s` 往上取整；寫「買 N 秒」前先查 `lock.json` 的 `visual_kind`（clip、still 或 cut） |

## 提示詞的字、長度、審核與風格（2026-10-05 補）

來源標名：官方頁面寫站名與讀取日；`A-cat-with-carrots/OnlyShot`（MIT，即夢／Seedance 的 CLI 產線，17 個失敗模式）、`ayase0307/h3-video-prompting`（MIT）、`smixs/visual-skills`（CC BY 4.0）是社群文件，`MiniMax-AI/MiniMax-H3` 是官方 skill；數字各自標「官方」或「社群」。各模型的長度表在 `.agents/skills/animation-camera/references/camera-keywords.md` 第五節。

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 61 | 正文或 CLI 參數混進 CJK 引號與全形標點（「」『』（）、全形逗號、`@` 與半全形混用）。OnlyShot 的即夢 CLI 實測（社群）：bash `eval` 遇到這些字 quoting 解析壞，server 建了任務卻靜默丟棄——立刻「下載失敗」、`list_task` 永遠 querying、不扣點、網頁看不到；同一套的參考圖 regex 漏了全形 `）`，少傳兩張參考圖才發現。H3 官方格式只允許畫面裡的字用英文雙引號逐字、台詞在 `<d>` 內保留原標點；Kling 3.0 官方範例裡的「」只出現在原生對白 | 無：產線的 `video.json` 是 JSON，lint 不查標點；網頁路線沒有程式讀正文；`shot_plan.mjs` 的 sha256 只證明貼的是同一份 | 網頁一支點數；CLI 假死 30 分鐘一輪 | 正文全 ASCII 標點（產線的 prompt 本來就是英文）；要出現的中文字另外合成（#20）；走 CLI 時參數用 args list 不走 shell 字串；送出前用 `grep -P '[^\x00-\x7F]'` 看正文 |
| 62 | 審核拒絕。MiniMax API：`base_resp.status_code` 1026 `input new_sensitive`、1027 `output new_sensitive`（platform.minimax.io/docs/api-reference/errorcode，2026-10-05 讀）；社群實測（atlascloud 2026-08-16）：命名 IP（`Darth Vader from Star Wars`）7 秒內回 1026；血與尖叫不報錯但畫面裡被靜默拿掉（「partial refusal without reporting one」）；親吻、遊戲裡的步槍過。Kling API：1301「Trigger the platform's content security policy」（官方錯誤碼頁是 SPA，2026-10-05 抓到空殼，數字來自 API 使用者整理）；網頁只顯示「Generation failed, try a different prompt」。即夢 5.0（OnlyShot，2026-05 實測）：`generation failed: final generation failed` | 產線：`apps/api/app/video_media/providers/minimax.py` 把 1026／1027 當 `blocked` 回 422，job 記成 `video_media_rejected`（`apps/api/app/video_media/jobs.py`），take 算失敗；Gemini 回 `Gemini refused the request`；網頁路線無 | 一次 take；網頁的點數退不退未驗（MiniMax 的 1026 在生成前就擋下） | 替換表（下）；不寫 IP 名與真人名、寫外觀；臉部特寫不疊紅暈類的詞；血與傷放負面欄或不寫；被拒就改字不換 seed（#39） |
| 63 | 正文超過上限或被截斷。官方上限：MiniMax v2（H3）每個 `text` ≤ 7,000 字元、Hailuo 2.3 i2v ≤ 2,000；Kling API `prompt`／`negative_prompt` 各 ≤ 2,500（已停更的官方文件 2024-09-19 紀錄；現行頁面 SPA）；Veo 3.1 三個模型 Text input 1,024 tokens；MiniMax 圖片的 adapter 常數 `IMAGE_PROMPT_LIMIT = 1500`。社群：即夢 ≤ 1,500 字元，超過回 `ret=1046 InvalidNode`（OnlyShot 實測，非官方常數）。產線：`prompt` 1000、`camera` 120、`motion` 300（`LIMITS`），組好的提示切 4,000（`MAX_PROMPT_CHARS`，先掉的是角色外觀）。網頁輸入框的上限（Hailuo、Kling）未驗 | lint 擋 `LIMITS`；`shot_reading` 報 `prompt.length`；API 回 2013／400；網頁輸入框截斷不提示 | 砍尾先掉 `Characters:` 的外觀 → identity 題失分；網頁被截的正文跟鎖定包 sha256 對不上，重現不了 | `shot_plan.mjs` 的 `chars` 欄對上表；H3 正文照社群甜蜜點 300–700 英文字、有首格時更短；Kling 圖生影片 20–40 字只寫動作 |
| 64 | 風格指紋漂移：設定圖通過後，後面的關鍵影格或片段的畫法、線條、色板漸漸離開設定圖；或反向，`look.style` 的場景句污染個別鏡頭（**試拍** S03 R01：倉庫火光漏進婚宴桌）。OnlyShot：角色 A 的 ref 漫畫風、角色 B 寫實 → 影片段畫風跳（它的 #9），修法是把「視覺指紋」段逐字 append 到每個 prompt；但 ref 階段的 `neutral/flat` 指紋 append 到分鏡圖會把 dramatic 光中和掉（它的 #16，加 `--no-fingerprint`）。smixs：同樣的東西用同樣的字，每支 prompt 重複 identity／style block | judge 的 `style` 題（權重 1）只對 `look.style`，不對設定圖；`keyframes` 的 dHash 只比相鄰兩鏡；沒有工具把關鍵影格跟設定圖比（`JudgeKind` 的 `continuity` 沒人呼叫）；人看聯絡表 | 一張 0.134 ＋ judge；晚發現就整場重畫；改 look 等於整套重買（#7） | `look.style` 只放整部片不變的畫法、線條、色板、鏡頭質感，場景光寫每鏡 `prompt`；風格句逐字進每張關鍵影格（`shotPrompt` 的 `Style:` 自動接）與每支網頁正文（`shot_plan.mjs` 接 `look.motion`）；小樣先出三張並排對設定圖；偏了改個別鏡的 `prompt`，不改 look |
| 65 | Omni 自己切鏡：官方提示指南（ai.google.dev/gemini-api/docs/omni，2026-09-23 更新，2026-10-05 讀）說 Omni Flash **預設**會做成幾個鏡頭，要單鏡得寫 `In a single unbroken scene`／`In a single continuous shot`／`No scene cuts`；產線 `look.motion` 的預設句只有否定的 `no cuts`（`tools/video/core/drama.mjs` 的 `PRESETS`） | `qc.mjs` 的切鏡檢查（#33）在花錢之後 | 一次素材 | Omni 的 `look.motion` 寫正向句 `In a single continuous shot`（在 `look` 之前定，它在 `lookHash` 裡）；Kling 關 Multi-Shot、H3 只寫 `[Shot 1]`（#54） |

替換表（#62）：全部是社群文件記的實例，哪一家擋的標在來源；同義替換是起點，不保證過。

| 寫了 | 改成 | 誰擋過（來源） |
| --- | --- | --- |
| 命名 IP、真人名（`Darth Vader from Star Wars`） | 寫外觀與服裝，不寫名字 | MiniMax H3 1026（atlascloud 實測，社群） |
| `blood runs down her collarbone`、尖叫 | 放負面欄 `no blood, no gore, no wounds`，或畫面外處理 | MiniMax H3 靜默省略、不報錯（同上） |
| 角色的 `sinister`、`leans menacingly`、`with dark intent`、`possessive gaze`、`cold smirk` | `moody`、`leans forward`、`quiet`／`focused`、`subtle smirk` | 即夢 5.0 `generation failed`（OnlyShot，社群） |
| 顏色與光的 `dark cyan`、`dark teal`、`dark shadows engulf`、`harsh shadow`、`sinister spotlight` | `deep cyan`、`deep teal`、`shadows along edges`、`soft shadow`、`moody spotlight` | 同上（偶發） |
| 臉部特寫加 `blush on cheeks`、`pink blush`、`internal glow`、`pulsing softly` | `rose tint`、`pink glow`、刪、`glowing steadily`；`extreme close-up` 改 `medium close-up` | 同上：特寫＋面部紅暈類描述必擋 |
| `strolls past camera`（像街拍）、具體食物名 | `walks across stage center`、泛稱 | 同上（作者推測是肖像類審核） |
| 中文字幕段的「反派」「磕」「不死心」 | 刪、「圍觀」、「還在惦記」 | 同上 |
| 人臉、頭盔、墨鏡、像名人的參考圖 | 自有或合成的角色參考 | Seedance 2.0 的人臉過濾（smixs，社群；2.5 不適用） |

## Hailuo 網頁整集製作：送出與取回（2026-10-15 補）

標 **E1** 的是《偶的江湖》第一集在 Hailuo 網頁做完整集時真的發生的（17 輪，2026-10-09 → 10-15）；「R n」「補 n」是交接檔的輪次與第十七輪的補記，出處與做法都在 `.agents/skills/animation-production/references/hailuo-episode-operations.md`。點數：H3 2K 影片 12 點／秒（實測 2026-10-04），首格 GPT Image 2.5 Sunburst 16:9 High 2K 為 20＋參考張數。

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 67 | 拿畫廊卡片的圖當首格：create 頁卡片 `img` 的 `.png`（去掉 `?x-oss-process` 也一樣）是烙了 MINIMAX／Hailuo AI 浮水印的另一個檔，檔案 id 不同（**E1** R7，10-10） | 無：`clips import` 的 ffmpeg 檢查也看不出浮水印；E1 是事後對檔案 id 才發現 | 14 支影片用了帶標首格：6 支已算圖、312 點作廢，8 支排隊中取消退 408 點；24 張首格重抓、24 支重買 1,272 點；帳本表達不了「後來才退」，要站主跑關帳腳本改 9 個動作檔、重設基準 | 首格與影片只從作品詳情頁的「無水印下載」拿（`downloadWithoutMark` 的 `onClick`＋fetch 鉤子），收據記 `download_method` 與網址；送影片前用首格 SHA 對建檔的 `-official.png` |
| 68 | 送出就被海螺的文字過濾擋下：按創建什麼都沒發生，只有 toast「文字內容違反社區準則，請修改後重試。」（**E1** a02-s030 t2，補十五，10-14）；或生成後才被「內容違反社群指南」退件、退點（a01-s047 影片 t1，補十三） | 提供者；頁面上沒有新卡，要用頁面文字差分抓 toast；帳本的 intent 留著 → `SHOT_HOLD` 擋住這一鏡 | 0 點，但 24 點保留卡住、這一鏡的 take 算用掉；要站主跑關帳腳本（`failure_kind: provider_text_filter_refused_at_submit`，補十六），再放寬修圖路線才能畫第三張 | 被擋的字不會告訴你：a02-s030 t3 拿掉 insert、push、rising、bare、kneel、figure、silhouette、face、relaxed、falling、chest 才過（補十七）；生成後退件的 a01-s047 同一正文重送 t2 就過（補十三）；「Policy check temporarily unavailable; retry.」是暫時的，重跑 |
| 69 | 卡片晚出現，沒重掃就再按一次創建（**E1** a05-s004：4 秒讀回時卡還沒出現，R16，10-12） | 下一筆 intent 的 `BALANCE`（頁面餘額比帳本預期少 23） | 多一張首格 23 點，兩張都要建檔、寫收據、加 `operator_note` | 創建後輪詢最多 20 秒等新的 `media-group-<id>`；沒重掃不准再按；影片同理 |
| 70 | 進入生成就卡死、沒有取消：a04-s021 7 s（84 點）10-10 09:41 送出，「正在生成」四天多，佔佇列 12 格中的一格；伺服器旗標 canCancel、canRetry、canAppeal、canRecreate 全 false（**E1** R6–補十八） | 無；只有排隊中的卡有「取消」→「確認」（立即退點，R7 退過 408 點） | 84 點；佇列少一格（R11 兩次按創建沒反應）；站主最後裁定關成 failed、84 點算已花（10-14），t2 重拍再 84 點（補十八） | 送之前查清楚，排隊中發現錯就取消；卡超過一天請站主選：等退點、找客服、或關帳重拍；佇列滿 12 時 toast「視頻隊列限制: 12」、按創建不扣點，不要重按 |

## Hailuo 網頁整集製作：首格內容與修圖

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 71 | 首格沒有動作需要的東西，模型自己長一個：a02-s028 首格提示詞寫「只到上胸、手和匣在畫外」，鎖定的動作是「雙手按平在匣蓋上」，影片長出一個棕色木匣（不是劇裡的黑漆匣）（**E1** 補十七，10-14）；同類：a04-s016 繩樁第二秒才長出來（R12），a03-s074 t2 扇脫手浮起、手裡又長出第二把（補十八） | 無：首格 QA 只看圖本身，影片 QA 才看到 | 一支影片 60 點（limited）＋兩張修圖首格 46 點＋重拍 60 點；修圖額度放寬兩次（1,590→1,778→1,803） | 寫首格提示詞時把 motion 的受詞（手、道具、對象）逐一對過，都要在畫內而且是起始狀態；首格 QA 加「動作需要的東西在不在」；道具材質拿已做的鄰鏡首格當參考（a02-s028 t3 用 a02-s027 的匣，補二十） |
| 72 | 起始／結束幀的結束幀沒拿起始幀當參考，尺度漂：a04-s043 結束幀 t1 只用四張板，比起始幀緊約兩成、冠被切（**E1** 補十九，10-15） | 首格 QA 把兩張並排才看得出 | 一張 24 點，加站主放寬修圖路線一次（1,469→1,590） | 結束幀的參考 1 是起始幀的乾淨 CDN 副本（pilot a02-s037 的做法；t2 這樣做，一次對上）；影片意向兩張幀都綁 |
| 73 | GPT Image 的左右偏誤：近側臉朝下時把遠側眼角的霜花畫到近側臉頰，2／2，把左右規則整句移到提示詞最前面也沒用（**E1** a02-s028 t3、t4，補二十，10-15）；早先霜花落在頰側（a03-s044／046，R5）、念珠或刀換手（a02-s056／074、a01-s038，R7） | 首格 QA 的左右規則（每角色一條，寫在包裡） | 兩張 46 點，加修圖上限 3→4 的放寬；最後要本機修圖、站主親手選檔上傳 | 有遠近側標記的鏡頭在規劃時排正面或另一側；明寫一句有時有用（a05-s063 袈裟寫「LEFT shoulder ONLY」，t2 一次對，R17）；兩次不對就停，改本機修圖（紀錄＋收據＋站主同意） |

## Hailuo 網頁整集製作：台詞秒數與 D 軌

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 74 | 片子買完才發現台詞比買的片長長：長老的後台錄音每句 2.4–4.2 秒，照 `action_seconds` 定的 `buy_s` 裝不下（**E1** R8、R9、R13，10-11 → 10-12）；接續 #66 | 無：D 軌 builder 在買完之後才算出溢出，只出 D、不合成畫面 | 14 支已出片的鏡重買 1,116 點（第二張變更單，R17）；另 15 鏡在第一張變更單加 21 秒（單 take +252 點）；保留的鏡等了一輪 | 第 13 包起建包前先量（需求＝台詞＋句間 300 ms＋場尾 1,000 ms＋前導），對**實際片長**（4 s＝4.458、5 s＝5.167、6 s＝6.583、7 s＝7.292），裝不下的保留、開變更單；9 秒以上先買一支量實長（9.417 s）再決定 |
| 75 | 場尾停頓（300＋700 ms）溢出到下一鏡，下一鏡的前導卻吃不下：a03-s030→a03-s031 差 0.168 s（兩鏡 take 都已用完）、a04-s054→a04-s055 差 0.240 s（a04-s054 的 take 已用完）（**E1** R17，10-12）；a05-s081 的 0.733 s 要 a05-s082 吸收（補十） | D 軌 builder 的 carry-in 斷言（建置會停）、每包的接點表 | 重買下一鏡（a04-s055 5 s、60 點，第四張變更單），或剪接時縮停頓（a03-s030），或下一鏡改長（a05-s082 6 s，第六張變更單） | 買之前也量下一鏡的前導；吸收要站主選、寫成 `owner-absorb-*.json`，下一鏡開頭至少留那麼多靜音；剪接決定寫進變更單那行的 `editorial_decisions` |
| 76 | 原地改已被 D 軌綁住的 QA 收據（加 `qa_corrected_at`／`qa_correction_note`）：D 軌的 `timeline-and-sources.json` 綁的是改前的 SHA（**E1** a05-s023、a05-s034，R16，10-12） | D 軌子代理複查綁定時 | 兩個 D 軌資料夾作廢重建（舊的搬到 `-superseded/`），其他 29 個要唯讀複查 | 收據寫一次（腳本用 `wx`）；要更正先查有沒有被綁，被綁就寫新收據或在結算摘要更正，再重建下游；動作檔同理（a02-s028 的 `upload_method` 寫錯，只在摘要與收據更正，補二十）；QA 收據寫好才交給 D 軌 |

## Hailuo 網頁整集製作：帳本、租約、工具與瀏覽器

| # | 錯誤 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- |
| 77 | 前一個 session 結束，製作租約的背景程序跟著死，授權檔的 `lease_pid` 指向死掉的 pid（**E1** 10-12、10-13、10-15 三次） | `guard()`：`Unexpected lease owner/PID`，intent 與 update 都被拒 | 10-12 三支已下載的影片沒記到帳，要事後用只做 update 的腳本補記（R15）；失敗的 intent 留下 `<id>-before.*`，重跑被 `wx` 擋 | 每個 session 開工第一件事：重跑 lease 腳本 → 站主跑 lease-resume（只改 `lease_pid`，`lease_resumes[]` 記一筆）→ `guard()` 過了才送；`before` 證據檔改名 `.orphan-*` |
| 78 | 用錯包號或過期的操作腳本：腳本照包編號複製（`ffNN.sh`、`vstepNN.sh`、`fstepNN-js.mjs`、`prepNN.sh`、`rbNN.sh`）；漏帶 `PKT=16`，`file-vid.sh` 從第 7 包讀卡片（a04-s057，R17）；`claude-submit.mjs intent` 的期別讀 `LEDGER_PERIOD`、預設 A，B 期回 `SCOPE`（R11）；`image-step.sh` 餘額給空字串、參數位移讀到預設包（R11）；變更單後 `make-video-inputs.mjs` 仍用建包時的 `buy_s`（補十七）；手打 batch 把 SHA 尾碼打錯（a05-s019，R16） | 頁內 SHA 檢查擲錯（不扣點）；帳本 `SCOPE`、`CANONICAL`；有的要到收據才看出來（PSNR 算不出） | 一輪時間；錯的紀錄要趕在收據綁定前改正 | 建包時寫 `operator-copies.json`：每支腳本的 sed 指令（只換包號 token，並列出不能換的字串，例如 `30+ s`、`s.slice(0, 30)`）與預期 SHA，複製後 `sha256sum` 對過（第 31 包）；batch 一律貼產出的原文，不手打；變更單後重產步驟檔 |
| 79 | 預檢依賴的頁面標籤搬家或失真：10-15 起「參考圖片 N」是歷史卡片的標籤、不是作曲區的（**E1** 補十九）；「16:9」字樣在設定抽屜關著時仍留在 DOM，比例籤在「自動」也通過（R12） | 無：預檢照樣通過 | 參考圖張數錯（多注一張 → 報價 22 對 21，a05-s087，R17），或比例錯（#80） | 預檢讀不會搬的訊號：縮圖數＋CDN 來源＋報價（20＋參考張數）、底欄籤的**順序**（model／16:9／High／2K）、時長籤＝`buy_s`；頁面改版後先確認預檢在一張錯的設定上會失敗，再放量 |
| 80 | 每次重載後設定被重設：比例退回「自動」或 21:9、張數退回 4（報價 ×4，80–96 點）（**E1** R7、R12、補十四、補十九） | 報價擋得住張數；比例沒人擋 | 10-12：第 10、11 包 45 張首格在「自動」下出成 1672×941（不是 2560×1440），收據還抄成 2560×1440；a03-s070 t1 出成 2:3 直式 1024×1536（23 點）（R12）；要重出等於連影片重做，站主沒重出 | 每次載入先跑設定腳本（`set-aspect-169.js`：點目前的籤再選 16:9、張數設 1，過濾空字串葉節點），預檢讀籤的順序與報價；收據尺寸用 ffprobe 量 |
| 81 | 隱藏窗格下的腳本逾時：`javascript_tool` 一次 45 秒，逾時後頁面裡的腳本還在跑；計時器被節流、CSS 離場動畫跑不完、antd 下拉不渲染（**E1** R7–補十九） | 工具回逾時，但「逾時」不等於「沒做」 | a05-s087 的 A 步逾時後才注入，重跑又塞一張參考（2/16、報價 22），預檢擋下、全部清掉重來（R17）；卡片 40 張以上時全頁掃描就超過 45 秒（a05-s014，R16）；時長 popover 停在 `ant-zoom-big-leave` 讓預檢誤判成開著（a04-s057、a04-s061，R17） | 每步拆到 38 秒內（首格三步、影片四步）；逾時先用便宜的 JS 讀狀態，重跑注入前先清空參考；只掃創作列、不掃全頁；停在離場動畫的 popover 不算開著；兩個分頁不同時下指令 |
| 82 | 要上傳本機檔（修圖版首格、缺副本的參考圖），內建瀏覽器做不到：對 `127.0.0.1`／`localhost` 的 fetch 一律 `ERR_BLOCKED_BY_CLIENT`、沒有選檔工具、幾 MB 的 base64 塞不進頁面（**E1** 補二十，10-15；2026-10-04 首見） | 無：卡在送出前 | 時間；10-10 估算時約 42 鏡因參考圖不在帳號裡做不了；10-13 站主在自己 Chrome 上傳的三張其實沒送出（補八） | 本機檔請站主在窗格的原生選檔框親手選，或用 Claude in Chrome 的 `file_upload`（已連線且先問）；選完用提供者副本對本機檔算 PSNR 證明選對檔；參考圖有沒有進帳號用上傳清單查，不靠「傳好了」一句話 |
| 83 | 子代理共用一個 scratchpad、又同時寫同一個製作目錄：scratchpad 路徑跟著父 session、不跟著代理（2026-09-27 兩個代理互蓋過 PR 內文）；E1 的 D 軌子代理把量台詞的腳本只放在自己的暫存區，下一個 session 只能照算法重寫（R14）；建包子代理寫檔時主對話正在改 `F/actions`，被 protected 檢查擋過一次（R15） | 無；protected 檢查只擋得住它看的檔 | 重寫工具、重跑建包 | 每個代理一個子目錄（E1 用 `r17`、`r17m`、`r17u`、`r17w`）；要留給下一輪的工具放進製作目錄（`H/` 或包資料夾）並記 SHA；子代理只寫自己的資料夾，全部檢查過才一次寫檔（`protected_fingerprint`）；用 scratchpad 的檔之前先讀回確認 |
