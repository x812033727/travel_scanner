---
id: 2026-10-24-manga-sticker-drama-pace-visible-camera
title: 貼圖漫劇（manga）節奏：看得見的運鏡、2–3.5 秒一切、停頓與音效、說書人聲音——照兩支十萬點閱參考片量出來的差距改
status: review
priority: P1
area: tools
owner: claude-fable-5-1-manga-pace
claimed_at: 2026-10-24T15:38:07Z
created_at: 2026-10-24T15:30:00Z
completed_at:
branch: claude/vibrant-satoshi-a86eb7
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - docs/videos/BINGE.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
  - docs/videos/series-plans/xitong-shuo-wo-shi-bug/authoring.md
  - docs/videos/series-plans/xitong-shuo-wo-shi-bug/site-note.md
---

# 貼圖漫劇（manga）節奏：看得見的運鏡、2–3.5 秒一切、停頓與音效、說書人聲音

## Why

站主 2026-10-24 看《系統說我是 BUG》第 1 集成片：「有點單調、節奏有點慢」，要我看 YouTube 上別人怎麼做。用同一把尺（96×54 灰階、每 0.25 秒一幀的相鄰幀差；切點≥45、鏡內動量＝切點以外的中位差；語速從字幕算）量了兩支參考與我們的成片：

| | 桃桃爱漫画 `0r9ZmCt-BtQ`（109 分、20.6 萬次） | 花影漫剧 `zH9N0JXvhlQ`（125 分、11.6 萬次，BINGE.md 的參考） | 我們 e001 body（172 秒） |
| --- | --- | --- | --- |
| 鏡長中位（硬切） | 開場 1.75 s、中段 3.25 s（最長 6.5） | 開場 2.5 s（最長 6.25） | **3.75 s**（最長 7.25） |
| 鏡內動量中位 | 10–12.5 | 7.8 | **1.2** |
| 靜止幀比（差 <3） | 0% | 15% | **80%** |
| 語速 | — | 句內 5.0–5.4 字/秒；每 10 分鐘 36–43 個 >1.5 秒空檔，37–45% 的時間沒人說話 | 3.03 字/秒，全集只有約 1 秒空檔 |

單調來自三件事疊加：

1. **運鏡幾乎看不見。** `tools/video/assemble/drama.mjs`：`MOTION_ZOOM 0.10`、`MOTION_PAN_ZOOM 1.08`、`MOTION_DRIFT_ZOOM 0.04`、travel 要 6 秒才走完（`MOTION_TRAVEL_SECONDS`），註解寫明「small on purpose: a still is meant to read as a held shot」。這是為插圖投影片寫的；動態漫畫的參考片整張圖一直在動（動量 8–12 對我們的 1.2）。
2. **切得慢。** 規則是「每 3–5 秒一張」（`prompts.mjs` manga 段落、BINGE.md §畫面等級、企劃包 authoring／site-note），e001 實際 46 鏡／172 秒＝3.7 秒；參考 1.75–3.2 秒。
3. **旁白是教學片的聲音指示。** drama 分頁 `drama_voice` 空 → `settingsFor` 退回教學片的 Sulafat「Relaxed, conversational tech explainer… Medium-brisk pace」，所以 manga 提示詞裡寫的「說書人、節奏快、尾音乾脆」從沒到過 TTS；3 字/秒連著念、沒有停頓、沒有音效（主機沒有 `_sfx` 組，寫手也不寫 sfx）。參考是句內快講＋大量停頓讓音效與畫面接手。

## Definition of done

- [x] manga 等級的 still 運鏡看得見：同一把尺量新成片，鏡內動量中位 ≥ 6、靜止幀比 ≤ 20%（參考 7.8–12.5／0–15%）；其他等級與插圖投影片的運鏡一個位元組不變（分開的常數與 `MOTION_ENCODER_VERSION`／segment key，讓舊片不重算、新片不撞快取）。→ 程式與本機量測做完（Notes 的表），成片的數字等 e005。
- [x] manga 的切法改成每 2–3.5 秒一張（lint 對 manga 的鏡長有上限警告），BINGE.md、企劃包 authoring／site-note、`prompts.mjs` 同步；每集圖數約 +40%（US$0.4／集），寫進 BINGE.md 的估算。→ 美元數字沒寫死（單價隨 catalog 的圖片模型），BINGE.md §成本與吞吐寫的是鏡數與倍數。
- [x] 旁白：撰稿規則要求「叮」之後、揭曉前留一拍空檔（線上 pause 節拍或空白句），manga 的 narration performance 直接寫進 video.json 的旁白 voice.style（不依賴 drama 分頁的 `drama_voice`），或 `settingsFor` 對 manga 給說書預設；drama 分頁 `drama_voice` 為空時的退回值改成說書式（`models.py` DEFAULT_VOICE 那段）。→ 做在 `flow.mjs` `settle`（見 Notes）；`models.py` 沒動，理由在 Notes。
- [ ] 音效：至少「叮」（面板跳字）有音效。主機沒有 `_sfx` 組，要站主放授權檔（YouTube 音效庫）進 `<work base>/_sfx/<set>/` 並寫 manifest（ILLUSTRATED.md §音效）；寫手在 manga 等級為每個「叮」放 cue。沒有音效組就只做前三項。→ **沒做**：主機沒有音效組，等站主放檔；放了之後另開票讓寫手為「叮」放 cue。

