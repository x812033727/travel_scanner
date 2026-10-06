---
name: animation-production
description: AI 漫劇的製作實務：階段前提、關卡與雜湊、估價、重買範圍、錯誤診斷、收工帳本與檢討；伺服器 API 與使用者指定的 Hailuo／Kling 內建瀏覽器路線，CLI／MCP 為另選方案。要手動跑 look／keyframes／clips、估預算、用瀏覽器製作並匯入外部片段、先驗三個連續鏡頭的 pilot、查結束碼 2／3 或報帳時先讀；付費之前的分鏡表、動態分鏡與開拍鎖定在 animation-preproduction。不取代 youtube-video 的 drama.md、drama-craft.md 與 visual-quality.md。Plan, preflight, price and audit animation production through the server or a user-selected Hailuo or Kling browser route, with source-bound keyframes, a three-shot pilot and honest receipts.
metadata:
  short-description: 動畫製作：階段前提、成本、三條路線、錯誤目錄、檢討
---

# 動畫製作（animation-production）

給**用手跑一集 AI 漫劇**的代理：自己下 `look`、`tts`、`keyframes`、`clips`、`music`、`assemble`，或在試拍後向站主報帳、寫檢討的人。主機工人（`node tools/video/cli.mjs auto`）不讀 skill，它該守的規矩都在 `tools/video`；這裡寫的是程式碼不替你擋、花了錢才知道的事：每個付費階段前要成立什麼、一鏡一集一個月各多少錢、哪個改動會重買什麼、哪些錯誤最貴、收工要交什麼。

每個數字後面標來源：**工具規定**（檔案與函式或常數；行號只在 `.agents/skills/animation-production/references/stage-preconditions.md`，那裡註明讀取日）、**價目**（檔案或網址，加查閱日）、**模型限制**、**量到的**（試拍紀錄）、**編輯判斷／換算**。沒標的就當沒驗。路徑相對於 repo 根目錄；工作區在 `<VIDEO_WORKDIR>/<SLUG>/`（repo 外）。

此版本的 Lite adapter 與 clip judge 相容修正描述的是 repo 程式碼；實際後端須核對部署版本。本機估價／preflight 通過不代表正式服務已更新、付費請求成功或素材通過驗收。

## 什麼時候用、什麼時候不用

- 用：手動跑一集或一段試拍；估一集、一個月的錢；選片段路線；把 Hailuo 網頁或 Kling 做的片段放進產線；階段以 2 或 3 停下而 `status` 看不出原因；試拍後寫 post-mortem；站主問「這樣要多少錢、為什麼重買」。
- 不用：開拍前的規劃、分鏡表、每鏡路線與秒數、動態分鏡、開拍鎖定與變更單（`.agents/skills/animation-preproduction/SKILL.md`，**付費之前先走完它**）；寫劇本與分鏡（`.agents/skills/youtube-video/references/drama-craft.md` 與 `.agents/skills/animation-camera/SKILL.md`）；畫面粗糙怎麼改（`visual-quality.md`）；主機工人自動跑的集（它照 `tools/video/automation/flow.mjs`，不照這裡）；教學投影片與品牌故事（沒有 clips，錢只有圖）。

## 先讀

| 你要做的 | 讀 |
| --- | --- |
| 付費之前：分鏡表、風險分級、每鏡路線與買幾秒、動態分鏡、三鏡小樣、開拍鎖定包、變更單 | `.agents/skills/animation-preproduction/SKILL.md` |
| 每一集的 19 步、指令、關卡與 `video.json` 欄位 | `.agents/skills/youtube-video/references/drama.md` |
| 分鏡的規格與檢查腳本（中位數、開場、鏡位） | `.agents/skills/youtube-video/references/drama-craft.md`、`.agents/skills/youtube-video/scripts/drama_craft_check.mjs` |
| 一鏡的 camera／prompt／motion 怎麼寫才被三個讀法讀成同一件事 | `.agents/skills/animation-camera/SKILL.md` |
| 十部動畫的 Veo Lite 契約、未成年、CC | `.agents/skills/youtube-video/references/animation-production.md` |
| 一版做出來之後怎麼診斷、怎麼停 | `.agents/skills/youtube-video/references/visual-quality.md` |
| 每個常數的出處、逐層算例、雜湊定義、估價與實際的已知落差 | `.agents/skills/animation-production/references/cost-model.md` |
| 每個階段真正查的前提、結束碼、dry-run、STOP、快取、外部片段用 `clips import` 匯入（唯一的一份程序） | `.agents/skills/animation-production/references/stage-preconditions.md` |
| 60 條錯誤：階段、哪個檢查抓、漏掉多少錢、預防（#51–#60 是規劃與網頁路線） | `.agents/skills/animation-production/references/error-catalogue.md` |
| 三條路線的方案、價目、隊列、版權、操作步驟 | `.agents/skills/animation-production/references/providers-and-plans.md` |
| 使用者指定 Hailuo／Kling 內建瀏覽器：本次工具能力、首格、三鏡 pilot、送出與下載收據 | `.agents/skills/animation-production/references/browser-production.md` |
| 指定「真一隻布袋喵」的鏡位與畫面感 | `.agents/skills/animation-camera/references/budaimiao-style.md`（沿用其中的觀察範圍與待驗項目） |
| 檢討表單與 2026-10-03 試拍的填法 | `.agents/skills/animation-production/references/post-mortem.md` |

## 階段順序與每個付費階段前要成立的事

