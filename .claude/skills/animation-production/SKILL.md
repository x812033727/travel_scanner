---
name: animation-production
description: AI 漫劇的製作實務：階段順序與每個付費階段前要成立的事（關卡、雜湊、結束碼 2／3）、一鏡／一集／一個月的錢怎麼算、三條生成路線（伺服器 API、Hailuo 網頁方案、Kling MCP）各自的價、隊列、版權與怎麼進產線、哪個改動會重買什麼、重做還是重設計、最貴的錯誤目錄與抓它的檢查、收工的帳本與五種狀態、post-mortem 表單，加三支離線腳本：估價、開跑前預檢、收工報告。要手動跑一集漫劇的 look／keyframes／clips、估一集或一個月的預算、決定片段用哪條路線、把外部做的片段放進產線、查階段為什麼以結束碼 2 或 3 停下、或在試拍後寫檢討時，先讀這個 skill；它不取代 youtube-video 的 drama.md（怎麼跑）、drama-craft.md（分鏡規格）與 visual-quality.md（畫面診斷），只補它們沒有的錢與錯誤。Plan, price, preflight and post-mortem an AI drama episode run by hand through the server API, a Hailuo web plan or Kling's MCP, with every number traced to its constant or price page.
metadata:
  short-description: 動畫製作：階段前提、成本、三條路線、錯誤目錄、檢討
---

# 動畫製作（animation-production）

給**用手跑一集 AI 漫劇**的代理：自己下 `look`、`tts`、`keyframes`、`clips`、`music`、`assemble`，或在試拍後向站主報帳、寫檢討的人。主機工人（`node tools/video/cli.mjs auto`）不讀 skill，它該守的規矩都在 `tools/video`；這裡寫的是程式碼不替你擋、花了錢才知道的事：每個付費階段前要成立什麼、一鏡一集一個月各多少錢、哪個改動會重買什麼、哪些錯誤最貴、收工要交什麼。

每個數字後面標來源：**工具規定**（檔案與函式或常數；行號只在 `references/stage-preconditions.md`，那裡註明讀取日）、**價目**（檔案或網址，加查閱日）、**模型限制**、**量到的**（試拍紀錄）、**編輯判斷／換算**。沒標的就當沒驗。路徑相對於 repo 根目錄；工作區在 `<VIDEO_WORKDIR>/<SLUG>/`（repo 外）。

## 什麼時候用、什麼時候不用

- 用：手動跑一集或一段試拍；估一集、一個月的錢；選片段路線；把 Hailuo 網頁或 Kling 做的片段放進產線；階段以 2 或 3 停下而 `status` 看不出原因；試拍後寫 post-mortem；站主問「這樣要多少錢、為什麼重買」。
- 不用：寫劇本與分鏡（`.agents/skills/youtube-video/references/drama-craft.md` 與 `.agents/skills/animation-camera/SKILL.md`）；畫面粗糙怎麼改（`visual-quality.md`）；主機工人自動跑的集（它照 `tools/video/automation/flow.mjs`，不照這裡）；教學投影片與品牌故事（沒有 clips，錢只有圖）。

## 先讀

| 你要做的 | 讀 |
| --- | --- |
| 每一集的 19 步、指令、關卡與 `video.json` 欄位 | `.agents/skills/youtube-video/references/drama.md` |
| 分鏡的規格與檢查腳本（中位數、開場、鏡位） | `.agents/skills/youtube-video/references/drama-craft.md`、`.agents/skills/youtube-video/scripts/drama_craft_check.mjs` |
| 一鏡的 camera／prompt／motion 怎麼寫才被三個讀法讀成同一件事 | `.agents/skills/animation-camera/SKILL.md` |
| 十部動畫的 Veo Lite 契約、未成年、CC | `.agents/skills/youtube-video/references/animation-production.md` |
| 一版做出來之後怎麼診斷、怎麼停 | `.agents/skills/youtube-video/references/visual-quality.md` |
| 每個常數的出處、逐層算例、雜湊定義、估價與實際的已知落差 | `.agents/skills/animation-production/references/cost-model.md` |
| 每個階段真正查的前提、結束碼、dry-run、STOP、快取、外部片段手動匯入（唯一的一份程序） | `.agents/skills/animation-production/references/stage-preconditions.md` |
| 50 條錯誤：階段、哪個檢查抓、漏掉多少錢、預防 | `.agents/skills/animation-production/references/error-catalogue.md` |
| 三條路線的方案、價目、隊列、版權、操作步驟 | `.agents/skills/animation-production/references/providers-and-plans.md` |
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

