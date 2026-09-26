---
id: 2026-09-26-video-drama-assemble
title: Video drama T7: assemble motion clips with fit, burned-in subtitles and ducked music
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:40Z
completed_at:
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

- [ ] `plan.mjs`：`layoutDrama`、`fitPlan`（auto／freeze／slow／trim）、`subtitleTrack`（總格數＝場景格數、不重疊）、`clipSegmentKey`、`clipSegmentArgs`（scale/pad → setpts → fps=30 → tpad → trim → overlay 字幕條，`-tune film`，其餘同 `segmentArgs`）、段內 dissolve、`mixFilter`／`measureMixArgs`／`mixArgs`（`sidechaincompress`、`amix=duration=first`、兩段式 loudnorm）、`clipSampleProblem`。
- [ ] `cli.mjs`：drama 分支讀六個雜湊、找 `_music/` 或 `music/`、編段、串接、混音、mux、檢查（格數、第 0 格 PSNR、凍格 >60、音樂床 ≤ −24 LUFS、既有探測與響度）；`package` 比對六個雜湊並在 `UPLOAD.md` 加揭露、劇情獨立、音樂授權三行。
- [ ] `synthetic.mjs` 造關鍵影格、片段（一段短 2 秒、一段長 3 秒）、音樂；`smoke.mjs --fixture drama` 全程綠並加進 `.github/workflows/video-tooling.yml`。
- [ ] slides 的 `smoke.mjs` 仍綠，`ENCODER_VERSION` 不變。

## Steps

- [ ] plan 純函式與測試 → cli → synthetic 與 smoke → package → CI。

## How to verify

```bash
node --test tools/video/assemble/*.test.mjs tools/video/package/*.test.mjs
node tools/video/assemble/smoke.mjs --fixture drama --channel msedge
node tools/video/assemble/smoke.mjs --channel msedge
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 不用 `xfade`（要重編串接）、不用 `minterpolate`（工人沒 GPU、3 GB）。