手跑一集的人第一個問題是「現在按下去會不會以 2 或 3 停」，錢是第二個。順序是 `DRAMA_STEPS`（`tools/video/core/state.mjs`）：文件 → 劇本（`script` 關卡）→ `look` → `look` 關卡 → `tts` → `check-audio`（`audio` 關卡）→ `keyframes` → `storyboard` 關卡 → `render` → `clips` → `music` → `assemble` → `captions` → `final` 關卡 → `package` → `publish` 關卡。結束碼 `EXIT`（`tools/video/cli.mjs`）：1 lint 或檢查沒過、2 用法或順序、3 要站主、4 外部服務、5 工具沒裝；`MediaError` 的 `who` 決定 3／2／4（`tools/video/media/cli.mjs` 的 `exitFor`）。下表只列程式碼真的查的；完整版、行號與每個訊息在 stage-preconditions.md。

| 階段 | 花什麼 | 前提（成立才不會白跑或白花） | 出處 |
| --- | --- | --- | --- |
| `look` | 角色數 × 候選數的圖與 judge；沒過補一輪（`MAX_LOOK_ROUNDS` 2） | lint 零錯誤（否則 1）；有角色（無角色是 2，直接 `keyframes`）；漫劇開著、有圖片金鑰、本機權杖（否則 3）。**劇本已核准不是 `look.mjs` 查的**，是 drama.md 的規矩與工人的順序，手動跑也守 | `tools/video/media/look.mjs` 的 lint 檢查、`UsageError`、`requireCredentials`、`statusProblem` |
| `tts` | 站上 TTS 額度 | lint 零錯誤；權杖、金鑰（3）。不查任何關卡 | `tools/video/tts/cli.mjs` |
| `keyframes` | 每個要畫的鏡頭一張圖 ＋ judge，最多 3 次；`end_frame` 多一張、不 judge | lint；有角色時 `look` 關卡 `approved` 且每角色有選定（或 judge 建議）的設定圖，否則 **3**，訊息分 absent／missing／stale。不讀 timeline，所以可以在 `tts` 之前跑 | `tools/video/media/keyframes.mjs` 的 look 關卡檢查（`approvalState` ＋ `lookChosen`） |
| `render` | 0 | 縮圖那一鏡的關鍵影格已畫（否則 2）；burn-in 才要 timeline | `tools/video/render/cli.mjs` |
| `clips` | 每個 clip 鏡頭 `seconds` × 單價 ＋ judge，最多 2 次 | lint（1）；`timeline.json` 的 `speech_hash` 等於現在的劇本（否則 **2**）；`keyframes/manifest.json` 綁現在的 `look_hash` 與 `visual_hash`（否則 **2**）；每個 clip 與 still 鏡頭有通過 judge 的關鍵影格（否則 2）；`storyboard` 關卡 `approved`（否則 **3**）；production profile 的 provider／model／解析度與伺服器一致（否則 3，`requiredVideo` 檢查）；單支上限每次送出前查（否則 3）；ffmpeg（否則 5） | `tools/video/media/clips.mjs`、`tools/video/media/stages.mjs` 的 `Stage.spend` |
| `music` | 一首 | `timeline.json`（2）；自帶曲子在 `_music/` 且 `sha256` 對（否則 3）；`music_enabled`（3） | `tools/video/media/music.mjs` |
| `assemble` | 0 | timeline、旁白音檔證據、`frames/manifest.json`、`clips/manifest.json` 三個雜湊、production 檢查（都是 2）；`checks.json` 沒過 1 | `tools/video/assemble/cli.mjs` |

- **劇本關卡綁 `script.md`**（`tools/video/core/approvals.mjs` 的 `GATES`），由 `video.json` 的敘事重寫；改 prompt／camera／motion 不會讓它失效，改台詞才要再送。
- **look 與 storyboard 綁 manifest 的 SHA-256。** 重跑 `look` 或 `keyframes` 一定重寫 manifest（`generated_at` 也變，`keyframes.mjs` 與 `look.mjs` 寫 manifest 前那一行），就算每張都從 `media/cache.json` 拿回來，核准也變 `stale`，下一個階段以 3 停下。
- **`--shot` 只在雜湊沒變時有用**（例如給 `needs_review` 的鏡頭多 `--takes`）。改了任一鏡的 prompt／camera／motion 之後 `visualHash` 已變，`keyframes` 從空的 manifest 重建（`keyframes.mjs` 建 manifest 那一行的 `shots: {}`），這時 `--shot s04` 寫出來的 manifest 只有 s04，`clips` 對其他每一鏡回「have no passed keyframe」結束碼 2；要讓它們回來只能整個 `keyframes` 再跑，沒改的鏡頭從快取拿圖、但每鏡再 judge 一次（60 鏡 ＝ 60 × 0.01）。`clips` 同理（`clips.mjs` 的 `current` 不成立就 `shots: {}`）。所以改 prompt 只有一條路：攢齊再跑整個 `keyframes`。
- 每個付費階段都有 `--dry-run`（印估價與本月剩餘）；跑之前先 `drama_preflight.mjs`，它把上表的每一列算一遍。手動跑一集的骨架：