## 三條路線：伺服器 API、Hailuo 網頁方案、Kling MCP

站主 2026-10-03 定的：Hailuo 的方案由代理在網頁上操作，Kling 用 MCP。方案與價目在 `references/providers-and-plans.md`（2026-10-03 讀官方頁，表裡只列決定用的幾個數）。

**有 production profile 的集今天只能走伺服器 API。** 正在做的那部（`docs/videos/series-plans/competition-20261002/pilot/series.json` 的 `production.profile.video`，同 `docs/videos/series-plans/production-20261001/profile.json`）就釘了 gemini／`veo-3.1-lite-generate-preview`／1080p、`visual_tier: clips`：`clips` 擋伺服器選了別的模型（`clips.mjs` 的 `requiredVideo` 檢查，3）；`tools/video/core/lint.mjs` 的 `productionClipProblems` 擋 manifest 裡別的 provider／model／解析度，`productionClipSizeProblem` 擋非原生 1920×1080（H3 的 2K 與 768P 都不是），`status` 與 `assemble` 都呼叫它。站主要的 Hailuo 與 Kling 兩條路眼下只能用在試拍與沒 profile 的集；要讓正片用，得先改 profile（換掉核准的設計雜湊），或等 `clips import` 的票把 `provider: "external"` 納進 profile 檢查（第二張票，站主決定）。

| | 伺服器 API（`clips` 階段） | Hailuo 網頁方案（hailuoai.video） | Kling MCP（kling.ai/mcp 官方 connector；或社群 mcp-kling 用 API 金鑰） |
| --- | --- | --- | --- |
| 誰跑 | 工人或代理，一條指令 | 代理在內建瀏覽器或 Playwright 裡用**站主的登入**操作 SPA（React，WebFetch 只拿到殼）；不用代理自己的帳號 | 代理透過 Claude Desktop／claude.ai 的 connector（官方，登入 Kling 帳號）或 `generate_image_to_video`（社群，API 金鑰對） |
| 怎麼要一段 | 關鍵影格當首格 ＋ `clipPrompt`（motion ＋ camera ＋ look.motion）＋ look.negative ＋ 參考圖 ≤ 4（Lite 0） | `/create/image-to-video`：上傳關鍵影格當首格、參考圖欄「參考（0/12）」、選模型／解析度／秒數／比例、貼 prompt | 首格 ＋ motion prompt ＋ camera control `static`／`zoom`／`pan`／`auto`（社群 MCP 的參數） |
| 每 8 秒 1080p 級畫面 | Lite US$0.64、Omni 1.20、H3 2K 1.04、Veo 3.1 3.20（catalog.py） | Pro 以上 H3 768P 8 秒 ≈ 56 點、2K ≈ 96 點（頁面秒數／月反推，換算）。折美金看怎麼付：年繳（頁面的 0.047／0.081 per s）≈ US$0.38／0.65；月繳 54.99 攤（一點 ≈ 0.0122）≈ US$0.68／1.17——月繳時 768P 已比伺服器 Lite 的 0.64 貴。Standard 2K 0.101/s | 3.0 Omni 標準 5 秒 ≈ 35–45 點、10 秒約兩倍（第三方 2026 數字，**未驗**；8 秒不是 Kling 的檔位）；Pro US$37／3,000 點 → 10 秒約 US$1；開發者 API 1080p ≈ US$0.112/s |
| 隊列與併發 | 一次一鏡順序跑；伺服器每小時 60 次送出、360 次 judge；job 24 小時沒完成就 `expired` | Standard 8 排／1 跑；Pro 8／2；Master、Max 12／2（條款另寫「最多 5 個併發」） | 付費方案「無限排隊、快速通道」；API 套餐 20 併發 |
| 浮水印與版權 | 無浮水印（Lyria 的曲子帶 SynthID） | 付費方案下載無浮水印、保留商用權；免費有浮水印 | 付費方案去浮水印、可商用 |
| 進產線 | 自動：manifest、QC、judge、帳本 | 手動匯入（stage-preconditions.md 最後一節，唯一的一份程序）：放 mp4、手寫 manifest 條目。`assemble` 只驗格數、第 0 格 PSNR（切鏡對來源格）、fit 的停格 > 60 格與響度；黑格、freezedetect、模型自己切鏡只在 `clips` 的 `qc.mjs` 跑，外部片段要自己用 `blackdetectArgs`／`freezedetectArgs`／`sceneCutArgs` 跑一次；沒有 judge | 同左 |
| 帳本知道 | 全部 | 不知道，`status` 也分不出它是買的；`clips import` 做好前都這樣（票 `tasks/open/2026-10-03-clips-import-bring-a-clip-made.md`） | 不知道 |

