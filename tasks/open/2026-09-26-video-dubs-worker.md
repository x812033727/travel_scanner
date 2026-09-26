---
id: 2026-09-26-video-dubs-worker
title: Video dubs: the worker synthesizes, shortens, checks and packages the tracks, and qa reports them
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-26T17:59:41Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-dubs-command
  - 2026-09-26-video-dubs-check-language
  - 2026-09-26-video-dubs-setting
  - 2026-09-26-video-dubs-captions-package
scope:
  - tools/video/automation
  - tools/video/qa
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - .claude/skills/youtube-video/references/prompts/caption-translate.md
  - .claude/skills/youtube-video/references/prompts/caption-review.md
---

# Video dubs: the worker synthesizes, shortens, checks and packages the tracks, and qa reports them

## Why

前四張票做出指令、檢查、設定與上傳包之後，主機工人要自己把配音做完，站主只在 Studio 上傳檔案（`docs/videos/DUBS.md`、`HANDS-OFF.md`）。塞不下的句子要交給翻譯模型縮短、被 Jev 標記的句子要重錄，兩輪不成就跳過那個語系，不能卡住整支影片。

## Definition of done

- [ ] 設定 `dub_locales` 不是空的時，「captions written」之後多一步 `dubs synthesized`，在送審成片之前：
  - `dub --locale <全部>`；結束碼 1 → 翻譯階段的「縮短」模式，只給 `fit.json` 列的句子與 `max_chars`（數字、專有名詞、說法不能改，字幕跟著用縮短後的句子）→ `i18n-merge` → 再 `dub`，每個語系最多 2 輪；
  - `check-audio --locale` → Jev 標記 → `dub --redo`，最多 2 輪；
  - 仍不行的語系寫 `dubs/<locale>/skipped.json`（原因），繼續往下，不 block；
  - 配音做完再跑 `captions`（讓有配音的語系改用配音時間軸），再 `review-push --gate final`。
- [ ] 設定是空的時，流程和現在一個位元組都不差（測試）。
- [ ] `qa` 多一項 `dubs`：設定裡的每個語系，不是有一條當前而且檢查過的音軌，就是有跳過的原因；跳過的算過、細節列成警告，缺的算沒過。
- [ ] 翻譯提示 `caption-translate.md` 說明 `max_chars` 與縮短模式，`caption-review.md` 檢查預算；`.claude/skills` 複本同步。
- [ ] `AUTOMATION.md`：步驟表加 `dubs synthesized`、設定表加 `dub_locales`、輪數常數、成本連到 DUBS.md。
- [ ] `automation.test.mjs` 用假的 runner 走：一次成功、縮短一輪後成功、兩輪後跳過、設定空白不跑。

## Steps

- [ ] `flow.mjs` 的步驟與兩個迴圈；`prompts.mjs` 的縮短模式。
- [ ] `qa` 的 `dubs` 項。
- [ ] 提示詞與複本；`AUTOMATION.md`。
- [ ] 測試；主機上開 `dub_locales=["en"]` 看一支跑完。

## How to verify

```bash
npm run test:tools
```

主機：後台設定勾 en，等下一支影片的工人日誌出現 `dubs synthesized`；`/admin/videos` 的「確認上架」附件裡有 `dubs/en.m4a`；`qa.json` 的 `dubs` 項是 ok。

## Notes

- 工人在容器裡跑 `tools/video`，ffmpeg 是 `assemble` 用的那一個；要用 `--format mp3` 時先確認容器的 ffmpeg 有 libmp3lame。
- 上傳包每條音軌約 28 MB（m4a），送審的分段上傳與 `video_review_max_total_bytes` 要夠。
- 伺服器的 Gemini 月額度先調高再開設定（見 `video-dubs-setting` 的 Notes）。
