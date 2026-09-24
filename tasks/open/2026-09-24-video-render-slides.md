---
id: 2026-09-24-video-render-slides
title: 影片產線 T3：Mokaair 深色投影片版型與 Playwright 截圖
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:03Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-tooling-core
scope:
  - tools/video/templates
  - tools/video/render
---

# 影片產線 T3：Mokaair 深色投影片版型與 Playwright 截圖

## Why

畫面是 Mokaair 深色版型的投影片（底色 `#102A2B`、文字 `#F7F1E8`、強調 `#0D6B68` 系），一個投影片狀態一張 1920×1080 PNG，逐條出現的轉場截 8–10 張短影格。用 repo 已有的 Playwright（`tools/claude-code-series/render-art.mjs` 的做法），不用 Remotion（不支援 Windows ARM64）。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `node tools/video/cli.mjs render --slug <slug> --workdir <dir>` 產生 `frames/` 與 `contact-sheet.png`，重跑時沒變的畫面不重截。
- [ ] 版型：title、chapter、bullets、compare、steps、table、code、big、diagram、screenshot、outro、thumb；每個版型有範例資料與截圖。
- [ ] 文字超框或缺字（字型沒有該字、悄悄換字型）時失敗並指出場景 id。
- [ ] 縮圖 1280×720 JPEG ＜ 2 MB。
- [ ] 所有網路請求被擋，版型與字型由 `page.route` 的假網域提供。

## Steps

- [ ] 字型：用 T1 已加進根目錄 devDependencies 的 `@fontsource` 套件（Noto Sans TC＋等寬字型），由 `page.route` 從 `node_modules` 提供。
- [ ] `tools/video/templates/`：主題 CSS 與各版型 HTML。
- [ ] `tools/video/render/`：狀態展開（場景 × reveal）、截圖、轉場影格（Web Animations 固定 currentTime；不可用 `animations: 'disabled'`）、聯絡表、縮圖。
- [ ] 量這台機器（Chromium 以 x64 模擬執行）的截圖速度，寫進 Notes。

## How to verify

```bash
node --test tools/video/render/*.test.mjs
node tools/video/cli.mjs render --slug <slug> --workdir <VIDEO_WORKDIR>
```
打開 `contact-sheet.png` 看每個狀態。

## Notes