同一集 60 鏡放到三條路線上（素材而已，不含圖與 judge；編輯換算，Hailuo 的美元都用**月費攤**，年繳換算在 cost-model.md §四）：

| 路線 | 買到的秒數 | 錢或點數（月費攤） | 佔月額度 | 幾小時 |
| --- | --- | --- | --- | --- |
| 伺服器 Lite 1080p | 480 | US$39.00 | 片段秒 16% | ≥ 1 小時（每小時 60 次送出） |
| 伺服器 Omni 1080p | 240 | US$36.60 | 8% | ≥ 1 小時 |
| Hailuo Pro，H3 768P 每鏡 4 秒 | 240 | ≈ 1,680 點（≈ 7 點/秒）≈ US$20.5 | 4,500 點的 37%；2K 是 64%；跟 Lite 一樣買 8 秒就 75%／128% | 2 個同時跑，每支時間沒量 |
| Kling Pro，3.0 Omni 標準 5 秒 | 300 | ≈ 2,100–2,700 點（未驗）≈ US$26–33 | 3,000 點的 70–90% | 無限排隊，時間沒量 |

決定規則（編輯判斷）：

1. **預設走伺服器 API**：關卡、快取、帳本、judge、單支上限只認得它；有 profile 的集只有它（上段）。沒有 profile 時伺服器買哪個模型以後台的 clip 設定為準：新裝的預設是 `gemini-omni-1.1-flash`（`catalog.py` 的 `DEFAULT_CLIP`；後台可能改過，`media-status` 才是真的），估價時 `--model` 對齊它——這決定 3 秒的鏡頭買 4 秒（US$0.60、利用率 75%）還是 8 秒（0.64、37.5%），也決定切鏡槓桿與 Lite 陷阱會不會發生。
2. **Hailuo 網頁**划算的條件有三個，同時成立才走：站主已付的點數反正月底歸零（條款）；這一鏡不靠角色參考圖保一致（網頁能上傳參考，但沒有我們的 identity 題）；你接受手動匯入、沒有帳本。算式只有一條：方案贏過伺服器要這個月**真的用掉的秒數 ≥ 月費 ÷ 伺服器每秒價**——Pro 月繳 54.99 ÷ 0.15（Omni）≈ 367 秒、÷ 0.08（Lite）≈ 687 秒而 Pro 一個月只有 375 秒 2K，不可能；`episode_estimate.mjs --plan hailuo:pro --resolution 768p|2k` 把這一集的伺服器價、方案的兩種美元與損益平衡秒數印在一起。Max 的無限模式只給 Hailuo 2.0／2.3（哪些模型、兩個來源怎麼說：providers §1.2 的 Max 列），不是 H3。
3. **Kling MCP**：要運鏡控制或動作戲時用；每支影片的點數只在登入後的生成頁看得到，MCP 扣哪個方案的點數、官方 connector 要不要 API 套餐，都先在站主帳號裡讀，再估價。
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
| `look.negative: ""`（Lite 陷阱的權宜，錯誤目錄第 1 條） | lookHash | 全部（第一列）——所以要在 `look` 之前就覆寫，不是 `clips` 之前 | 全部 |

## 重做還是重設計

judge 的 `problems` 文字先分類，再決定花不花第二次的錢：