```bash
node tools/video/cli.mjs status --slug <SLUG>                                   # 做到哪、下一步；stale 的核准在 note
node tools/video/cli.mjs media-status --slug <SLUG>                             # 供應商、本月剩餘、這支的花費
node .agents/skills/animation-production/scripts/episode_estimate.mjs <VIDEO_DOCS>/video.json   # 開拍前：這一集值多少
node tools/video/cli.mjs look --slug <SLUG> --dry-run                           # 每個付費階段：先 dry-run
node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <SLUG> --stage look  # 再預檢
node tools/video/cli.mjs look --slug <SLUG> && node tools/video/cli.mjs review-push --slug <SLUG> --gate look
#   tts → check-audio → review-push --gate audio → keyframes（dry-run、preflight）→ review-push --gate storyboard
node tools/video/cli.mjs clips --slug <SLUG> --shot <第一鏡>                      # 第一鏡單獨跑：主機地區有沒有被擋
node tools/video/cli.mjs clips --slug <SLUG>                                    # 其餘；中途要停就放 STOP 檔
#   music → assemble → captions → review-push --gate final → package → review-push --gate publish
node .agents/skills/animation-production/scripts/run_report.mjs --slug <SLUG> --markdown   # 收工
```

## 錢怎麼算：一鏡、一集、一個月

一個 clip 鏡頭 ＝ 一張關鍵影格 ＋ 一次 judge ＋ 一份素材 ＋ 一次 judge；`visual: "still"` 少掉後兩項；`data.source` 的切鏡四項都不買（帳本記 `status: "cut"`）。**買的秒數不是鏡長**：`clipSeconds`（工具規定，`tools/video/media/clips.mjs`）在 `veo-3.1*` 配 **1080p** 時固定 8 秒，其他（含 Lite 720p）是 `clamp(ceil(frames/30), 4, 10)` 再往上貼齊模型的秒數表。價目都是 `apps/api/app/video_media/catalog.py`（2026-09-26 讀，圖片 09-28 再讀）；judge 每次 US$0.01（同檔 `JUDGE_USD_PER_CALL`，記帳用的定值，不是廠商的 token 帳）；圖 Gemini 3 Pro Image US$0.134；上限是 `MAX_KEYFRAME_TAKES` 3（`keyframes.mjs`）與 `MAX_CLIP_TAKES` 2（`clips.mjs`）。

| 一鏡 3 秒台詞 | 買幾秒 | 一次 | 到上限（圖 3 次、素材 2 次） |
| --- | --- | --- | --- |
| Veo 3.1 Lite 1080p（US$0.08/s） | 8 | 0.144 ＋ 0.65 ＝ **US$0.79** | 0.432 ＋ 1.30 ＝ US$1.73 |
| Gemini Omni 1.1 Flash（US$0.15/s，後台預設） | 4 | 0.144 ＋ 0.61 ＝ US$0.75 | US$1.65 |
| Veo 3.1（US$0.40/s） | 8 | 0.144 ＋ 3.21 ＝ US$3.35 | US$6.85 |
| MiniMax H3 2K（US$0.13/s；catalog 秒數 4–10） | 4 | 0.144 ＋ 0.53 ＝ US$0.67 | US$1.49 |
| still（只有圖） | 0 | US$0.144 | US$0.432 |
| `data.source` 切鏡 | 0 | 0 | 0 |

一集 3 分鐘、60 鏡（drama-craft 的中位數 2.5–3.5 秒，編輯判斷）、3 個角色各 3 張候選設定圖（`DEFAULT_LOOK_CANDIDATES`，`tools/video/core/drama.mjs`）、一首 Lyria（US$0.08）。數字是算式，不是量到的；試拍只買過 10 張圖、6 份素材。

| 等級（`series.json` 的 `visual_tier`，上限 `TIER_CLIP_SHARE_MAX`：clips 100%、hybrid 40%、stills 10%） | 設定圖 | 關鍵影格 | 素材（Lite／Omni／H3／Veo 3.1） | 一次合計（Lite） | 到上限（Lite） | 買到的片段秒數（Lite） |
| --- | --- | --- | --- | --- | --- | --- |
| clips：60 clip | US$1.30 | US$8.64 | 39.00／36.60／31.80／192.60 | **US$49.0** | US$106.6 | 480（上限 960） |
| hybrid：24 clip ＋ 36 still | 1.30 | 8.64 | 15.60／14.64／12.72／77.04 | US$25.6 | US$59.8 | 192 |
| stills：6 clip ＋ 54 still | 1.30 | 8.64 | 3.90／3.66／3.18／19.26 | US$13.9 | US$36.4 | 48 |

Veo 3.1 在 clips 等級一次就 US$202.6，過了單支上限 US$200（`max_usd_per_video` 預設，`apps/api/app/video_automation/models.py`）：最後幾鏡會以 3 停下（`stages.mjs` 的 `Stage.spend` → `capProblem`）。judge：一次 9 ＋ 60 ＋ 60 ＝ 129 次，到上限 318 次。一個月（預設額度 `models.py`：片段 3,000 秒、圖 1,500、judge 3,000、音樂 60；站主 2026-09-26 刻意開大）：Lite 下片段秒數是瓶頸，一集 480 秒 → 一個月 6 集（每鏡兩次 take 就 3 集），Omni／H3 是 12 集；judge 3,000 次 → 25 輪全集重跑；單支 US$200 只有 Veo 3.1 會破；細表在 cost-model.md §三。伺服器另有每小時上限：片段與音樂送出 60 次、圖 240 次、judge 360 次（`apps/api/app/video_media/admin_api.py`）——60 鏡一次 take 的 `clips` 至少排一小時，兩次兩小時。

**重跑時綁住你的是 judge。** 任何一鏡的 prompt 改了，keyframes 與 clips 的 manifest 都重建：沒改的鏡頭從 `media/cache.json` 拿回不付錢，但每一鏡都再 judge 一次（60 ＋ 60 ＝ 120 次 ＝ US$1.20，佔一小時額度的三分之一），storyboard 核准也失效。一個月 3,000 次只夠 25 輪這種全集重跑。

