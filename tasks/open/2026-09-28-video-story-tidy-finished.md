---
id: 2026-09-28-video-story-tidy-finished
title: 影片上架後清掉工人的工作檔
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-video-story-tidy
claimed_at: 2026-09-28T11:20:25Z
created_at: 2026-09-28T03:31:14Z
completed_at:
branch: claude/video-story-tidy-finished
depends_on: []
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/cli.test.mjs
  - tools/video/cli.mjs
  - docs/videos/AUTOMATION.md
---

# 影片上架後清掉工人的工作檔

## Why

工人的工作區（volume `video_work`）沒有任何清理。一支品牌故事約留下 1.3–2 GB（音檔、關鍵影格、每鏡一段的片段、成片），每天兩支一個月就是幾十 GB（`docs/videos/STORY.md` §上限與成本），主機磁碟會先滿。

## Definition of done

- [x] 影片已經記下 YouTube id（狀態 `done`）而且超過保留天數時，刪掉它工作區裡可以重做的大檔：`segments/`、`build/`、`audio/`、`keyframes/`、`clips/`、`final.mp4` 與預覽；留下 `auto.json`、`state.json`、`checks.json`、帳本與核准紀錄。
- [x] 還在製作、卡住、等站主的影片一個檔都不刪。
- [x] 每一輪最多清一支，印出刪了什麼、釋放多少空間；`--dry-run` 只列不刪。
- [x] 測試涵蓋：已上架、剛上架未滿保留天數、製作中、已放棄四種狀態。

## Steps

- [x] `tidy.mjs`：判斷與刪除；保留天數預設 7 天，與審核檔案區刪 mp4 的規則一致。
- [x] 在工人每輪的最後呼叫一次。
- [x] 測試。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"   # tidy.test.mjs 與 cli.test.mjs 在裡面
npm run test:tools
node tools/video/cli.mjs tidy --dry-run           # 手動看下一輪會清什麼，不刪
```

## Notes

- 已放棄的影片照同一條規則清（放棄滿保留天數）。
- 作品的共用存檔 `_series/<作品>/`（設定圖、風格錨定圖）與 `_music/` 不清。
- 2026-09-28 認領時拿掉 `depends_on: 2026-09-28-video-story-worker`：清理在 `auto` 每一輪的最後呼叫一次（`tools/video/automation/cli.mjs`），不在故事的流程裡，也不讀故事工人寫的任何東西，所以不必等那張票。
- scope 加上：`automation/cli.mjs`（每輪最後的呼叫）與它的測試 `automation/cli.test.mjs`、`tools/video/cli.mjs`（指令表加 `tidy` 讓人手動跑與 `--dry-run`，`status` 遇到已清理的影片不再寫「下一步：assemble」）、`docs/videos/AUTOMATION.md`（工人的環境變數）。`flow.mjs`、`series.mjs`、`prompts.mjs` 只讀不改（#897、#904 正在改）。
- 以 `--force` 認領，原因：`2026-09-26-video-dubs-worker`、`2026-09-27-video-drama-room-worker`、`2026-09-27-video-split-settings-worker`、`2026-09-27-video-drama-room-skill-docs` 四張票停在 `review`，scope 含 `tools/video/automation` 或 `docs/videos/AUTOMATION.md`，但它們的工作已在 #870（79e26fcdf，2026-09-27）合併進 main，只是票沒有移到 done；沒有開著的 PR 或分支在做清理（`git ls-remote`、`gh pr list` 都查過）。這四張票不動。
- **名單從哪裡來**（`ARTIFACTS` 與各階段實際寫的檔案，寫在 `tidy.mjs` 的 `TARGETS`）：`final.mp4`（`ARTIFACTS.video`，assemble／compile）；`upload/final.mp4`（package 整份複製，跟成片一樣大；合集是硬連結，後台從這裡下載合集）；`upload/dubs/`（package 複製的配音）；`segments/`、`build/`（assemble 與 compile 的片段、接好的畫面、混好的聲音、`.partial.mp4`）；`audio/`、`narration.wav`（tts，`ARTIFACTS.audio`／`narration`）；`frames/`（render 的每個投影片狀態、字幕條、卡片 PNG 與其 manifest）；`keyframes/`、`clips/`（連 manifest 與聯絡表）；配音的 `dubs/<語系>/audio/`、`dubs/<語系>/narration.wav`、`dubs/<語系>.<m4a|mp3|wav>`（`dubArtifacts`）；`review/preview-<16 位雜湊>.mp4`、`review/narration-<16 位雜湊>.m4a`（review-push 的預覽，`review/sync.mjs` `preview()`）。比原本的清單多了 `frames/`、`narration.wav`、`upload/final.mp4`、配音音檔，都是大檔、影片結束後沒有人讀。
- **刻意留下**：`music/`（配樂數 MB，manifest 記錄來源）、`characters/`（設定圖與站主的選擇 `choice.json`；作品的設定圖另存在 `_series/`）、`media/`（帳本 `ledger.json`、快取、工作）、`thumbnail.jpg`、`contact-sheet.png`、上傳包的文字檔與縮圖、`captions/`、`i18n/`、`review/` 的 JSON 與頁面、`answers/`、`timeline.json`、`approvals.json`、`checks.json`、`state.json`、`languages.json`。
- **哪個欄位記「什麼時候」**：`auto.json` 只有放棄的 `dropped.at`（站上的 `dropped_at`）；上 YouTube 的沒有日期——`recordVideoId` 只寫 `status: done` 與 `youtube_video_id`，`created_at` 是開始做的時間，而 `flow.mjs` 這張票不能改。所以照網站刪 mp4 的規則（`prune_published_previews`）算：上架確認核准的時間（工作區 `approvals.json` 的 `publish` 項、每輪影片清單的 `publish_approved_at`，取晚的）與 `youtube_publish_at`，再取晚的。都沒有就不清，每一輪印一行。站上的清單只回最新 200 支（`list_projects` 的 `limit`），掉出清單的舊影片只用 `approvals.json` 的日期。
- **比 brief 多留的**（為了少刪）：語言還沒決定或還在做（清單的 `locales_decided_at`、`languages`）；開了合集的作品裡、合集還沒上 YouTube 的集數（compile 要接每集的 `final.mp4` 與字幕，縮圖從前三集的關鍵影格挑）；工作區裡有 `STOP` 檔的。
- **清完之後**：`status` 改寫清理說明、不寫 `Next:`；`auto` 對 `done` 的影片不 `advance`，`languages()` 要 `final.mp4` 還在（成片核准）才動，所以不會重做。缺口：清理之後才勾的語言做不出來，站上會一直「製作中」——另開 `2026-09-28-video-tidied-late-languages`（要改 `flow.mjs`）。
- 合集的後台下載（API 唯讀掛載工作區、讀 `upload/final.mp4`）在合集上 YouTube 滿保留天數後就沒有檔案，跟審核檔案區刪 mp4 一致。#904 的 `shorts/cli.mjs from-episode` 從長片的關鍵影格剪 Shorts，要在清理前做（它的排程是公開後 16 與 46 小時，在 7 天內）。
- 設定只有工人的環境變數 `VIDEO_TIDY_DAYS`（預設 7，1–3650，`off` 關掉；填錯那一輪不清）。工人容器只收 compose 列出的變數，要改就在 `docker-compose.prod.yml` 的 `video-worker.environment` 加一行；網站不用改。
- Windows 上沒有權限做檔案 symbolic link（EPERM），那一項測試 skip；資料夾連結用 junction，Windows 與 Linux 都跑。檔案 symlink 那一項在 Linux CI（Video tooling、web 的 `test:tools`）跑。