| `problems` 裡的字 | 類別 | 做法 |
| --- | --- | --- |
| extra hand、second watch、another pen、pen lifted、switched hands、outfit changed、morphing back | 內容 | 改 prompt／motion／camera 或拆鏡（visual-quality.md：保留首格構圖與 camera，插鏡只寫袖口、錶、道具）；換 seed 沒用 |
| not the same person、face differs from the sheet | 內容（參考圖） | 看送了幾張參考（≤ 4；Lite 一張都不送，只靠首格）；首格本身先像設定圖 |
| text、letters、watermark | 內容偏隨機 | 關鍵影格：prompt 或 `look.style` 寫 no text；片段：`motion`（或 `look.motion`）寫，`data.prompt` 片段模型看不到；Lite 的 negative 進不去（錯誤目錄第 1 條） |
| fingers、warped face、smeared background、flicker | 隨機 | 下一個 seed |
| eyes opening／blink（試拍 S01 R04 的 6.72） | 判讀 | 逐幀看、記下差異；不改分、不重判 |
| first frame does not show the keyframe（PSNR） | QC | 首格不是這一鏡的關鍵影格；外部片段最常見 |
| the model cut at N s；frozen inside the narrated part | QC | 一鏡一事、拆短、motion 寫看得見的動作 |

- 「換 seed」對圖片只是再抽一次：seed 是 take 編號（1、2、3），Gemini 圖片 API 不收 seed（`apps/api/app/video_media/providers/gemini_images.py` 不送）；Veo／Omni 收。
- 第二次的價：圖 US$0.144；素材 Lite 0.65、Omni 0.61、H3 0.53、Veo 3.21；Hailuo Pro 768P 約 56 點、Kling 標準 5 秒約 35–45 點（未驗）。被退回的圖與素材都付了錢，留著當證據，不刪。
- 停的規則照 visual-quality.md：到 retake 上限、同一缺陷重複出現、付費結果不明就停那條分支；不改分、不降 `judge_min_score`（預設 7，單項低於 4 也不過，`apps/api/app/video_media/judge.py` 的 `MIN_CRITERION`）、不重複評分抽到過。試拍的證據：S01 四次素材、S03 兩次，退回原因都是同一類內容問題（多手、換腕、抬筆），重拍沒有收斂——這是重設計的訊號，不是再買一次的理由。

## 錯誤目錄：最貴的十二條

完整 50 條、按階段分組，在 `references/error-catalogue.md`（第 9 條是 0 元但整集排隊，留著）。

