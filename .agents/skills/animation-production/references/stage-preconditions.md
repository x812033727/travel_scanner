# 每個階段真正查的前提：結束碼、dry-run、STOP、快取、地區、外部片段怎麼進來

`SKILL.md` 的表是摘要；這裡逐階段列程式碼查什麼、以哪個結束碼停、印什麼訊息，給 `drama_preflight.mjs` 當規格，也給你在它說不清楚時對照原始碼。**行號 2026-10-03 讀**（疊在 PR #1170 上），程式改了以函式名為準，行號只是當天的座標。結束碼表在 `tools/video/cli.mjs` 的 `EXIT`：`{ ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5, incomplete: 6 }`（6 是 `STOP` 檔讓 `tts`／`check-audio` 停在半途，2026-10-05 加）。媒體階段丟 `MediaError` 時由 `exitFor`（`tools/video/media/cli.mjs:26-30`）決定：`who: "owner"` → 3、`"tool"` → 2、其他 → 4；`UsageError` 與 `parseArgs` 的錯 → 2（`cli.mjs:238-241`）。

關卡的狀態（`approvalState`，`tools/video/core/approvals.mjs:91-106`）：`absent`（綁的檔還不存在）、`missing`（檔在、沒核准過）、`stale`（核准過，檔的 SHA-256 變了）、`approved`。綁的檔：`script` → `<VIDEO_DOCS>/script.md`；`look` → `characters/manifest.json`；`storyboard` → `keyframes/manifest.json`；`audio` → `timeline.json`（另驗每句 WAV 與整段旁白的雜湊）；`final` → `final.mp4`；`publish` → `upload/metadata.json`。

## 順序

`DRAMA_STEPS`（`tools/video/core/state.mjs:119-139`）：brief → outline approved → script passes lint → fact-checked → script approved → look generated → look approved → narration synthesized → narration approved → keyframes drawn → storyboard approved → frames rendered → clips generated → music generated → video assembled → captions written → final video approved → upload package → on YouTube。沒有角色的漫劇少掉兩個 look 步；沒有 `music` 少一步。`status --slug` 照這個順序印第一個沒完成的步與它的指令；它不印 kept／new，也不印外部片段。

## 逐階段

### `look`（`tools/video/media/look.mjs`）

| 查 | 不成立 | 行 |
| --- | --- | --- |
| lint 零錯誤 | 印 `has N lint errors; run lint first`，**1** | 84-87 |
| `format: "drama"` 且 `characters` 非空 | `UsageError`「a drama with none has no look stage: run keyframes」，**2** | 89 |
| `--candidates` 1–6（預設 `look.candidates`；`video.json` 裡 lint 只收 2–4，預設 3） | `UsageError`，2 | 105-106 |
| `--dry-run`：印角色 × 候選、每角色的 sheet prompt、伺服器狀態、一輪的錢、這支已花多少 | 0 | 107-119 |
| 本機權杖 | `requireCredentials` → MediaError owner，**3**「run login」 | 122 |
| 漫劇開著、圖片供應商有金鑰 | `statusProblem` → 3 | 125-126 |
| 單支上限（每張送出前） | `Stage.spend` → `video_media_cap`，3 | `stages.mjs:148-151` |
| 作品有存檔就沿用設定圖，只畫新角色（`reuseSheets`） | — | 18, 145 |

沒過的角色補一輪（seed 101…，`MAX_LOOK_ROUNDS` 2）；仍沒有一張通過 → `ERROR <id>: no candidate passed the judge`，**1**，改 `appearance` 或 `sheet_prompt` 再跑。`--choose jingwei=2` 本機選圖後 `approve --gate look`。**劇本關卡不在這裡查**：`look` 是第一筆花錢的東西，工人在劇本核准前不跑它（`drama.md` 的坑），手動也別跑。

### `tts`（`tools/video/tts/cli.mjs`）

