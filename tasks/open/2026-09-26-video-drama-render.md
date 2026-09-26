---
id: 2026-09-26-video-drama-render
title: Video drama T6: render skips shots, draws subtitle strips and keyframe thumbnails
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T01:53:37Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-core
scope:
  - tools/video/render
  - tools/video/templates
---

# Video drama T6: render skips shots, draws subtitle strips and keyframe thumbnails

## Why

漫劇的畫面主體是片段，但開場／章節／結尾卡片、縮圖、燒錄字幕仍由 render 用 Playwright 畫。字幕不用 libass：內建字型只有 woff2，fontconfig 會悄悄換成系統字型，Windows、CI、工人三邊會不一樣；改成每個不同的字幕文字出一張 1920×260 透明 PNG，assemble 再疊上去，斷句與計時和 CC 同一套（`core/captions.mjs` 的 `buildCues`）。

## Definition of done

- [ ] `renderPlan` 對鏡頭場景回 `{ kind: "clip", states: [] }`，卡片場景照舊；`renderProblems` 跳過鏡頭。
- [ ] `subtitles.burn_in` 開時：`render/subtitles.mjs` 依 zh-TW cue 出 `frames/sub-<key>.png`（`omitBackground`）與 `frames/sub-blank.png`，樣式 `drama`（Noto Sans TC 600 56px、4px 黑描邊、置中、離底 56px）；缺字結束碼 1；manifest 多 `speech_hash`、`subtitles_hash`、`subtitles: { blank, cues }`。
- [ ] `thumbnail.data.shot` 有值時縮圖以該關鍵影格當底圖（`/work/keyframes/...` 已由假網域提供）。
- [ ] 只有卡片場景時才畫聯絡表；slides 影片的輸出與快取鍵不變。

## Steps

- [ ] `render/plan.mjs`、`render/subtitles.mjs`、`render/cli.mjs`、`templates/templates.mjs`（縮圖底圖）→ 測試。

## How to verify

```bash
node --test tools/video/render/*.test.mjs tools/video/templates/*.test.mjs
node tools/video/cli.mjs render --file tools/video/core/fixtures/drama/video.json --workdir <DIR> --channel msedge
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
