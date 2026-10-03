# 每個階段真正查的前提：結束碼、dry-run、STOP、快取、地區、外部片段怎麼進來

`SKILL.md` 的表是摘要；這裡逐階段列程式碼查什麼、以哪個結束碼停、印什麼訊息，給 `drama_preflight.mjs` 當規格，也給你在它說不清楚時對照原始碼。**行號 2026-10-03 讀**（疊在 PR #1170 上），程式改了以函式名為準，行號只是當天的座標。結束碼表在 `tools/video/cli.mjs:21`：`{ ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 }`。媒體階段丟 `MediaError` 時由 `exitFor`（`tools/video/media/cli.mjs:26-30`）決定：`who: "owner"` → 3、`"tool"` → 2、其他 → 4；`UsageError` 與 `parseArgs` 的錯 → 2（`cli.mjs:238-241`）。

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

## STOP、快取、job、帳本

- **STOP**：工作區或它的上一層有 `STOP` 檔（`tools/video/core/paths.mjs:85-86`），每次送出前與每次 judge 前都看（`stages.mjs:143-145, 168, 233`）。碰到就把這一鏡標 `needs_review: true, incomplete: true`、寫 manifest、印 `stopped by the STOP file after N new …; rerun to continue`、結束碼 0。重跑接著做。檔忘了拿掉，下一個階段一開始就停。
- **`media/cache.json`**：請求 key → 檔；同一個 key 不付第二次（`cached`，驗檔的 SHA-256 還在才算）。改 prompt、negative、參考圖、seed、秒數任何一樣都是新 key。
- **`media/jobs.json`**：送出了但沒等完的 job（STOP、當掉、逾時），下一次先輪詢它們（`pendingJob`），不重送；伺服器端 24 小時沒完成的 job `expired`。等待上限：圖 10 分鐘、片段 30、音樂 15（`stages.mjs:32`）。
- **`media/ledger.json`**：每筆生成與 judge（`bookJob`、`appendLedger`）；切鏡 `bookReuse` 記 `status: "cut"`、`saved_seconds`、`saved_usd`。失敗的 job 記 `cost_usd: 0`、`status: "failed"`，之後同一個 job 成功就覆寫，但已經記過的費用不會被失敗抹掉。
- **伺服器那邊**：預算在送廠商前預留，廠商拒收、濾掉、判失敗才退；**生成成功但下載失敗不退**（`apps/api/app/video_media/jobs.py:558-607`）；同一 `(slug, request hash)` 失敗 3 次 → 409，換提示詞或 seed。

## 主機地區：第一鏡先單獨跑

Gemini 的影片功能在歐洲經濟區與英國部分不開放，Veo 在歐盟只允許 `allow_adult`；基本的圖生影片會不會依呼叫端 IP 擋，沒查到（`docs/videos/DRAMA.md` §供應商「地區」）。所以每支的第一鏡先 `clips --slug <SLUG> --shot <第一鏡>` 單獨跑；被擋先回報，profile 釘了模型的集不自己換供應商（`drama.md` 的坑）。

## 外部片段怎麼進來（Hailuo 網頁、Kling MCP 做的）

今天沒有 `clips import`（票 `tasks/open/2026-10-03-clips-import-bring-a-clip-made.md`），只能手動；**這一節是唯一的一份程序**，`SKILL.md`、`providers-and-plans.md` §3、animation-camera 與 `drama_preflight.mjs` 都指到這裡，票落地後只改這裡。前提：這一集**沒有** production profile（有的話 `productionClipProblems`／`productionClipSizeProblem` 擋 manifest 裡的 provider／model／resolution 與非原生 1920×1080，`tools/video/core/lint.mjs:408-434`）；這一鏡的關鍵影格已通過 judge 而且 storyboard 已核准（`clips` 的規矩，手動也守）；外部生成時**用這張關鍵影格當首格**。