**第一條槓桿：鏡頭切短不省錢。** Lite 1080p 永遠買 8 秒，Omni／H3 最少 4 秒；一個 2 秒的鏡頭跟 4 秒的同價。密度（drama-craft 要的 2.5–3.5 秒中位數）只在兩種鏡頭上省得回來：回到同一鏡位的 `data.source` 切鏡（不畫圖、不買素材、不 judge）與 `visual: "still"`（production profile 不准）。利用率 ＝ 需要的秒數 ÷ 買到的秒數：60 鏡 × 3 秒在 Lite 下是 180 ÷ 480 ＝ 37.5%，沒有任何工具記這個數，`run_report.mjs` 補算。

其他槓桿（都在 `keyframes` 之前決定，之後每改一次就是上面那 120 次 judge）：

- **切鏡**：說—聽—說回到同一鏡位的第二、三鏡寫 `data.source`。可切的秒數是**來源鏡頭實際買到的**，不是 lint 的 10 秒或 profile 的 8 秒：Lite 1080p 永遠有 8 秒；Omni／H3 只買 `ceil(需要)` 且最少 4，3 秒的來源只買 4 秒、第二鏡只剩 1 秒可切（`clips.mjs` 在來源買下之後才把切鏡標 `needs_review`）。Omni／H3 下要嘛刻意把來源鏡頭寫長（多買秒數），要嘛接受重播來源自己用過的那段；這條槓桿只在 Lite 1080p 固定 8 秒時好用。一場說—聽—說的對話約省三分之一的素材（本 skill 的編輯判斷，未量過；切鏡規則在 drama-craft §五）。`episode_estimate.mjs` 的候選只比鏡位（camera 整行 ＋ prompt 第一子句，同 `craft.mjs` 的 `setupKey`），畫面一不一樣要人看，它只在 prompt 相似度低時標「同鏡位、畫面不同」；既有的 `data.source` 它對來源的買秒驗一次。
- **模型**：沒有 profile 釘模型時，Omni／H3 的 4 秒檔位比 Lite 的 8 秒省一半素材秒數（同價位下 Lite 0.64 vs Omni 0.60 一鏡，但 Omni 的利用率高一倍）；Veo 3.1 只給主鏡頭。
- **候選數**：`look.candidates` 2–4（lint，`drama.mjs` 的 look 檢查「must be 2 to 4」；預設 3）；`look --candidates` 1–6 只改這一次跑的張數，不進 `video.json`。角色多的集先用 2，不過再補一輪，比一開始就 4 張便宜。
- **超過 8 秒的鏡頭**：拆成兩鏡多買一份素材，但 Omni／H3 的 9–10 秒檔位本來就比兩個 4 秒貴；先看 `episode_estimate.mjs` 的「可併鏡」與「超過 8 秒」兩列再決定。
- **解析度**：伺服器按秒計價不看解析度（`meter.py` 的 `usd_for`），但 Lite 固定 8 秒只在 1080p（`clipSeconds` 的條件）；沒有 profile 的集把 Lite 設 720p，3 秒的鏡頭買 4 秒 ＝ US$0.32，是 1080p 的一半。有 profile 的集不能（`productionClipSizeProblem` 要原生 1920×1080），720p 的畫質也沒驗。
- **不省的**：judge 不能關；重跑 `keyframes --takes 1` 省的是上限不是一次。

## 三條路線：伺服器 API、Hailuo 網頁、Kling 網頁與選用的 CLI／MCP

使用者本次指定 Hailuo 或 Kling，並提供內建瀏覽器操作，**這次先沿指定的網頁路線**；不因過去選過 Kling CLI 或工具預設 API 就換路。CLI／MCP 是另行選用的替代方案。實作前讀 `.agents/skills/animation-production/references/browser-production.md`：核對本次工具的 upload／download 能力、先用已核准首格做三個連續鏡頭的 pilot、保留收據並實速看片，再擴大。方案與價目在 `.agents/skills/animation-production/references/providers-and-plans.md`；其中「實測 2026-10-04」保留的是歷史 Hailuo 一支 H3 2K 文生影片與 Kling CLI 輸出，不代表本次 Codex 瀏覽器或新素材已驗證。

**目前 `clips import` 對任何存在的 `series.production.profile` 都以 3 拒絕**（`tools/video/media/clips.mjs` 的 `importClip`），單改 profile 的 provider／model 也不會開放匯入。既有 profile 另由 `productionClipProblems` 與 `productionClipSizeProblem` 驗 provider、model、解析度、原生 1920×1080 及全鏡動態；目前作品的 Lite 契約在 `docs/videos/series-plans/production-20261001/profile.json`。外部路線可用於沒有 profile 的 pilot 或作品；現有正片要採用，須另做受核准的外部路線產線支援與契約更新，不能刪 profile 或偽標素材來繞過。這次 skill 更新不改這些程式條件，付費生成前先確認目的地收得進去。