## Steps

- [x] `assemble/drama.mjs`：讀 `series.json` 的 `visual_tier`（assemble 已拿 `project.series`），manga 用一組大的常數，相鄰鏡頭方向輪替已有；加 `MOTION_MANGA_VERSION` 進 segment key。測試量 zoompan 表達式。
- [x] `prompts.mjs` manga 段落「A new picture every 3 to 5 seconds」→ 2 到 3.5 秒，一鏡一句；`lint.mjs` 對 manga 鏡頭 >4 秒警告；BINGE.md §畫面等級與企劃包規則同步；`validate.mjs` 不動（它量的是鉤子）。
- [x] 旁白停頓與聲音：見 DoD 第 3 項；e001 的基準：48 句、170.8 秒有聲、空檔 1 秒。
- [ ] 改完先用 e005（還沒畫）試一集，同一把尺量成片，數字進這張票；e001–e004 不重做。→ 等部署後第一集新組的片。

## How to verify

主機 video-worker：`ffmpeg -v error -i build/body.mp4 -vf "fps=4,scale=96:54,format=gray" -f rawvideo -pix_fmt gray -` 餵 node 算相鄰幀差（腳本在 Notes），鏡內動量中位 ≥ 6、靜止幀比 ≤ 20%、鏡長中位 ≤ 3.5 秒；`node --test tools/video/assemble/drama.test.mjs`。

## Notes

- 量法細節與數字在記憶 `travel-scanner-manga-pace-reference-20261024`；YouTube 頁內的 timedtext 沒登入會回空，花影的字幕是本機 `python -m yt_dlp --skip-download --write-subs --sub-langs zh-Hant --sub-format json3` 抓的。
- 參考合集沒有每集章節卡（花影只有三個通用時間戳），我們 compile 的 2 秒章節卡＋每集 YouTube 章節保留，站主 10-24 要「合集分章節就好」。
- 旁白比例 80% 字數不是問題：爽文動態漫畫本來就是旁白帶，問題在速度與停頓。
- 改 `drama.mjs`／`prompts.mjs`／`lint.mjs` 會讓時長收據過期，要獨立審查者做增量（記憶 travel-scanner-duration-receipt）。

### 2026-10-25 做了什麼（claude-fable-5-1-manga-pace）

這張票原本只在 #1798 的分支上，先 `git show origin/claude/bug-story-120min-planning-a85b50:tasks/open/…` 複製進來再認領（`--force`：五張重疊範圍的票都是別的分支上 in-progress 的 lint／prompts 共用檔）。#1798 合併後若這檔衝突，以這邊的版本為準。

