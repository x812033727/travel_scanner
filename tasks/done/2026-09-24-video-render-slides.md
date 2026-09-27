---
id: 2026-09-24-video-render-slides
title: 影片產線 T3：Mokaair 深色投影片版型與 Playwright 截圖
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T01:06:48Z
created_at: 2026-09-24T00:41:03Z
completed_at: 2026-09-24T01:51:46Z
branch: claude/video-render-slides
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

- [x] `node tools/video/cli.mjs render --slug <slug> --workdir <dir>`（或 `--file` 指向範例）產生 `frames/`、`frames/manifest.json`（帶 `visual_hash`）、`contact-sheet.png`、`thumbnail.jpg`；重跑時內容沒變的狀態直接沿用（依 HTML＋主題雜湊快取）。
- [x] 版型：title、chapter、bullets、compare、steps、table、code、big、diagram、screenshot、outro＋縮圖 thumb；全部都在 `tools/video/templates/fixtures/showcase/video.json` 裡用過一次，實際渲染過。
- [x] 文字縮到 60% 還放不下、內容超出版面、圖片沒載入、字型沒載入、或字型沒有某個字（例如 emoji），都會失敗並指出場景 id 與狀態（`tools/video/render/fonts.mjs` 用 fontsource 的 unicode-range 判斷）。
- [x] 縮圖 1280×720 JPEG，超過 2 MB 就失敗（實測約 60 KB）。
- [x] 除了假網域 `https://video.local` 上的頁面、主題、`node_modules` 裡的字型、`apps/web/public/` 與 `docs/videos/` 的圖片，其他請求一律擋掉並列為錯誤。

## Steps

- [x] 字型：T1 已加進根目錄 devDependencies 的 `@fontsource-variable/noto-sans-tc`、`@fontsource-variable/jetbrains-mono`，由 `page.route` 從 `node_modules` 提供。
- [x] `tools/video/templates/theme.css`：Mokaair 深色主題（網站圖解配色反轉，強調色青綠 `#4fc1b5`、重點字橘 `#f0a04b`），下緣 132 px 不放東西（YouTube 控制列與 CC）。
- [x] `tools/video/templates/templates.mjs`：每個版型的資料檢查、可逐條出現的數量、HTML 產生（純函式）。
- [x] `tools/video/render/`：`plan.mjs`（狀態展開與快取鍵）、`fonts.mjs`（缺字檢查）、`browser.mjs`（Playwright、假網域、自動縮字、版面檢查、Web Animations 逐格凍結）、`contact.mjs`（聯絡表）、`cli.mjs`（`render` 子指令）。
- [x] 量這台機器的速度（見 Notes）。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs render --file tools/video/templates/fixtures/showcase/video.json --workdir <VIDEO_WORKDIR> --channel msedge
```

打開 `<VIDEO_WORKDIR>/template-showcase/contact-sheet.png` 看 17 個狀態，`thumbnail.jpg` 看縮圖。

## Notes

- **逐條出現**：一個場景的 `reveal` 總數套在版型的**最後幾個**元素上。三個項目、三次 reveal，就是從零開始每次多一個；沒有 reveal 就全部一開始就在。還沒出現的元素是 `visibility: hidden`，所以出現時版面不會跳動。
- **轉場**：每個狀態新出現的元素帶 `enter`（上浮＋淡入 300 ms，一起出現的元素間隔 70 ms）。渲染時暫停所有動畫，按 1/30 秒逐格截圖；逐條出現一次是 9 格（0.3 秒），場景開頭依元素多寡 12–16 格。`manifest.json` 每個狀態有 `transition`（逐格檔名）與 `still`，assemble（T4）先放轉場格、剩下的時間放 still。狀態順序與 `estimateTimeline()` 的 `scenes[].states` 一一對應。
- **中文字型的誤報**：Noto Sans CJK 的字身比緊的行高高，單行文字也會「溢出」零點幾個字高。只有超出 0.4 個字高（等於多一行）才算放不下。
- **瀏覽器**：這個 worktree 的 Playwright 1.63 要的 Chromium（`chromium_headless_shell-1243`）這台沒有，而且在 Windows ARM64 上是模擬執行。本機用 `--channel msedge`（系統內建 Edge，原生 ARM64），或設 `VIDEO_BROWSER_CHANNEL=msedge`。沒有瀏覽器時回結束碼 5 並提示這兩個做法。CI 用 Playwright 自己的 Chromium（T4 的煙霧測試會裝）。
- **實測（2026-09-24，Snapdragon X Plus，Edge）**：17 個狀態（約 220 張 1920×1080 PNG，含轉場格）75–90 秒，`frames/` 約 77 MB。10 分鐘影片估計 60–80 個狀態，約 5 分鐘、300 MB。
- **縮圖**：重點詞（`**…**`）不斷行；標題裡的 `\n` 是手動斷行。右側是純 CSS 的圓環與圓點，品牌圖 `apps/web/public/brand/mokaair-monogram.png` 是白底棕字，放在深色主題上不協調，所以沒用。
- `status` 只比 `visual_hash`（場景資料）；改了 `theme.css` 或版型程式，status 仍會說 frames 是最新的，但 `render` 重跑會因為快取鍵變了而重畫。改版型後要記得重跑 render。
- 版型資料的檢查目前只在 `render` 跑；把它接進 `lint`（要改 `tools/video/core/lint.mjs`，屬於已結案的 T1 scope）可以另開小票。