| | 伺服器 API（`clips` 階段） | Hailuo 網頁方案（hailuoai.video） | Kling 網頁；CLI／MCP 為選用方案 |
| --- | --- | --- | --- |
| 誰跑 | 工人或代理，一條指令 | 代理在使用者提供的內建瀏覽器用**站主的登入**操作；依當次工具文件查 upload／download，歷史 Claude 限制不當成本次能力結論 | 本次先用同一個內建瀏覽器操作 Kling 網頁；另選官方 CLI／MCP 或社群 MCP 時才讀 providers §1.3 |
| 怎麼要一段 | 關鍵影格當首格 ＋ `clipPrompt`（motion ＋ camera ＋ look.motion）＋ look.negative ＋ 參考圖 ≤ 4（catalog 寫 0 的 Lite 與 H3 不送） | 網頁上傳本鏡核准首格，貼完整提示，選 16:9／單鏡／足夠秒數；歷史 H3 UI 是 768p／2K、4–15 秒，當次仍從表單核對 | 同左；本次模型／參數／點數以網頁為準。CLI 的 `first_image`、`enable_audio`／`prefer_multi_shots` 與 MCP camera control 只在另選那條 route 時用，不當作網頁欄位 |
| 每 8 秒 1080p 級畫面 | Lite US$0.64、Omni 1.20、H3 2K 1.04、Veo 3.1 3.20（catalog.py）；網頁照鏡長買，一鏡的錢可能比較少（`animation-preproduction/references/route-decisions.md` 第三節） | H3 2K 8 秒 96 點（12 點／秒，實測 2026-10-04：5 秒扣 60；輸出 2560×1440）；768P 8 秒 ≈ 56 點（頁面秒數／月反推，推算，沒量）。折美金看怎麼付（768P／2K）：年繳（頁面的 0.047／0.081 per s）≈ US$0.38／0.65；月繳 54.99 攤（一點 ≈ 0.0122）≈ US$0.68／1.17——月繳時 768P 已比伺服器 Lite 的 0.64 貴。Standard 2K 0.101/s | VIDEO 3.0／3.0 Omni 不開音訊 1080p 8 點／秒、720p 6（官方 2026-10-04，還沒在站主帳號實扣）：8 秒 64 點，Pro 月費攤 ≈ US$0.79；3–15 秒整數，照鏡長買。開發者 API 1080p US$0.112/s（官方） |
| 隊列與併發 | 一次一鏡順序跑；伺服器每小時 60 次送出、360 次 judge；job 24 小時沒完成就 `expired` | Standard 8 排／1 跑；Pro 8／2；Master、Max 12／2（官方方案表，2026-10-04 再讀；條款 2025-07-14 版的「排 5、跑 2」是舊的）。一支 H3 2K 5 秒、沒有排隊，送出到完成約 4 分 40 秒（實測 2026-10-04） | 付費方案「無限排隊、快速通道」；API 套餐 20 併發 |
| 浮水印與版權 | 無浮水印（Lyria 的曲子帶 SynthID） | 付費方案保留商用權，但乾淨的檔要走「全部下載 → 無水印下載」：結果卡 `<video>` 的 src 是有浮水印的版本（實測 2026-10-04），`clips import` 的 ffmpeg 檢查抓不到，只有 `--judge` 的 `no_text` 題可能抓到。免費有浮水印。輸出帶 AAC 音軌，成片不用 | 付費方案去浮水印、可商用 |
| 進產線 | 自動：manifest、QC、judge、帳本 | `clips import --provider hailuo-web`（stage-preconditions.md 最後一節）：前提同 `clips` 且不能有 profile，跑 ffmpeg QC；judge 要帶 `--judge` 才問 | 網頁用 `--provider external --note "route=kling-web …"`；CLI／MCP 用 `kling-mcp`，不把網頁來源寫成 MCP |
| 帳本知道 | 全部 | 匯入時記一筆 `status: "imported"`（點數、秒數；美元要 `--usd` 給），`status` 與 `clips --dry-run` 標出匯入幾支；快取與伺服器的每月預算不知道，`clips --force` 會把它重買 | 同左 |

同一集 60 鏡放到三條路線上（素材而已，不含圖與 judge；編輯換算，Hailuo 的美元都用**月費攤**，年繳換算在 cost-model.md §四）：

| 路線 | 買到的秒數 | 錢或點數（月費攤） | 佔月額度 | 幾小時 |
| --- | --- | --- | --- | --- |
| 伺服器 Lite 1080p | 480 | US$39.00 | 片段秒 16% | ≥ 1 小時（每小時 60 次送出） |
| 伺服器 Omni 1080p | 240 | US$36.60 | 8% | ≥ 1 小時 |
| Hailuo Pro，H3 768P 每鏡 4 秒 | 240 | ≈ 1,680 點（≈ 7 點/秒，推算）≈ US$20.5 | 4,500 點的 37%；2K（12 點/秒，實測 2026-10-04）是 64%；跟 Lite 一樣買 8 秒就 75%／128% | 2 個同時跑；量過一支：2K 5 秒、沒有排隊約 4 分 40 秒（實測 2026-10-04），768P 沒量 |
| Kling Pro，3.0 1080p 照鏡長每鏡約 4 秒 | 240 | 1,920 點（官方每秒價，未實扣）≈ US$23.7 | 3,000 點的 64% | 無限排隊，時間沒量 |

決定規則（編輯判斷）：