lint 零錯誤（1）；權杖與站上 TTS 設定（3）；`--dry-run` 印每個聲音的字數與額度。不查任何關卡。`timeline.json` 寫 `speech_hash`。改了 `video.json` 的句子之後，沒重跑 `tts` 的話下游全部 2。

### `keyframes`（`tools/video/media/keyframes.mjs`）

| 查 | 不成立 | 行 |
| --- | --- | --- |
| lint 零錯誤 | 1 | 115-119 |
| 漫劇或插畫投影片 | `UsageError`，2 | 120 |
| `--shot a,b` 只畫這幾鏡（`data.source` 的鏡頭不畫） | 名字對不上 → 2 | 131-134 |
| `--takes` 1–6（預設 `MAX_KEYFRAME_TAKES` 3） | 2 | 135-136 |
| 有角色：`look` 關卡 `approved` **且**每角色有選定或建議的設定圖 | MediaError owner，**3**：「the look is not generated yet (run look)」／「not approved yet」／「changed since it was approved」／「approved but a character has no chosen sheet」 | 143-150 |
| `--dry-run`：每鏡完整 prompt 與參考圖、伺服器狀態、一次與到上限的錢 | 0 | 160-175 |
| 權杖、供應商 | 3 | 177-181 |
| manifest 沿用的條件：`look_hash`、`visual_hash`、同一個圖片模型、沒 `--force` | 否則從空的重建（每鏡再 judge） | 195-198 |
| 單支上限 | 3 | `stages.mjs:148-151` |

不讀 `timeline.json`：可以在 `tts` 之前跑。每鏡：有通過的就 `kept`；否則 take 1…N，judge 過就停；全沒過 → `needs_review`，印 `ERROR <id>: no take passed the judge`，**1**。`end_frame.prompt` 另畫一張（seed 1）、不 judge。畫完算相鄰 dHash（< 8 位元警告）、聯絡表、`generated_at`，再寫 manifest——所以**每次跑都改 manifest 的 SHA-256**，storyboard 核准變 stale。接著 `review-push --gate storyboard`。

### `render`（`tools/video/render/cli.mjs`）

lint（1）；縮圖鏡頭（`thumbnail.data.shot`）的關鍵影格要在 `keyframes/manifest.json`，否則 2（243-252）；`subtitles.burn_in: true` 才要 `timeline.json`（206-210，否則 2）；瀏覽器沒裝 5。不花錢。

### `clips`（`tools/video/media/clips.mjs`）

| 查 | 不成立 | 行 |
| --- | --- | --- |
| lint 零錯誤 | 1 | 119-123 |
| `format: "drama"` | 2 | 124 |
| `timeline.json` 存在且 `speech_hash` 等於現在的 | 「timeline.json is missing or was built for an older script; run tts first」，**2** | 130-134 |
| production profile 的鏡長規則（still、freeze、> 8 秒、切鏡超過 8 秒） | MediaError owner，3 | 135-136 |
| `keyframes/manifest.json` 的 `look_hash` 與 `visual_hash` 等於現在的 | 「keyframes/manifest.json is missing or was drawn for an older script or look; run keyframes first」，**2** | 137-141 |
| `--shot` 名字對得上 | 2 | 142-147 |
| 每個 clip 與 still 鏡頭有 `file` 且不是 `needs_review` | 「shots … have no passed keyframe; run keyframes first」，2 | 148-153 |
| `storyboard` 關卡 `approved` | 「the storyboard is not approved yet／changed since it was approved: run review-push --gate storyboard …」，**3** | 154-158 |
| `--takes` 1–5（預設 `MAX_CLIP_TAKES` 2） | 2 | 163-164 |
| `--dry-run`：每鏡的秒數、still／cut／clip、完整 clip prompt、伺服器、估價、本月剩餘 | 0 | 166-198 |
| Lite 下的未成年（`video_constraints`） | 3 | 200-215 |
| 權杖、供應商、`clip` 開著 | 3 | 217-221 |
| profile 釘的 provider／model／resolution 等於伺服器選的 | 「the approved production profile requires …; the server selects …」，**3** | 222-225 |
| ffmpeg | 5 | 230-237 |
| manifest 沿用的條件：三個雜湊 ＋（profile 下）同一個 provider／model／resolution ＋ 沒 `--force` | 否則重建 | 241-244 |
| 快取的素材不符 profile（`productionClipProblems`） | 3 | 268-273 |
| `start_frame.shot` 的素材已存在 | 2 | 287-293 |
| 單支上限（每份送出前） | 3 | `stages.mjs:148-151` |
| `data.source` 的來源素材已通過且夠長 | `needs_review`（來源沒過、太短） | 420-442 |

