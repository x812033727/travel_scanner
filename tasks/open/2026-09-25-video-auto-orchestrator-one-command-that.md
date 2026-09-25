---
id: 2026-09-25-video-auto-orchestrator-one-command-that
title: Video auto orchestrator: one command that takes a video from topic to the owner's review
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-25T07:38:49Z
completed_at:
branch:
depends_on:
  - 2026-09-25-video-auto-settings-models-schedule-video
scope:
  - tools/video/automation
---

# Video auto orchestrator: one command that takes a video from topic to the owner's review

## Why

原本由代理做的企劃、撰稿、查核、聽眾審稿、翻譯，要變成工具自己能跑的步驟，主機和本機都能用。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [ ] `node tools/video/cli.mjs auto [--once]`：問 API 這一輪該做什麼，做完一步就記下狀態，中斷後從同一步繼續。
- [ ] 流程照 AUTOMATION.md「一支影片的自動流程」；三個等站主的關卡都停下來送審。
- [ ] 查核：工人自己抓 `claims.md` 的網址（Mokaair-editorial UA、每個網域間隔 1 秒），頁面文字交給查核模型；改超過 3 個事實就開新對話再查一輪。
- [ ] 站主退回的理由會交給下一次撰稿或聽眾審稿。

## Steps

- [ ] 狀態機與各階段的提示組裝（提示詞沿用 skill 的 `references/prompts/*.md`）。
- [ ] lint 錯誤回饋給撰稿模型，最多 3 次。
- [ ] 單元測試用假的 API。

## How to verify

`npm run test:tools`；本機對一個測試題目跑 `auto --once` 到送審大綱為止。
