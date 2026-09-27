---
id: 2026-09-25-video-auto-orchestrator-one-command-that
title: Video auto orchestrator: one command that takes a video from topic to the owner's review
status: done
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-25T08:59:18Z
created_at: 2026-09-25T07:38:49Z
completed_at: 2026-09-25T08:59:47Z
branch: claude/video-auto-orchestrator
depends_on:
  - 2026-09-25-video-auto-settings-models-schedule-video
scope:
  - tools/video/automation
---

# Video auto orchestrator: one command that takes a video from topic to the owner's review

## Why

原本由代理做的企劃、撰稿、查核、聽眾審稿、翻譯，要變成工具自己能跑的步驟，主機和本機都能用。設計全文在 `docs/videos/AUTOMATION.md`。站主 2026-09-25 的決定：在正式站主機上跑；設定放在「影片審核」頁；旁白 Jev 全數通過就自動核准，其他關卡等站主；寫稿用 API 金鑰（預設 Sonnet 寫、Opus 查）；題目先看站上新聞與文章，不夠再用 Brave 搜尋補。

## Definition of done

- [x] `node tools/video/cli.mjs auto [--once]`：
  - 每次跑都做到所有影片都在等站主、或還沒到產生下一支草稿的時間為止；`--once` 只做一步。
  - 下一步由 `pipelineStatus` 依檔案雜湊判斷；它看不到的事記在 `<工作區>/<slug>/auto.json`，所以中斷後從同一步接著做：查核輪數、聽眾審稿做了沒、重錄次數、站主的退回理由。
- [x] 流程照 AUTOMATION.md「一支影片的自動流程」；選大綱、成片、上架確認三關都停下來送審。
- [x] 查核：工人自己讀 `claims.md`、`sources` 與企劃裡列的網址，頁面文字交給查核模型。
  - 讀網頁用 Mokaair-editorial UA，每個網域至少隔 1 秒，只讀 https。
  - 每輪都是新的對話；改超過 3 個事實就再查一輪，最多照設定的輪數。
- [x] 站主退回時：
  - 大綱：帶著理由重寫企劃，最多兩次；
  - 旁白：理由交給聽眾審稿；
  - 成片與上架：影片標成 blocked，在後台顯示原因。

## Steps

- [x] 狀態機與各階段的提示詞（`prompts.mjs`，從 skill 的代理提示改寫成「所有資料都在 payload、回一個 JSON」）。
- [x] lint 錯誤回饋給撰稿模型，最多 3 次。
- [x] 單元測試：用假的網站（API、模型、來源網頁），一支影片從選題走到該做旁白為止。

## How to verify

- `node --test tools/video/automation/automation.test.mjs`：7 個通過。
- `npm run test:tools`：256 個通過。
- 部署後由主機的工人實際跑第一支，在 `video-auto-rollout` 做。

## Notes

- 大綱送審直接打 API，不用 `review-push`：`review-push` 一開始就要讀 `video.json`，但選大綱時還沒有稿子。
- 網站文章的內容包如果不在 repo 裡（例如新聞自動化發的文章只在資料庫），`video.json` 就不寫 `source_guide`，改在 `sources` 列出文章網址。
- 自動影片不用圖解和截圖版型：工人產生不了圖檔。
- 訂閱帳號全部到門檻時，這一輪 `auto` 直接結束（結束碼 4），不在同一輪重試。
