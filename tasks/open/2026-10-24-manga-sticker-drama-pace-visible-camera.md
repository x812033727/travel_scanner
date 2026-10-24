---
id: 2026-10-24-manga-sticker-drama-pace-visible-camera
title: 貼圖漫劇（manga）節奏：看得見的運鏡、2–3.5 秒一切、停頓與音效、說書人聲音——照兩支十萬點閱參考片量出來的差距改
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-24T15:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/core/lint.mjs
  - docs/videos/BINGE.md
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

- [ ] manga 等級的 still 運鏡看得見：同一把尺量新成片，鏡內動量中位 ≥ 6、靜止幀比 ≤ 20%（參考 7.8–12.5／0–15%）；其他等級與插圖投影片的運鏡一個位元組不變（分開的常數與 `MOTION_ENCODER_VERSION`／segment key，讓舊片不重算、新片不撞快取）。
- [ ] manga 的切法改成每 2–3.5 秒一張（lint 對 manga 的鏡長有上限警告），BINGE.md、企劃包 authoring／site-note、`prompts.mjs` 同步；每集圖數約 +40%（US$0.4／集），寫進 BINGE.md 的估算。
- [ ] 旁白：撰稿規則要求「叮」之後、揭曉前留一拍空檔（線上 pause 節拍或空白句），manga 的 narration performance 直接寫進 video.json 的旁白 voice.style（不依賴 drama 分頁的 `drama_voice`），或 `settingsFor` 對 manga 給說書預設；drama 分頁 `drama_voice` 為空時的退回值改成說書式（`models.py` DEFAULT_VOICE 那段）。
- [ ] 音效：至少「叮」（面板跳字）有音效。主機沒有 `_sfx` 組，要站主放授權檔（YouTube 音效庫）進 `<work base>/_sfx/<set>/` 並寫 manifest（ILLUSTRATED.md §音效）；寫手在 manga 等級為每個「叮」放 cue。沒有音效組就只做前三項。

## Steps

- [ ] `assemble/drama.mjs`：讀 `series.json` 的 `visual_tier`（assemble 已拿 `project.series`），manga 用一組大的常數（例如 zoom 0.25、pan zoom 1.25、drift 0.12 加 30% 橫移，travel 在鏡長內走完、不等 6 秒），相鄰鏡頭方向輪替已有；加 `MOTION_MANGA_VERSION` 進 segment key。測試量 zoompan 表達式。
- [ ] `prompts.mjs` manga 段落「A new picture every 3 to 5 seconds」→ 2 到 3.5 秒，一鏡一句；`lint.mjs` 對 manga 鏡頭 >4 秒警告；BINGE.md §畫面等級與企劃包規則同步；`validate.mjs` 不動（它量的是鉤子）。
- [ ] 旁白停頓與聲音：見 DoD 第 3 項；量 e001 的 timeline 作基準（48 句、170.8 秒有聲、空檔 1 秒）。
- [ ] 改完先用 e005（還沒畫）試一集，同一把尺量成片，數字進這張票；e001–e004 不重做。

## How to verify

主機 video-worker：`ffmpeg -v error -i build/body.mp4 -vf "fps=4,scale=96:54,format=gray" -f rawvideo -pix_fmt gray -` 餵 node 算相鄰幀差（腳本在這張票的 Notes），鏡內動量中位 ≥ 6、靜止幀比 ≤ 20%、鏡長中位 ≤ 3.5 秒；`node --test tools/video/assemble/drama.test.mjs`。

## Notes

- 量法細節與數字在記憶 `travel-scanner-manga-pace-reference-20261024`；YouTube 頁內的 timedtext 沒登入會回空，花影的字幕是本機 `python -m yt_dlp --skip-download --write-subs --sub-langs zh-Hant --sub-format json3` 抓的。
- 參考合集沒有每集章節卡（花影只有三個通用時間戳），我們 compile 的 2 秒章節卡＋每集 YouTube 章節保留，站主 10-24 要「合集分章節就好」。
- 旁白比例 80% 字數不是問題：爽文動態漫畫本來就是旁白帶，問題在速度與停頓。
- 改 `drama.mjs`／`prompts.mjs`／`lint.mjs` 會讓時長收據過期，要獨立審查者做增量（記憶 travel-scanner-duration-receipt）。
