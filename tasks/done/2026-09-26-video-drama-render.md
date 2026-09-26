---
id: 2026-09-26-video-drama-render
title: Video drama T6: render skips shots, draws subtitle strips and keyframe thumbnails
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T05:44:49Z
created_at: 2026-09-26T01:53:37Z
completed_at: 2026-09-26T05:58:15Z
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

- [x] `renderPlan` 對鏡頭場景回 `{ kind: "clip", states: [] }`，卡片場景照舊（`kind: "stills"`）；`renderProblems` 跳過鏡頭。
- [x] `subtitles.burn_in` 開時：`render/subtitles.mjs` 依 zh-TW cue 出 `frames/sub-<key>.png`（`omitBackground`）與 `frames/sub-blank.png`，樣式 `drama`（Noto Sans TC 600 56px、5px 黑描邊（paint-order 後外露約 2.5px）、置中、離底 56px、行高 1.5）；缺字結束碼 1；manifest 多 `speech_hash`、`subtitles_hash`、`subtitles: { style, size, blank, cues: [{ line, start_frame, end_frame, text, file }] }`。
- [x] `thumbnail.data.shot` 有值時縮圖以該關鍵影格當底圖（`/work/keyframes/...` 已由假網域提供）；關鍵影格的 sha256 進縮圖的 key。
- [x] 只有卡片場景時才畫聯絡表；slides 影片的輸出與快取鍵不變（縮圖底圖的 CSS 放在頁面 head，不動 theme.css，所以 `themeHash` 沒變）。

## Steps

- [x] `render/plan.mjs`、`render/subtitles.mjs`、`render/cli.mjs`、`templates/templates.mjs`（縮圖底圖）→ 測試。

## How to verify

```bash
node --test tools/video/render/*.test.mjs tools/video/templates/*.test.mjs
node tools/video/cli.mjs render --file tools/video/core/fixtures/drama/video.json --workdir <DIR> --channel msedge
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- 字幕條的 cue 來自 `buildCues(timeline, zh-TW 文字)`，與 CC 同一套斷句計時；毫秒轉成整格（四捨五入、夾在該句的格數內），`assemble`（T7）直接用 `start_frame`／`end_frame` 疊圖，沒字幕的區間用 `blank`。同一段文字共用一張條（key 是條的 HTML 雜湊，含樣式 CSS）；`speaker_prefix` 開時角色句的第一個 cue 前加「【名字】」（橘色）。
- 漫劇的 render 需要 `timeline.json`（`speech_hash` 對得上），否則結束碼 2 叫你先跑 tts；縮圖指名的鏡頭沒有關鍵影格也是結束碼 2。關鍵影格清單的 `shots[<id>].file` 要是相對工作目錄、斜線分隔的路徑（`keyframes/<shot>-<key>.png`），`sha256` 可有可無——T4 寫清單時照這個形狀。
- 行高從 1.3 改成 1.5：Noto Sans TC 的字框約 1.45 em，1.3 會讓每張條「高出 3px」被版面檢查擋下。
- 本機驗過：`render-drama.mjs`（scratchpad）用合成旁白與 ffmpeg 測試圖當關鍵影格，`--channel msedge` 畫出 1 張 outro 卡、10 張字幕條（1920×260 rgba，空白條 alpha 全 0）、縮圖（關鍵影格鋪滿、左側漸層遮罩、標題可讀），manifest 帶 `kind`、`speech_hash`、`subtitles_hash`、10 個 cue。
- 沒改 `core/state.mjs` 的 ARTIFACTS 註解（core 票的檔）；manifest 的 `scenes[].kind` 是新欄位，slides 影片也會帶（`stills`），T7 的 `layoutDrama` 可直接讀。