0. **付費之前先完成開拍鎖定包**（`.agents/skills/animation-preproduction/SKILL.md`）：每鏡的路線、模型、解析度、買幾秒、首尾格與定稿正文在那裡定、站主確認一次；這裡的規則是執行時的。
1. **使用者指定 route 優先，再查契約與能力**：本次是 Hailuo／Kling 內建瀏覽器；先照 browser-production 的三鏡 pilot 做。只在沒有指定 route 時，以伺服器 API 為預設；伺服器模型以 `media-status` 的實際設定為準，估價 `--model` 要對齊它。
2. **網頁成本與身份一致性要另外驗**：使用者選 Hailuo 或 Kling 不需要先通過「訂閱比 API 便宜」的假設；核對當次表單顯示的點數、剩餘額度、參考圖／首格能力與可下載規格，沿已授權預算操作。`episode_estimate.mjs --plan hailuo:pro --resolution 768p|2k` 可比較方案與 API；Kling 的每秒點數是官方價目、還沒實扣。Max 無限模式的適用模型照 providers §1.2，不假設 H3 免費。
3. **CLI／MCP 另選才用**：指令與歷史帳號實測在 providers §1.3；CLI 模型與參數不代表 Kling 網頁。網頁送出前後記點數與 job；結果不明先查任務／歷史與餘額，不重按建立。每鏡完整收據與 take 上限照 browser-production。
4. 不論哪條，**首格一律是這一鏡通過 judge 的關鍵影格**，否則 `assemble` 的第 0 格 PSNR ≥ 22（`tools/video/assemble/drama.mjs` 的 `KEYFRAME_MIN_PSNR`）過不了。

## 哪個改動會重買什麼

雜湊的定義：`lookHash` ＝ 解析後的 look（preset、style、negative、motion、candidates、style_frames）＋ 每個角色的 appearance 與 sheet_prompt（`tools/video/core/drama.mjs` 的 `lookHash`）；`visualHash` ＝ 縮圖 ＋ 每個場景的 id、template、chapter、`data`、句子 id 與 reveal、選用的命名造型（`tools/video/core/timeline.mjs` 的 `visualHash`）；`speechHash` ＝ 聲音、用到的字典條目、角色聲音、`action_seconds`、每句的文字／停頓／speaker／emotion（同檔 `speechHash`）。快取 key 含 prompt、negative、參考圖、seed、秒數（`drama.mjs` 的 `keyframeKey`／`clipKey`）。綁哪個檔在 cost-model.md §五；這張表是唯一的一份。

| 改了 | 變的雜湊 | 重買 | 失效的核准 |
| --- | --- | --- | --- |
| look 任一欄、角色 `appearance`、`sheet_prompt` | lookHash | **全部**設定圖、關鍵影格、素材（key 裡的 negative／參考圖都變了） | look、storyboard |
| 一鏡的 prompt／camera／motion／characters／fit／transition／source、縮圖、`character_looks` | visualHash | 那一鏡的圖與素材；其他鏡從快取拿回，但 judge 全部重付 | storyboard |
| 台詞文字、speaker、emotion、pause、`action_seconds`、角色聲音 | speechHash | 那幾句的 TTS；clips manifest 重建：秒數沒變的從快取拿回（Lite 1080p 永遠 8，不會變；Omni／H3 跨過整數秒才變），judge 全部重付 | audio |
| music 的 gain／duck／fade | mixHash | 只重混音 | final |
| `music.prompt` | mixHash ＋ key | 一首 US$0.08 | final |
| `subtitles` | subtitlesHash | burn-in 的字幕條與 assemble | final |
| 更改 `look.negative`（包括清空） | lookHash | 全部（第一列）；Lite adapter 已保留 avoidance，不需為相容性清空已核准的值 | 全部 |

## 重做還是重設計

judge 的 `problems` 文字先分類，再決定花不花第二次的錢：

| `problems` 裡的字 | 類別 | 做法 |
| --- | --- | --- |
| extra hand、second watch、another pen、pen lifted、switched hands、outfit changed、morphing back | 內容 | 改 prompt／motion／camera 或拆鏡（visual-quality.md：保留首格構圖與 camera，插鏡只寫袖口、錶、道具）；換 seed 沒用 |
| not the same person、face differs from the sheet | 內容（參考圖） | 看送了幾張參考（≤ 4；Lite 一張都不送，只靠首格）；首格本身先像設定圖 |
| text、letters、watermark | 內容偏隨機 | 關鍵影格：prompt 或 `look.style` 寫 no text；片段：`motion`（或 `look.motion`）寫，`data.prompt` 片段模型看不到；Lite adapter 會把完整 `look.negative` 接成 `Avoid: …`，非 Lite 保留原參數；不用為此更改已核准的 look |
| fingers、warped face、smeared background、flicker | 隨機 | 下一個 seed |
| eyes opening／blink（試拍 S01 R04 的 6.72） | 判讀 | 逐幀看、記下差異；不改分、不重判 |
| first frame does not show the keyframe（PSNR） | QC | 首格不是這一鏡的關鍵影格；外部片段最常見 |
| the model cut at N s；frozen inside the narrated part | QC | 一鏡一事、拆短、motion 寫看得見的動作 |

- 「換 seed」對圖片只是再抽一次：seed 是 take 編號（1、2、3），Gemini 圖片 API 不收 seed（`apps/api/app/video_media/providers/gemini_images.py` 不送）；Veo／Omni 收。
- 第二次的價：圖 US$0.144；素材 Lite 0.65、Omni 0.61、H3 0.53、Veo 3.21；Hailuo H3 2K 4 秒 48 點、768P 約 28 點（推算）；Kling 3.0 1080p 4 秒 32 點、720p 24 點（官方價，未實扣）。被退回的圖與素材都付了錢，留著當證據，不刪。
- 停的規則照 visual-quality.md：到 retake 上限、同一缺陷重複出現、付費結果不明就停那條分支；不改分、不降 `judge_min_score`（預設 7，單項低於 4 也不過，`apps/api/app/video_media/judge.py` 的 `MIN_CRITERION`）、不重複評分抽到過。試拍的證據：S01 四次素材、S03 兩次，退回原因都是同一類內容問題（多手、換腕、抬筆），重拍沒有收斂——這是重設計的訊號，不是再買一次的理由。

## 錯誤目錄：最貴的十二條