| # | 錯誤 | 階段 | 誰抓 | 漏掉的代價 | 預防 |
| --- | --- | --- | --- | --- | --- |
| 1 | Veo Lite 配任何命名 preset（`custom` 以外都有 negative）→ 廠商 HTTP 400 → 伺服器只說「Gemini refused the request」（`gemini_video.py` 對每個模型都送 `negativePrompt`；完整說法與對策只在 error-catalogue #23） | clips | 沒人；`estimate --model veo-3.1-lite*`、preflight 抓 | 每次 0.64 的預留（會退）＋ 一輪時間；試拍兩個 seed 都中 | 一開始就 `look.negative: ""`，等 `tasks/open/2026-10-02-honor-veo-lite-negativeprompt-compatibility.md` 落地 |
| 2 | keyframes 之後才改 look 或 appearance | 任一 | `status`、preflight | 整集重買 | 先定 look；改之前看上表 |
| 3 | 一鏡小修就跑整個 `keyframes`／`clips` | keyframes、clips | preflight 的 kept／new | 上面那 120 次 judge ＋ 站主再審分鏡 | 攢齊再跑；`--shot` 救不了（階段順序那節） |
| 4 | 設定圖通過 judge 但道具錯（試拍：知棠 A 的錶是圓的，來源是矩形銀錶） | look | 無；站主或獨立看圖 | 一張 0.144 ＋ 之後每張關鍵影格跟著錯 | 看圖再核准；`sheet_prompt` 把識別道具寫進去 |
| 5 | 內容問題（多手、第二支錶、抬筆）重拍同一 prompt 再中（試拍 S01 四次、S03 兩次，0 支接受） | clips | judge `clean`、`identity`；試拍是人 | 每次 0.65；兩次就把 `MAX_CLIP_TAKES` 用完 | 上節的分類表：內容問題改 prompt／motion，不換 seed |
| 6 | 把 job `ready` 當通過：試拍 16 jobs、14 ready、0 accepted | 收工 | `run_report.mjs` 五欄 | 誤報進度、放量 | 收工那節的五個數字 |
| 7 | 命名造型的 `appearance` 太長 → judge 題目超過 400 字 → 伺服器 422，在圖買完之後 | keyframes、clips | preflight | 圖的錢花了、judge 沒做 | `appearance` 約 160 字以內（換算自 `clips.mjs` 的 `clipRubric` 模板） |
| 8 | 兩鏡太像：lint 的 Jaccard 0.8 警告在前，dHash < 8 位元的警告在花錢之後；素材第 0 格比鄰鏡高不到 3 dB 就不過 | keyframes、clips | lint、`qc.mjs` | 兩鏡的圖與素材 | 回同一鏡位用 `data.source` |
| 9 | 第一鏡沒單獨跑：主機地區被 Gemini 擋，60 鏡排隊 | clips | 無 | 0 元，一輪 | `clips --shot <第一鏡>` |
| 10 | `end_frame.prompt` 寫了很多鏡 | keyframes | `estimate` | 每鏡多一張 0.134；dry-run 還多算 0.01 judge | 只給真的要末格的鏡 |
| 11 | 素材比句子短，`fit: "auto"` 慢到 0.85 倍還不夠、停格超過 60 格 | assemble | `freezeProblem` → 1 | 一輪；profile 下不准 `freeze` | 拆句或要更長的素材；`estimate` 的「超過 8 秒」列 |
| 12 | 外部片段的首格不是關鍵影格 → assemble PSNR < 22 → 1 | assemble | `assemble` | 整段匯入白做（點數不退） | 用這一鏡的關鍵影格當首格 |

## 收工

- **帳本** `media/ledger.json`：`entries[]` 的 `kind`（image／clip／music／judge）、`status`（ready／failed／judged／cut）、`cost_usd`、`seconds`；`totalsOf` 從 entries 重算，`savedTotals` 算切鏡省下的（`tools/video/media/ledger.mjs`）。它只記伺服器買的：外部片段、站上的保守預留（試拍的 US$10 manual reserve）、廠商實際帳單都不在裡面。
- **五個數字分開報**，不合成一個「完成」（錯誤 #6 指的就是這裡）：

| 數字 | 從哪裡算 | 試拍 2026-10-03（自己的 runner，不是 `clips` 階段） |
| --- | --- | --- |
| job `ready` | 伺服器 jobs | 14／16（2 failed） |
| QC ok | manifest 的 `qc.ok`；試拍是 root 與獨立 QA | 素材 1／6（S01 R04 抽樣可剪）；圖 4／10 |
| judge passed | manifest 的 `judge.passed` | 1／2（顧承川設定圖 7；S01 R04 片段 6.72 不過） |
| `needs_review` | manifest | — |
| 站主 accepted | `approvals.json` 的關卡；final 要站主看 | 0；60／100 |

- 列出每個關卡的 `approvalState`（approved／stale／missing／absent），stale 的要說是哪個改動害的。
- post-mortem 照 `references/post-mortem.md`，`run_report.mjs --markdown` 先把數字填好。素材與收據留 repo 外；公開文件不放憑證與機器路徑。

## 交接

停手前在票的 Notes 寫：到哪一步（`status` 的 next）、哪個關卡在等站主、`needs_review` 的鏡頭與 judge 的 problems、帳本總額與本月剩餘、`STOP` 檔有沒有留著、preflight 最後一次說了什麼。另一個代理接手只要這六樣；`media/jobs.json` 裡還在跑的 job 重跑階段會自己接著輪詢。

## 腳本

三支都離線、不花錢、不碰正式站，從 `tools/video` 相對路徑匯入；argv 只用 ASCII；結束碼 0、1（`--strict` 或有發現）、2（讀不到）。

