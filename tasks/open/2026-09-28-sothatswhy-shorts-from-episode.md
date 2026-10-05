---
id: 2026-09-28-sothatswhy-shorts-from-episode
title: So That's Why: cut two Shorts from each long episode's keyframes and script
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T06:00:00Z
completed_at:
branch: claude/knowledge-series-planning-v84n79
depends_on: []
scope:
  - tools/video/shorts/
  - tools/video/core/fixtures/explainer/shorts.json
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/so-thats-why/README.md
  - docs/videos/ai-shorts/README.md
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: cut two Shorts from each long episode's keyframes and script

## Why

「原來如此事務所」每集長片搭 2 支 Shorts（濃縮版、一個驚人事實；見 `docs/videos/so-thats-why/README.md` 的 Shorts 一節），要重用長片的關鍵影格，不另外生圖。現在的 `tools/video/shorts/` 只收獨立寫的 JSON：`series` 只能是 `daily|blind|prompts`、素材要是綁 SHA-256 的 evidence、聲音是本機 Windows 聲音，沒辦法從長片的 `video.json` 與關鍵影格切出來，也沒有正式頻道聲音。

## Definition of done

- [x] Shorts 規格接受 `series: "sothatswhy"`（要 `episode`，不要實驗欄位與 evidence），場景用 `shot` 引用長片的關鍵影格；建片時轉成綁雜湊的 evidence（`core.mjs` 的 `episodeShort`）。
- [x] 旁白可以用正式頻道聲音：`--voice server` 用長片的 `voice` 經旁白伺服器逐句合成（`voice.mjs`），也可以給 Windows 聲音或 `--audio-dir`。
- [x] 最後一格固定「完整版在長片 ▶」；說明欄第一行是長片連結（沒有 YouTube id 時寫待補，`UPLOAD.md` 提醒）。
- [x] 解說版撰稿順手寫 `docs/videos/<slug>/shorts.json`；寫壞只記 notes，不擋長片。
- [x] 測試涵蓋新 series、關鍵影格引用與雜湊、品牌、伺服器聲音、工人存檔。
- [ ] 在有 ffmpeg 的機器對一集真的跑 `from-episode` 出片（併在試片票 `2026-09-28-sothatswhy-pilot-3`）。

## Steps

- [x] 讀 `tools/video/shorts/core.mjs` 的 schema 與 `docs/videos/ai-shorts/README.md`。
- [x] `core.mjs`：series 分支驗證、`SERIES_BRAND`、`episodeShort`；`episode.mjs`：讀 shorts.json 與關鍵影格；`voice.mjs`；`build.mjs`：記憶體中的腳本與音檔、依 series 的說明欄與上傳說明；`cli.mjs`：`from-episode`。
- [x] 工人與提示詞：`writer:explainer` 回傳 `shorts`，`Automation.saveShorts` 存檔。
- [x] 文件：系列 README 的 Shorts 一節、ai-shorts README。

## How to verify

- `node --test tools/video/shorts/*.test.mjs tools/video/automation/automation.test.mjs`，`npm run test:tools`。
- 有 ffmpeg 與 Chromium、長片已畫好關鍵影格時：`node tools/video/shorts/cli.mjs from-episode --slug <slug> --check`，再加 `--workdir <repo 外>` 出兩支；看 `upload/final.mp4` 與 `UPLOAD.md`。

## Notes

- 2026-09-28 的開發容器沒有 ffmpeg，完整 `build` 沒跑過；驗證、雜湊綁定、品牌 HTML、伺服器聲音（假 fetch）、工人存檔都有測試。第一次真的出片放在試片票。
- 直式構圖沿用既有 `.asset` 版位（橫式關鍵影格等比縮進內容區、置中），沒有另外裁切；站主看過第一支再決定要不要改成裁 4:5。
- `--voice server` 每句一個請求，量得到每句的真實長度；計費照旁白伺服器的字數。
- 2026-09-28：`writer:explainer` 的縮圖說明改成系列規格（headline 每行 ≤ 10 字、≤ 2 行，`tag`／`pillar`，可選 `layout`，`variants` 的 B、C），原本寫 ≤ 12 字會一直被 lint 擋下再修。改在這張票，因為它的 scope 本來就含 `tools/video/automation`。
- 2026-09-28：併 #925（Shorts 腳本第 2 版、`speech.mjs`、`package`／`push`）後改寫：集的 Shorts 是第 2 版的 `line: "cut"`、`series: "sothatswhy"`、`source.slug`＝長片（`episode.mjs` 的 `episodeShortFields`），不再擴充第 1 版（#925 讓第 1 版只留給三支試片）。`build.mjs` 用 main 的原樣；`from-episode` 把 `shot` 換成關鍵影格後寫成腳本檔，交給一般 `build`（`--speech server` 預設），之後走 `check-audio`→`qa`→`package`→`push`，導回長片由 `package` 從網站讀網址。自己的 `voice.mjs` 刪掉（`speech.mjs` 的 server 旁白取代）。系列外觀是 `layouts.mjs` 的 `cut:sothatswhy` 主題（每張卡片底下「完整版在長片 ▶」，不再只有最後一格）。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus (since 2026-09-28T09:34:49Z) was stale and is released so it stops locking its scope. Landed: #904 #950 #962. Still open: Run from-episode for real on a machine with ffmpeg (folded into pilot ticket 2026-09-28-sothatswhy-pilot-3).