完整 50 條、按階段分組，在 `.agents/skills/animation-production/references/error-catalogue.md`（第 9 條是 0 元但整集排隊，留著）。

| # | 錯誤 | 階段 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- | --- |
| 1 | **歷史已修正**：試拍 Lite 因不支援的 `negativePrompt` 收到 HTTP 400；現行 adapter 省略該參數並完整保留限制到主提示（error-catalogue #23） | clips | 離線 provider request-body 回歸 | 當時每次 0.64 的預留（會退）＋ 一輪時間；試拍兩個 seed 都中 | `tasks/done/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md`；不清空已核准的 `look.negative`，不自動重買 |
| 2 | keyframes 之後才改 look 或 appearance | 任一 | `status`、preflight | 整集重買 | 先定 look；改之前看上表 |
| 3 | 一鏡小修就跑整個 `keyframes`／`clips` | keyframes、clips | preflight 的 kept／new | 上面那 120 次 judge ＋ 站主再審分鏡 | 攢齊再跑；`--shot` 救不了（階段順序那節） |
| 4 | 設定圖通過 judge 但道具錯（試拍：知棠 A 的錶是圓的，來源是矩形銀錶） | look | 無；站主或獨立看圖 | 一張 0.144 ＋ 之後每張關鍵影格跟著錯 | 看圖再核准；`sheet_prompt` 把識別道具寫進去 |
| 5 | 內容問題（多手、第二支錶、抬筆）重拍同一 prompt 再中（試拍：生成出來的 4 個 take 有 3 個在手與道具上出錯，S03 兩次上限用完、0 支可用；S01 R01／R02 是 API 400、沒生成） | clips | judge `clean`、`identity`；試拍是人 | 每次 0.65；兩次就把 `MAX_CLIP_TAKES` 用完 | 上節的分類表：內容問題改 prompt／motion，不換 seed |
| 6 | 把 job `ready` 當通過：試拍 16 jobs、14 ready、0 accepted | 收工 | `run_report.mjs` 五欄 | 誤報進度、放量 | 收工那節的五個數字 |
| 7 | keyframe 命名造型的 identity 題超過 400 字 → 伺服器 422，在圖買完之後；clip 的對應問題已修正 | keyframes | preflight 對本次要畫的鏡頭查實際題長 | 圖的錢花了、judge 沒做 | 修正真正超長的 keyframe 題；clip 已用有界題目與完整 context，不為它截短外觀或重做核准 |
| 8 | 兩鏡太像：lint 的 Jaccard 0.8 警告在前，dHash < 8 位元的警告在花錢之後；素材第 0 格比鄰鏡高不到 3 dB 就不過 | keyframes、clips | lint、`qc.mjs` | 兩鏡的圖與素材 | 回同一鏡位用 `data.source` |
| 9 | 第一鏡沒單獨跑：主機地區被 Gemini 擋，60 鏡排隊 | clips | 無 | 0 元，一輪 | `clips --shot <第一鏡>` |
| 10 | 關鍵影格畫完才改某一鏡的 `motion`／`camera`（圖片模型不讀 `motion`，但 `visualHash` 綁整個 `data`） | keyframes、clips | `plan_lock.mjs --check`；`status` | 每一鏡再 judge、storyboard 重審、已匯入的外部片段重匯 | 動作與運鏡在 `keyframes` 前定稿；改動攢齊走變更單（error-catalogue #51） |
| 11 | 素材比句子短，`fit: "auto"` 慢到 0.85 倍還不夠、停格超過 60 格 | assemble | `freezeProblem` → 1 | 一輪；profile 下不准 `freeze` | 拆句或要更長的素材；`estimate` 的「超過 8 秒」列 |
| 12 | 外部片段的首格不是關鍵影格 → `clips import` PSNR < 22 → `needs_review`，1 | clips import | `clips import` 的 `clipVerdict` | 那一支白做（點數不退） | 用這一鏡的關鍵影格當首格 |

## 收工

- **帳本** `media/ledger.json`：`entries[]` 的 `kind`（image／clip／music／judge）、`status`（ready／failed／judged／cut／imported）、`cost_usd`、`seconds`；`totalsOf` 從 entries 重算，`savedTotals` 算切鏡省下的、`importedTotals` 算 `clips import` 帶進來的（`tools/video/media/ledger.mjs`）。不在裡面的：沒給 `--usd` 的方案點數換成的美元、站上的保守預留（試拍的 US$10 manual reserve）、廠商實際帳單都不在裡面。
- **五個數字分開報**，不合成一個「完成」（錯誤 #6 指的就是這裡）：

| 數字 | 從哪裡算 | 試拍 2026-10-03（自己的 runner，不是 `clips` 階段） |
| --- | --- | --- |
| job `ready` | 伺服器 jobs | 14／16（2 failed） |
| QC ok | manifest 的 `qc.ok`；試拍是 root 與獨立 QA | 素材 1／6（S01 R04 抽樣可剪）；圖 4／10 |
| judge passed | manifest 的 `judge.passed` | 1／2（顧承川設定圖 7；S01 R04 片段 6.72 不過） |
| `needs_review` | manifest | — |
| 站主 accepted | `approvals.json` 的關卡；final 要站主看 | 0；60／100 |

- 列出每個關卡的 `approvalState`（approved／stale／missing／absent），stale 的要說是哪個改動害的。
- post-mortem 照 `.agents/skills/animation-production/references/post-mortem.md`，`run_report.mjs --markdown` 先把數字填好。素材與收據留 repo 外；公開文件不放憑證與機器路徑。

## 交接

