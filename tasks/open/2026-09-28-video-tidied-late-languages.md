---
id: 2026-09-28-video-tidied-late-languages
title: 清理過的影片被勾新語言時告訴站主
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-28T11:51:48Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-tidy-finished
scope:
  - tools/video/automation/flow.mjs
---

# 清理過的影片被勾新語言時告訴站主

## Why

工人會在影片上 YouTube 滿 7 天（`VIDEO_TIDY_DAYS`）後清掉它的工作檔（`tools/video/automation/tidy.mjs`，`docs/videos/AUTOMATION.md` §清理工作區）：成片、旁白、畫面都不在了。站主之後才在 `/admin/videos` 的語言面板多勾一個語言時，`Automation.languages()` 看到成片核准的 `final.mp4` 不在（`approvalState` 回 `absent`）就什麼都不做，站上那一格會一直停在「製作中」，站主不知道為什麼。

## Definition of done

- [ ] `auto.json` 有 `tidied_at` 的影片被勾了新的語言部件時，工人不重做影片，而是讓站主看到原因：每個還在「製作中」的部件在語言批次裡回報成 `{status: "skipped", reason: "工作檔已在 <日期> 清掉，…"}`，或卡片清單第一列寫出原因（選一種，照 `docs/videos/LANGUAGES.md` 的現有做法）。
- [ ] 沒清理過的影片行為不變。

## Steps

- [ ] 在 `flow.mjs` 的 `languages()` 裡辨認清理過的影片（讀 `auto.json` 的 `tidied_at`），決定回報方式。
- [ ] 測試：清理過的影片被勾新語言、沒清理過的影片照舊。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"
npm run test:tools
```

## Notes

- 2026-09-28 清理那張票（`2026-09-28-video-story-tidy-finished`）發現的缺口；那張票不能改 `flow.mjs`（#897、#904 正在改），所以另開。
- 標題、說明、CC 的翻譯本身不需要成片，但 `languages()` 最後一步的 `package` 要複製 `final.mp4`，所以只翻不包也送不出去；要做就是回報原因，不是重做。
