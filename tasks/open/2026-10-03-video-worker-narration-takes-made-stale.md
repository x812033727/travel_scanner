---
id: 2026-10-03-video-worker-narration-takes-made-stale
title: Video worker: narration takes made stale by the accent change are recorded again, not refused for ever
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-03T16:23:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/takes.mjs
  - tools/video/tts/tts.test.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Video worker: narration takes made stale by the accent change are recorded again, not refused for ever

## Why

2026-10-03 站主重試七支卡住的插圖投影片，工人接手後卡在
`tts failed: audio evidence refresh needs every original take cached and current`，再按重試也一樣。

- 這些旁白是 #1132 之前錄的，`timeline.json` 沒有 `audio_evidence`。
- 稿子沒變（speech hash 相同）時，`flow.mjs` 一律走 `tts --refresh-evidence`，它只綁證據、不錄音，遇到任何不是 current 的錄音就丟 UsageError。
- #1168 改了送去合成的口音寫法，請求鍵全變：主機上七支的 wav 都在，對得上的鍵是 0 筆。

站主 2026-10-03 決定：重錄旁白（新口音），不保留舊錄音。

## Definition of done

- [x] 同稿、沒有證據、錄音的鍵已經對不上時，工人跑一般的 `tts`（重錄，寫新的 timeline，旁白重新過關卡），不再走只會拒絕的 refresh。
- [x] 錄音都還 current 時行為不變：仍然 `--refresh-evidence`，不花合成費。
- [x] 判斷「錄音是不是 current」的規則只有一份（`tts/takes.mjs`），`tts` 與工人共用。
- [x] 時長審查收據由獨立代理做增量（審查者 `claude-pr-review-tts-stale-takes`，結論：沒有動到時長規則）。
- [ ] 部署後七支能走過「narration synthesized」。

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/tts/tts.test.mjs`、`node tools/video/long-form/cli.mjs check`。

## Notes

- 有 `audio_evidence` 但對不上錄音的情況沒動，照舊卡住要人處理。
- 七支裡 gemini-skills-replace-gems-move-checklist 與 openai-agent-posted-53-user-images 另有「約 7.9 分鐘、不足 8 分鐘」的 lint 錯誤，會先回撰稿。
- 審查者提的兩個已知風險：帶 `audio_ref` 的舊片若來源錄音還 current 但 cache 沒有它的 sha256，一般 `tts` 會以另一句 UsageError 停下（不是退步，原本 refresh 也拒絕）；以後再改送合成的內容，沒有證據的舊片會自動重錄，只受每月額度限制。
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by claude-opus-5-5 (since 2026-10-03T16:23:36Z) was stale and is released so it stops locking its scope. Landed: #1182. Still open: 部署後七支能走過「narration synthesized」.
- 2026-10-06 (about 23:20Z on 10-05), claude-opus-5-5-incomplete-tickets: read-only check of `video_projects` on production. No slides video is held by `audio evidence refresh needs every original take cached and current` any more. The illustrated-slides videos that were in the narration stage on 10-03 all have `narration_synthesized` and `narration_approved` done (three are on YouTube; sec-ai-trading-bot-whatsapp-scam, gemini-skills-replace-gems-move-checklist and gemini-4-argon-who-can-use-it went on to keyframes, where they are held for a different reason), except **openai-agent-posted-53-user-images**: it went back to the writer for its 7.9-minute lint, passed lint and the fact check, and on 10-04 13:13Z stopped at `tts failed: 請求過於頻繁，請稍後再試`, the speech route's own 429. That means the worker now records again instead of refusing, which is what this ticket fixed, but the last box (all seven through narration) is not met. The 429 is a separate defect, filed as 2026-10-05-a-burst-of-narration-lines-trips; the box stays open until that video passes, and the ticket stays open for it.