每鏡 take 1…N：`clipKey`（prompt、negative、秒數、解析度、seed、首尾幀、參考圖）查快取 → 送出（`native_audio: false`，伺服器對 Lite 強制 true）→ ffmpeg QC（`qc.mjs` 的門檻：≥ 1280×720、≥ 23 fps、短不超過 0.25 秒、黑格 ≥ 0.3 秒、旁白窗內凍格 ≥ 1 秒、0.1 秒後的切鏡、第 0 格 PSNR ≥ 22 且灰區 22–30 要比鄰鏡高 3 dB）→ judge（> 20 MB 自動 720p 代理）→ profile 下另驗原生 1920×1080 與素材蓋滿鏡長。全沒過 → `needs_review`，**1**，「fix the prompts of … and run clips again」。

`clips` 不讀開拍鎖定：一鏡鎖定時答應是 clip、現在 `visual: "still"`，它就照 still 做、不花錢也不問。擋這件事的是 `drama_preflight.mjs`（下面「開拍鎖定的承諾與連戲鎖」）。

### `music`（`tools/video/media/music.mjs`）

lint（1）；沒有 `music` → `UsageError` 2；`music.track`：檔在 `<VIDEO_WORKDIR>/_music/` 否則 3，`music.sha256` 不合 3，對了就寫 manifest 不花錢；`music.prompt`：`timeline.json`（2）、`--dry-run` 印秒數與價、`music_enabled` 與金鑰（3）、一首。

### `assemble`（`tools/video/assemble/cli.mjs`）

| 查 | 不成立 | 行 |
| --- | --- | --- |
| lint | 1 | 119-122 |
| `timeline.json` 的 `speech_hash` | 2 | 126-130 |
| 動畫類的正文長度 | 1 | 131-135 |
| 旁白音檔證據（每句 WAV 與 narration.wav 的雜湊） | 2 | 136-140 |
| `frames/manifest.json` 的 `visual_hash` | 2 | 141-146 |
| burn-in：字幕條綁現在的 `speech_hash` 與 `subtitles_hash` | 2 | 92-95 |
| `clips/manifest.json` 的 `speech_hash`、`visual_hash`、`look_hash` 三個都對 | 「clips/manifest.json is missing or was made for an older script or look; run clips first」，**2** | 97-99 |
| profile 下：每鏡素材有通過的 QC 證據且蓋滿鏡長、provider／model／resolution 對 | 2 | 153-158 |
| ffmpeg | 5 | 160-166 |
| 檢查（格數、響度、音樂床 ≤ −24 LUFS、每鏡第 0 格 PSNR ≥ 22、切鏡的 `source_frame_psnr`、凍格 > 60 格） | `checks.json.ok: false`，**1** | 360-466 |

不花錢；`checks.json` 寫六個雜湊（speech、visual、look、clips、subtitles、mix），`status` 靠它們判「video assembled」。

### 之後

`captions`（timeline，2）；`review-push --gate final` 先跑 `qa`；`package` 要 final 核准；`review-push --gate publish`。都不花錢。

## 開拍鎖定的承諾與連戲鎖（`plan/lock.json`，只有 `drama_preflight.mjs` 查）

