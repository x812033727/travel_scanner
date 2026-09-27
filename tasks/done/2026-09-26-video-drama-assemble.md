---
id: 2026-09-26-video-drama-assemble
title: Video drama T7: assemble motion clips with fit, burned-in subtitles and ducked music
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:17:00Z
created_at: 2026-09-26T01:53:40Z
completed_at: 2026-09-26T06:30:32Z
branch:
depends_on:
  - 2026-09-26-video-drama-core
  - 2026-09-26-video-drama-render
scope:
  - tools/video/assemble
  - tools/video/package
  - .github/workflows/video-tooling.yml
---

# Video drama T7: assemble motion clips with fit, burned-in subtitles and ducked music

## Why

現有 assemble 假設畫面是靜態 PNG（`-tune stillimage`、三格 PSNR）。漫劇的段是片段：要縮放到 1920×1080、對齊句子長度（截、慢放、凍格）、疊字幕條、可選溶接；音訊要把音樂在旁白下壓低。編碼參數與投影片段相同才能繼續 `-c copy` 串接，用獨立的 `CLIP_ENCODER_VERSION` 才不會讓 slides 的快取失效。煙霧測試不能碰任何服務，用 `lavfi` 造替身。

## Definition of done

- [x] `drama.mjs`（放在 `plan.mjs` 旁，不動 slides 的函式）：`layoutDrama`、`fitPlan`（auto／freeze／slow／trim）、`freezeProblem`、`subtitleTrack`（總格數＝場景格數、不重疊）、`clipFrames`、`clipSegmentKey`、`clipSegmentArgs`（scale/pad → setpts → fps=30 → tpad → trim → 溶接疊圖 → 字幕條疊圖，`-tune film`，其餘同 `segmentArgs`）、`lastFrameArgs`、`duckRatio`／`bedFilter`／`mixFilter`／`measureMixArgs`／`mixArgs`／`bedLoudnessArgs`（`sidechaincompress`、`amix=duration=first`、兩段式 loudnorm）、`bedLevel`／`checkBed`、`keyframeProblem`。
- [x] `cli.mjs`：drama 分支讀六個雜湊、找 `_music/` 或 `music/`、逐鏡探測片段長度→fit→字幕條 ffconcat→（溶接時抽上一段最後一格）→編段、串接、混音、mux、檢查（格數、片段第 0 格對關鍵影格 PSNR ≥22、凍格 >60（fit freeze 除外）、音樂床 ≤ −24 LUFS、既有探測與響度、卡片段照舊三格 PSNR）；`checks.json` 記六個雜湊與每鏡 fit；`package` 比對六個雜湊（`checksCurrent`）並在 `UPLOAD.md` 換成揭露、劇情獨立、音樂授權三行。
- [x] `synthetic.mjs` 造關鍵影格、片段（第二鏡短 2 秒、第三鏡長 3 秒）、20 秒雙音音樂；`smoke.mjs --fixture drama` 全程綠並加進 `.github/workflows/video-tooling.yml`。
- [x] slides 的 `smoke.mjs` 仍綠，`ENCODER_VERSION` 不變（測試釘住字面值）。

## Steps

- [x] plan 純函式與測試 → cli → synthetic 與 smoke → package → CI。

## How to verify

```bash
node --test tools/video/assemble/*.test.mjs tools/video/package/*.test.mjs
node tools/video/assemble/smoke.mjs --fixture drama --channel msedge
node tools/video/assemble/smoke.mjs --channel msedge
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 不用 `xfade`（要重編串接）、不用 `minterpolate`（工人沒 GPU、3 GB）。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- 給 T5 的合約：`clips/manifest.json` 要有 `speech_hash`、`visual_hash`、`look_hash`、`clips_hash`（`clipsHash([{id, sha256}])` 依鏡頭順序）、`shots[<id>] = { file（相對工作目錄、斜線）, sha256, seconds?, needs_review? }`；assemble 自己用 ffprobe 量片段長度算 fit，不讀 T5 的 fit_plan。`music/manifest.json`：`{ mix_hash, file, sha256 }`；站主自帶的曲子放 `<工作目錄底>/_music/<track>`，`music.sha256` 有給就核對。
- 關鍵影格 PSNR 量的是**片段本身**的第 0 格（不是段），所以溶接（第 0 格疊著上一鏡最後一格）不影響檢查；門檻 22，合成替身量到 44。
- 溶接：段內用上一段最後一格（`build/last-<id>-<key>.png`，抽自上一段）`fade alpha` 15 格疊在本段開頭，段的 key 含上一段的 key，所以上一鏡改了本段會重編。
- 壓低音樂：`sidechaincompress` 的 ratio 由 `duck_db` 換算（假設人聲高出門檻 20 dB：−10 dB → ratio 2），`amix=duration=first` 讓長度精確等於旁白；音樂床的 LUFS 用「床本身量到的值＋loudnorm 線性增益」推算，門檻 −24。試作時再校準這幾個數字。
- 本機 `smoke.mjs --fixture drama --channel msedge` 全程綠：farewell 鏡片段短 2 秒→0.85x 再凍 29 格、sea-storm 長 3 秒→截 113 格、bird 溶接；成片 1275 格、−13.9 LUFS、床 −43 LUFS（合成正弦波很小聲）。
