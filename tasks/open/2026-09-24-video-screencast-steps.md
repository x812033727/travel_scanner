---
id: 2026-09-24-video-screencast-steps
title: 影片產線 T9：Playwright 步驟腳本的螢幕操作教學
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-screencast
claimed_at: 2026-10-01T07:05:00Z
created_at: 2026-09-24T00:41:18Z
completed_at:
branch: claude/video-screencast-steps
depends_on:
  - 2026-09-24-video-pilot-ai-model-choice
scope:
  - tools/video/screencast
  - tools/video/core/schema.mjs
  - tools/video/core/lint.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/cli.mjs
  - tools/video/templates/templates.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# 影片產線 T9：Playwright 步驟腳本的螢幕操作教學

## Why

第三期：手把手操作教學。網頁操作用宣告式步驟 JSON（goto、click、fill、wait、capture、mask）讓 Playwright 自動操作並截靜態圖，游標、框選、放大由版型畫，畫面可重現、可快取。不用 Playwright 的 `recordVideo`（VP8、畫質差、變動畫格率、無法跟旁白同步）。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [x] `video.json` 的場景可以是 `screencast` 步驟，render 產生帶游標與框選動畫的影格。
- [x] 個資與秘密一律用 `mask` 遮掉；登入由站主自己做（持久 profile），代理不輸入帳密。
- [x] 用一支實際教學跑通。

## Steps

- [x] 步驟格式與驗證。
- [x] 截圖、游標與框選動畫版型。
- [x] 與 assemble 的每場景片段接起來。

## How to verify

```bash
node --test tools/video/screencast/*.test.mjs
# A real run against the public site (needs network and Edge or Playwright's Chromium):
VIDEO_BROWSER_CHANNEL=msedge node tools/video/cli.mjs render --file tools/video/screencast/fixtures/tutorial/video.json --workdir <DIR>
```

## Notes

- Claimed with `--force` on 2026-10-01: the dependency `2026-09-24-video-pilot-ai-model-choice` is still open only because the owner has not uploaded the pilot; the pipeline it was meant to prove has since produced more than a dozen videos.
- Scope additions, each the smallest hook into the existing stages:
  - `tools/video/core/schema.mjs`: accept `template: "screencast"` beside `shot` (it is not a slide template, so it stays out of `TEMPLATES` and `TEMPLATE_SPECS`; adding it there would break the "showcase uses every template" test and the render smoke fixture).
  - `tools/video/core/lint.mjs`: run the step validator and the reveal rule on screencast scenes, so a bad or unsafe step fails `lint` before any audio is paid for.
  - `tools/video/render/plan.mjs`: a screencast scene's states are built from its capture manifest, keyed by each still's sha256.
  - `tools/video/render/cli.mjs`: take (or reuse) the captures before planning; `--recapture`, `--profile`; exit 1 for a step problem, 4 for an unreachable page, 5 for no browser.
  - `tools/video/templates/templates.mjs`: export `page` and `chrome` (no behaviour change) so screencast frames carry the same chapter bar and brand.
  - `.agents/skills/youtube-video/references/automated.md`: one paragraph on the scene type. `SKILL.md` lists no templates, so it is unchanged.
- Design: the template draws the cursor, highlight, click ripple and zoom as CSS animations of at most 600 ms, which the existing renderer freezes frame by frame (18 frames). So a screencast scene comes out as ordinary stills plus transition frames in `frames/manifest.json`, and `assemble` needed no change: it encodes the scene as one segment like any slide scene. The browser part sits behind a driver interface (`runner.mjs`), so the tests use a fake page.
- Safety: `fill` refuses password, one-time-code, card, email and phone fields both by selector (lint) and by the field the page actually has (run time), and refuses values that look like an email, a phone or card number, or a key. No still is taken while any password field holds a value. A selector mask that matches nothing stops the run (unless `optional`). `goto` refuses http, private hosts, credentials and token-like query parameters. Every request carries the editorial User-Agent. `--profile` exists for the owner and was never used here.
- Verified on 2026-10-01 with `VIDEO_BROWSER_CHANNEL=msedge`: the fixture drove https://mokaair.com/zh-TW (mask over the login link, cursor to 旅遊情報攻略, click), the guides page (focus on the 交通 topic) and filled 東京交通 into the header search (zoom 1.6). Looked at the contact sheet, stills and transition frames: cursor glide, highlight with dimmed surroundings, ripple only after the cursor arrives, zoom, and the striped mask all as intended. A second render reused the captures without opening the page. Stand-in narration (`assemble/synthetic.mjs`) plus `assemble` produced final.mp4 (1283 frames, checks ok). Captured images were not committed.
- Learned from the live site: the header's login link is drawn after a client-side session check and once took over 10 s (waits now allow 25 s); the site keeps hidden mobile copies of its controls and a second search box on the guides page, so selectors count only visible elements and `click`/`fill` must match exactly one.
- Found, not fixed (out of scope): `assemble` skips the PSNR frame checks for every plain slides video, because `layoutScenes` gives its scenes no `kind` while the check looks for `kind === "stills"` (since #861). Filed as its own task.