階段模組（`look.mjs`、`keyframes.mjs`、`clips.mjs`、`assemble`）都不讀 `plan/lock.json`；是 `drama_preflight.mjs` 在每個階段多查這一項，而且只在有鎖定檔（animation-preproduction 的 `plan_lock.mjs --write`，第 3 版）時查，沒走開拍鎖定的集不受影響。承諾（delivery promise，OpenMontage 的叫法；AGPL，只借想法）是鎖定時每鏡答應的類型、買幾秒、路線與 `fit`；連戲鎖（continuity locks，drama-skills／shuohao-skills 分鏡表的欄位）是鎖定時從 `prompt` 抓出來、同場共用的道具／服裝字與時刻字。規格與詞表在 `.agents/skills/animation-preproduction/references/preproduction-flow.md`「鎖定包裡的承諾與連戲鎖」。

| 查 | 不成立 | finding 的 `id` |
| --- | --- | --- |
| 鎖定時答應 clip 的鏡頭現在還是 clip（不是 `visual: "still"`、不是 `source` 切的、沒從 `video.json` 刪掉） | refuse，**1**（lint 的碼）：「<id> 鎖定時答應的是 clip（買 N s，<路線>），現在是 still，沒有變更單」 | `promise.broken` |
| 鎖定時 `fit` 不是 `freeze` 的 clip，現在 `fit` 也不是 `freeze`（鎖定時就是 freeze 的不算） | refuse，**1**：「…現在 fit 是 freeze（鎖定時 auto），沒有變更單」 | `promise.broken` |
| 鎖住的道具／服裝／時刻字還在那一鏡的 `prompt` 裡（原樣的字、不分大小寫） | refuse，**1**：「<id> 鎖住的連戲字不在 prompt 裡了：時刻「dawn」，沒有變更單」 | `continuity.broken` |
| 上面任一項不成立，但 `plan/changes.jsonl` 有對照這把鎖（`previous_lock` ＝ 鎖的 `created_at`）、`shots` 記了這一鏡這個改動的變更單（`plan_lock.mjs --accept --note`） | note，不擋：「…有站主點頭的變更單（時間：站主的話）」 | `promise.signed`／`continuity.signed` |
| 鎖定檔讀得懂（第 3 版、欄位齊） | note：「plan/lock.json：version 2, …」，這一項不查 | — |

結果多一個 `lock` 欄：`{ file, created_at, version, problem, broken: { promise, continuity }, signed: { promise, continuity } }`（沒有鎖定檔是 `null`），文字輸出印成「開拍鎖定 <時間>：承諾改小 沒變更單 N／有 N；連戲字少了 沒變更單 N／有 N」。修法在 finding 的 `fix`：不是站主的意思就改回鎖定的樣子；是的話 `plan_lock.mjs --check` 印變更單、站主點頭後 `--accept --note "<站主的話>"`，或一次改完 `--write --force` 重鎖。收工時 `run_report.mjs` 把每鏡的承諾對交付（`clips/manifest.json`）與花的（ledger）列成「承諾 vs 交付」，守住幾鏡、改小幾鏡（其中沒簽變更單幾鏡）、承諾一次的價對實際花的差（負是省）。

## STOP、快取、job、帳本