停手前在票的 Notes 寫：到哪一步（`status` 的 next）、哪個關卡在等站主、`needs_review` 的鏡頭與 judge 的 problems、帳本總額與本月剩餘、`STOP` 檔有沒有留著、preflight 最後一次說了什麼。另一個代理接手只要這六樣；`media/jobs.json` 裡還在跑的 job 重跑階段會自己接著輪詢。

## 腳本

三支都離線、不花錢、不碰正式站，從 `tools/video` 相對路徑匯入；argv 只用 ASCII；結束碼 0、1（`--strict` 或有發現）、2（讀不到）。

```bash
# 估價：長度照 lint 的估法；每鏡買幾秒、圖、judge、一次與到上限的錢；每階段與整集的合計；
# --plan 換算成方案點數、月額度占比、跟伺服器並列的美元與損益平衡秒數；找槓桿（可切鏡、可 still、超過 8 秒、可併鏡）；
# 對 --cap、--month-clip-seconds、既有 data.source 的來源買秒下結論
node .agents/skills/animation-production/scripts/episode_estimate.mjs <VIDEO_DOCS>/video.json [--tier clips|hybrid|stills] [--model <id>] [--resolution 1080p|720p|768p|2k] [--plan hailuo:pro|kling:pro] [--credits-per-second 8] [--keyframe-takes 3] [--clip-takes 2] [--cap 200] [--month-clip-seconds 3000] [--strict] [--json]
#   --resolution 給伺服器模型的解析度；--plan hailuo:* 時它選 768p 或 2k 的檔位（不給就 2k；2K 輸出 2560×1440（實測 2026-10-04）、不是原生 1920×1080，768P 低於 1080p，哪個該選未驗）；--plan kling:* 時選 720p 或 1080p（不給就 1080p）
# 開跑前預檢：下一個（或 --stage 指定的）階段會拒絕或白花什麼：關卡狀態與會回的結束碼、manifest 綁哪個雜湊、kept／new、needs_review、STOP、judge 題目長度、profile 與伺服器、要花的 judge 次數、匯入與手放的外部片段；片段模型從 profile、存好的 manifest 或 --model 來（它不碰伺服器）
node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <SLUG> [--workdir <VIDEO_WORKDIR>] [--stage look|keyframes|clips|music|assemble] [--model <id>] [--json]
# 收工報告：帳本按種類與階段、每鏡 take 與通過、利用率、切鏡省的、外部片段、judge 次數、五個狀態、stale 的核准、每階段時間；--markdown 印填好數字的 post-mortem
node .agents/skills/animation-production/scripts/run_report.mjs --slug <SLUG> [--workdir <dir>] [--markdown] [--json]
```

價目在 `episode_estimate.mjs` 的 `PRICES` 表（以模型 id 或方案 id 為 key：Omni、Lite、Veo 3.1、Veo 3.1 Fast、H3、Pro Image、Lyria；別的模型給 `--price-per-second`），旗標可覆寫。`tools/animation-production.test.mjs` 對照 `catalog.py` 驗 API 價，並以合成劇本驗證 Lite 非空 avoidance 的估價／預檢、原核准不變、clip 有界題目與 keyframe 真長題拒絕。模型專屬 payload 的 Lite 省略／完整限制保留與非 Lite 參數保留由 `apps/api/tests/test_video_media_providers.py` 驗證；不以原始碼文字匹配代替行為測試。`.agents/skills/animation-production/references/post-mortem.md` 與原逐 take 表維持當時的試拍紀錄，不是修正後再付費驗收。

## 還沒驗、不能宣稱的事

- Kling：每秒點數有官方價目（2026-10-04 讀：1080p 不開音訊 8、720p 6），CLI 與網頁同一套積分也是官方說的，但站主帳號上還沒實扣過一支；輸出數是不是照支數乘、網頁 3.0 有沒有負面欄、實際輸出尺寸與 fps、付費方案在 CLI 上有沒有 1080p 都沒驗（providers §1.3）。
- Hailuo：量過的只有一支（實測 2026-10-04：H3 2K 5 秒文生影片，扣 60 點、約 4 分 40 秒、2560×1440、24 fps、帶 AAC 音軌）。768P 每秒幾點與輸出尺寸、有排隊時與 relax 隊列等多久、2K 縮成 1080p 與 768P 放大到 1080p 的畫質，都沒量。
- 歷史圖生影片（產線關鍵影格當首格）在 Hailuo 與 Kling 都還沒送過：當時 Claude 桌面版內建瀏覽器缺 upload 能力、Kling CLI 帳號沒有點數。這不是本次 Codex browser 的能力結論；依當次工具文件核對並把結果記進 browser-production 的能力表。
- `clips import`（PR #1183）用真的 ffmpeg 在下載的那支 Hailuo 片段上跑過（實測 2026-10-04）；它的檢查看不出浮水印，用關鍵影格做的外部片段還沒匯入過。
- 一集 60 鏡的估價是算式；試拍只買了 10 張圖與 6 份素材，廠商實際帳單對過前（`actual_billed_usd` 還是 null）預估不等於花費。
- 利用率沒有工具記，`run_report.mjs` 算的是 manifest 的 `needed_s ÷ seconds`。
- `max_clips_per_video`（預設 40）在 `media-status` 印得出來，2026-10-03 grep 沒找到伺服器或工具擋它的地方。
- Veo 3.1 的三個 id（Lite、Fast、generate-001）在 catalog 的 `status` 仍是 `preview`；Omni 不是。H3 的秒數 catalog 寫 4–10、官方頁寫 4–15。