1. **運鏡**（`assemble/drama.mjs`、`assemble/cli.mjs`）：`layoutDrama(..., { tier })` 由 cli 傳 `project.series?.visual_tier`；manga 的 still 運鏡物件多 `profile: "manga"`，`zoompanExpr`／`motionTravel`／`motionChain` 從 `motionProfile(move)` 讀常數：`MANGA_MOTION = { zoom 0.20, panZoom 1.12, driftZoom 0.10, driftShare 0.30, travelSeconds 3, travelMin 0.6 }`（原 still 常數 0.10／1.08／0.04／0.15／6 秒／0.5 一個不動）。`motionSegmentKey` 在有 profile 時多推 `MOTION_MANGA_VERSION`＋profile；沒有 profile 的 key 測試釘住 main 的值（`d6b028730031d355`、`5090ede238e2ddfc`），所以其他等級、插圖投影片、Shorts（`shorts/motion.mjs` 走 `motionMove` 沒帶 profile）與舊片都不重算。
   - 常數是量出來的，不是票上例舉的 0.25／1.25／0.12：本機用 ffmpeg 對一張柔化的 1080p 圖（接近動漫圖的頻率）組 3 秒段，用票的尺量（4 fps、96×54 灰階、相鄰幀平均差中位）：

     | 運鏡 | 原 still 常數 | 0.25／1.25／0.12（票的例子） | **0.20／1.12／0.10（採用）** | 0.18／1.10／0.08 |
     | --- | --- | --- | --- | --- |
     | push／pull | 3.8（靜止幀 36%） | 16.0 | **13.5** | 12.7 |
     | pan | 11.1 | 45.3（最大 47，會被當成硬切） | **29.2** | 25.4 |
     | tilt | 5.6 | 29.4 | **16.1** | 13.7 |
     | drift | 1.65（靜止幀 100%） | 11.5 | **10.1** | 8.0（靜止幀 9%） |

     e001 幾乎全是 drift／push，所以整集 1.2；參考 7.8–12.5。採用的一組五種運鏡都 ≥ 10、靜止幀 0%，pan 的最大差 35 離硬切門檻 45 還有距離（票例子的 1.25 會讓量尺把 pan 數成切點）。
   - 量測腳本（也是部署後量 e005 的腳本；主機上把 `motionSegmentArgs` 那段換成直接讀 `build/body.mp4`）：

     ```js
     // node measure.mjs body.mp4 ：fps=4、96×54 灰階；差 ≥45 算硬切；切點以外的中位差＝鏡內動量；差 <3 的幀比例＝靜止比
     import { spawnSync } from "node:child_process";
     const raw = spawnSync("ffmpeg", ["-v", "error", "-i", process.argv[2], "-vf", "fps=4,scale=96:54,format=gray", "-f", "rawvideo", "-pix_fmt", "gray", "-"], { encoding: "buffer", maxBuffer: 1 << 30 }).stdout;
     const size = 96 * 54, frames = Math.floor(raw.length / size), diffs = [];
     for (let f = 1; f < frames; f++) { let s = 0; for (let i = 0; i < size; i++) s += Math.abs(raw[f * size + i] - raw[(f - 1) * size + i]); diffs.push(s / size); }
     const cuts = diffs.map((d, i) => (d >= 45 ? i : -1)).filter((i) => i >= 0);
     const shots = cuts.map((c, i) => (c - (cuts[i - 1] ?? 0)) / 4).sort((a, b) => a - b);
     const inside = diffs.filter((d) => d < 45).sort((a, b) => a - b);
     console.log({ seconds: frames / 4, cuts: cuts.length, shot_median_s: shots[Math.floor(shots.length / 2)], motion_median: inside[Math.floor(inside.length / 2)].toFixed(2), still_share: (inside.filter((d) => d < 3).length / inside.length * 100).toFixed(0) + "%" });
     ```

2. **切法**：`prompts.mjs` manga 段落改「every 2 to 3.5 seconds, one line per shot…the lint warns on any shot over 4 seconds」；`lint.mjs` 新增 `MANGA_SHOT_MAX_SECONDS = 4`、`mangaShotLengthProblems`，只在 `context.series.visual_tier === "manga"` 跑，訊息標「estimated」。BINGE.md §畫面等級表格與新的一條、§成本與吞吐、authoring.md、site-note.md 同步。**site-note.md 是站主貼進站上作品備註的文字，改檔不會改站上的備註**；要讓寫手拿到新規則，站主得把 site-note.md 第一段重新貼進《系統說我是 BUG》的作品備註（提示詞的 manga 段落已經改了，所以只貼不貼差在備註與規則一致）。
3. **旁白**：`flow.mjs` `settle` 在 `format === "drama" && series.visual_tier === "manga"` 且 drama 分頁 `drama_voice` 為空、聲音是 Gemini 時，把 `voice.style` 寫成 `CHANNEL_ACCENT。MANGA_NARRATION_PERFORMANCE`（後者從 `prompts.mjs` 匯出，是 manga 提示詞裡站主 10-22 的那句說書指示）；站主選了 `drama_voice` 就以它為準。`models.py` 的 `DEFAULT_VOICE` **沒改**：它在程式裡本來就是說書式（09-29 的 register），正式站的 settings 列是站主貼的教學片文字，改程式預設不會動到已存在的列；而且記憶寫 10-24 站主已把正式站 drama 分頁 `drama_voice` 設成 Sulafat＋說書式，第 5 集起生效，所以這個退回值是給新安裝或清空設定時的保險。撰稿規則多兩拍：每個「叮」自成一句（`"text": "叮。"`、`pause_after_ms` 500），揭曉或反轉前一句 `pause_after_ms` 800。
4. **沒做**：音效（主機沒有 `_sfx`）；e005 的成片量測（等部署）；`binge_quote` 的 `SHOTS_PER_MINUTE` 沒改（在時長收據裡且不在這張票的範圍，BINGE.md 寫了低估多少）。
5. 時長收據：`prompts.mjs`、`lint.mjs`、`lint.test.mjs`、`flow.mjs`、`assemble/cli.mjs`、`automation.test.mjs` 六個在 `REVIEW_FILES`（`assemble/drama.mjs` 不在），PR 由獨立審查代理做 DURATION_ONLY 增量（見 PR）。