- **STOP**：工作區或它的上一層有 `STOP` 檔（`tools/video/core/paths.mjs:85-86`），每次送出前與每次 judge 前都看（`stages.mjs:143-145, 168, 233`）。碰到就把這一鏡標 `needs_review: true, incomplete: true`、寫 manifest、印 `stopped by the STOP file after N new …; rerun to continue`、結束碼 0。重跑接著做。檔忘了拿掉，下一個階段一開始就停。
- **`media/cache.json`**：請求 key → 檔；同一個 key 不付第二次（`cached`，驗檔的 SHA-256 還在才算）。改 prompt、negative、參考圖、seed、秒數任何一樣都是新 key。
- **`media/jobs.json`**：送出了但沒等完的 job（STOP、當掉、逾時），下一次先輪詢它們（`pendingJob`），不重送；伺服器端 24 小時沒完成的 job `expired`。等待上限：圖 10 分鐘、片段 30、音樂 15（`stages.mjs:32`）。
- **`media/ledger.json`**：每筆生成與 judge（`bookJob`、`appendLedger`）；切鏡 `bookReuse` 記 `status: "cut"`、`saved_seconds`、`saved_usd`。失敗的 job 記 `cost_usd: 0`、`status: "failed"`，之後同一個 job 成功就覆寫，但已經記過的費用不會被失敗抹掉。
- **伺服器那邊**：預算在送廠商前預留，廠商拒收、濾掉、判失敗才退；**生成成功但下載失敗不退**（`apps/api/app/video_media/jobs.py:558-607`）；同一 `(slug, request hash)` 失敗 3 次 → 409，換提示詞或 seed。

## 主機地區：第一鏡先單獨跑

Gemini 的影片功能在歐洲經濟區與英國部分不開放，Veo 在歐盟只允許 `allow_adult`；基本的圖生影片會不會依呼叫端 IP 擋，沒查到（`docs/videos/DRAMA.md` §供應商「地區」）。所以每支的第一鏡先 `clips --slug <SLUG> --shot <第一鏡>` 單獨跑；被擋先回報，profile 釘了模型的集不自己換供應商（`drama.md` 的坑）。

## 外部片段怎麼進來（Hailuo／Kling 網頁、選用的 CLI／MCP）

用 `clips import`（`tools/video/media/clips.mjs` 的 `importClip`；設計在 `docs/videos/DRAMA.md`「外面做的片段」）。**這一節是唯一的一份程序**，`SKILL.md`、`providers-and-plans.md` §3、animation-camera 與 `drama_preflight.mjs` 都指到這裡。

```bash
node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"] [--judge] [--force]
```

**外部生成之前**：先確認 `series.production.profile` 不存在；目前 `importClip` 看到任何 profile 都以 3 拒絕，單改 provider／model 不會開放。既有正片的外部支援與契約更新是另一項工作，本次技能不改它。再用 `clips --slug <SLUG> --dry-run` 診斷 timeline／keyframes、抄本鏡需求秒數與 clip prompt；它的 server 模型／價不代表網頁。本次瀏覽器的能力核對、三個連續鏡頭 pilot 與完整 job／提示／首格 hash／點數收據照 `browser-production.md`。**用這一鏡通過 judge 的關鍵影格當首格**，否則匯入第 0 格 PSNR 過不了。送出結果未知先查任務歷史與餘額，不重買。

**來源值**：Hailuo 網頁用 `hailuo-web`；Kling 網頁用 `external`，在 `--note` 記 `route=kling-web`、job id 與外部收據位置；CLI／MCP 用 `kling-mcp` 並記實際 route。現有 provider enum 沒有 `kling-web`，不新增旗標、不把網頁偽標為 MCP。`--credits` 用實際餘額差額，未知扣點先留外部收據，不填 0 宣稱免費。

**指令依序查的前提**（任何一項不成立就停，檔案不複製、帳本不記）：

| 查什麼 | 不成立的結束碼 |
| --- | --- |
| `--slug`、`--shot`、`--file` 都有且檔案存在；`--provider` 是三個值之一；`--credits`／`--usd` 是 ≥ 0 的數 | 2 |
| lint 零錯誤 | 1 |
| 這一集**沒有** `series.production.profile` | **3**（`importClip` 對任何 profile 都拒絕；單改 profile provider／model 不解除，另需受核准的產線支援與契約更新） |
| 這一鏡是 clip 鏡：不是 still、不是 `source` 切的 | 2 |
| `timeline.json` 是現在的台詞；`keyframes/manifest.json` 是現在的劇本與 look；這一鏡的關鍵影格通過 judge | 2 |
| storyboard 已核准 | 3 |
| ffmpeg 與 ffprobe 在 | 5 |

