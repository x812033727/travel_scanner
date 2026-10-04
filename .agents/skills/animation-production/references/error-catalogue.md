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
| 51 | 關鍵影格畫完（或 storyboard 核准後）才改某一鏡 `motion`／`camera`／`prompt` 的一個字；`motion` 圖片模型不讀，但 `visualHash` 綁整個 `scene.data` | `plan_lock.mjs --check`；`status` 的 stale | keyframes manifest 重建、每一鏡再 judge（60 鏡 US$0.60）、storyboard 重審；已匯入的外部片段要重匯 | 動作與運鏡在 `keyframes` 之前定稿；鎖定後的改動攢齊走變更單 |
| 52 | 小樣或批次中途為一鏡改 `video.json` 或網頁正文 | `plan_lock.mjs --check`（定稿正文的 SHA-256 對不上收據） | 同 51，加上收據重現不了 | 記下問題，這一批做完一起改、重鎖 |
| 53 | Kling 的「輸出數」沒設 1、或開了原生音訊 | 無（Generate 旁的點數） | 多份輸出照支數扣（推算）；音訊 1080p 每秒多 4 點（官方） | 送出前清單（`animation-preproduction/references/route-decisions.md` 第七節） |
| 54 | Kling Multi-Shot 開著，或 H3 正文寫了 `[Shot 2]`，模型在一支裡切鏡 | `clips import` 的切點檢查 → `needs_review`，1 | 那一支白做 | Multi-Shot 關；H3 只寫 `[Shot 1]`（`shot_plan.mjs` 的正文） |
| 55 | 網頁正文把 `look.negative` 的否定句照抄進去 | 無 | 否定的東西被畫出來（**試拍**：already closed 畫成開著的門） | 負面欄真的有才貼；正文寫看得到的正面狀態 |
| 56 | 網頁買的秒數剛好等於需要的秒數 | `assemble` 的 fit／freeze | 收勢被切掉、或要放慢補長度 | 尾巴留 0.5 秒（`shot_plan.mjs --handle`）；圖生影片沒有頭的把手 |
| 57 | 沒做動態分鏡，節奏與資訊順序在素材買完才看出來 | 無 | 重剪不夠就重買 | `animatic.mjs` 文字卡版在 P3 之後就看；關鍵影格版在 storyboard 關卡前看 |
| 58 | C 級鏡頭（手指拿小道具、兩人接觸、吃喝、變身、要讀的字）照原樣排進批次 | `shot_plan.mjs` 的風險級 | **試拍** S01 四次、S03 兩次都沒收斂；到 take 上限就停 | 前期重設計（`shot-risk.md` 的招式），非做不可就放進小樣 |
| 59 | Hailuo 的 AI Polish、Kling 的 AI Prompter 開著卻沒記 | 無 | 實際送出的不是鎖定的字，下一次重現不了 | 鎖定包寫明開或關；收據記 |
| 60 | 用有 production profile 的集規劃網頁路線 | `shot_plan.mjs`（refuse）；`clips import` → 3 | 做出來進不了產線 | P0 條件卡先查 profile |