```bash
# 估價：長度照 lint 的估法；每鏡買幾秒、圖、judge、一次與到上限的錢；每階段與整集的合計；
# --plan 換算成方案點數、月額度占比、跟伺服器並列的美元與損益平衡秒數；找槓桿（可切鏡、可 still、超過 8 秒、可併鏡）；
# 對 --cap、--month-clip-seconds、既有 data.source 的來源買秒、Lite 配非空 look.negative 下結論
node .agents/skills/animation-production/scripts/episode_estimate.mjs <VIDEO_DOCS>/video.json [--tier clips|hybrid|stills] [--model <id>] [--resolution 1080p|720p|768p|2k] [--plan hailuo:pro|kling:pro] [--credits-per-video 40] [--keyframe-takes 3] [--clip-takes 2] [--cap 200] [--month-clip-seconds 3000] [--strict] [--json]
#   --resolution 給伺服器模型的解析度；--plan hailuo:* 時它選 768p 或 2k 的檔位（不給就 2k；2K 不是原生 1920×1080，768P 低於 1080p，哪個該選未驗）
# 開跑前預檢：下一個（或 --stage 指定的）階段會拒絕或白花什麼：關卡狀態與會回的結束碼、manifest 綁哪個雜湊、kept／new、needs_review、STOP、Lite 的 negative、judge 題目長度、profile 與伺服器、要花的 judge 次數、沒帳本的外部片段；片段模型從 profile、存好的 manifest 或 --model 來（它不碰伺服器）
node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <SLUG> [--workdir <VIDEO_WORKDIR>] [--stage look|keyframes|clips|music|assemble] [--model <id>] [--json]
# 收工報告：帳本按種類與階段、每鏡 take 與通過、利用率、切鏡省的、外部片段、judge 次數、五個狀態、stale 的核准、每階段時間；--markdown 印填好數字的 post-mortem
node .agents/skills/animation-production/scripts/run_report.mjs --slug <SLUG> [--workdir <dir>] [--markdown] [--json]
```

價目在 `episode_estimate.mjs` 的 `PRICES` 表（以模型 id 或方案 id 為 key：Omni、Lite、Veo 3.1、Veo 3.1 Fast、H3、Pro Image、Lyria；別的模型給 `--price-per-second`），旗標可覆寫；`tools/animation-production.test.mjs` 對照 `catalog.py` 驗 API 價，並驗 `gemini_video.py` 仍送 `negativePrompt`。那條測試紅的那天（上面那張票落地）要刪的 Lite 陷阱：這裡錯誤目錄第 1 條、「哪個改動會重買什麼」最後一列、「重做還是重設計」text 列的 Lite 半句、`references/error-catalogue.md` #7 與 #23、`references/cost-model.md` §一 Lite 列的註與 §五最後一列、`references/providers-and-plans.md` §1.1 的坑、`scripts/drama_preflight.mjs` 的 `LITE_MODEL` 檢查、`scripts/episode_estimate.mjs` 的 `liteNegativeProblem`、測試裡那條 assertion；animation-camera 的 `references/model-misreads.md` 第三節、其 SKILL.md「三個欄位各給誰讀」的 negative 句、「同一鏡在 Hailuo 與 Kling 怎麼寫」表的否定列、檢查清單第 10 條、「模型畫錯過的事」末句。`references/post-mortem.md` 範例裡的 Lite 句是試拍紀錄，留著。

## 還沒驗、不能宣稱的事

- Kling 每支影片的點數、MCP 扣哪個方案、官方 connector 的操作頁（登入後才看得到）；第三方的 35–45 點是傳聞。
- Hailuo 網頁一支的生成時間、relax 隊列等多久、條款的「5 個併發」與方案表的 8／2 哪個算數；2K 輸出的像素尺寸；768P 放大到 1080p 的畫質。
- 一集 60 鏡的估價是算式；試拍只買了 10 張圖與 6 份素材，廠商實際帳單對過前（`actual_billed_usd` 還是 null）預估不等於花費。
- 利用率沒有工具記，`run_report.mjs` 算的是 manifest 的 `needed_s ÷ seconds`。
- `max_clips_per_video`（預設 40）在 `media-status` 印得出來，2026-10-03 grep 沒找到伺服器或工具擋它的地方。
- Veo 3.1 的三個 id（Lite、Fast、generate-001）在 catalog 的 `status` 仍是 `preview`；Omni 不是。H3 的秒數 catalog 寫 4–10、官方頁寫 4–15。