**它做的事**：

1. 複製成 `clips/<shot>-import-<n>.mp4`（同一個檔再匯一次沿用編號，帳本也只留一筆）。
2. `ffprobe` 加 `tools/video/media/qc.mjs` 的黑格、旁白範圍內的凍格、模型自己切鏡、1280×720 與 23 fps 下限、第 0 格對這一鏡與相鄰關鍵影格的 PSNR，餵 `clipVerdict`——跟買來的 take 同一組，只少「比要求的秒數短」那一項（沒有向誰要過秒數；比台詞短只印提醒，由 `assemble` 的 `fitPlan` 慢放與停格，停格超過 60 格而 `fit` 不是 `"freeze"` 會在那裡不過）。
3. `--judge` 才把片段與角色設定圖上傳媒體庫、問 `clipRubric`（US$0.01，記帳；太大時跟 `clips` 一樣改送 720p proxy）。不帶 `--judge` 完全不碰網站，也不需要權杖。
4. 寫 manifest 的 `shots.<shot>`：`clips` 寫的形狀（`file`、`sha256`、`seconds`、`frames`、`needed_s`、`first_frame`、`qc`、`judge`、`takes`、`needs_review`）加 `provider`、`plan`、`credits`、`imported_at`（`--note` 寫進 `note`）；原本買的 take 留在 `takes`。從這一鏡切出去的鏡頭（`source`）跟著改指新檔。`clips_hash` 重算，`state.json` 記一次 `clips`。
5. 帳本一筆 `{ stage: "clips", kind: "clip", id, provider, plan, credits, seconds, cost_usd, file, sha256, status: "imported" }`：`seconds` 是量到的秒數四捨五入，`cost_usd` 是 `--usd`、沒給是 0——點數換美元照 `providers-and-plans.md` §1.2／§1.3 的表自己乘，工具不代換。沒過的也記（點數已經花了）。`totals.clip_seconds` 與單支上限都算它，`importedTotals`（`tools/video/media/ledger.mjs`）另外加總。

**結束碼**：0 過了；**1** 沒過——`needs_review: true`、`problems` 寫原因，重做一支再匯入，或 `--force` 留下它（`needs_review: false`、`forced: true`；量到的問題留在 `qc.problems`，那是看過之後的決定，不是量到的通過）；從這一鏡切出去的鏡頭因新檔太短而 `needs_review` 時也是 1。

**之後**：`status` 的 `clips generated` 後面寫「N of M clips imported: hailuo-web 1, …」；`clips --dry-run` 把它列成 imported、不估價；`clips` 留用它（`kept (imported from …)`）；`run_report.mjs` 與 `drama_preflight.mjs` 把匯入的與買的分開列。然後照常 `music`、`assemble`。

還是少掉的：judge 預設不問；`media/cache.json` 沒有它的請求鍵，所以 **`clips --force` 會把它重買**（要重做別的鏡用 `--shot`）；伺服器的每月預算與後台的 `media_usd` 不知道它；站方的任務 id、提示詞、送出與完成時間工具不記（要留就寫 `--note`）；relax 隊列的片段回來時台詞或鏡頭已經改了，指令以 2 停下，重跑 `tts`／`keyframes` 之後關鍵影格也換了，片段多半要重做；24 fps 或 768P 的檔會在 `assemble` 被重編碼進 30 fps 1080p 的時間軸，畫質沒驗。

**指令落地前手放的片段**（`clips/<shot>-ext<n>.mp4`，manifest 條目 `provider: "external"` 加 `external: { route, plan, credits }`，沒有帳本）：`run_report.mjs` 與 `drama_preflight.mjs` 仍認得，列成「手放」；它們沒經過 `clips` 的 QC，用 `clips import --file <那個 mp4>` 重新帶進來一次。