1. 先跑一次 `clips --slug <SLUG> --dry-run` 確認 timeline 與 keyframes 都是現在的；再跑 `clips --slug <SLUG> --shot <其他鏡>` 或至少讓 `clips/manifest.json` 存在且三個雜湊對（手寫也行：`speech_hash`、`visual_hash`、`look_hash` 從 `status --json` 或 `drama_preflight.mjs --json` 抄；頂層另有 `clip: { provider, model, resolution }`，下一次 `clips` 會改成伺服器的選擇）。
2. 把 mp4 放到 `<VIDEO_WORKDIR>/<SLUG>/clips/<shot>-ext<n>.mp4`（工具自己的 take 叫 `-1`、`-2`，外部用 `-ext1`、`-ext2`，不要跟 seed 編號撞；票落地後指令會寫 `-import-<n>`）。
3. `ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_read_packets,duration -of json <mp4>`：記 `frames`（`nb_read_packets`）、`seconds`（整數秒）、`width`、`height`、`fps`；算 sha256。
4. 自己跑 `clips` 階段對買來的 take 做的 ffmpeg QC——**`assemble` 不跑這些**：`tools/video/media/qc.mjs` 的 `blackdetectArgs`（黑格 ≥ 0.3 秒）、`freezedetectArgs`（旁白窗內凍格 ≥ 1 秒）、`sceneCutArgs`（0.1 秒後模型自己切鏡）、`framePsnrArgs`（第 0 格對關鍵影格，`THRESHOLDS.keyframe_min_psnr` 22），用 `node -e` 匯入它們拿到 ffmpeg 參數跑一次，結果餵 `clipVerdict` 得到 `qc: { ok, problems, metrics }`。沒跑就不要寫 `qc.ok: true`——那是你的斷言，不是量到的；沒有 profile 時 assemble 不讀 `qc`，留 `null` 也行。
5. 在 `clips/manifest.json` 的 `shots.<shot>` 寫一筆，欄位照 `clips` 自己寫的形狀（`clips.mjs:391-406` 的 `record`）：

   ```json
   {
     "file": "clips/wr-e01-s03-ext1.mp4", "sha256": "<檔案 sha256>", "key": null, "seed": null,
     "seconds": 8, "frames": 200, "needed_s": 3.4,
     "first_frame": { "file": "keyframes/wr-e01-s03-2.png", "sha256": "<該圖 sha256，抄 keyframes/manifest.json>" },
     "qc": { "ok": true, "problems": [], "metrics": { "width": 1920, "height": 1080, "fps": 25, "duration": 8.0, "black": 0, "freezes": 0, "cuts": 0, "keyframe_psnr": 31.2, "judge": null } },
     "judge": null, "takes": [], "needs_review": false,
     "provider": "external", "external": { "route": "hailuo-web", "plan": "pro", "credits": 96, "model": "MiniMax-H3", "resolution": "2K", "record": "clips/wr-e01-s03-ext1.external.json" }
   }
   ```

   `needed_s` 是鏡長（timeline 的格數 ÷ 30）；`qc` 只寫第 4 步量到的（例子裡的數字是示意）；`needs_review` 不是 `false` 的鏡 assemble 拒絕。`provider` 與 `external` 是本 skill 加的，工具不讀也不壞：`run_report.mjs` 與 `drama_preflight.mjs` 靠 `provider: "external"` 或帳本沒有這一鏡的 job 認出它，路線與點數從 `external` 讀；`clips import` 落地後改用票裡平鋪的 `provider`、`plan`、`credits`、`imported_at`。`clips_hash` 用 `clipsHash([{ id, sha256 }…])`（`tools/video/core/drama.mjs:606`）照鏡頭順序重算（`node -e` 匯入它），否則 `status` 與 `checks.json` 對不上。
6. 每一段記一份 `clips/<shot>-ext<n>.external.json`（和試作的 `docs/videos/series-plans/competition-20261002/cost-ledger.csv` 同一套欄位；§3 的 import 工具就讀這個）：

   ```json
   {
     "shot": "wr-e01-s03", "route": "hailuo-web", "plan": "pro", "billing": "monthly",
     "credits_before": 4120, "credits_after": 4024, "credits": 96,
     "model": "MiniMax-H3", "resolution": "2K", "seconds": 8, "ratio": "16:9",
     "first_frame_sha256": "<keyframes/manifest.json 的 sha256>", "last_frame_sha256": null,
     "prompt_sha256": "<送出的提示詞的 sha256>", "task_id": "<站方的任務 id>",
     "submitted_at": "2026-10-03T10:12:00+08:00", "ready_at": "2026-10-03T10:19:00+08:00",
     "file": "clips/wr-e01-s03-ext1.mp4", "sha256": "<下載檔的 sha256>",
     "probe": { "width": 2048, "height": 1152, "fps": 25, "duration": 8.0 },
     "accepted": null, "rejection_reason": null
   }
   ```

   （`probe` 的像素是示意；H3 2K 的實際尺寸沒有讀，以 `ffprobe` 為準。）可選：在 `media/ledger.json` 的 `entries` 加 `{ at, stage: "clips", kind: "clip", id: "<shot>", provider: "external", plan, credits, seconds, cost_usd: 0, status: "imported" }`；`totalsOf` 下次寫入時會重算。沒加也行，`run_report.mjs` 把 manifest 有、帳本沒有的列成 external。
7. 跑 `assemble`。它對外部素材真正做的檢查（`tools/video/assemble/cli.mjs` 只匯入 `freezeProblem`、`keyframeProblem`、`sourceFrameProblem` 與 `checkBed`）：檔案存在；`ffprobe` 的格數減 `from_frame` 要 > 0；`fitPlan`（`tools/video/assemble/drama.mjs`）——比句子長就從尾端裁、比句子短就最多放慢到 0.85×（`fit: "slow"` 到 0.5×）再停格補，停格超過 60 格（`MAX_FREEZE_FRAMES`）而 `fit` 不是 `"freeze"` 就 CHECK 不過；**第 0 格對關鍵影格 PSNR ≥ 22**（`KEYFRAME_MIN_PSNR`，寫進 `checks.json.metrics.shots[].keyframe_psnr`；切鏡對來源格是 `sourceFrameProblem`）；然後整支的 probe、響度、音樂床。沒過就 `checks.json` 說哪一鏡，**1**。24 fps 或 768P 的檔會被重編碼進 30 fps 1080p 的時間軸，畫質沒驗。

少掉的：judge（identity、motion、clean、no_text 都沒人問）；黑格、freezedetect、模型自己切鏡、1280×720 與 23 fps 下限、時長短於要求 0.25 秒、相鄰關鍵影格的 3 dB 餘裕只在 `clips` 的 `clipVerdict` 跑（第 4 步自己跑）；帳本與 `media-status` 不知道、`status` 把它當買的、下一次 `clips --force` 會把它覆蓋掉（它的 key 不在快取裡）。relax 隊列的片段回來時 timeline 已經改了的話，manifest 的雜湊對不上，整個 manifest 要重建，條目也要重寫。
